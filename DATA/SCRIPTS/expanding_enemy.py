import pygame
from math import*

screen = None
def init(scrn):
    global screen
    screen = scrn

class ExpandingEnemy():
    def __init__(self, startx, starty):
        self.bullet_vectors = [pygame.Vector2(0, 1), pygame.Vector2(0, -1),
                               pygame.Vector2(1, 0), pygame.Vector2(-1, 0),
                               pygame.Vector2(1, 1), pygame.Vector2(-1, -1),
                               pygame.Vector2(1, -1), pygame.Vector2(-1, 1)]
        for i in range(len(self.bullet_vectors)):
            self.bullet_vectors[i] = self.bullet_vectors[i].normalize()
        
        self.bullet_speed = 4
        self.follow_speed = 1
        self.time_delta  = 0
        
        self.parent_rect = pygame.FRect(0, 0, 50, 50)
        self.parent_rect.center = (startx, starty)
        self.bullet_rects = []
    
    def update(self, boundry_rect):
        for i in self.bullet_rects:
            if not i[0].colliderect(boundry_rect):
                try:
                    self.bullet_rects.remove(i)
                except:
                    pass
    
    def draw(self, parent_color, bullet_color):
        for i in self.bullet_rects:
            pygame.draw.circle(screen, bullet_color, i[0].center, i[0].w/2)
        pygame.draw.circle(screen, parent_color, self.parent_rect.center, self.parent_rect.w/2)
    
    def bullet_attack(self):
        for i in range(8):
            rect = pygame.FRect(self.parent_rect.center, (20, 20))
            rect.center = self.parent_rect.center
            self.bullet_rects.append([rect, self.bullet_vectors[i], i*360/8, 0])
    
    def bullet_attack_cardinal(self):
        for i in range(4):
            rect = pygame.FRect(self.parent_rect.center, (20, 20))
            rect.center = self.parent_rect.center
            self.bullet_rects.append([rect, self.bullet_vectors[i], i*360/8, 0])
    
    def bullet_attack_ordinal(self):
        for i in range(4, 8):
            rect = pygame.FRect(self.parent_rect.center, (20, 20))
            rect.center = self.parent_rect.center
            self.bullet_rects.append([rect, self.bullet_vectors[i], i*360/8, 0])
    
    def bullet_move(self):
        for i in self.bullet_rects:
            i[0].center += i[1]*self.bullet_speed
    
    def bullet_collide(self, rect):
        return rect.collidelist([i[0] for i in self.bullet_rects]) != -1
    
    def follow_rect(self, rect):
        vect = pygame.math.Vector2([rect.centerx-self.parent_rect.centerx, rect.centery-self.parent_rect.centery])
        vect = vect.normalize() * self.follow_speed
        self.parent_rect.center += vect
    
    def sine_wave(self, mult, sec, offsetx, offsety):
        for i in self.bullet_rects:
            i[0].centerx = offsetx + i[1].x*self.bullet_speed*mult*sin((pygame.time.get_ticks()-self.time_delta)/sec)
            i[0].centery = offsety + i[1].y*self.bullet_speed*mult*sin((pygame.time.get_ticks()-self.time_delta)/sec)
    
    def circle_motion(self, angle_amnt):
        for i in self.bullet_rects:
            i[0].centerx = cos(radians(i[2]))*i[3]+self.parent_rect.centerx
            i[0].centery = sin(radians(i[2]))*i[3]+self.parent_rect.centery
            i[2] += angle_amnt
            i[3] += self.bullet_speed
    
    def sine_circle(self, angle_amnt, div):
        for i in self.bullet_rects:
            i[0].centerx = cos(radians(i[2]))*sin((pygame.time.get_ticks()-self.time_delta)/div)*self.bullet_speed+self.parent_rect.centerx
            i[0].centery = sin(radians(i[2]))*sin((pygame.time.get_ticks()-self.time_delta)/div)*self.bullet_speed+self.parent_rect.centery
            i[2] += angle_amnt
    
    def bullet_bounce(self, left, right, top, bottom):
        for i in self.bullet_rects:
            if i[0].left <= left or i[0].right >= right:
                i[1].x *= -1
            if i[0].top <= top or i[0].bottom >= bottom:
                i[1].y *= -1
    
    def homing_turn(self, rect):
        for i in self.bullet_rects:
            point1 = i[0].center
            point2 = [i[0].centerx+i[1].x, i[0].centery+i[1].y]
            crs_pdct = int((rect.centerx-point1[0])*(point2[1]-point1[1])-(rect.centery-point1[1])*(point2[0]-point1[0]))
            vector = pygame.math.Vector2(rect.centerx-i[0].centerx, rect.centery-i[0].centery)
            if vector.length() <= 150:
                turning = (vector.length()**2)/100+1
                if turning == 0:
                    turning = 0.001
                angle = degrees(acos(round(vector.dot(i[1])/(vector.length()*i[1].length()), 3))) / turning
                if crs_pdct > 0:
                    i[1] = i[1].rotate(-angle)
                elif crs_pdct <= 0:
                    i[1] = i[1].rotate(angle)