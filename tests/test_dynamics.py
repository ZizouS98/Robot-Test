import time
from src.robot_client import RobotClient
from src.simulator import SimSerial

def new_bot():
    return RobotClient(transport=SimSerial("01"), addr="01")

def non_decreasing(seq):
    return all(b >= a for a, b in zip(seq, seq[1:]))

def test_position_monotonic_during_move_forward():
    bot = new_bot(); bot.set_speed(6); 
    pos0 = bot.get_pos(); 
    target = pos0 + 500; 
    bot.move(500)
    samples = []; 
    t_end = time.time() + 5
    while time.time() < t_end:
        p = bot.get_pos(); samples.append(p)
        if p == target: break
        time.sleep(0.02)
    assert bot.wait_until(target, timeout_s=5)
    assert non_decreasing(samples)

def test_stability_after_move():
    bot = new_bot(); 
    bot.set_speed(5); 
    pos0 = bot.get_pos(); 
    target = pos0 + 300; bot.move(300)
    assert bot.wait_until(target, timeout_s=8)
    reads = [bot.get_pos() for _ in range(5)]
    assert all(r == target for r in reads)
