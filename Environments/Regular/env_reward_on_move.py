from Environments.env_base_regular import EnvironmentBase
import numpy as np
import torch

class Environment(EnvironmentBase):
    def action(self, action):
        super().action(action)

        done = 0 if (len(self.get_actions()) != 0 or self.old_pos == self.pos) else 1
        reward = 0

        for x, y in self.gate0:
            if x == self.pos[0] and y == self.pos[1]:
                reward = -100
                done = 1
                break
        for x, y in self.gate1:
            if x == self.pos[0] and y == self.pos[1]:
                reward = 100
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
        state = []

        for i in range(self.width):
            for j in range(self.height):
                for k in range(8):
                    state.append((self.visited[i][j]//(2**k))%2)

        for i in range(self.width):
            for j in range(self.height):
                state.append(0 if self.pos[0] != i or self.pos[1] != j else 1)

        return torch.from_numpy(np.array(state, dtype="float32"))


