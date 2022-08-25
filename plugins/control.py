import asyncio
from arclet.alconna import Args, Option, CommandMeta, ArgField
from arclet.alconna.graia import Alconna, Match, command, match_path
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image  # Forward, ForwardNode
from graia.ariadne.model import Group
from graia.ariadne.app import Ariadne
from graia.ariadne.util.saya import decorate
from loguru import logger

from app import RaianMain, Sender, require_admin
from utils.generate_img import create_image

shutdown = Alconna("关机", Args["time", int, 0], meta=CommandMeta("关闭机器人", hide=True))

module_control = Alconna(
    "模块",
    options=[
        Option("列出", alias=["list"]),
        Option(
            "卸载",
            Args["name", str, ArgField(completion=lambda: "试试用‘control’")],
            alias=["关闭", "uninstall"],
            help_text="卸载一个模块",
        ),
        Option(
            "安装",
            Args["name", str, ArgField(completion=lambda: "试试用‘control’")],
            alias=["开启", "install"],
            help_text="安装一个模块",
        ),
        Option(
            "重载",
            Args["name", str, ArgField(completion=lambda: "试试用‘control’")],
            alias=["重启", "reload"],
            help_text="重新载入一个模块",
        ),
    ],
    meta=CommandMeta("管理机器人的模块", example="$模块 列出\n$模块 卸载 setu"),
)

function_control = Alconna(
    "功能",
    options=[
        Option("列出", alias=["list"]),
        Option(
            "禁用",
            Args["name", str, ArgField(completion=lambda: "试试用‘greet’")],
            alias=["ban"],
            help_text="禁用一个功能",
        ),
        Option(
            "启用",
            Args["name", str, ArgField(completion=lambda: "试试用‘greet’")],
            alias=["active"],
            help_text="启用一个功能",
        ),
    ],
    meta=CommandMeta("管理机器人的功能", example="$功能 列出\n$功能 禁用 greet"),
)

group_control = Alconna(
    "群管",
    options=[
        Option("当前状态|群组状态|状态|信息", dest="status", help_text="查看当前群组信息"),
        Option("黑名单 列入|加入", dest="add", help_text="将当前群组加入黑名单"),
        Option("黑名单 解除|移出|移除", dest="remove", help_text="将当前群组移出黑名单"),
        Option("退出"),
    ],
    meta=CommandMeta("操作当前群组", example="$群管 当前状态\n$群管 黑名单 加入"),
)


@command(Alconna("调试", meta=CommandMeta("显示调试信息")))
@decorate(require_admin())
async def debug(app: Ariadne, sender: Sender, bot: RaianMain):
    mds = f"当前共加载模块：{len(bot.saya.channels)}个\n已禁用模块: {bot.config.disabled_plugins}"
    groups_debug = f"当前共加入群：{len(bot.data.groups)}个"
    users_debug = f"当前共有：{len(bot.data.users)}人参与签到"
    res = [mds, groups_debug, users_debug]
    if isinstance(sender, Group):
        group = bot.data.get_group(sender.id)
        fns = "所在群组已列入黑名单" if group.in_blacklist else f"所在群组已禁用功能: {group.disabled}"
        res.append(fns)
    return await app.send_message(sender, MessageChain("\n".join(res)))


@command(shutdown)
@decorate(require_admin(True))
async def _s(app: Ariadne, sender: Sender, time: Match[int], bot: RaianMain):
    await app.send_message(sender, MessageChain("正在关机。。。"))
    await asyncio.sleep(time.result)
    bot.stop()
    await asyncio.sleep(0.1)


@command(module_control, send_error=True)
@decorate(match_path("列出"))
async def _m_list(app: Ariadne, sender: Sender, bot: RaianMain):
    saya = bot.saya
    res = "=================================\n"
    enables = list(saya.channels.keys())
    e_max = max(len(i) for i in enables) if saya.channels else 0
    d_max = (
        max(
            (len(i) + len(bot.config.plugin_path) + 1)
            for i in bot.config.disabled_plugins
        )
        if bot.config.disabled_plugins
        else 0
    )
    l_max = max(e_max, d_max)
    for name in enables:
        res += name.ljust(l_max + 1) + "已安装\n"
    for name in bot.config.disabled_plugins:
        res += f"{bot.config.plugin_path}.{name}".ljust(l_max + 1) + "已卸载\n"
    res += "================================="
    return await app.send_message(
        sender, MessageChain(Image(data_bytes=await create_image(res)))
    )


