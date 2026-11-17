# The Great Robot Race

A text-based race where robots move through a maze toward a goal. My job was to fill in the race logic using Python's specialized containers.

**What I did**
- Used a `deque` to store every robot move in order, then replayed the moves one by one with `popleft()`.
- Used `Counter` to count moves and collisions for each robot.
- Used a `namedtuple` (`BotScoreData`) to keep each robot's name, moves, collisions and score.
- Used a dictionary to find each robot object by its name while replaying the race.

**Files**
- `robot_race.py`: my code (the main script).
- `robot_race_functions.py`: helper functions provided by Codecademy (reading the maze, moving robots, printing).
- `maze_data_1.csv`, `maze_data_2.csv`, `maze_data_3.csv`: the mazes. Change `maze_file_name` in `robot_race.py` to try another one.

**Run it:** `python robot_race.py` (no extra libraries needed).

**Skills:** `collections` (deque, Counter, namedtuple), dictionaries, loops.
