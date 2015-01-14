import pygame, sys, random
from pygame.locals import *
from numpy import matrix, transpose, angle
from numpy.linalg import norm
from math import sin, cos, sqrt, degrees, pi
import Algebra as alg
import PacketParser

def tremble_list(l, r, skip=1):
    def tremble_point(t, r):
        rnd = random.randrange
        return (t[0] + rnd(-r, r), t[1] + rnd(-r, r))
    return [tremble_point(p, r) for p in l][::skip]

def is_in_region(re, x, y):
    return (re[0][0] < x < re[1][0]) and (re[0][1] < y < re[1][1])

def alt_line(surface, color, start, end, w=1):
    w /= 2
    _start = matrix([start[0], start[1]]).T
    _end   = matrix([end[0], end[1]]).T
    arrow  = _end - _start

    l = norm(arrow) #Vector norm
    t = alg.angle_from_vector(arrow)
    rot = alg.get_rot_matrix(t)

    vertex = [
        matrix([0, w]).T,
        matrix([l, w]).T,
        matrix([l, -w]).T,
        matrix([0, -w]).T
    ]

    vertex = [rot * v + _start for v in vertex] #Rotate and shift
    vertex = [(v[0,0], v[1,0]) for v in vertex] #Convert in tuples

    pygame.draw.polygon(surface, color, vertex, 0)

def alt_lines(surface, color, vertex, w=1):
    for (v1, v2) in zip(vertex[:-1], vertex[1:]):
        alt_line(surface, color, v1, v2, w)

def arrow_line(surface, color, start, end, w=1, ratio=2):
    w_line, w_tri = w, (w/2)*ratio
    _start, _end = matrix([start[0], start[1]]).T, matrix([end[0], end[1]]).T
    vector = _end - _start
    t = alg.angle_from_vector(vector)
    rot = alg.get_rot_matrix(t)

    vertex = [
        matrix([0, w_tri]).T,
        matrix([0, -w_tri]).T,
        matrix([sqrt(3.0)*w_tri, 0]).T
    ]

    vertex = [rot * v + _end for v in vertex] #Rotate and shift
    vertex = [(v[0,0], v[1,0]) for v in vertex] #Convert in tuples

    alt_line(surface, color, start, end, w_line)
    pygame.draw.polygon(surface, color, vertex, 0)

def draw_stroke_order(surface, font, color, stroke, num, r, w, l):
    """Draws number and arrow by a stroke.

    Args:
      surface (pygame.Surface): The surface you want it to draw on.
      font (pygame.font): The font of number.
      color (pygame.Color): Color of number and arrow.
      stroke ([tuple]): List of points.
      num (int): Number of arrow.
      r (int): Radius between an arrow and a stroke.
      w (int): Width of arrow.
      l (int): Length of arrow.

    """

    dist = alg.get_stroke_distance(stroke)
    dl = 0 #Sum of distances between each points on a stroke
    st = stroke#[::2] #Reduce points for performance
    st_pair = zip(st[:-1], st[1:])

    for ((i, j), k) in zip(st_pair, range(len(st))):
        vec_rel = matrix(j) - matrix(i)
        dl += norm(vec_rel)
        if dl > (dist*0.1):
            p1 = k
            break

    dl = 0
    for ((i, j), k) in zip(st_pair, range(p1, len(st))):
        vec_rel = matrix(j) - matrix(i)
        dl += norm(vec_rel)
        if dl > (dist*0.2):
            p2 = k
            break

    p_from = list(st[p1])
    rel    = alg.vec_between_two(st[p1], st[p2], normalize=True, rtype=tuple)
    rel    = [v*l for v in rel]
    p_to   = [sum(x) for x in zip(list(st[p1]), rel)]

    shift  = alg.vec_between_two(p_from, p_to, normalize=True, rtype=matrix).T

    if -pi/2 < alg.angle_from_vector(shift) < pi/2:
        shift_dir = -pi/2
    else:
        shift_dir = pi/2

    shift  = alg.get_rot_matrix(shift_dir) * shift
    shift  = shift.T.tolist()
    shift  = [shift[0][0], shift[0][1]]
    p_from = [v+(s*r) for (v, s) in zip(p_from, shift)]
    p_to   = [v+(s*r) for (v, s) in zip(p_to, shift)]

    arrow_line(surface, color, tuple(p_from), tuple(p_to), w)

    pos_num = [v+(s*r) for (v, s)
               in zip(alg.middle_between_two(p_from, p_to), shift)]
    surface_num = font.render(str(num), False, color)
    rect_num = surface_num.get_rect()
    rect_num.midbottom = tuple(pos_num)
    surface.blit(surface_num, rect_num)


def main():
    wx, wy, over = 640, 480, 2  #over = oversampling

    parser = PacketParser.Parser(port = 6)
    parser.start()

    pygame.init()
    fps = pygame.time.Clock()
    window = pygame.display.set_mode((wx, wy))
    surface = pygame.Surface((wx*over, wy*over))
    font = pygame.font.Font('C:\\windows\\fonts\\lucon.ttf', 50)
    scale = 0.15 * over
    stroke_list = []
    color_list = []

    col = {
        'black': pygame.Color(0, 0, 0),
        'red': pygame.Color(255, 0, 0),
        'white': pygame.Color(255, 255, 255)
    }

    region = {
        'black': ((515.0, 650.0), (775.0, 915.0)),
        'red': ((775.0, 650.0), (1035.0, 915.0))
    }

    mode = {
        'normal': K_1,
        'tremble': K_2,
        'order': K_3
    }

    mode_inv = dict((b, a) for (a,b) in mode.items())

    current_color = col['black']
    chose_mode = mode['normal']

    while True:
        if parser.get_locked(): # Get mutex mine / Get stroke
            stroke = parser.get_stroke();
            for rn in region.keys(): # Whether be changing color or not
                if is_in_region(region[rn], stroke[0].x, stroke[0].y):
                    current_color = col[rn]
                    break
            else:
                stroke_list.append([(p.x * scale, p.y * scale) for p in stroke])
                color_list.append(current_color)

        surface.fill(col['white']) # Let there be light

        mouse = pygame.mouse.get_pos()
        mouse_dist = norm(mouse)
        #arrow_line(surface, col['red'], (500, 400), mouse, mouse_dist/8, 3)

        for (st, co, i) in zip(stroke_list, color_list, range(1, len(stroke_list)+1)): # Draw lines
            if len(st) >= 5:
                if   chose_mode == mode['normal']:
                    pygame.draw.lines(surface, co, 0, st, 6*over)

                elif chose_mode == mode['tremble']:
                    pygame.draw.lines(surface, co, 0, tremble_list(st, 5, 2), 6*over)
                    #alt_lines(surface, co, tremble_list(st, 3, 2), 20)
                elif chose_mode == mode['order']:
                    pygame.draw.lines(surface, co, 0, st, 6*over)
                    draw_stroke_order(surface, font, col['red'], st,
                                      i, 15*over, 10*over, 30*over)

        for event in pygame.event.get(): # Deal with events
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit()

                elif event.key in mode.values():
                    chose_mode = mode[mode_inv[event.key]]

        pygame.display.set_caption('Digital Pen Test  fps:%d' % fps.get_fps())
        window.blit(pygame.transform.smoothscale(surface, (wx, wy)), (0, 0))
        pygame.display.update()
        fps.tick(60)

if __name__ == '__main__':
    main()