@command(module_control, send_error=True)
@decorate(require_admin(True), match_path("卸载"))
async def _m_uninstall(app: Ariadne, sender: Sender, name: Match[str], bot: RaianMain):
    saya = bot.saya
    channel_name = (name.result.split(".")[-1]) if name.available else "control"
    if channel_name == "control":
        return await app.send_message(sender, MessageChain("该模组未安装, 您可能需要安装它"))
    parent = bot.config.plugin_path
    module_path = f"{parent}.{channel_name}"
    if not (_channel := saya.channels.get(module_path)):
        return await app.send_message(sender, MessageChain("该模组未安装, 您可能需要安装它"))
    try:
        saya.uninstall_channel(_channel)
    except Exception as e:
        await app.send_message(sender, MessageChain(f"卸载 {module_path} 失败！"))
        raise e
    else:
        bot.config.disabled_plugins.append(channel_name)
        return await app.send_message(sender, MessageChain(f"卸载 {module_path} 成功"))


@command(module_control, send_error=True)
@decorate(require_admin(True), match_path("安装"))
async def _m_install(app: Ariadne, sender: Sender, name: Match[str], bot: RaianMain):
    saya = bot.saya
    channel_name = (name.result.split(".")[-1]) if name.available else "control"
    if channel_name == "control":
        return
    parent = bot.config.plugin_path
    module_path = f"{parent}.{channel_name}"
    if (
        channel_name in saya.channels
        and channel_name not in bot.config.disabled_plugins
    ):
        return await app.send_message(sender, MessageChain("该模组已安装"))
    try:
        with bot.context.use(bot):
            with saya.module_context():
                saya.require(module_path)
    except Exception as e:
        await app.send_message(sender, MessageChain(f"安装 {module_path} 失败！"))
        raise e
    else:
        if channel_name in bot.config.disabled_plugins:
            bot.config.disabled_plugins.remove(channel_name)
        return await app.send_message(sender, MessageChain(f"安装 {module_path} 成功"))


@command(module_control, send_error=True)
@decorate(require_admin(True), match_path("重载"))
async def _m_reload(app: Ariadne, sender: Sender, name: Match[str], bot: RaianMain):
    saya = bot.saya
    channel_name = (name.result.split(".")[-1]) if name.available else "control"
    if channel_name == "control":
        return
    parent = bot.config.plugin_path
    module_path = f"{parent}.{channel_name}"
    if not (_channel := saya.channels.get(module_path)):
        return await app.send_message(sender, MessageChain("该模组未安装, 您可能需要安装它"))
    try:
        with bot.context.use(bot):
            with saya.module_context():
                saya.reload_channel(_channel)
    except Exception as e:
        await app.send_message(sender, MessageChain(f"重载 {module_path} 失败！"))
        raise e
    else:
        return await app.send_message(sender, MessageChain(f"重载 {module_path} 成功"))


@command(module_control, send_error=True)
@decorate(match_path("$main"))
async def _m_main(app: Ariadne, sender: Sender):
    return await app.send_message(sender, MessageChain(module_control.get_help()))


@command(function_control, send_error=True)
@decorate(match_path("$main"))
async def _f_main(app: Ariadne, sender: Sender):
    return await app.send_message(sender, MessageChain(function_control.get_help()))


@command(function_control, private=False, send_error=True)
@decorate(match_path("列出"))
async def _f_list(app: Ariadne, sender: Group, bot: RaianMain):
    group = bot.data.get_group(sender.id)
    res = f"{sender.name} / {sender.id} 统计情况\n"
    res += "====================================\n"
    funcs = [
        (
            f"{i} {'(默认禁用)' if i in bot.data.disable_functions else ''} "
            f"备注: {bot.data.func_description(i)}"
        )
        for i in bot.data.funcs
    ]
    for sign, nm in zip(funcs, bot.data.funcs):
        res += (
            f"{'【禁用】' if nm in group.disabled or group.in_blacklist else '【启用】'} {sign}"
            + "\n"
        )
    res += "===================================="
    return await app.send_message(
        sender, MessageChain(Image(data_bytes=(await create_image(res))))
    )


