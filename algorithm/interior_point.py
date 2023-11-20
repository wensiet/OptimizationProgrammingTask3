import numpy as np


class InteriorPoint:
    def __init__(self, c: list = None, a: list[list] = None, alpha: float = None,
                 x: list = None):
        self.c = np.array(c, float)
        self.a = np.array(a, float)
        self.alpha = alpha
        self.x = np.array(x, float)

    def add_slack_vars(self):
        if self.a.ndim == 1:
            np.append(self.a, 1)
            np.append(self.c, 0)
            return
        identity = np.eye(self.a.shape[0])
        total_rows = self.a.shape[0]
        total_cols = self.a.shape[1] + self.a.shape[0]
        new_a = np.zeros((total_rows, total_cols)).astype('int')
        new_a[0:total_rows, 0:self.a.shape[1]] = self.a
        new_a[0:total_rows, self.a.shape[1]:total_cols] = identity
        self.a = new_a
        for i in range(total_rows):
            self.c = np.append(self.c, 0)

    def solve_llp(self):
        self.add_slack_vars()
        while True:
            x = self.x
            D = np.diag(self.x)

            new_a = np.dot(self.a, D)
            new_c = np.dot(D, self.c)

            identity = np.eye(len(self.c))

            aat = np.dot(new_a, np.transpose(new_a))

            aat_inv = np.linalg.inv(aat)

            matrix_h = np.dot(np.transpose(new_a), aat_inv)

            matrix_p = np.subtract(identity, np.dot(matrix_h, new_a))
            gradient = np.dot(matrix_p, new_c)

            v = np.absolute(np.min(gradient))

            new_x = np.add(np.ones(len(self.c), float), (self.alpha / v) * gradient)
            self.x = np.dot(D, new_x)
            if np.linalg.norm(np.subtract(self.x, x), ord=2) < 0.0001:
                break

        self.print_solution()

    def print_solution(self):
        optimal = sum(self.c[i] * self.x[i] for i in range(len(self.c)))
        for i in range(len(self.x)):
            if self.a.ndim == 1 and i < len(self.x) - 1 or self.a.ndim > 1 and i < len(self.x) - self.a.shape[0]:
                print(f"x{i + 1}={format(self.x[i], '.2f')}", end=" ")
            else:
                print(f"s{i + 1}={format(self.x[i], '.2f')}", end=" ")
        print(f"with optimal {format(optimal, '.2f')}")
