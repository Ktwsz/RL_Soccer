from Environments.env_base_conv import EnvironmentBase
import numpy as np
from torchvision import transforms

class Environment(EnvironmentBase):
    def action(self, action):
        super().action(action)

        done = 0 if len(self.get_actions()) != 0 else 1
        reward = 0

        for x, y in self.gate0:
            if x == self.pos[0] and y == self.pos[1]:
                reward = -10
                done = 1
                break
        for x, y in self.gate1:
            if x == self.pos[0] and y == self.pos[1]:
                reward = 10
                done = 1
                break

        return reward, self.get_state(), done
    
    def get_actions(self):
        correct_actions = []

        for i in range(8):
            new_pos = self.match_action_id(i)
            if (self.visited[self.pos[0]][self.pos[1]]//(2**i))%2 != 0 and self.visited[new_pos[0]][new_pos[1]] - 2**self.rev_action[i] != 0 and new_pos != self.pos:
                correct_actions.append(i)

        return correct_actions
    
    def get_state(self):

        trans = transforms.Compose([transforms.ToPILImage(), transforms.ToTensor()])

        state = np.ndarray(shape=((self.height-1)*3+1, (self.width-1)*3+1, 1), dtype=np.uint8)
        for i in range(3*(self.height-1)+1):
            for j in range(3*(self.width-1)+1):
                state[i][j] = np.array(self.state[j][i], dtype=np.uint8)
        
        return trans(state)


