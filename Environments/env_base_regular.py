import pygame
from copy import copy
from math import sqrt, pi, asin

class EnvironmentBase(object):
    def __init__(self, width, height, showcase):
        self.showcase = showcase

        self.width = width
        self.height = height+2

        if self.showcase: 
            pygame.init()
            self.screen = pygame.display.set_mode(((self.width-1)*50+20, (self.height-1)*50))
            self.screen.fill((255,255,255))

        self.rev_action = [1, 0, 3, 2, 7, 6, 5, 4]

        self.pos = [self.width//2, self.height//2]

        self.gate0 = [(self.pos[0], 0), (self.pos[0]-1, 0), (self.pos[0]+1, 0)]
        self.gate1 = [(self.pos[0], self.height-1), (self.pos[0]-1, self.height-1), (self.pos[0]+1, self.height-1)]

        self.reset()

    def coord(self, x, y):
        return (22+x*45, 10+y*45)


    def draw_env(self):
        for i in range(1, self.width-1):
            for j in range(2, self.height-2):
                pygame.draw.circle(self.screen, (0,0,0), self.coord(i, j), 3)

        pygame.draw.circle(self.screen, (0,0,0), self.coord(self.gate0[0][0], self.gate0[0][1]+1), 3)
        pygame.draw.circle(self.screen, (0,0,0), self.coord(self.gate1[0][0], self.gate1[0][1]-1), 3)

        pygame.draw.line(self.screen, (0,0,0), self.coord(0, 1), self.coord(0, self.height-2), 3)

        pygame.draw.line(self.screen, (0,0,0), self.coord(0, 1), self.coord(self.gate0[1][0], 1), 3)
        pygame.draw.line(self.screen, (0,0,0), self.coord(self.gate0[2][0], 1), self.coord(self.width-1, 1), 3)

        pygame.draw.line(self.screen, (0,0,0), self.coord(self.width-1, 1), self.coord(self.width-1, self.height-2), 3)
        
        pygame.draw.line(self.screen, (0,0,0), self.coord(0, self.height-2), self.coord(self.gate1[1][0], self.height-2), 3)
        pygame.draw.line(self.screen, (0,0,0), self.coord(self.gate1[2][0], self.height-2), self.coord(self.width-1, self.height-2), 3)

        pygame.draw.line(self.screen, (0,0,0), self.coord(self.gate0[1][0], 0), self.coord(self.gate0[2][0], 0), 3)
        pygame.draw.line(self.screen, (0,0,0), self.coord(self.gate0[1][0], 0), self.coord(self.gate0[1][0], 1), 3)
        pygame.draw.line(self.screen, (0,0,0), self.coord(self.gate0[2][0], 0), self.coord(self.gate0[2][0], 1), 3)

        pygame.draw.line(self.screen, (0,0,0), self.coord(self.gate1[1][0], self.height-1), self.coord(self.gate1[2][0], self.height-1), 3)
        pygame.draw.line(self.screen, (0,0,0), self.coord(self.gate1[1][0], self.height-2), self.coord(self.gate1[1][0], self.height-1), 3)
        pygame.draw.line(self.screen, (0,0,0), self.coord(self.gate1[2][0], self.height-2), self.coord(self.gate1[2][0], self.height-1), 3)

        player_color = (255,0,0) if self.player == 0 else (0,0,255)
        pygame.draw.circle(self.screen, player_color, (22+self.pos[0]*45,10+self.pos[1]*45), 3)
        pygame.display.update()

    def draw_line(self, target):
        player_color = (255,0,0) if self.player == 0 else (0,0,255)
        pygame.draw.line(self.screen, (154, 148, 152), self.coord(self.pos[0], self.pos[1]), self.coord(target[0], target[1]), 3)
        pygame.draw.circle(self.screen, (0,0,0), self.coord(target[0], target[1]), 3)
        pygame.draw.circle(self.screen, player_color, self.coord(self.pos[0], self.pos[1]), 3)
        pygame.display.update()

    def match_action_id(self, id):
      tmp = copy(self.pos)
      match id:
        case 0:
          if tmp[0]-1 >= 0:
            tmp[0] -= 1
        case 1:
          if tmp[0]+1 < self.width:
            tmp[0] += 1
        case 2:
          if tmp[1]-1 >= 0:
            tmp[1] -= 1
        case 3:
          if tmp[1]+1 < self.height:
            tmp[1] += 1
        case 4:
          if tmp[0]-1 >= 0 and tmp[1]-1 >= 0:
            tmp[0] -= 1
            tmp[1] -= 1
        case 5:
          if tmp[0]-1 >= 0 and tmp[1]+1 < self.height:
            tmp[0] -= 1
            tmp[1] += 1
        case 6:
          if tmp[0]+1 < self.width and tmp[1]-1 >= 0:
            tmp[0] += 1
            tmp[1] -= 1
        case 7:
          if tmp[0]+1 < self.width and tmp[1]+1 < self.height:
            tmp[0] += 1
            tmp[1] += 1
      return tmp

    def action(self, action):
        self.old_pos = copy(self.pos)
        self.old_player = copy(self.player)

        if (self.visited[self.pos[0]][self.pos[1]] // (2**action)) % 2 == 1:

            self.visited[self.pos[0]][self.pos[1]] -= 2**action

            self.pos = self.match_action_id(action)            

            if self.old_pos[0] != self.pos[0] or self.old_pos[1] != self.pos[1]:
                self.visited[self.pos[0]][self.pos[1]] -= 2**self.rev_action[action]

            if not self.vertices_visited[self.pos[0]][self.pos[1]]:
                self.vertices_visited[self.pos[0]][self.pos[1]] = True
                self.player = 1-self.player
        
            if self.showcase:
                self.draw_line(self.old_pos)
            
    def reset(self):
        self.pos = [self.width//2, self.height//2]

        self.visited = [ [ 255 for i in range(self.height) ] for j in range(self.width) ]
        self.vertices_visited = [ [ False for i in range(self.height) ] for j in range(self.width) ]
        self.vertices_visited[self.pos[0]][self.pos[1]] = True

        for i in range(self.gate0[1][0]+1):
            self.vertices_visited[i][1] = True
            self.vertices_visited[i][-2] = True

            self.visited[i][1] = 168
            self.visited[i][-2] = 84

            self.vertices_visited[i][0] = 0
            self.vertices_visited[i][-1] = 0
        
        for i in range(self.gate0[2][0], self.width):
            self.vertices_visited[i][1] = True
            self.vertices_visited[i][-2] = True

            self.visited[i][1] = 168
            self.visited[i][-2] = 84
            
            self.vertices_visited[i][0] = 0
            self.vertices_visited[i][-1] = 0

        for i in range(self.height):
            self.vertices_visited[0][i] = True
            self.vertices_visited[-1][i] = True

            self.visited[0][i] = 194
            self.visited[-1][i] = 49

        self.visited[0][1] = 128
        self.visited[-1][1] = 32
        self.visited[0][-2] = 64
        self.visited[-1][-2] = 16

        self.visited[self.gate0[1][0]][self.gate0[1][1]+1] = 234
        self.visited[self.gate0[2][0]][self.gate0[2][1]+1] = 185
        self.visited[self.gate1[1][0]][self.gate1[1][1]-1] = 214
        self.visited[self.gate1[2][0]][self.gate1[2][1]-1] = 117


        self.player = 0
        
        if self.showcase:
            self.screen.fill((255,255,255))
            self.draw_env()


    def mouse_controls(self, mouse_x, mouse_y):
        curr_pos = self.coord(self.pos[0], self.pos[1])
        vec = (mouse_x-curr_pos[0], curr_pos[1]-mouse_y)
        s = vec[1]/sqrt(vec[0]*vec[0]+vec[1]*vec[1])
        if vec[0] >= 0 and vec[1] >= 0:
           fi = asin(s)
        if vec[0] < 0 and vec[1] >= 0:
           fi = pi-asin(s)
        if vec[0] < 0 and vec[1] < 0:
           fi = pi-asin(s)
        if vec[0] >= 0 and vec[1] < 0:
           fi = 2*pi+asin(s)
        
        angle = 20
        for i in range(1, 18, 2):
            val = i*pi/8-fi
            if val > 0:
                angle = i
                break

        angle %= 16
        angle //= 2

        map_to_actions = [1, 6, 2, 4, 0, 5, 3, 7]
        
        return self.action(map_to_actions[angle])