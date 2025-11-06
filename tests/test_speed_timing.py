import time
from src.robot_client import RobotClient
from src.simulator import SimSerial

def test_speed_affects_time():
    sim = SimSerial(addr="01")
    bot = RobotClient(transport=sim, addr="01")
    distance = 2000; timings = []
    for sp in (2,5,10):
        bot.set_speed(sp)
        p0 = bot.get_pos()
        t0 = time.time()
        bot.move(distance)
        assert bot.wait_until(p0 + distance, timeout_s=20), f"Timeout à speed={sp}"
        dt = time.time() - t0; timings.append(dt)
        bot.move(-distance); assert bot.wait_until(p0, timeout_s=20)
    assert timings[0] > timings[1] * 1.05 and timings[1] > timings[2] * 1.05, f"Durées inattendues: {timings}"
