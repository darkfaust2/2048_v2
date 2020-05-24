from Expectimax2_v2 import Node as Node
from Game import Game
import csv


def max_v(grid):
    return max(max(grid[0]), max(grid[1]), max(grid[2]), max(grid[3]))


game_count = int(input("Please set the count of game(s): "))
max_depth = int(input("Please set the max_depth: "))
filename = input("Please input the filename of data set: ") + ".csv"
b = int(input("Please input b (how many threshold we will try in one game?): "))
# 8, 16, 32...
score_index = {}
for i in range(3, 20):
    score_index[int(pow(2, i))] = int(pow(2, i)) * (i-2)

with open(filename, "a+", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    avg_score = 0
    avg_steps = 0
    writer.writerow(["steps", "score", "max_num"])
    a = [i + 1 for i in range(b)]
    for k in range(game_count):
        T = [score_index[8] * 8 * int(pow(4, 15)) for i in range(b)]
        score_list = []
        scn_list1 = []
        scn_list2 = []
        step = 0
        next_n = [8 for i in range(b)]
        next_num = 8
        game = Game()
        game.random_field()
        game.random_field()
        scn = None
        while not game.is_end(game.grid):
            if not scn:
                pass
            else:
                max_value = max_v(game.grid)
                # change the threshold
                for i in range(b):
                    if max_value >= next_n[i]:
                        next_n[i] *= int(pow(2, a[i]))
                        T[i] = (score_index[next_n[i]]) * next_n[i] * int(pow(4, 15))
                # change the next num
                if max_value >= next_num:
                    next_num *= 2
                    score_list.append(game.score)
                    scn_list1.append(scn)
            node = Node(game.grid, game.score, 0, max_depth, "Max", T)
            action, scn = node.evaluation()
            scn_list2.append(scn)
            print("scn:{s}".format(s=scn))
            game.print_screen()
            game.update_grid(action)
            step += 1
            game.random_field()
        terminal_node = Node(game.grid, game.score, 0, max_depth, "Max", T)
        scn = terminal_node.evaluation()[1]
        scn_list2.append(scn)
        print("scn:{s}".format(s=scn))
        game.print_screen()
        avg_score += game.score
        avg_steps += step
        writer.writerow([step, game.score, max_value])
        print([int(pow(2, i)) for i in range(3, len(score_list)+3)])
        writer.writerow([int(pow(2, i)) for i in range(3, len(score_list)+3)])
        writer.writerow(score_list)
        for k in range(b):
            writer.writerow([scn_list1[i][k] for i in range(len(scn_list1))])
        for k in range(b):
            writer.writerow([scn_list2[i][k] for i in range(len(scn_list2))])
    avg_score /= game_count
    avg_steps /= game_count
    writer.writerow(["max_depth", "game_count", "Avg(score)", "Avg(steps)"])
    writer.writerow([max_depth, game_count, int(avg_score), int(round(avg_steps))])
    writer.writerow([])