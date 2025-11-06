from src.robot_client import RobotClient
from src.simulator import SimSerial

def new_bot():
    sim = SimSerial(addr="01")
    return RobotClient(transport=sim, addr="01")

def test_get_pos_returns_int():
    bot = new_bot()
    p = bot.get_pos()
    assert isinstance(p, int)

def test_get_speed_in_range():
    bot = new_bot()
    s = bot.get_speed()
    assert 1 <= s <= 10

def test_move_forward_increases_pos():
    bot = new_bot()
    pos0 = bot.get_pos()
    bot.set_speed(5)
    bot.move(1000)
    assert bot.wait_until(pos0 + 1000, timeout_s=10)
    pos1 = bot.get_pos()
    assert pos1 - pos0 == 1000

def test_move_backward_decreases_pos():
    bot = new_bot()
    pos0 = bot.get_pos()
    bot.set_speed(5)
    bot.move(-500)
    assert bot.wait_until(pos0 - 500, timeout_s=10)
    pos1 = bot.get_pos(); assert pos1 - pos0 == -500

def test_move_zero_no_change():
    bot = new_bot()
    posA = bot.get_pos()
    bot.move(0)
    posB = bot.get_pos()
    assert posB == posA
