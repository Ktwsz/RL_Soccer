from Environments.Regular.env_reward_on_goal import Environment
from Models.Regular.model_lambda import Model

import torch.optim as optim
import torch 

load_model = False

def main():
    env_size_x = 9
    env_size_y = 13
    m = Model(9*(env_size_y+2)*env_size_x, 8, 0.9, 1, -1/100000, 0.9, 0.01)
    if load_model: m.net.load_state_dict(torch.load("model.pt", map_location=torch.device("cpu")))
    env = Environment(env_size_x, env_size_y, False)

    optimizer = optim.Adam(m.parameters(), lr=0.01)

    loss_avg = 0

    for epoch in range(100000):
        done = False

        while not done:
            done = m.policy(env)
        
        loss = m.train(optimizer)
        loss_avg += loss
        env.reset()

        if epoch % 1000 == 0:
            print(f"Epoch {epoch}, average loss is {loss_avg/1000}")
            loss_avg = 0
    
            torch.save(m.net.state_dict(), "model.pt")
    

if __name__ == '__main__':
    main()