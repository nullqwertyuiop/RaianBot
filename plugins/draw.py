import json
import random
from typing import Union
from datetime import datetime
from arclet.alconna.graia import Alconna, AlconnaDispatcher
from arclet.alconna.graia.saya import AlconnaSchema
from graia.saya.channel import Channel
from graia.saya.builtins.broadcast import ListenerSchema
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Source
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.model import Group, Member, Friend
from graia.ariadne.app import Ariadne

from app import RaianMain
from modules.rand import random_pick_small

bot = RaianMain.current()
channel = Channel.current()
json_filename = "assets/data/draw_poetry.json"
with open(json_filename, 'r', encoding='UTF-8') as f_obj:
    draw_poetry = json.load(f_obj)['data']

draw = Alconna(
    "抽签",
    headers=bot.config.command_prefix,
    help_text="进行一次抽签, 可以解除",
)

undraw = Alconna(
    "解签",
    headers=bot.config.command_prefix,
    help_text="解除上一次的抽签",
)


@channel.use(AlconnaSchema(AlconnaDispatcher(alconna=draw, help_flag="reply")))
@channel.use(ListenerSchema([GroupMessage, FriendMessage]))
async def draw(
        app: Ariadne,
        sender: Union[Group, Friend],
        target: Union[Member, Friend],
        source: Source
):
    today = datetime.now().day
    if not bot.data.exist(target.id):
        return await app.sendMessage(sender, MessageChain.create("您还未找我签到~"), quote=source.id)
    user = bot.data.get_user(target.id)
    if not user.additional.get('draw_info'):
        user.additional['draw_info'] = [-1, "无"]
    local_day, draw_ans = user.additional['draw_info']
    if today != local_day:
        some_list = [0, 1, 2, 3, 4, 5, 6]  # 大凶，凶，末吉，小吉，中吉，吉，大吉
        probabilities = [0.09, 0.25, 0.06, 0.07, 0.11, 0.25, 0.17]
        draw_num = random_pick_small(some_list, probabilities)
        poetry_data = draw_poetry[draw_num]
        draw_ans = poetry_data['type']
        text = poetry_data['poetry'][random.randint(1, poetry_data['count']) - 1]
        user.additional['draw_info'] = [today, draw_ans]
        bot.data.update_user(user)
        return await app.sendMessage(
            sender, MessageChain(f"您今日的运势抽签为：{draw_ans}\n{text}"),
            quote=source.id
        )
    bot.data.update_user(user)
    return await app.sendMessage(
        sender, MessageChain(f"您今天已经抽过签了哦,运势为{draw_ans}"),
        quote=source.id
    )


@channel.use(AlconnaSchema(AlconnaDispatcher(alconna=undraw, help_flag="reply")))
@channel.use(ListenerSchema([GroupMessage, FriendMessage]))
async def draw(
        app: Ariadne,
        sender: Union[Group, Friend],
        target: Union[Member, Friend],
        source: Source
):
    if not bot.data.exist(target.id):
        return await app.sendMessage(sender, MessageChain.create("您还未找我签到~"), quote=source.id)
    user = bot.data.get_user(target.id)
    if not (info := user.additional.get('draw_info')) or info[0] == -1:
        return await app.sendMessage(sender, MessageChain.create("您今日还未抽签~"), quote=source.id)
    info[0] = -1
    return await app.sendMessage(sender, MessageChain.create("您已成功解签"), quote=source.id)