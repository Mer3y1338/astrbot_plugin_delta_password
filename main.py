import aiohttp
from astrbot.api.event import filter, AstrMessageEvent, MessageChain
from astrbot.api.star import Context, Star, register

@register("astrbot_plugin_delta_password", "Hermes", "三角洲行动每日密码查询插件", "1.0.1")
class DeltaPasswordPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("粥密码", alias={"每日密码", "三角洲密码"})
    async def deltaforce_daily_password(self, event: AstrMessageEvent):
        """查询三角洲行动各地图每日密码"""
        url = "https://tmini.net/api/sjzmm?type=json"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    data = await resp.json()
                    if data.get("status") == "success" and data.get("data", {}).get("passwords"):
                        passwords = data["data"]["passwords"]
                        results = []
                        for item in passwords:
                            map_name = item.get("map_name", "未知")
                            password = item.get("password", "未知")
                            results.append(f"🗺 {map_name}：🔑 {password}")
                        result_text = "\n".join(results)
                        msg = f"🔐 三角洲行动每日密码\n{'─' * 22}\n{result_text}\n{'─' * 22}\n⏰ 数据来源：Tmini.net"
                    else:
                        msg = "❌ 暂无密码数据，请稍后再试"
            except Exception as e:
                msg = f"⚠️ 查询失败：{str(e)}"

        yield event.plain_result(msg)
