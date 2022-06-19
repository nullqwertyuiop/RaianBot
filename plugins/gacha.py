from typing import Union
from arclet.alconna import Args
from arclet.alconna.graia import Alconna, AlconnaDispatcher
from arclet.alconna.graia.dispatcher import AlconnaProperty
from arclet.alconna.graia.saya import AlconnaSchema
from graia.ariadne.message.element import Image
from graia.saya.channel import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.model import Group, Friend, Member
from graia.ariadne.app import Ariadne


from app import RaianMain
from modules.arknights import ArknightsGacha
from utils.control import require_function

channel = Channel.current()
bot = RaianMain.current()
draw = Alconna(
    "(抽卡|寻访)", Args["count", int, 1],
    headers=bot.config.command_prefix,
    help_text=f"模拟方舟寻访 Example: {bot.config.command_prefix[0]}抽卡 300;",
)


@bot.data.record("抽卡")
@channel.use(AlconnaSchema(AlconnaDispatcher(alconna=draw, help_flag="reply")))
@channel.use(ListenerSchema([GroupMessage, FriendMessage], decorators=[require_function("抽卡")]))
async def draw(
        app: Ariadne,
        sender: Union[Group, Friend],
        target: Union[Friend, Member],
        result: AlconnaProperty
):
    """模拟抽卡"""
    file = bot.config.plugin.get('gache', 'assets/data/gacha_arknights.json')
    count = result.result.count
    if count < 1:
        count = 1
    if count > 300:
        count = 300
    if bot.data.exist(target.id):
        user = bot.data.get_user(target.id)
        if not user.additional.get('gacha_proba'):
            user.additional['gacha_proba'] = {'arknights': [0, 2]}
        elif not user.additional['gacha_proba'].get('arknights'):
            user.additional['gacha_proba']['arknights'] = [0, 2]
        six_statis, six_per = user.additional['gacha_proba']['arknights']
        gacha = ArknightsGacha(file=file, six_per=six_per, six_statis=six_statis)
        data = gacha.gacha(count)
        user.additional['gacha_proba']['arknights'] = [gacha.six_statis, gacha.six_per]
        bot.data.update_user(user)
    else:
        gacha = ArknightsGacha(file=file)
        data = gacha.gacha(count)
    return await app.send_message(sender, MessageChain(Image(data_bytes=data)))
