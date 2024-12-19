import time
import warnings

# Define the size of the board, target score and the set of numbers
BOARD_SIZE = 6
TARGET_SCORE = 2024
START_SUM = 50

# Possible moves for a knight on the board
knight_moves = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]


# Function to check if the position is within board bounds
def is_within_bounds(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

t_start = time.time()
number_set = [0, 0, 0]
step_duration = []
step_time = [t_start]
for total_sum in range(START_SUM, 5, -1):
    print(total_sum)
    def find_solution():
        for C in [11, 8, 4, 2]:
            for B in range(total_sum - C - 1, 1, -1):
                number_set[2] = C
                number_set[1] = B
                number_set[0] = total_sum - C - B
                if len(set(number_set)) < 3:
                    continue

                # Initialize the board based on the line rules
                board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                for x in range(BOARD_SIZE):
                    for y in range(BOARD_SIZE):
                        if y < 5.5 - 2 * x:
                            board[y][x] = number_set[0]  # First value (left of the line y = 5.5 - 2x)
                        elif y > 9.5 - 2 * x:
                            board[y][x] = number_set[2]  # Third value (right of the line y = 9.5 - 2x)
                        else:
                            board[y][x] = number_set[1]  # Second value (between the lines)


                # Function to find all paths from (x, y) to target with a specific score
                def find_paths(x, y, target_x, target_y, path, score, all_paths):
                    # Stop if the score has already reached the target score before reaching the end
                    if score == TARGET_SCORE and (x, y) == (target_x, target_y):
                        all_paths.append((path[:], score))
                        return
                    elif score >= TARGET_SCORE:
                        return  # Stop further exploration if the score exceeds or reaches the target score

                    # Get the current cell's value
                    current_value = board[x][y]

                    # Try each possible move for the knight
                    for move_x, move_y in knight_moves:
                        new_x, new_y = x + move_x, y + move_y

                        # Check if new position is within bounds and not visited in the current path
                        if is_within_bounds(new_x, new_y) and (new_x, new_y) not in [(px, py) for (px, py, _) in path]:
                            # Get the value of the new cell
                            new_value = board[new_x][new_y]

                            # Calculate the new score based on the new cell's value
                            if new_value == current_value:
                                new_score = score + new_value
                            else:
                                new_score = score * new_value

                            # Add the position, value, and new score to the path and continue the search
                            path.append((new_x, new_y, new_value))
                            find_paths(new_x, new_y, target_x, target_y, path, new_score, all_paths)
                            # Backtrack
                            path.pop()


                # Main function to start the path-finding from the top-left corner to the bottom-right
                def knight_paths(method='regular'):
                    all_paths = []
                    if method == 'regular':
                        start_x, start_y = 0, 0
                        target_x, target_y = BOARD_SIZE - 1, BOARD_SIZE - 1
                    elif method == 'cross':
                        start_x, start_y = BOARD_SIZE - 1, 0
                        target_x, target_y = 0, BOARD_SIZE - 1
                    else:
                        start_x, start_y = 0, 0
                        target_x, target_y = BOARD_SIZE - 1, BOARD_SIZE - 1
                        warnings.warn('Regular start')

                    # Start the path with the initial position, its value, and the initial score
                    initial_value = board[start_x][start_y]
                    find_paths(start_x, start_y, target_x, target_y, [(start_x, start_y, initial_value)], initial_value,
                               all_paths)
                    return all_paths


                # Generate all paths that exactly reach the target score
                all_knight_paths_regular = knight_paths('regular')
                if len(all_knight_paths_regular) > 0:
                    all_knight_paths_cross = knight_paths('cross')
                    if len(all_knight_paths_cross) > 0:
                        # Print paths that exactly reach the target score and end in the opposite corner
                        matching_paths_regular = [path for path, score in all_knight_paths_regular if score == TARGET_SCORE]
                        matching_paths_cross = [path for path, score in all_knight_paths_cross if score == TARGET_SCORE]
                        print("Example path (with cell numbers and exact target score):", matching_paths_regular[0])
                        print("Example path (with cell numbers and exact target score):", matching_paths_cross[0])
                        step_time.append(round(time.time(), 2))
                        step_duration.append(step_time[-1]-step_time[-2])
                        return

    find_solution()