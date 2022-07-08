from nonebot import on_regex
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
from utils.utils import scheduler, get_bot
from utils.manager import group_manager
from configs.config import Config
import time

__zx_plugin_name__ = "水晶推车"
__plugin_usage__ = """
usage: 某些只会在风图玩黑魔的功利逼献上的推车地图提醒器
    指令：
        crystal
""".strip()
__plugin_des__ = "某些只会在风图玩黑魔的功利逼献上的推车地图提醒器"
__plugin_cmd__ = ["crystal"]
__plugin_version__ = 0.1
__plugin_author__ = "sandbagimon"

__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["crystal"],
}
__plugin_task__ = {"crystal_conflict": "推车地图"}
Config.add_plugin_config(
    "_task",
    "DEFAULT_CRYSTAL",
    True,
    help_="被动 显示当前水晶推车地图 进群默认开启状态",
    default_value=True,
)

crystal = on_regex("^推车地图$", priority=5, block=True)
map = {0: "操场", 1: "火山", 2: "风图"}


@crystal.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    try:
        ts = int(time.time())
        map_type = ts // 5400 % 3  ## 2 风 ， 0 操场， 1 火山
        remain_time = ts % 5400
        minutes, seconds = divmod(remain_time, 60)

        str = "Bot为您报时，现在的地图为{}, 距离下次更新地图还有{}分{}秒".format(
            map[map_type],
            minutes,
            seconds
        )

        msg_id = await crystal.send(str)
    except Exception as e:
        await crystal.send("BOT...再起不能！")
        logger.error(f"crystal 发送了未知错误 {type(e)}：{e}")

# @scheduler.scheduled_job(
#     "cron",
#     hour=12,
#     minute=1,
# )
# async def _():
#     # 每小时提醒
#     bot = get_bot()
#     if bot:
