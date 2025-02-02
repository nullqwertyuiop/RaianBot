from contextlib import suppress
from pathlib import Path
from typing import Union

from app import RaianBotInterface, Sender, record, accessable, exclusive
from arclet.alconna import Args, CommandMeta, Option, Kw
from arclet.alconna.graia import Alconna, Match, alcommand, assign
from arknights_toolkit.wordle import Guess, OperatorWordle
from arknights_toolkit import initialize
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.model import Friend, Group
from graia.ariadne.util.interrupt import FunctionWaiter

alc = Alconna(
    "猜干员",
    Args["max_guess", int, 8],
    Args["simple", Kw @ bool, False],
    Option("更新"),
    Option("规则"),
    Option("重置"),
    meta=CommandMeta("明日方舟猜干员游戏", usage="可以指定最大猜测次数"),
)


@alcommand(alc)
@record("猜干员")
@assign("规则")
@exclusive
@accessable
async def guess_info(app: Ariadne, sender: Sender):
    image = Path("assets/image/guess.png").open("rb").read()
    return await app.send_message(sender, MessageChain(Image(data_bytes=image)))


@alcommand(alc)
@record("猜干员")
@assign("更新")
@exclusive
@accessable
async def guess_update(app: Ariadne, sender: Sender):
    initialize()
    return await app.send_message(sender, "更新完毕")


@alcommand(alc)
@record("猜干员")
@assign("重置")
@exclusive
@accessable
async def guess_reset(
    app: Ariadne,
    sender: Sender,
    bot: RaianBotInterface,
):
    id_ = f"{app.account}_g{sender.id}" if isinstance(sender, Group) else f"{app.account}_f{sender.id}"
    if (file := Path(f"{bot.base_config.plugin_cache_dir / 'guess' / f'{id_}.json'}")).exists():
        file.unlink(missing_ok=True)
    return await app.send_message(sender, "重置完毕")


@alcommand(alc)
@record("猜干员")
@assign("$main")
@exclusive
@accessable
async def guess(
    app: Ariadne,
    sender: Sender,
    bot: RaianBotInterface,
    max_guess: Match[int],
    simple: Match[bool],
):
    id_ = f"g{sender.id}" if isinstance(sender, Group) else f"f{sender.id}"

    wordle = OperatorWordle(f"{bot.base_config.plugin_cache_dir / 'guess'}", max_guess.result)
    if (Path(f"{bot.base_config.plugin_cache_dir / 'guess' / f'{id_}.json'}")).exists():
        if id_ not in bot.data.cache.setdefault("$guess", []):
            return await app.send_message(sender, f"游戏异常，请重置后再试\n重置方法：{bot.base_config.command.headers[0]}猜干员 重置")
        await app.send_message(sender, "游戏继续！")
    else:
        wordle.select(id_)
        await app.send_message(sender, "猜干员游戏开始！\n发送 取消 可以结束当前游戏")

    async def waiter(waiter_sender: Sender, message: MessageChain):
        name = str(message)
        if sender.id == waiter_sender.id:
            if name.startswith("取消"):
                await app.send_message(sender, "已取消")
                return False
            with suppress(ValueError):
                return wordle.guess(name, id_)
            return
    bot.data.cache.setdefault("$guess", []).append(id_)
    while True:
        res: Union[bool, Guess, None] = await FunctionWaiter(
            waiter,
            [GroupMessage, FriendMessage],
            block_propagation=isinstance(sender, Friend),
        ).wait(timeout=120, default=False)
        if res is None:
            continue
        if not res:
            wordle.restart(id_)
            bot.data.cache["$guess"].remove(id_)
            return await app.send_message(
                sender,
                f"{'' if isinstance(sender, Friend) else f'{sender.name}的'}游戏已结束！",
            )
        try:
            if simple.result:
                await app.send_message(sender, MessageChain(wordle.draw(res, simple=True)))
            else:
                await app.send_message(sender, MessageChain(Image(data_bytes=wordle.draw(res))))
        except Exception as e:
            await app.send_friend_message(bot.config.admin.master_id, f'{e}')
            break
        if res.state != "guessing":
            break
    wordle.restart(id_)
    bot.data.cache["$guess"].remove(id_)
    return await app.send_message(
        sender,
        f"{'' if isinstance(sender, Friend) else f'{sender.name}的'}游戏已结束！\n答案为{res.select}",
    )
