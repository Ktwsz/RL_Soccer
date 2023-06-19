from Environments.Conv.env_reward_on_goal import Environment


moves = {113: 4, 119: 2, 101: 6, 97: 0, 100: 1, 122: 5, 120: 3, 99: 7}

load_model = True

def main():
    env_size_x = 7
    env_size_y = 13
    env = Environment(env_size_x, env_size_y, True)

    for i in range(7):
        for j in range(15):
            env.pos = (i, j)
            print(env.get_actions())
            input()
                

if __name__ == '__main__':
    main()