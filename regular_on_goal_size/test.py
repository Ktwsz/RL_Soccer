from Environments.Regular.env_reward_on_goal import Environment
import pygame

moves = {113: 4, 119: 2, 101: 6, 97: 0, 100: 1, 122: 5, 120: 3, 99: 7}

load_model = True

def main():
    env_size_x = 9
    env_size_y = 13
    env = Environment(env_size_x, env_size_y, True)

    done = False
    while not done:
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
    input()    
                

if __name__ == '__main__':
    main()