import pygame, sys, random
from pygame.locals import *
import PacketParser

def tremble_list(l, r, skip=1):
    def tremble_point(t, r):
        rnd = random.randrange
        return (t[0] + rnd(-r, r), t[1] + rnd(-r, r))
    return tuple([tremble_point(p, r) for p in l][::skip])

def is_in_region(re, x, y):
    return (re[0][0] < x < re[1][0]) and (re[0][1] < y < re[1][1])

def main():
    wx, wy = 640, 480

    parser = PacketParser.Parser(port = 6)
    parser.start()

    pygame.init()
    fps = pygame.time.Clock()

    window = pygame.display.set_mode((wx, wy))
    pygame.display.set_caption('Digital Pen Demo')
    surface = pygame.Surface((wx*2, wy*2))

    col = {
        #'black': pygame.Color('0x000000'),
        #'red': pygame.Color('0xFF0000'),
        #'white': pygame.Color('0xFFFFFF')
        'black': pygame.Color(0, 0, 0),
        'red': pygame.Color(255, 0, 0),
        'white': pygame.Color(255, 255, 255)
    }

    region = {
        'black': ((515.0, 650.0), (775.0, 915.0)),
        'red': ((775.0, 650.0), (1035.0, 915.0))
    }

    scale = 0.15
    tremble = False
    stroke_list = []
    color_list = []
    current_color = col['black']

    while True:
        if parser.get_locked(): # Get mutex mine / Get stroke
            stroke = parser.get_stroke();
            for rn in region.keys(): # Whether be changing color or not
                if is_in_region(region[rn], stroke[0].x, stroke[0].y):
                    current_color = col[rn]
                    break
            else:
                stroke_list.append(tuple((p.x * scale, p.y * scale) for p in stroke))
                color_list.append(current_color)

        surface.fill(col['white']) # Let there be light

        for (st, co) in zip(stroke_list, color_list): # Draw lines
            if len(st) >= 2:
                if tremble:
                    pygame.draw.lines(surface, co, 0, tremble_list(st, 3, 2), 5)
                else:
                    pygame.draw.lines(surface, co, 0, st, 5)

        for event in pygame.event.get(): # Deal with events
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.display.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                tremble = not tremble

        window.blit(pygame.transform.smoothscale(surface, (wx, wy)), (0, 0))
        pygame.display.update()
        fps.tick(60)

if __name__ == '__main__':
    main()