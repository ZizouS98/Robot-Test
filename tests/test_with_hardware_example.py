import os
import pytest
from src.robot_client import RobotClient

# ****$Configuration hardware via variables d'environnement****
#   ROBOT_PORT : /dev/ttyUSB0 (Linux)
#   ROBOT_ADDR : exemple "01"

PORT = os.getenv("ROBOT_PORT", None)
ADDR = os.getenv("ROBOT_ADDR", "01")

pytestmark = pytest.mark.skipif(
    not PORT,
    reason="Test matériel ignoré : définir ROBOT_PORT pour activer ces tests."
)

def new_bot_hw():
    """
    Crée un RobotClient connecté AU MATERIEL REEL (port série).
    Timeout/baud ajustés pour un robot physique réel.
    """
    return RobotClient(port=PORT, baud=115200, addr=ADDR, timeout=1.0)

# T1 — Lecture de la position initiale
def test_get_pos_returns_int_hw():
    bot = new_bot_hw()
    p = bot.get_pos()
    assert isinstance(p, int)

# T2 — Lecture de la vitesse par défaut
def test_get_speed_in_range_hw():
    bot = new_bot_hw()
    s = bot.get_speed()
    assert 1 <= s <= 10

# T3 — Déplacement avant (+1000)
def test_move_forward_increases_pos_hw():
    bot = new_bot_hw()
    pos0 = bot.get_pos()
    bot.set_speed(5)               # vitesse nominale
    bot.move(1000)
    assert bot.wait_until(pos0 + 1000, timeout_s=20)  
    pos1 = bot.get_pos()
    assert pos1 - pos0 == 1000

# T4 — Déplacement arrière (-500)
def test_move_backward_decreases_pos_hw():
    bot = new_bot_hw()
    pos0 = bot.get_pos()
    bot.set_speed(5)
    bot.move(-500)
    assert bot.wait_until(pos0 - 500, timeout_s=20)
    pos1 = bot.get_pos()
    assert pos1 - pos0 == -500

# T5 — Déplacement nul (0)
def test_move_zero_no_change_hw():
    bot = new_bot_hw()
    posA = bot.get_pos()
    bot.move(0)
    posB = bot.get_pos()
    assert posB == posA
