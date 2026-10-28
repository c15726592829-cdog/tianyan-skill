"""每日一卦：AstrBot QQ private-chat adapter for Tianyan Wenwang Najia."""
import asyncio
import json
import weakref
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from astrbot.api.event import AstrMessageEvent,filter
from astrbot.api.star import Star,StarTools
from .daily_gua.storage import GuaStore
from .daily_gua.service import DailyGuaService,QUOTA_ZONE,DEFAULT_QUESTION
from .daily_gua.presentation import chart_text,audit_text,image_path,render
from .daily_gua.interpretation import prompt_for

class DailyGua(Star):
    def __init__(self,context,config=None):
        super().__init__(context)
        self.settings=config if config is not None else {}
        self.data=Path(StarTools.get_data_dir('astrbot_plugin_daily_gua'))
        self.store=GuaStore(self.data/'gua.sqlite3')
        self.now=lambda:datetime.now(QUOTA_ZONE)
        self.service=DailyGuaService(self.store,now=lambda:self.now(),self_location=self.settings.get('self_location','北京'))
        self.locks=weakref.WeakValueDictionary()
        configured=self.settings.get('self_home','')
        self.home=Path(configured).resolve() if configured else (self.data/'self').resolve()

    def permitted(self,event):
        name=event.get_platform_name() if hasattr(event,'get_platform_name') else ''
        return bool(self.settings.get('enabled',True)) and event.is_private_chat() and (event.get_platform_id()=='qq-napcat' or name=='aiocqhttp')

    def scope(self,event,target):
        if target in ('self','fish','自己'):return 'fish:self'
        if target not in ('user','me','用户'):raise ValueError('target只能是当前用户user或鱼鱼自己self。')
        return 'user:'+str(event.get_sender_id())

    def lock_for(self,record):
        key=record['scope']+'|'+record['date']
        lock=self.locks.get(key)
        if lock is None:lock=asyncio.Lock();self.locks[key]=lock
        return lock

    async def interpret(self,record,event=None):
        if not record.get('chart') or record.get('reading') or not self.settings.get('enable_interpretation',True):return record
        async with self.lock_for(record):
            record=self.store.get(record['scope'],record['date'])
            if record.get('reading'):return record
            try:
                provider=self.settings.get('provider_id','')
                if not provider:provider=await self.context.get_current_chat_provider_id(event.unified_msg_origin if event else '')
                system,prompt=prompt_for(record)
                result=await asyncio.wait_for(self.context.llm_generate(chat_provider_id=provider,prompt=prompt,system_prompt=system,tools=None),90)
                text=(result.completion_text or '').strip()
                if not text:raise ValueError('empty interpretation')
                record=self.store.patch(record['scope'],record['date'],reading=text[:2400],reading_status='ready')
            except asyncio.CancelledError:raise
            except Exception as error:
                record=self.store.patch(record['scope'],record['date'],reading_status='unavailable')
                self.logger.warning('每日一卦解读暂不可用（%s），保留原卦不重起。',type(error).__name__)
        return record

    async def card(self,record):
        if not record.get('chart') or not self.settings.get('render_image',True):return None
        path=image_path(self.data/'cards',record)
        try:
            if not path.exists():await asyncio.to_thread(render,record,path,self.settings.get('font_path',''))
            return path
        except Exception as error:
            self.logger.warning('每日一卦使用文字盘（%s）。',type(error).__name__)
            return None

    async def save_self(self,record,path):
        if not record.get('chart'):return
        self.home.mkdir(parents=True,exist_ok=True)
        targets={}
        for folder in ('创作','笔记','运行记录'):
            dest=(self.home/folder).resolve()
            if not dest.is_relative_to(self.home):raise ValueError('小屋路径越界')
            dest.mkdir(parents=True,exist_ok=True);targets[folder]=dest
        text=chart_text(record)+'\n\n'+record.get('reading','解读暂不可用，可继续核对原卦。')+'\n\n'+audit_text(record)
        required=len(text.encode('utf-8'))+len(json.dumps(record,ensure_ascii=False).encode('utf-8'))+(path.stat().st_size if path else 0)
        if sum(p.stat().st_size for p in self.home.rglob('*') if p.is_file() and not p.is_symlink())+required>5*1024**3:raise ValueError('小屋已达到5GB，请先整理')
        (targets['笔记']/('自己的每日一卦_'+record['date']+'.md')).write_text(text,encoding='utf-8')
        (targets['运行记录']/('每日一卦_'+record['date']+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        if path:(targets['创作']/('自己的每日一卦_'+record['date']+'.png')).write_bytes(path.read_bytes())

    async def draw_self(self):
        if not self.settings.get('enabled',True):return {'new':False,'disabled':True}
        fresh,record=await asyncio.to_thread(self.service.draw,'fish:self')
        record=await self.interpret(record)
        path=await self.card(record)
        await self.save_self(record,path)
        return {'new':fresh,'record':record,'image':str(path) if path else None}

    async def prepare(self,event,action='draw',question='',location='',timezone='',target='user',lines='',cast_time=''):
        scope=self.scope(event,target)
        if action=='location':
            self.service.set_location(scope,location,timezone or 'Asia/Shanghai')
            return False,None,None,'地点已记为'+location+'；以后可修改，已起的卦不会重算。'
        if action in ('review','audit'):
            record=await asyncio.to_thread(self.service.recover_chart,scope)
            fresh=False
            if record is None:return False,None,None,'今天还没有起卦。说“帮我起今日一卦”，并提供城市即可。'
        elif action=='draw':
            fresh,record=await asyncio.to_thread(self.service.draw,scope,question,location,timezone,lines,cast_time)
        else:raise ValueError('action仅支持draw、review、audit、location，不支持绕过每日次数。')
        if not record.get('chart'):return fresh,record,None,'今日名额已留存，起卦中断或仍在处理中；不重抛。可稍后查看或审计原始记录。'
        if action!='audit':record=await self.interpret(record,event)
        path=await self.card(record)
        if scope=='fish:self':await self.save_self(record,path)
        return fresh,record,path,''

    @filter.llm_tool(name='fish_daily_gua')
    async def gua_tool(self,event:AstrMessageEvent,action:str='draw',question:str='',location:str='',timezone:str='',target:str='user',lines:str='',cast_time:str='')->str:
        """文王纳甲每日一卦。每人北京时间每天仅一卦，鱼鱼自己独立一卦；必须调用程序，不能凭空报卦。地点缺失不扣次数。只有明确要求起卦才用draw；继续问原卦用review。

        Args:
            action(string): draw起卦，review查看/解读原卦，audit审计原始抛钱，location设置当前用户城市；均不绕过限额。
            question(string): 用户确定的单个问题，留空为今天行事与应对的文化参考；同日不能改问重起。
            location(string): 起卦城市，好友首次必填；鱼鱼自己默认北京。不猜测用户地点。
            timezone(string): IANA时区，国内默认Asia/Shanghai；每日次数始终按北京时间零点重置。
            target(string): user当前聊天者，self鱼鱼自己；不能指定其他QQ好友。
            lines(string): 仅当用户明确提供爻象时填，自下而上六个6/7/8/9或中文爻名；否则留空由程序模拟三硬币。
            cast_time(string): 仅手工爻象可填其真实起卦时间YYYY-MM-DD HH:MM；自动起卦必须留空，用实际执行时刻。
        """
        if not self.permitted(event):return '每日一卦只在QQ私聊中使用。'
        try:fresh,record,path,message=await self.prepare(event,action,question,location,timezone,target,lines,cast_time)
        except (ValueError,KeyError) as error:return '尚未起新卦：'+str(error)[:250]
        if message:return message
        if action=='audit':return audit_text(record)
        sent=False
        if fresh and path:
            try:
                await event.send(event.image_result(str(path)));sent=True
                event.set_extra('fish_card_image_sent',True);event.set_extra('fish_hexagram_image_sent',True)
            except Exception:self.logger.warning('每日一卦图片发送未确认，保留本日原卦，不自动重发。')
        result={'new':fresh,'already_cast':not fresh,'date':record['date'],'location':record['location'],'cast_time':record['cast']['cast_time'],'timezone':record['timezone'],'question':record['question'],'chart_text':chart_text(record),'reading':record.get('reading','解读暂不可用，可根据原盘继续核对，不重新起卦。'),'image_sent':sent,'audit_available':'/每日一卦 审计','instruction':'先给出地点、时间与自下而上爻值，再转述工具已有纳甲解读。不改原问题、不重抛、不重复发图或配表情包。已起卦时说明仍在看同一卦。'}
        cast=record['cast']
        if cast.get('throws'):result['coin_audit']={'entropy':cast['entropy_hex'],'throws':[''.join(c['side'][0] for c in row['coins'])+'='+str(row['line_value']) for row in cast['throws']]}
        return json.dumps(result,ensure_ascii=False)

    @filter.command('每日一卦',alias={'今日一卦','一卦'})
    async def gua_command(self,event:AstrMessageEvent):
        if not self.permitted(event):return
        event.stop_event()
        text=event.message_str.strip().lstrip('/').split(maxsplit=1)
        arg=text[1].strip() if len(text)>1 else ''
        target='self' if arg.startswith('自己') else 'user'
        if target=='self':arg=arg[2:].strip()
        action='review' if arg in ('查看','复盘') else 'audit' if arg=='审计' else 'location' if arg.startswith('地点 ') else 'draw'
        location=arg.split(maxsplit=1)[1] if action=='location' else ''
        question=''
        if action=='draw' and '|' in arg:location,question=[x.strip() for x in arg.split('|',1)]
        elif action=='draw' and arg:question=arg
        try:fresh,record,path,message=await self.prepare(event,action,question,location,target=target)
        except (ValueError,KeyError) as error:
            yield event.plain_result(str(error)+'\n可用：/每日一卦 地点 北京，或 /每日一卦 北京 | 今天学习安排有什么要留意？');return
        if message:yield event.plain_result(message);return
        if action=='audit':yield event.plain_result(audit_text(record));return
        if path and (fresh or action=='review'):
            event.set_extra('fish_card_image_sent',True);yield event.image_result(str(path))
        header='' if fresh else '今天已经起过，下面仍是原卦，不重起。\n'
        yield event.plain_result(header+chart_text(record)+'\n\n'+record.get('reading','解读暂不可用，原始卦盘已保留。')+'\n\n审计原始抛钱：/每日一卦 审计')

    @filter.on_llm_request()
    async def gua_context(self,event:AstrMessageEvent,req):
        if not self.permitted(event):return
        own=self.service.today('user:'+str(event.get_sender_id()))
        fish=self.service.today('fish:self')
        text='每日一卦已替代旧小签/塔罗，使用fish_daily_gua。每人北京时间每天一卦，鱼鱼自己独立一卦、默认北京。好友首次需城市，不猜地点；缺地点不扣次数。只有明确要求才起，复盘用review。今天本聊天者'+('已起卦，不可重起。' if own else '尚未起卦。')
        if fish and fish.get('chart'):text+='你自己的今日卦为'+fish['chart']['primary']['name']+'，详情可查self的review。'
        req.system_prompt=(req.system_prompt or '')+'\n'+text
