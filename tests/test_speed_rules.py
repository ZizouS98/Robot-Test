import pytest
from src.robot_client import RobotClient
from src.simulator import SimSerial

def new_bot():
    return RobotClient(transport=SimSerial("01"), addr="01")

def test_speed_bounds_accept():
    bot = new_bot()
    bot.set_speed(1)
    assert bot.get_speed() == 1
    bot.set_speed(10)
    assert bot.get_speed() == 10

def test_speed_out_of_range_rejected():
    bot = new_bot()
    for bad in (0, 11, -1):
        with pytest.raises(Exception):
            bot.set_speed(bad)

def test_speed_type_invalid_rejected():
    bot = new_bot()
    st, val = bot.send("/01 set speed abc")
    assert st == "RJ" and val in ("BADVAL","BADARGS","BADFMT")
    st, val = bot.send("/01 set speed 3.5")
    assert st == "RJ" and val in ("BADVAL","BADARGS","BADFMT")

def test_speed_persists_across_move():
    bot = new_bot()
    bot.set_speed(7)
    start = bot.get_pos()
    bot.move(200)
    assert bot.wait_until(start + 200, timeout_s=10)
    assert bot.get_speed() == 7
