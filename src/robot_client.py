import time, re
try:
    import serial
except ImportError:
    serial = None

class RobotClient:
    def __init__(self, port=None, baud=115200, addr="01", timeout=1.0, transport=None):
        self.addr = addr
        self.timeout = timeout
        if transport is not None:
            self.ser = transport
        else:
            if serial is None:
                raise RuntimeError("Installez pyserial (pip install pyserial), ou passez un transport simulateur.")
            self.ser = serial.Serial(port, baudrate=baud, timeout=timeout)
        self._re = re.compile(rf"^@{addr}\s+(OK|RJ)\s+(.+)$")
    def send(self, line: str):
        if not line.endswith("\n"): line += "\n"
        self.ser.write(line.encode())
        resp = self.ser.readline().decode().strip()
        m = self._re.match(resp)
        if not m: raise RuntimeError(f"Réponse mal formée/adresse inattendue: '{resp}'")
        return m.group(1), m.group(2)
    def get_pos(self) -> int:
        st, v = self.send(f"/{self.addr} get pos");
        if st != "OK": raise RuntimeError(f"get pos rejeté: {v}")
        return int(v)
    def get_speed(self) -> int:
        st, v = self.send(f"/{self.addr} get speed");
        if st != "OK": raise RuntimeError(f"get speed rejeté: {v}")
        return int(v)
    def set_speed(self, s: int):
        st, v = self.send(f"/{self.addr} set speed {s}");
        if st != "OK": raise RuntimeError(f"set speed rejeté: {v}")
    def move(self, d: int):
        st, v = self.send(f"/{self.addr} move {d}");
        if st != "OK": raise RuntimeError(f"move rejeté: {v}")
    def wait_until(self, target: int, timeout_s=10.0, poll=0.05, settle_reads=3):
        end = time.time() + timeout_s; last = []
        while time.time() < end:
            p = self.get_pos(); last.append(p)
            if len(last) > settle_reads: last.pop(0)
            if p == target and len(last) == settle_reads and all(x == target for x in last):
                return True
            time.sleep(poll)
        return False
