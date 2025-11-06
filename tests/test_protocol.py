import pytest
from src.robot_client import RobotClient
from src.simulator import SimSerial

def new_bot():
    return RobotClient(transport=SimSerial("01"), addr="01")

def test_unknown_command_rejected():
    bot = new_bot()
    st, val = bot.send("/01 tourne 10")
    assert st == "RJ" and val == "UNKNOWN"

def test_missing_arguments_rejected():
    bot = new_bot()
    st, val = bot.send("/01 move")
    assert st == "RJ" and val in ("BADVAL","BADARGS","BADFMT")
    st, val = bot.send("/01 set speed")
    assert st == "RJ" and val in ("BADARGS","BADVAL","BADFMT")

def test_wrong_address_no_response():
    bot = new_bot()
    with pytest.raises(RuntimeError):
        bot.send("/02 get pos")

def test_multiple_spaces_tolerated():
    bot = new_bot()
    st, val = bot.send("/01  get   pos")
    assert st == "OK"; int(val)

def test_case_insensitive_verbs():
    bot = new_bot()
    st, val = bot.send("/01 GET pos")
    assert st == "OK" and isinstance(int(val), int)
    st, val = bot.send("/01 Set speed 5")
    assert st == "OK" and val == "5"
