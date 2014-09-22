import pygame, threading, serial, sys, random
from pygame.locals import *

class Packet(object):
    """Abstract class of a packet."""
    def __init__(self, arg):
        self.code = arg[0]
        self.length = arg[2]

class InitPacket(Packet):
    """This class contains the informations of a initialization packet."""
    def __init__(self, arg):
        super().__init__(arg)

class StrokePacket(Packet):
    """This class contains the informations of stroke packets."""
    def __init__(self, arg):
        super().__init__(arg)
        self.x = arg[19] * 256 + arg[20]
        self.y = arg[21] * 256 + arg[22]
        self.pressure = 256 - arg[23]

class PenParser(threading.Thread):
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
                pct = pct[:] + list(self.s.read( pct[2] ))
                self.init = InitPacket(pct)

            elif pct[0] == 0x03 :
                if len(self.copied) > 0:
                    self.copied = []

                pct = pct[:] + list(self.s.read( pct[2] ))
                _p = StrokePacket(pct)
                self.stroke.append(_p)

                print(    "0x03: stroke packet, Length =", _p.length,
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

def blur(t, r):
    rnd = random.randrange
    return (t[0] + rnd(-r, r), t[1] + rnd(-r, r))

def blur_list(l, r, skip=1):
    return tuple([blur(p, r) for p in l][::skip])

def is_in_region(re, x, y):
    return (re[0][0] < x < re[1][0]) and (re[0][1] < y < re[1][1])

def main():
    parser = PenParser(port = 6)
    parser.start()

    pygame.init()
    fps = pygame.time.Clock()

    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Digital Pen Demo")

    color_black = pygame.Color(0, 0, 0)
    color_red = pygame.Color(255, 0, 0)
    color_white = pygame.Color(255, 255, 255)
    current_color = color_black

    scale = 0.15
    blur_flag = False
    region_black = [(515.0, 650.0), (775.0, 915.0)]
    region_red = [(775.0, 650.0), (1035.0, 915.0)]

    stroke_list = []
    color_list = []

    while True:
        if parser.get_locked():
            stroke = parser.get_stroke();
            if is_in_region(region_black, stroke[0].x, stroke[0].y):
                current_color = color_black
            elif is_in_region(region_red, stroke[0].x, stroke[0].y):
                current_color = color_red
            else:
                stroke_list.append(tuple((p.x * scale, p.y * scale) for p in stroke))
                color_list.append(current_color)

        window.fill(color_white)

        for (l, col) in zip(stroke_list, color_list):
            if len(l) >= 2:
                if blur_flag:
                    pygame.draw.lines(window, col, 0, blur_list(l, 3, 2), 5)
                else:
                    pygame.draw.lines(window, col, 0, l, 5)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.display.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                blur_flag = not blur_flag

        pygame.display.update()
        fps.tick(15)

if __name__ == "__main__":
    main()