@command(function_control, private=False, send_error=True)
@decorate(require_admin(), match_path("启用"))
async def _f_active(app: Ariadne, sender: Group, name: Match[str], bot: RaianMain):
    group = bot.data.get_group(sender.id)
    if not name.available:
        return await app.send_message(sender, MessageChain("该功能未找到"))
    name = name.result
    if group.in_blacklist or sender.id in bot.data.cache["blacklist"]:
        return await app.send_message(sender, MessageChain("所在群组已进入黑名单, 设置无效"))
    if name not in bot.data.funcs:
        return await app.send_message(sender, MessageChain(f"功能 {name} 不存在"))
    if name not in group.disabled:
        return await app.send_message(sender, MessageChain(f"功能 {name} 未禁用"))
    group.disabled.remove(name)
    bot.data.update_group(group)
    return await app.send_message(sender, MessageChain(f"功能 {name} 启用成功"))


@command(function_control, private=False, send_error=True)
@decorate(require_admin(), match_path("禁用"))
async def _f(app: Ariadne, sender: Group, name: Match[str], bot: RaianMain):
    group = bot.data.get_group(sender.id)
    if not name.available:
        return await app.send_message(sender, MessageChain("该功能未找到"))
    name = name.result
    if group.in_blacklist or sender.id in bot.data.cache["blacklist"]:
        return await app.send_message(sender, MessageChain("所在群组已进入黑名单, 设置无效"))
    if name not in bot.data.funcs:
        return await app.send_message(sender, MessageChain(f"功能 {name} 不存在"))
    if name in group.disabled:
        return await app.send_message(sender, MessageChain(f"功能 {name} 已经禁用"))
    group.disabled.append(name)
    bot.data.update_group(group)
    return await app.send_message(sender, MessageChain(f"功能 {name} 禁用成功"))


@command(group_control, send_error=True)
@decorate(match_path("$main"))
async def _g_main(app: Ariadne, sender: Sender):
    return await app.send_message(sender, MessageChain(group_control.get_help()))


@command(group_control, private=False, send_error=True)
@decorate(require_admin(True), match_path("退出"))
async def _g_quit(app: Ariadne, sender: Group, bot: RaianMain):
    await app.send_message(sender, "正在退出该群聊。。。")
    logger.debug(f"quiting from {sender.name}({sender.id})...")
    bot.data.remove_group(sender.id)
    return await app.quit_group(sender)


@command(group_control, private=False, send_error=True)
@decorate(match_path("status"))
async def _g_state(app: Ariadne, sender: Group, bot: RaianMain):
    group = bot.data.get_group(sender.id)
    fns = "所在群组已列入黑名单" if group.in_blacklist else f"所在群组已禁用功能: {group.disabled}"
    return await app.send_message(sender, fns)


@command(group_control, private=False, send_error=True)
@decorate(require_admin(), match_path("黑名单_add"))
async def _f(app: Ariadne, sender: Group, bot: RaianMain):
    group = bot.data.get_group(sender.id)
    if group.in_blacklist or sender.id in bot.data.cache["blacklist"]:
        return await app.send_message(sender, "该群组已加入黑名单!")
    group.in_blacklist = True
    bot.data.update_group(group)
    bot.data.cache["blacklist"].append(sender.id)
    return await app.send_message(sender, "该群组列入黑名单成功!")


@command(group_control, private=False, send_error=True)
@decorate(require_admin(), match_path("黑名单_remove"))
async def _f(app: Ariadne, sender: Group, bot: RaianMain):
    group = bot.data.get_group(sender.id)
    if group.in_blacklist or sender.id in bot.data.cache["blacklist"]:
        group.in_blacklist = False
        bot.data.update_group(group)
        if sender.id in bot.data.cache["blacklist"]:
            bot.data.cache["blacklist"].remove(sender.id)
        return await app.send_message(sender, "该群组移出黑名单成功!")
    return await app.send_message(sender, "该群组未列入黑名单!")
