from app import RaianBotService, Sender, Target
from arclet.alconna import Args, CommandMeta, Option, Arg
from arclet.alconna.graia import Alconna, Match, alcommand, assign
from arknights_toolkit.record import ArkRecord
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image

alc = Alconna(
    "抽卡查询",
    Args["count#最近x抽", int, -1],
    Option("绑定", Args[Arg("token", str, seps='\n')]),
    meta=CommandMeta(
        "明日方舟抽卡数据查询，数据来源为方舟官网",
        usage="""

**token获取方法**：在官网登录后，根据你的服务器，选择复制以下网址中的内容

官服：https://web-api.hypergryph.com/account/info/hg

B服：https://web-api.hypergryph.com/account/info/ak-b

***请在浏览器中获取token，避免在QQ打开的网页中获取，否则可能获取无效token***

        """
    ),
)

bot = RaianBotService.current()

querier = ArkRecord(
    f"{bot.config.cache_dir}/plugins/gacha_record/",
    f"{bot.config.cache_dir}/plugins/arkrecord.db",
)


@alcommand(alc)
@assign("$main")
async def query(app: Ariadne, target: Target, sender: Sender, count: Match[int]):
    try:
        querier.database.read_token_from_db(str(target.id))
    except (AssertionError, RuntimeError):
        return await app.send_message(
            sender, """您未绑定您的方舟账号 token！
            
token获取方法：在官网登录后，根据你的服务器，选择复制以下网址中的内容

官服：https://web-api.hypergryph.com/account/info/hg

B服：https://web-api.hypergryph.com/account/info/ak-b

请在浏览器中获取token，避免在QQ打开的网页中获取，否则可能获取无效token
"""
        )
    try:
        file = querier.user_analysis(str(target.id), count.result)
        return await app.send_message(sender, MessageChain(Image(path=file)))
    except RuntimeError as e:
        return await app.send_message(sender, str(e))


@alcommand(alc)
@assign("绑定")
async def bind(app: Ariadne, target: Target, sender: Sender, token: Match[str]):
    try:
        res = querier.user_token_save(token.result, str(target.id))
    except RuntimeError as e:
        return await app.send_message(sender, str(e))
    return await app.send_message(sender, res)
