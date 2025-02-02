import asyncio
from typing import Tuple
from arclet.alconna import Args, Option, Field, CommandMeta, MultiVar
from arclet.alconna.graia import Alconna, alcommand, Match, Query
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Source
from graia.ariadne.app import Ariadne
from graiax.playwright import PlaywrightBrowser
from arknights_toolkit.recruit import recruitment

from app import Sender, accessable, exclusive

recruit = Alconna(
    "公招",
    Args["tags", MultiVar(str, "+"), Field('...', completion=lambda: "高资")],
    Option("详细|--d", dest="detail"),
    meta=CommandMeta("自助访问 prts 的公招计算器并截图", usage="标签之间用空格分隔", example="$公招 高资 生存"),
)
running = asyncio.Event()


@alcommand(recruit, send_error=True)
@exclusive
@accessable
async def recruit(
    app: Ariadne, sender: Sender, source: Source, tags: Match[Tuple[str, ...]], detail: Query = Query("detail")
):
    if not tags.available:
        return await app.send_message(sender, MessageChain("不对劲..."))
    if running.is_set():
        return await app.send_message(sender, "请耐心排队~")
    await app.send_message(sender, MessageChain("正在获取，请稍等。。。"), quote=source.id)
    # Click html
    browser: PlaywrightBrowser = app.launch_manager.get_interface(PlaywrightBrowser)
    # Go to https://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88
    url = recruitment(
        list(map(lambda x: x.replace("干员", "").replace("高级资深", "高级资深干员"), tags.result)), not detail.available
    )
    try:
        running.set()
        async with browser.page() as page:
            await page.goto(
                url, timeout=60000, wait_until="networkidle" if result.find("detail") else "load"  # type: ignore
            )
            elem = await page.query_selector("table#calc-result")
            data = await elem.screenshot(type="png")
            await app.send_message(sender, MessageChain(Image(data_bytes=data)))
    except Exception:
        await app.send_message(sender, MessageChain("prts超时，获取失败"), quote=source.id)
        await app.send_message(sender, MessageChain(url), quote=source.id)
    finally:
        running.clear()
