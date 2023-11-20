class Matrix:
    def __init__(self, matrix: list[list] = None):
        self.matrix = matrix

    def rows(self):
        return len(self.matrix)

    def columns(self):
        return len(self.matrix[0])

    def __str__(self):
        output = ""
        for i in range(self.rows()):
            output += f"{self.matrix[i]}\n"
        return output


class Vector(Matrix):
    def __init__(self, matrix: list[list] = None):
        super().__init__(matrix)
