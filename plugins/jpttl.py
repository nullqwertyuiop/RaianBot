import re
from aiohttp import ClientSession, TCPConnector
from arclet.alconna import Args, ArgField, CommandMeta
from arclet.alconna.graia import Alconna, command, Match
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.app import Ariadne
from graia.ariadne.message.element import Voice
from graiax.silkcoder import async_encode
from typing import Tuple

from app import Sender


@command(
    Alconna(
        "日本语",
        Args[
            "jp;S",
            str,
            ArgField(completion=lambda: "比如说，daisuki"),
        ],
        meta=CommandMeta("日本语本当上手", usage="日语文本的tts", example="$日本语 suki"),
    )
)
async def weather(app: Ariadne, sender: Sender, jp: Match[Tuple[str]]):
    sentence = " ".join(jp.result)
    if not sentence.strip() or re.search(r"[\d_+=\-/@#$%^&*(){}\[\]|\\]", sentence):
        return await app.send_message(sender, "无效的文本")
    async with ClientSession(connector=TCPConnector(limit=64, verify_ssl=False)) as session:
        try:
            async with session.post(
                    "https://cloud.ai-j.jp/demo/aitalk2webapi_nop.php",
                    data={"speaker_id": 1209, "text": sentence, "speed": 0.8, "pitch": 1.1},

            ) as resp:
                audio_name = (await resp.text())[47:-3]
            async with session.get(
                    f"https://cloud.ai-j.jp/demo/tmp/{audio_name}"
            ) as resp:
                data = await resp.read()
            time = len(data) * 8 / 128000
            start = 3.8 if time > (3.1 if len(sentence) < 4 else 4.5) else 2.3
            if time - start < 0.3:
                return await app.send_message(sender, "有误的文本")
            res = await async_encode(data[int(start * 128000 / 8):], ios_adaptive=True)
            return await app.send_message(sender, MessageChain(Voice(data_bytes=res)))
        except Exception:
            return await app.send_message(sender, "未知错误")
