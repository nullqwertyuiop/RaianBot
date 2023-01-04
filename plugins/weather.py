from arclet.alconna import Args, Arparma, Field, CommandMeta
from arclet.alconna.graia import Alconna, alcommand, Match
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.app import Ariadne
from graiax.playwright import PlaywrightBrowser
from app import Sender, accessable, exclusive, record

city_ids = {
    "七台河": "101051002",
    "万宁": "101310215",
    "万州天城": "101041200",
    "万州龙宝": "101041300",
    "万盛": "101040600",
    "三亚": "101310201",
    "三明": "101230801",
    "三门峡": "101181701",
    "上海": "101020100",
    "上饶": "101240301",
    "东丽": "101030400",
    "东方": "101310202",
    "东莞": "101281601",
    "东营": "101121201",
    "中卫": "101170501",
    "中山": "101281701",
    "丰台": "101010900",
    "丰都": "101043000",
    "临夏": "101161101",
    "临汾": "101100701",
    "临沂": "101120901",
    "临沧": "101291101",
    "临河": "101080801",
    "临高": "101310203",
    "丹东": "101070601",
    "丽水": "101210801",
    "丽江": "101291401",
    "乌兰浩特": "101081101",
    "乌海": "101080301",
    "乌鲁木齐": "101130101",
    "乐东": "101310221",
    "乐山": "101271401",
    "九江": "101240201",
    "云浮": "101281401",
    "云阳": "101041700",
    "五指山": "101310222",
    "亳州": "101220901",
    "仙桃": "101201601",
    "伊宁": "101131001",
    "伊春": "101050801",
    "佛山": "101280800",
    "佛爷顶": "101011700",
    "佳木斯": "101050401",
    "保亭": "101310214",
    "保定": "101090201",
    "保山": "101290501",
    "信阳": "101180601",
    "儋州": "101310205",
    "克拉玛依": "101130201",
    "八达岭": "101011600",
    "六安": "101221501",
    "六盘水": "101260801",
    "兰州": "101160101",
    "兴义": "101260906",
    "内江": "101271201",
    "凉山": "101271601",
    "凯里": "101260501",
    "包头": "101080201",
    "北京": "101010100",
    "北京城区": "101012200",
    "北海": "101301301",
    "北碚": "101040800",
    "北辰": "101030600",
    "十堰": "101201101",
    "南京": "101190101",
    "南充": "101270501",
    "南宁": "101300101",
    "南川": "101040400",
    "南平": "101230901",
    "南昌": "101240101",
    "南汇": "101020600",
    "南沙岛": "101310220",
    "南通": "101190501",
    "南阳": "101180701",
    "博乐": "101131601",
    "厦门": "101230201",
    "双鸭山": "101051301",
    "台中": "101340401",
    "台北县": "101340101",
    "台州": "101210601",
    "合作": "101161201",
    "合川": "101040300",
    "合肥": "101220101",
    "吉安": "101240601",
    "吉林": "101060201",
    "吉首": "101251501",
    "吐鲁番": "101130501",
    "吕梁": "101101100",
    "吴忠": "101170301",
    "周口": "101181401",
    "呼伦贝尔": "101081000",
    "呼和浩特": "101080101",
    "和田": "101131301",
    "咸宁": "101200701",
    "咸阳": "101110200",
    "哈密": "101131201",
    "哈尔滨": "101050101",
    "唐山": "101090501",
    "商丘": "101181001",
    "商洛": "101110601",
    "喀什": "101130901",
    "嘉兴": "101210301",
    "嘉定": "101020500",
    "嘉峪关": "101161401",
    "四平": "101060401",
    "固原": "101170401",
    "垫江": "101042200",
    "城口": "101041600",
    "塔城": "101131101",
    "塘沽": "101031100",
    "大兴": "101011100",
    "大兴安岭": "101050701",
    "大同": "101100201",
    "大庆": "101050901",
    "大港": "101031200",
    "大理": "101290201",
    "大足": "101042600",
    "大连": "101070201",
    "天水": "101160901",
    "天津": "101030100",
    "天门": "101201501",
    "太原": "101100101",
    "奉节": "101041900",
    "奉贤": "101021000",
    "威海": "101121301",
    "娄底": "101250801",
    "孝感": "101200401",
    "宁德": "101230301",
    "宁河": "101030700",
    "宁波": "101210401",
    "安庆": "101220601",
    "安康": "101110701",
    "安阳": "101180201",
    "安顺": "101260301",
    "定安": "101310209",
    "定西": "101160201",
    "宜宾": "101271101",
    "宜昌": "101200901",
    "宜春": "101240501",
    "宝坻": "101030300",
    "宝山": "101020300",
    "宝鸡": "101110901",
    "宣城": "101221401",
    "宿州": "101220701",
    "宿迁": "101191301",
    "密云": "101011300",
    "密云上甸子": "101011900",
    "屯昌": "101310210",
    "山南": "101140301",
    "岳阳": "101251001",
    "崇左": "101300201",
    "崇明": "101021100",
    "巢湖": "101221601",
    "巫山": "101042000",
    "巫溪": "101041800",
    "巴中": "101270901",
    "巴南": "101040900",
    "常州": "101191101",
    "常德": "101250601",
    "平凉": "101160301",
    "平谷": "101011500",
    "平顶山": "101180501",
    "广元": "101272101",
    "广安": "101270801",
    "广州": "101280101",
    "庆阳": "101160401",
    "库尔勒": "101130601",
    "廊坊": "101090601",
    "延吉": "101060301",
    "延安": "101110300",
    "延庆": "101010800",
    "开县": "101041500",
    "开封": "101180801",
    "张家口": "101090301",
    "张家界": "101251101",
    "张掖": "101160701",
    "彭水": "101043200",
    "徐家汇": "101021200",
    "徐州": "101190801",
    "德宏": "101291501",
    "德州": "101120401",
    "德阳": "101272001",
    "忠县": "101042400",
    "忻州": "101101001",
    "怀化": "101251201",
    "怀柔": "101010500",
    "怒江": "101291201",
    "恩施": "101201001",
    "惠州": "101280301",
    "成都": "101270101",
    "房山": "101011200",
    "扬州": "101190601",
    "承德": "101090402",
    "抚州": "101240401",
    "抚顺": "101070401",
    "拉萨": "101140101",
    "揭阳": "101281901",
    "攀枝花": "101270201",
    "文山": "101290601",
    "文昌": "101310212",
    "斋堂": "101012000",
    "新乡": "101180301",
    "新余": "101241001",
    "无锡": "101190201",
    "日喀则": "101140201",
    "日照": "101121501",
    "昆明": "101290101",
    "昌吉": "101130401",
    "昌平": "101010700",
    "昌江": "101310206",
    "昌都": "101140501",
    "昭通": "101291001",
    "晋中": "101100401",
    "晋城": "101100601",
    "晋江": "101230509",
    "普洱": "101290901",
    "景德镇": "101240801",
    "景洪": "101291601",
    "曲靖": "101290401",
    "朔州": "101100901",
    "朝阳": "101071201",
    "本溪": "101070501",
    "来宾": "101300401",
    "杭州": "101210101",
    "松原": "101060801",
    "松江": "101020900",
    "林芝": "101140401",
    "果洛": "101150501",
    "枣庄": "101121401",
    "柳州": "101300301",
    "株洲": "101250301",
    "桂林": "101300501",
    "梁平": "101042300",
    "梅州": "101280401",
    "梧州": "101300601",
    "楚雄": "101290801",
    "榆林": "101110401",
    "武威": "101160501",
    "武汉": "101200101",
    "武清": "101030200",
    "武都": "101161001",
    "武隆": "101043100",
    "毕节": "101260701",
    "永川": "101040200",
    "永州": "101251401",
    "汉中": "101110801",
    "汉沽": "101030800",
    "汕头": "101280501",
    "汕尾": "101282101",
    "江津": "101040500",
    "江门": "101281101",
    "池州": "101221701",
    "汤河口": "101011800",
    "沈阳": "101070101",
    "沙坪坝": "101043700",
    "沧州": "101090701",
    "河池": "101301201",
    "河源": "101281201",
    "泉州": "101230501",
    "泰安": "101120801",
    "泰州": "101191201",
    "泸州": "101271001",
    "洛阳": "101180901",
    "津南": "101031000",
    "济南": "101120101",
    "济宁": "101120701",
    "济源": "101181801",
    "浦东": "101021300",
    "海东": "101150201",
    "海北": "101150801",
    "海南": "101150401",
    "海口": "101310101",
    "海淀": "101010200",
    "海西": "101150701",
    "涪陵": "101041400",
    "淄博": "101120301",
    "淮北": "101221201",
    "淮南": "101220401",
    "淮安": "101190901",
    "深圳": "101280601",
    "清远": "101281301",
    "渝北": "101040700",
    "温州": "101210701",
    "渭南": "101110501",
    "湖州": "101210201",
    "湘潭": "101250201",
    "湛江": "101281001",
    "滁州": "101221101",
    "滨州": "101121101",
    "漯河": "101181501",
    "漳州": "101230601",
    "潍坊": "101120601",
    "潜江": "101201701",
    "潮州": "101281501",
    "潼南": "101042100",
    "澄迈": "101310204",
    "濮阳": "101181301",
    "烟台": "101120501",
    "焦作": "101181101",
    "牡丹江": "101050301",
    "玉林": "101300901",
    "玉树": "101150601",
    "玉溪": "101290701",
    "珠海": "101280701",
    "琼中": "101310208",
    "琼山": "101310102",
    "琼海": "101310211",
    "璧山": "101042900",
    "甘孜": "101271801",
    "白城": "101060601",
    "白山": "101060901",
    "白沙": "101310207",
    "白银": "101161301",
    "百色": "101301001",
    "益阳": "101250700",
    "盐城": "101190701",
    "盘锦": "101071301",
    "眉山": "101271501",
    "石嘴山": "101170201",
    "石家庄": "101090101",
    "石景山": "101011000",
    "石柱": "101042500",
    "石河子": "101130301",
    "神农架": "101201201",
    "福州": "101230101",
    "秀山": "101043600",
    "秦皇岛": "101091101",
    "綦江": "101043300",
    "红河": "101290301",
    "绍兴": "101210501",
    "绥化": "101050501",
    "绵阳": "101270401",
    "聊城": "101121701",
    "肇庆": "101280901",
    "自贡": "101270301",
    "舟山": "101211101",
    "芜湖": "101220301",
    "苏州": "101190401",
    "茂名": "101282001",
    "荆州": "101200801",
    "荆门": "101201401",
    "荣昌": "101042700",
    "莆田": "101230401",
    "莱芜": "101121601",
    "菏泽": "101121001",
    "萍乡": "101240901",
    "营口": "101070801",
    "葫芦岛": "101071401",
    "蓟县": "101031400",
    "蚌埠": "101220201",
    "衡水": "101090801",
    "衡阳": "101250401",
    "衢州": "101211001",
    "襄樊": "101200201",
    "西宁": "101150101",
    "西安": "101110101",
    "西沙": "101310217",
    "西青": "101030500",
    "许昌": "101180401",
    "贵港": "101300801",
    "贵阳": "101260101",
    "贺州": "101300701",
    "资阳": "101271301",
    "赣州": "101240701",
    "赤峰": "101080601",
    "辽源": "101060701",
    "辽阳": "101071001",
    "达州": "101270601",
    "运城": "101100801",
    "连云港": "101191001",
    "通化": "101060501",
    "通州": "101010600",
    "通辽": "101080501",
    "遂宁": "101270701",
    "遵义": "101260201",
    "邢台": "101090901",
    "那曲": "101140601",
    "邯郸": "101091001",
    "邵阳": "101250901",
    "郑州": "101180101",
    "郴州": "101250501",
    "都匀": "101260401",
    "鄂尔多斯": "101080701",
    "鄂州": "101200301",
    "酉阳": "101043400",
    "酒泉": "101160801",
    "重庆": "101040100",
    "金华": "101210901",
    "金山": "101020700",
    "金昌": "101160601",
    "钦州": "101301101",
    "铁岭": "101071101",
    "铜仁": "101260601",
    "铜川": "101111001",
    "铜梁": "101042800",
    "铜陵": "101221301",
    "银川": "101170101",
    "锡林浩特": "101080901",
    "锦州": "101070701",
    "镇江": "101190301",
    "长寿": "101041000",
    "长春": "101060101",
    "长沙": "101250101",
    "长治": "101100501",
    "门头沟": "101011400",
    "闵行": "101020200",
    "阜新": "101070901",
    "阜阳": "101220801",
    "防城港": "101301401",
    "阳江": "101281801",
    "阳泉": "101100301",
    "阿克苏": "101130801",
    "阿勒泰": "101131401",
    "阿图什": "101131501",
    "阿坝": "101271901",
    "阿拉善左旗": "101081201",
    "阿拉尔": "101130701",
    "阿里": "101140701",
    "陵水": "101310216",
    "随州": "101201301",
    "雅安": "101271701",
    "集宁": "101080401",
    "霞云岭": "101012100",
    "青岛": "101120201",
    "青浦": "101020800",
    "静海": "101030900",
    "鞍山": "101070301",
    "韶关": "101280201",
    "顺义": "101010400",
    "香格里拉": "101291301",
    "马鞍山": "101220501",
    "驻马店": "101181601",
    "高雄": "101340201",
    "鸡西": "101051101",
    "鹤壁": "101181201",
    "鹤岗": "101051201",
    "鹰潭": "101241101",
    "黄冈": "101200501",
    "黄南": "101150301",
    "黄山": "101221001",
    "黄石": "101200601",
    "黑河": "101050601",
    "黔江": "101041100",
    "黔阳": "101251301",
    "齐齐哈尔": "101050201",
    "龙岩": "101230701",
}
times = {"今天": 1, "明天": 2, "后天": 3, "大后天": 4, "老后天": 5}


