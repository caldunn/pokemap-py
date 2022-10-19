from enum import Enum
import sys

def main():
    arena = Arena.default()
    arena = Arena.from_points((10,10), [
        [(4,4), (0,4)], 
        [(1,3), (3,3)], 
        [(0,0), (0,3)],
        [(6,3), (6,6)], 
        [(7,3), (7,6)] 
        ])
    print("\x1b[1A \x1b7 \x1b[?47h")
    while True:
        print("\x1b[H \x1b[0J")
        arena.draw_map()
        action = Action.from_character(input('Next move: '))
        arena.apply_action(action)
        print("-----------------------")

class Action(Enum):
    W_LEFT = 1
    W_RIGHT = 2
    W_DOWN = 3
    W_UP = 4
    INTERACT = 5

    @classmethod
    def from_character(cls, char: str):
        match char.lower():
            case 'w': 
                return Action.W_UP
            case 's':
                return Action.W_DOWN
            case 'a':
                return Action.W_LEFT
            case 'd':
                return Action.W_RIGHT
            case _:
                return Action.INTERACT


class Point:
    def __init__(self, x: int,y: int):
        self.x = x;
        self.y = y;

class Arena:
    def __init__(self, size: tuple[int, int], objects: list[list[int]],
                 player_pos: tuple[int, int] = (0,0)):
        self.size = size
        self.objects = objects
        self.player_pos = player_pos


    @classmethod
    def from_points(cls, size: tuple[int, int], vertices: list[list[tuple[int, int]]]):  
        def subtract_two_tuples(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
            return (-x[0] + y[0], -x[1] + y[1])

        # Create the map matrix
        map_matrix = [[0 for x in range(size[0])] for y in range(size[1])] 
        for wall in vertices:
            for i in range(0, len(wall) - 1):
                vector = subtract_two_tuples(wall[i], wall[i+1])
                if vector[0] == 0:
                    x = wall[i][0]
                    y1, y2 = (wall[i][1], wall[i+1][1])
                    upper, lower = (max(y1, y2), min(y1, y2))
                    for j in range(lower, upper + 1):
                        map_matrix[j][x] = 1
                elif vector[1] == 0:
                    y = wall[i][1]
                    x1, x2 = (wall[i][0], wall[i+1][0])
                    upper, lower = (max(x1, x2), min(x1, x2))
                    for j in range(lower, upper + 1):
                        map_matrix[y][j] = 1

        return cls(size, map_matrix)

    @classmethod
    def default(cls):
        return cls((7, 7), [
            [0,0,1,0,1,0,0], 
            [0,0,1,0,1,0,0], 
            [1,1,1,0,1,1,1], 
            [0,0,0,0,0,0,0], 
            [1,1,1,0,1,1,1], 
            [0,0,1,0,1,0,0], 
            [0,0,1,0,1,0,0], 
            ], (6, 3))

    def draw_map(self):
        print('%  ' * (self.size[0]+1))
        for i, row in enumerate(self.objects):
            print('%', end="")
            for j, element in enumerate(row):
                if (i, j) == self.player_pos:
                    print("\x1b[32m * \x1b[0m", end="")
                    continue

                if element == 1:
                    print("\x1b[31m # \x1b[0m", end="")
                else: 
                    print("   ", end="")
            print('%', end="")
            print()
        print(' % ' * (self.size[0]+1))

    def apply_action(self, action: Action):
        vector = (0, 0)
        match action:
            case Action.W_UP:
                vector = (-1, 0)
            case Action.W_DOWN:
                vector = (1, 0)
            case Action.W_RIGHT:
                vector = (0, 1)
            case Action.W_LEFT:
                vector = (0, -1)

        # move if valid
        player_pos = tuple(map(sum, zip(self.player_pos, vector)))
        # index range
        if 0 <= player_pos[0] < self.size[0] and 0 <= player_pos[1] < self.size[1]: 
            if self.objects[player_pos[0]][player_pos[1]] == 0:
                            self.player_pos = player_pos

if __name__ == '__main__':
    try: 
        main()
    except KeyboardInterrupt as ki:
        print("\x1b8 \x1b[?47l")
        sys.exit(1)

