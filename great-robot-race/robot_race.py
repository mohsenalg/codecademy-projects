import robot_race_functions as rr
from collections import deque, Counter, namedtuple
from time import time, sleep

maze_file_name = 'maze_data_1.csv'
seconds_between_turns = 0.3
max_turns = 35

# Initialize the robot race
maze_data = rr.read_maze(maze_file_name)
rr.print_maze(maze_data)
walls, goal, bots = rr.process_maze_init(maze_data)

# Populate a deque of all robot commands for the provided maze
robot_moves = deque()
num_of_turns = 0
while not rr.is_race_over(bots) and num_of_turns < max_turns:
    # Task 5: get a move for every robot that has not finished
    for bot in bots:
        if bot.has_finished == False:
            move = rr.compute_robot_logic(walls, goal, bot)
            robot_moves.append(move)
    num_of_turns += 1

# Task 6: count the number of moves based on the robot names
moves_count = Counter(move[0] for move in robot_moves)

# Task 7: count the number of collisions by robot name
collisions_count = Counter(move[0] for move in robot_moves if move[2] == True)

# Task 8: namedtuple to keep track of each robot's points
BotScoreData = namedtuple('BotScoreData', ['name', 'num_moves', 'num_collisions', 'score'])

# Task 9: calculate the score (moves + collisions) for each robot
bot_scores = []
for bot in bots:
    num_moves = moves_count[bot.name]
    num_collisions = collisions_count[bot.name]
    score = num_moves + num_collisions
    bot_scores.append(BotScoreData(bot.name, num_moves, num_collisions, score))

# Task 10: dict to find each robot object by its name
bot_data = {}
for bot in bots:
    bot_data[bot.name] = bot

# Task 11: replay the moves to show the race live
while len(robot_moves) > 0:
    move = robot_moves.popleft()
    bot_data[move[0]].process_move(move[1])

    rr.update_maze_characters(maze_data, bots)
    rr.print_maze(maze_data)
    sleep(seconds_between_turns - time() % seconds_between_turns)

# Task 12: print the results at the end
rr.print_results(bot_scores)