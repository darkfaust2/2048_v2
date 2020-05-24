from Game import Game
from math import pow
from copy import deepcopy


class Node:
    def __init__(self, grid, agent_depth, max_depth, node_type, t, position=None):
        self.grid = grid
        self.max_depth = max_depth
        self.agent_depth = agent_depth
        self.node_type = node_type
        w_n = [[15, 14, 13, 12], [8, 9, 10, 11], [7, 6, 5, 4], [0, 1, 2, 3]]
        self.weight = [[int(pow(4, w_n[i][j])) for j in range(4)] for i in range(4)]
        if self.node_type == "Chance":
            self.position = position
        self.t = t.copy() # threshold
        self.scn = []

    def evaluation(self):
        if self.agent_depth >= self.max_depth or Game.is_end(self.grid):
            score = 0
            for i in range(4):
                for j in range(4):
                    score += self.grid[i][j] * self.weight[i][j]
            scn = []
            if Game.is_end(self.grid):
                for t in self.t:
                    if score >= t:
                        scn.append(0)
                    else:
                        scn.append(1000000)
            else:
                for t in self.t:
                    if score >= t:
                        scn.append(0)
                    else:
                        scn.append(1)
            return score, scn
        if self.node_type == "Max":
            max_score = -1
            act = None
            operator = {"w": Game.up, "a": Game.left, "s": Game.down, "d": Game.right}
            possible_action = []
            a = -1
            for op in ["w", "a", "s", "d"]:
                new_grid = operator[op](self.grid)[0]
                if new_grid != self.grid:
                    possible_action.append((new_grid, op))
            scn = [1000000 for i in range(len(self.t))]
            for g in possible_action:
                child_node = Node(g[0], self.agent_depth, self.max_depth, "Min", self.t)
                child_score, scn_c = child_node.evaluation()
                if child_score > max_score:
                    max_score = child_score
                    act = g[1]
                for i in range(len(scn)):
                    if scn_c[i] < scn[i]:
                        scn[i] = scn_c[i]
            if self.agent_depth == 0:
                return act, scn
            else:
                return max_score, scn
        elif self.node_type == "Min":
            min_score = int(pow(2, 50))
            possible_position = []
            for x in range(4):
                for y in range(4):
                    if self.grid[x][y] == 0:
                        possible_position.append((self.weight[x][y], (x, y)))
            possible_position = sorted(possible_position, reverse=True)
            tiles = min(self.max_depth-self.agent_depth, len(possible_position))
            scn = [0 for i in range(len(self.t))]
            for i in range(tiles):
                new_grid = deepcopy(self.grid)
                new_position = possible_position[i][1]
                child_node = Node(new_grid, self.agent_depth, self.max_depth, "Chance", self.t, new_position)
                child_score, scn_c = child_node.evaluation()
                if child_score < min_score:
                    min_score = child_score
                for k in range(len(scn)):
                    scn[k] += scn_c[k]
            return min_score, scn
        else:
            # probability of the new number 2 and 4
            p = [0.8, 0.2]
            average_score = 0
            scn = [0 for i in range(len(self.t))]
            for i in range(2):
                new_grid = deepcopy(self.grid)
                new_grid[self.position[0]][self.position[1]] = int(pow(2, i+1))
                child_node = Node(new_grid, self.agent_depth+1, self.max_depth, "Max", self.t)
                child_score, scn_c = child_node.evaluation()
                average_score += int(p[i]*child_score)
                for k in range(len(scn)):
                    scn[k] += scn_c[k]
            return average_score, scn


if __name__ == '__main__':
    pass
