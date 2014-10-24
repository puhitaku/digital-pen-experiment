import serial, threading

class Packet(object):
    """Abstract class of a packet."""
    def __init__(self, arg):
        self.code = arg[0]
        self.length = arg[2]

    def join_bytes(self, l):
        l.reverse()
        s = 0
        for i,j in enumerate(l):
            s += j * 256 ** i
        return s

class InitPacket(Packet):
    """This class contains the informations of a initialization packet."""
    def __init__(self, arg):
        super().__init__(arg)
        self.time = self.join_bytes(arg[9:13])

class StrokePacket(Packet):
    """This class contains the informations of stroke packets."""
    def __init__(self, arg):
        super().__init__(arg)
        self.time = self.join_bytes(arg[7:11])
        self.x = self.join_bytes(arg[19:21])
        self.y = self.join_bytes(arg[21:23])
        self.pressure = 256 - arg[23]

class Parser(threading.Thread):
    def __init__(self, port=0):
        super().__init__()
        self.lock = threading.Lock()
        self.stroke = []
        self.copied = []

        print("Parser: opening COM" + str(port))
        self.s = serial.Serial(
            port='COM' + str(port),
            baudrate=9600,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=None,
            xonxoff=0,
            rtscts=0,
            writeTimeout=None,
            dsrdtr=None)
        print("Serial port is initialized.")

    def run(self):
        while True:
            #Get packet's code
            pct = list(self.s.read(3))

            if pct[0] == 0x02 :
                pct.extend(list(self.s.read( pct[2] )))
                self.init = InitPacket(pct)
                print(  "0x02: initiation packet, Length =", self.init.length,
                        ", Time =", self.init.time)

            elif pct[0] == 0x03 :
                if len(self.copied) > 0:
                    self.copied = []

                pct.extend(list(self.s.read( pct[2] )))
                _p = StrokePacket(pct)
                self.stroke.append(_p)

                print(  "0x03: stroke packet, Length =", _p.length,
                        ", Time =", _p.time,
                        ", X =", _p.x,
                        ", Y =", _p.y,
                        ", Pressure =", _p.pressure)
                
            elif pct[0] == 0x04 :
                print("0x04: end packet")
                self.copied = self.stroke

            else :
                print("Unknown packet, Length =", len(pct))

    def get_locked(self):
        state = False
        if self.lock.acquire(False):
            if len(self.copied) > 0:
                ax = sum([p.x for p in self.copied]) / len(self.copied)
                ay = sum([p.y for p in self.copied]) / len(self.copied)
                print("Got:", len(self.copied), "points")
                print("Average X:", ax)
                print("Average Y:", ay)
                state = True
            else:
                state = False
            self.lock.release()
        return state

    def get_stroke(self):
        if self.copied != []:
            _ = self.copied
            self.copied = []
            self.stroke = []
            return _