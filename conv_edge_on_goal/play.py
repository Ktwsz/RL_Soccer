from Environments.Conv.env_reward_on_goal import Environment
from Models.Conv.model_edge import Model

import pygame
import torch as torch

moves = {113: 4, 119: 2, 101: 6, 97: 0, 100: 1, 122: 5, 120: 3, 99: 7}

load_model = True

from time import sleep

def main():
    env_size_x = 7
    env_size_y = 13
    m = Model(env_size_x*env_size_y*2+9, 8, 0.9, 0, 0)
    m.net.load_state_dict(torch.load("model.pt", map_location=torch.device("cpu")))
    env = Environment(env_size_x, env_size_y, True)

    done = False
    while not done:
        if env.player == 1:
            done = m.policy(env)
            sleep(0.2)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in list(moves.keys()):
                        r, s, done = env.action(moves[event.key])
                    else:
                        r, s, done = env.action(int(event.key-48))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    r, s, done = env.mouse_controls(x, y)
                    #r, s, done = env.mouse_controls(x, y)
                    #print(env.get_actions())

    input()

if __name__ == '__main__':
    main()