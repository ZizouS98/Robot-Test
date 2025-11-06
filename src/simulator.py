import time, re

class SimSerial:
    def __init__(self, addr="01"):
        self.addr = addr
        self.buf = b""
        self.pos = 0
        self.speed = 5
        self.target = None
        self.last = time.time()
    def _tick(self):
        now = time.time()
        dt = now - self.last
        self.last = now
        if self.target is None:
            return
        step = int(self.speed * 200 * dt)
        if step <= 0:
            return
        if self.target > self.pos:
            self.pos = min(self.pos + step, self.target)
        else:
            self.pos = max(self.pos - step, self.target)
        if self.pos == self.target:
            self.target = None
    def write(self, data: bytes):
        cmd = data.decode().strip()
        self._tick()
        m = re.match(r"^/(\d{2})\s+(\w+)(?:\s+([^\s]+))?(?:\s+([^\s]+))?\s*$", cmd)
        if not m:
            self.buf = f"@{self.addr} RJ BADFMT\n".encode(); return
        addr, verb, a1, a2 = m.groups()
        if addr != self.addr:
            self.buf = b""; return
        verb = verb.lower()
        if verb == "get":
            if a1 == "pos": self.buf = f"@{self.addr} OK {self.pos}\n".encode()
            elif a1 == "speed": self.buf = f"@{self.addr} OK {self.speed}\n".encode()
            else: self.buf = f"@{self.addr} RJ BADKEY\n".encode()
        elif verb == "set":
            if a1 != "speed" or a2 is None:
                self.buf = f"@{self.addr} RJ BADARGS\n".encode(); return
            try:
                v = int(a2)
            except:
                self.buf = f"@{self.addr} RJ BADVAL\n".encode(); return
            if not (1 <= v <= 10):
                self.buf = f"@{self.addr} RJ RANGE\n".encode()
            else:
                self.speed = v; self.buf = f"@{self.addr} OK {v}\n".encode()
        elif verb == "move":
            try:
                d = int(a1)
            except:
                self.buf = f"@{self.addr} RJ BADVAL\n".encode(); return
            self.target = self.pos + d
            self.buf = f"@{self.addr} OK 0\n".encode()
        else:
            self.buf = f"@{self.addr} RJ UNKNOWN\n".encode()
    def readline(self) -> bytes:
        for _ in range(20):
            self._tick(); time.sleep(0.002)
        out, self.buf = self.buf, b""; return out
