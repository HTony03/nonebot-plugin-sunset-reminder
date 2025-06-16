from typing import Literal
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebug import App
import pytest


class ANY:
    def __eq__(self, other) -> Literal[True]:
        return True


@pytest.mark.asyncio
async def test_city(app: App) -> None:
    import nonebot
    from nonebot import require
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    assert require("nonebot_plugin_sunset_reminder")

    from nonebot.adapters.onebot.v11.event import MessageEvent
    from nonebot.adapters.onebot.v11 import Message

    event = MessageEvent(
        time=123456,
        self_id=123456,
        post_type="message",
        user_id=1234567890,
        message_type="group",
        message_id=1234567890,
        message=Message("/search -c 上海"),
        raw_message="/search -c 上海",
        original_message=Message("/search -c 上海"),
        sub_type="normal",
        sender={"user_id": 1234567890, "nickname": "测试用户"},
        font=123,
    )

    try:
        from nonebot_plugin_sunset_reminder.commands import search
    except ImportError:
        pytest.skip("nonebot_plugin_sunset_reminder.commands.search not found")

    async with app.test_matcher(search) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, ANY(), result=None, bot=bot)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_latest_remind(app: App):
    import nonebot
    from nonebot import require
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    assert require("nonebot_plugin_sunset_reminder")

    # 构造 shell command 事件
    from nonebot.adapters.onebot.v11.event import MessageEvent
    from nonebot.adapters.onebot.v11 import Message

    event1 = MessageEvent(
        time=123456,
        self_id=123456,
        post_type="message",
        user_id=1234567890,
        message_type="group",
        message_id=1234567890,
        message=Message("/latest_sunset_remind"),
        raw_message="/latest_sunset_remind",
        original_message=Message("/latest_sunset_remind"),
        sub_type="normal",
        sender={"user_id": 1234567890, "nickname": "测试用户"},
        font=123,
    )
    event2 = MessageEvent(
        time=123456,
        self_id=123456,
        post_type="message",
        user_id=1234567890,
        message_type="group",
        message_id=1234567890,
        message=Message("/latest_sunrise_remind"),
        raw_message="/latest_sunrise_remind",
        original_message=Message("/latest_sunrise_remind"),
        sub_type="normal",
        sender={"user_id": 1234567890, "nickname": "测试用户"},
        font=123,
    )

    async with app.test_matcher() as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        ctx.receive_event(bot, event1)
        ctx.should_call_send(event1, ANY(), result=None, bot=bot)
        ctx.should_finished()
        ctx.receive_event(bot, event2)
        ctx.should_call_send(event2, ANY(), result=None, bot=bot)
        ctx.should_finished()
