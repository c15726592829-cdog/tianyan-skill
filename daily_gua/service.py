"""Actual three-coin casting and Wenwang Najia, independent of the LLM."""
import re
from datetime import datetime
from zoneinfo import ZoneInfo
if __package__=="daily_gua":
    from scripts.qi_gua import build_cast
    from scripts.pai_gua import build_chart,parse_line_values,parse_cast_time
else:
    from ..scripts.qi_gua import build_cast
    from ..scripts.pai_gua import build_chart,parse_line_values,parse_cast_time

QUOTA_ZONE=ZoneInfo("Asia/Shanghai")
DEFAULT_QUESTION="我今天行事与安排，有哪些需要留意、怎样应对更稳妥？"

def city_name(value):
    value=re.sub(r"[\x00-\x1f]","",str(value or "")).strip()
    if not value or len(value)>60:raise ValueError("请提供起卦城市，例如北京；不需要精确地址。")
    return value

class DailyGuaService:
    def __init__(self,store,now=None,self_location="北京"):
        self.store=store;self.now=now or (lambda:datetime.now(QUOTA_ZONE))
        self.self_location=city_name(self_location)
    def today(self,scope):
        return self.store.get(scope,self.now().astimezone(QUOTA_ZONE).date())
    def set_location(self,scope,city,timezone="Asia/Shanghai"):
        if scope=="fish:self":raise ValueError("鱼鱼自己的地点由插件配置设定。")
        city=city_name(city);ZoneInfo(timezone);self.store.set_location(scope,city,timezone)
    def draw(self,scope,question="",location="",timezone="",lines="",cast_time=""):
        moment=self.now();day=str(moment.astimezone(QUOTA_ZONE).date())
        old=self.store.get(scope,day)
        if old:return False,old
        saved=self.store.location(scope)
        if scope=="fish:self":
            if location and city_name(location)!=self.self_location:raise ValueError("鱼鱼自己的地点固定使用插件配置。")
            city,tz=self.self_location,"Asia/Shanghai"
        else:
            city=city_name(location or (saved['city'] if saved else ""))
            tz=timezone or (saved['timezone'] if saved else "Asia/Shanghai")
        ZoneInfo(tz);question=question.strip() or DEFAULT_QUESTION
        if len(question)>500:raise ValueError("问题请控制在500字以内，一次聚焦一件事。")
        values=parse_line_values(lines) if lines else None
        if cast_time and values is None:raise ValueError("自动三硬币使用执行时刻，不接受指定日期或时间起卦。")
        manual_time=cast_time or moment.astimezone(ZoneInfo(tz)).strftime("%Y-%m-%d %H:%M")
        if values is not None:parse_cast_time(manual_time,tz)
        payload={'scope':scope,'date':day,'question':question,'location':city,'timezone':tz,'created_at':moment.isoformat(timespec='seconds'),'status':'reserved','quota_timezone':'Asia/Shanghai'}
        fresh,record=self.store.reserve(scope,day,payload)
        if not fresh:return False,record
        # Reserve BEFORE entropy: crashes/failures never silently trigger a reroll.
        try:
            if values is None:cast=build_cast(question,tz,moment=moment,location=city)
            else:cast={'method':'user_supplied','mode':'manual','question':question,'location':city,'cast_time':manual_time,'timezone':tz,'line_values':list(values),'line_values_text':','.join(map(str,values)),'input_order':'bottom_to_top'}
            record=self.store.patch(scope,day,cast=cast,status='cast')
            chart=build_chart(question,cast['cast_time'],tz,cast['line_values'],location=city)
            record=self.store.patch(scope,day,chart=chart,status='ready')
            if scope!='fish:self':self.store.set_location(scope,city,tz)
        except Exception as error:record=self.store.patch(scope,day,status='failed',error_type=type(error).__name__)
        return True,record
    def recover_chart(self,scope):
        record=self.today(scope)
        if record and record.get('cast') and not record.get('chart'):
            cast=record['cast'];chart=build_chart(record['question'],cast['cast_time'],record['timezone'],cast['line_values'],location=record['location'])
            return self.store.patch(scope,record['date'],chart=chart,status='ready')
        return record
