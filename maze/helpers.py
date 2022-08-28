import numpy as np
from rest_framework.exceptions import ValidationError

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def convert_alpha_to_index(wall):
    j = alphabet.find(wall[0])
    i = int(wall[1]) - 1
    return i, j


def create_matrix(m, n):
    zeors_array = np.zeros((m, n), dtype=int)
    print(zeors_array)
    return zeors_array


def walls_to_matrix(walls, walls_matrix):
    for wall in walls:
        i, j = convert_alpha_to_index(wall)
        walls_matrix[i][j] = 1
    # print(m)
    print("Walls")
    print(walls_matrix)


def get_path(m, end: tuple):
    i, j = end
    k = m[i][j]
    the_path = [(i, j)]
    while k > 1:
        if i > 0 and m[i - 1][j] == k - 1:
            i, j = i - 1, j
            the_path.append((i, j))
            k -= 1
        elif j > 0 and m[i][j - 1] == k - 1:
            i, j = i, j - 1
            the_path.append((i, j))
            k -= 1
        elif i < len(m) - 1 and m[i + 1][j] == k - 1:
            i, j = i + 1, j
            the_path.append((i, j))
            k -= 1
        elif j < len(m[i]) - 1 and m[i][j + 1] == k - 1:
            i, j = i, j + 1
            the_path.append((i, j))
            k -= 1

    # translate_path
    arr = []
    for item in the_path:
        i = item[1]
        j = item[0]
        index = alphabet[int(i)]
        index += str(j + 1)
        arr.append(index)
    arr.reverse()
    return arr


class MinPath:
    find_existed_point = ()

    def make_step(self, k, m, a):
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == k:
                    if i > 0 and m[i - 1][j] == 0 and a[i - 1][j] == 0:
                        m[i - 1][j] = k + 1
                    if j > 0 and m[i][j - 1] == 0 and a[i][j - 1] == 0:
                        m[i][j - 1] = k + 1
                    if i < len(m) - 1 and m[i + 1][j] == 0 and a[i + 1][j] == 0:
                        m[i + 1][j] = k + 1
                        self.is_edge_touched(i, j, m)
                    if j < len(m[i]) - 1 and m[i][j + 1] == 0 and a[i][j + 1] == 0:
                        m[i][j + 1] = k + 1

    def is_edge_touched(self, i, j, m):
        if i + 1 == len(m) - 1:
            if len(self.find_existed_point)==0:
                self.find_existed_point = (i + 1, j)
            else:
                raise ValidationError("There are more than one exit point")

    def __init__(self, m, n, walls_matrix, entrance):
        self.x = m
        self.y = n
        self.walls_matrix = walls_matrix
        self.entrance = entrance

    def solve(self):
        x = self.x
        y = self.y
        output_matrix = create_matrix(x, y)  # m
        walls_matrix = self.walls_matrix  # walls

        # walls = ["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6", "E6",
        #          "G6", "H6", "B7", "D7", "G7", "B8"]
        # walls = ["A1", "B2", "C3", "D4", "E5", "F6", "G7"]
        # walls = ["A2","A3","A4","A5","A6","A7","A8","B8", "C8", "D8", "E8", "F8", "G8"]
        # walls = ["A2","A3","A4","A5","A6","A7","A8","B8", "C8", "D8", "E8", "F8", "G8", "H8"]
        # walls = ["B8", "C8", "D8", "E8", "F8", "G8", "H8", "C2", "C3", "C4", "C5", "C6", "C7"]
        # todo change to entrance
        # output_matrix[0][0] = 1
        output_matrix[convert_alpha_to_index(self.entrance)] = 1

        longest_point_arr = []  # Append path to this array
        path = []
        for i in range(1, x * y):
            if len(self.find_existed_point) != 0:
                # print(i)
                path = get_path(output_matrix, self.find_existed_point)
                # longest_point_arr.append(output_matrix[self.find_existed_point])
                # output_matrix[self.find_existed_point] = 0
                # break
            self.make_step(i, output_matrix, walls_matrix)
            print(f"Step {i}")
            print(output_matrix)
        if not self.find_existed_point:
            raise ValidationError("There is not existed point")

        return path, self.find_existed_point


max_path = []


class MaxPath:

    def __init__(self, m, n, entrance: tuple, walls_matrix, destination: tuple):
        self.m = m
        self.n = n
        self.entrance = entrance
        self.walls_matrix = walls_matrix
        self.destination = destination

    @staticmethod
    def is_safe(matrix, visited, x, y):
        return 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and \
               not (matrix[x][y] == 0 or visited[x][y])

    # Find the longest possible route in a matrixrix `matrix` from the source cell (i, j)
    # to destination cell `destination`.
    # `max_dist` —> keep track of the length of the longest path from source to destination
    # `dist` —> length of the path from the source cell to the current cell (i, j)
    def longest_path(self, matrix, visited, max_path_matrix, i, j, destination, max_dist=0, dist=0):
        # if the destination is not possible from the current cell
        if matrix[i][j] == 0:
            return 0

        # if the destination is found, update `max_dist`
        if (i, j) == destination:
            # Calculate max between old value and new value
            global max_path
            max_path_matrix[i][j] = dist + 1
            path_tmp = get_path(max_path_matrix, (i, j))
            if len(max_path) < len(path_tmp):
                max_path = path_tmp
            return max(dist, max_dist)

        # set cell as visited
        visited[i][j] = 1
        if dist + 1 > 1:
            max_path_matrix[i][j] = dist + 1

        # recursive scenario started
        # go to the bottom cell
        if MaxPath.is_safe(matrix, visited, i + 1, j):
            max_dist = self.longest_path(matrix, visited, max_path_matrix, i + 1, j, destination, max_dist, dist + 1)

        # go to the right cell
        if MaxPath.is_safe(matrix, visited, i, j + 1):
            max_dist = self.longest_path(matrix, visited, max_path_matrix, i, j + 1, destination, max_dist, dist + 1)

        # go to the top cell
        if MaxPath.is_safe(matrix, visited, i - 1, j):
            max_dist = self.longest_path(matrix, visited, max_path_matrix, i - 1, j, destination, max_dist, dist + 1)

        # go to the left cell
        if MaxPath.is_safe(matrix, visited, i, j - 1):
            max_dist = self.longest_path(matrix, visited, max_path_matrix, i, j - 1, destination, max_dist, dist + 1)

        # backtrack: remove (i, j) from the visited matrix
        visited[i][j] = 0

        return max_dist

    # Wrapper over findLongestPath() function

    def find_longest_path_length(self, m, n, matrix, src, destination):
        # get source cell (i, j)
        i, j = convert_alpha_to_index(src)

        # get destination cell (x, y)
        x, y = destination

        # base case
        # if len(matrix) == 0 or matrix[i][j] == 0 or matrix[x][y] == 0:
        #     return 0

        # `M × N` matrixrix
        (M, N) = (len(matrix), len(matrix[0]))

        # construct an `M × N` matrixrix to keep track of visited cells
        # todo use mu func
        visited = [[0 for x in range(N)] for y in range(M)]
        max_path_matrix = [[0 for x in range(N)] for y in range(M)]
        max_path_matrix[i][j] = 1
        # visited = create_matrix(m,n)

        # (i, j) are the source cell coordinates, and (x, y) are the
        # destination cell coordinates
        max = self.longest_path(matrix, visited, max_path_matrix, i, j, destination)
        return max_path, max

    def solve(self):

        return self.find_longest_path_length(self.m, self.n, self.walls_matrix, self.entrance, self.destination)
