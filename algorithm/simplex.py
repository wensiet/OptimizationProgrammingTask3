from algorithm.utility import Matrix, Vector


class Simplex:
    def __init__(self, c: list = None, a: list[list] = None, b: list = None, t: str = None, e: float = 0.00001):
        self.t = t
        if self.t == "max":
            for i in range(len(c)):
                c[i] = c[i] * -1
        self.c = Vector(c)
        self.a = Matrix(a)
        self.b = Vector(b)
        self.e = e
        self.iteration_count = 0
        self.basis = []

    def _approximation(self):
        i = 0
        while self.e < 1:
            self.e *= 10
            i += 1
        return i

    def _validate_input(self):
        for i in range(0, self.b.rows()):
            if self.b.matrix[i] < 0:
                print("Wrong inputs")
                return False
        return True

    def solve(self):
        if not self._validate_input():
            return "Wrong inputs"
        optimal = 0
        rounding = self._approximation()
        for i in range(self.a.columns(), self.a.columns() + self.a.rows()):
            self.basis.append(i)
        self._add_slack_variables()
        z_initial = []
        for element in self.c.matrix:
            z_initial.append(element)
        while not self._check_optimal():
            self._change_rows(self._pivot())
        for i in range(len(self.basis)):
            optimal += z_initial[self.basis[i]] * self.b.matrix[i]
        swapped = False
        for i in range(len(self.basis)):
            for j in range(0, len(self.basis) - i - 1):
                if self.basis[j] > self.basis[j + 1]:
                    swapped = True
                    self.basis[j], self.basis[j + 1] = self.basis[j + 1], self.basis[j]
                    self.b.matrix[j], self.b.matrix[j + 1] = self.b.matrix[j + 1], self.b.matrix[j]
            if not swapped:
                break
        basis_index = 0
        slacks_counter = 0
        result = ""
        for i in range(self.a.columns()):
            if i < self.a.rows():
                if basis_index < len(self.basis) and i == self.basis[basis_index]:
                    print(f"x{i + 1}={round(self.b.matrix[basis_index], rounding)}", end=" ")
                    result += f"x{i + 1}={round(self.b.matrix[basis_index], rounding)} "
                    basis_index += 1
                else:
                    print(f"x{i + 1}=0", end=" ")
                    result += f"x{i + 1}=0 "
            else:
                if basis_index < len(self.basis) and i == self.basis[basis_index]:
                    print(f"s{slacks_counter + 1}={round(self.b.matrix[basis_index], rounding)}", end=" ")
                    result += f"s{slacks_counter + 1}={round(self.b.matrix[basis_index], rounding)} "
                    basis_index += 1
                else:
                    print(f"s{slacks_counter + 1}=0", end=" ")
                    result += f"s{slacks_counter + 1}=0 "
                slacks_counter += 1
        optimal = optimal * -1
        print(f"with optimal {round(optimal, rounding)}")
        result += f"with optimal {round(optimal, rounding)}"
        return result

    def _add_slack_variables(self):
        new_a = Matrix()
        new_a.matrix = self.a.matrix
        identity = []
        for i in range(self.a.rows()):
            current_row = []
            for j in range(self.a.rows()):
                if i == j:
                    current_row.append(1)
                else:
                    current_row.append(0)
            identity.append(current_row)
        for i in range(self.a.rows()):
            new_a.matrix[i].extend(identity[i])
            self.c.matrix.append(0)
        self.a = new_a

    def _check_optimal(self):
        for i in self.c.matrix:
            if i < 0:
                return False
        return True

    def _pivot(self):
        pivot_column_index = self.c.matrix.index(min(self.c.matrix))
        results = []
        j = 0
        for i in self.b.matrix:
            if self.a.matrix[j][pivot_column_index] != 0 and i / self.a.matrix[j][pivot_column_index] > 0:
                results.append(i / self.a.matrix[j][pivot_column_index])
            else:
                results.append(float('inf'))
            j += 1
        pivot_row_index = results.index(min(results))
        self.basis[pivot_row_index] = pivot_column_index
        return [pivot_row_index, pivot_column_index]

    def _change_rows(self, indices):
        pivot_element = self.a.matrix[indices[0]][indices[1]]
        for i in range(self.a.columns()):
            self.a.matrix[indices[0]][i] /= pivot_element
        self.b.matrix[indices[0]] /= pivot_element
        for i in range(self.a.rows()):
            if i != indices[0]:
                pivot_coefficient = self.a.matrix[i][indices[1]] / self.a.matrix[indices[0]][indices[1]] * -1
                for j in range(self.a.columns()):
                    if self.a.matrix[indices[0]][j] != 0:
                        self.a.matrix[i][j] = self.a.matrix[i][j] + pivot_coefficient * self.a.matrix[indices[0]][j]
                self.b.matrix[i] = self.b.matrix[i] + pivot_coefficient * self.b.matrix[indices[0]]
        pivot_coefficient = self.c.matrix[indices[1]] / self.a.matrix[indices[0]][indices[1]] * -1
        for i in range(self.a.columns()):
            self.c.matrix[i] = self.c.matrix[i] + pivot_coefficient * self.a.matrix[indices[0]][i]
