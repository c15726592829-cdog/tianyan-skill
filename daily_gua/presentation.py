"""Readable text and a deterministic Chinese Najia chart card."""
import hashlib
from pathlib import Path

def chart_text(record):
    c=record.get('chart')
    if not c:
        return '本日名额已记录，排盘尚未完成；保留原始数据，不重抛。'
    cal=c['calendar'];moving=c['moving_lines']
    result=[
        '每日一卦 · 文王纳甲',
        f"地点：{record['location']}　起卦：{record['cast']['cast_time']}（{record['timezone']}）",
        f"所问：{record['question']}",
        '六爻自下而上：'+' '.join(map(str,c['line_values'])),
        '本卦：'+c['primary']['name']+(' → '+c['changed']['name'] if moving else '（静卦，无动爻）'),
        f"八宫：{c['palace']['name']}宫{c['palace']['element']} · {c['palace']['generation']}；世{c['shi_line']}应{c['ying_line']}",
        f"月建：{cal['month_commander']}　日辰：{cal['day']}　旬空：{''.join(cal['xunkong'])}",
        '盘图自上而下：'
    ]
    for row in reversed(c['lines']):
        tag='世' if row['shi'] else '应' if row['ying'] else ''
        mark='━' if row['yin_yang']=='阳' else '╍'
        line=f"{row['line']} {row['spirit']} {row['relative']}{row['najia']}{row['branch_element']} {mark} {tag}"
        if row['moving']:line+=' 动→'+row['changed_relative']+row['changed_najia']+row['changed_branch_element']
        if row.get('hidden'):
            h=row['hidden'];line+=' 伏：'+h['relative']+h['najia']+h['branch_element']
        result.append(line)
    result.append('次数按北京时间零点重置；干支按上游23点换日法。地点仅记录，不暗算真太阳时。')
    return '\n'.join(result)

def audit_text(record):
    cast=record.get('cast',{})
    rows=[chart_text(record),'','起卦方法：'+str(cast.get('method','尚未完成'))]
    if cast.get('throws'):
        rows.append('原始18枚硬币（从初爻向上）：')
        for throw in cast['throws']:
            rows.append(str(throw['line'])+'：'+''.join(c['side'][0] for c in throw['coins'])+'='+str(throw['line_value']))
        rows+=['算法：'+cast['algorithm'],'熵：'+cast['entropy_hex'],'SHA256：'+cast['derived_sha256_hex']]
    else:rows.append('使用用户提供的爻象，没有模拟或重抛硬币。' if cast else '起卦中断，未生成第二卦。')
    return '\n'.join(rows)

def image_path(directory,record):
    token=hashlib.sha256((record['scope']+'|'+record['date']).encode()).hexdigest()[:24]
    return Path(directory)/(token+'.png')

def render(record,path,font_path=''):
    from PIL import Image,ImageDraw,ImageFont
    candidates=[font_path,'C:/Windows/Fonts/msyh.ttc','C:/Windows/Fonts/simhei.ttf','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc']
    selected=next((p for p in candidates if p and Path(p).is_file()),None)
    if not selected:raise RuntimeError('未找到中文字体，改为文字卦盘')
    def font(n):return ImageFont.truetype(selected,n)
    image=Image.new('RGB',(1100,1110),'#f2f5f4');d=ImageDraw.Draw(image)
    d.rounded_rectangle((25,25,1075,1085),radius=30,fill='#fffdf6',outline='#bfcbbf',width=3)
    d.rounded_rectangle((45,45,1055,220),radius=24,fill='#173d4c')
    d.text((78,65),'每日一卦',font=font(47),fill='#fbf2d2')
    d.text((80,135),'文王纳甲 · 三枚硬币模拟' if record['cast']['method']=='three_coin' else '文王纳甲 · 用户提供爻象',font=font(25),fill='#d5e8e6')
    d.text((80,178),record['cast']['cast_time']+'  '+record['location'][:18],font=font(23),fill='#d5e8e6')
    c=record['chart'];moving=c['moving_lines']
    d.text((78,245),c['primary']['name']+('  →  '+c['changed']['name'] if moving else ' · 静卦'),font=font(36),fill='#173d4c')
    cal=c['calendar']
    d.text((80,301),f"月建 {cal['month_commander']}   日辰 {cal['day']}   旬空 {''.join(cal['xunkong'])}",font=font(25),fill='#5c6c65')
    question=record['question'];line='';ys=345
    for ch in question[:65]:
        if d.textlength(line+ch,font=font(24))>915:
            d.text((80,ys),line,font=font(24),fill='#3e514b');ys+=33;line=''
        line+=ch
    if line:d.text((80,ys),line,font=font(24),fill='#3e514b')
    d.text((80,435),'爻位 / 六神',font=font(21),fill='#6b786f')
    d.text((275,435),'本卦',font=font(21),fill='#6b786f')
    d.text((655,435),'动变 / 伏神',font=font(21),fill='#6b786f')
    labels={1:'初',2:'二',3:'三',4:'四',5:'五',6:'上'}
    for i,row in enumerate(reversed(c['lines'])):
        y=490+i*74;colour='#ae5147' if row['moving'] else '#24473f'
        d.text((78,y-8),labels[row['line']]+' '+row['spirit'],font=font(24),fill=colour)
        if row['yin_yang']=='阳':d.rectangle((274,y,420,y+13),fill=colour)
        else:
            d.rectangle((274,y,333,y+13),fill=colour);d.rectangle((360,y,420,y+13),fill=colour)
        tag='世' if row['shi'] else '应' if row['ying'] else ''
        d.text((443,y-9),row['relative']+row['najia']+row['branch_element']+' '+tag,font=font(23),fill=colour)
        if row['moving']:d.text((680,y-9),'→ '+row['changed_relative']+row['changed_najia']+row['changed_branch_element'],font=font(22),fill=colour)
        if row.get('hidden'):
            h=row['hidden'];d.text((680,y+21),'伏 '+h['relative']+h['najia']+h['branch_element'],font=font(19),fill='#64776d')
    d.line((80,959,1020,959),fill='#c6d1c5',width=2)
    d.text((80,980),'自下而上：'+' '.join(map(str,c['line_values'])),font=font(23),fill='#4c685d')
    d.text((80,1020),'每人每日一卦 · 传统文化参考，选择仍由你决定',font=font(22),fill='#648073')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix('.tmp');image.save(temp,format='PNG');temp.replace(path)
    return path