@alcommand(
    Alconna(
        "{city}?天气",
        Args["time", times, Field(1, alias="今天", completion=lambda: list(times.keys()))],
        meta=CommandMeta("查询某个城市的天气", usage="提供五个可查询的时间段", example="$北京天气 明天"),
    )
)
@record("天气")
@exclusive
@accessable
async def weather(app: Ariadne, sender: Sender, time: Match[int], result: Arparma):
    city = result.header["city"] or "长沙"
    if city not in city_ids:
        return await app.send_message(sender, MessageChain("不对劲。。。"))
    browser: PlaywrightBrowser = app.launch_manager.get_interface(PlaywrightBrowser)
    async with browser.page() as page:
        await page.click("html")
        await page.goto(f"https://m.weather.com.cn/mweather1d/{city_ids[city]}.shtml?day={time.result}")
        # elem = page.query_selector("div#main")
        elem = page.locator("//div[@class='beijingbox']")
        elem1 = page.locator("//div[@class='box-all' and @id='day-tianqi']")
        elem2 = page.locator("//div[@class='timeWeather']")
        # # data = elem.screenshot(path='temp.png')
        bounding = await elem.bounding_box()
        # print(bounding)
        bounding1 = await elem1.bounding_box()
        bounding2 = await elem2.bounding_box()
        # print(bounding1)
        bounding["height"] += bounding1["height"]
        bounding["height"] += bounding2["height"]
        res = MessageChain(Image(data_bytes=await page.screenshot(full_page=True, clip=bounding)))
    return await app.send_message(sender, res)
