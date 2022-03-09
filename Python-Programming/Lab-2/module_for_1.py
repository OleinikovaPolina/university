import copy


class Matrix:
    def __init__(self, matrix):
        self.n = len(matrix)
        self.m = len(matrix[0])
        self.matrix = matrix

    @staticmethod
    def get_minor(matrix, i, j):
        minor = copy.deepcopy(matrix)
        del minor[i]
        for i in range(len(matrix[0]) - 1):
            del minor[i][j]
        return minor

    def det(self, matrix=None):
        if not matrix:
            matrix = self.matrix
        if len(matrix) != len(matrix[0]):
            return None
        if len(matrix[0]) == 1:
            return matrix[0][0]
        signum = 1
        determinant = 0
        for j in range(len(matrix[0])):
            determinant += matrix[0][j] * signum * self.det(self.get_minor(matrix, 0, j))
            signum *= -1
        return determinant

    def squaring(self):
        if self.n != self.m:
            return None
        new_matrix = []
        for i in range(self.n):
            new_matrix.append([])
        for i in range(self.n):
            for j in range(self.n):
                new_matrix[i].append(0)
                for k in range(self.n):
                    new_matrix[i][j] += self.matrix[i][k] * self.matrix[k][j]
        return new_matrix

    def transposition(self):
        new_matrix = [[self.matrix[j][i] for j in range(self.n)] for i in range(self.m)]
        return new_matrix

    def max(self):
        return max(map(max, self.matrix))

    def __str__(self):
        return '\n'.join(
            [' '.join(
                map(lambda x: '{}{}'.format((len(str(self.max())) - len(str(x))) * ' ', x), i))
                for i in self.matrix
            ])
