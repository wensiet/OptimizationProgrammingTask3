from copy import deepcopy

import numpy as np


class NorthWest:
    def __init__(self, s: list = None, c: list = None, d: list = None):
        self.s = np.array(s, float)
        self.c = np.array(c, float)
        self.d = np.array(d, float)

    def solve(self):
        supply = np.array(self.s, float)
        demand = np.array(self.d, float)
        cost = np.zeros(self.c.shape)
        j = 0
        i = 0
        while i != cost.shape[0]:
            while supply[i] != 0:
                if j == demand.shape[0]:
                    print("No solution found!")
                    return
                if demand[j] != 0:
                    cost[i][j] = min(supply[i], demand[j])
                    supply[i] = max(0, supply[i] - cost[i][j])
                    demand[j] = max(0, demand[j] - cost[i][j])
                if supply[i] != 0:
                    j += 1
            i += 1
        answer = 0
        for i in range(supply.shape[0]):
            for j in range(demand.shape[0]):
                answer += self.c[i][j] * cost[i][j]
        print("Northwest algorithm completed.\nHere is the obtained matrix:")
        print(cost)
        print("\nThe Total Transportation Cost:", answer, "\n\n")


class Vogel:
    def __init__(self, s: list = None, c: list[list] = None, d: list = None):
        self.s = s
        self.c = c
        self.d = d
        self.balance_problem()
        self.res = 0
        self.res_matrix = [[0 for _ in range(len(self.c[0]))] for _ in range(len(self.c))]

    def balance_problem(self):
        if sum(self.s) != sum(self.d):
            if sum(self.s) < sum(self.d):
                self.s.append(sum(self.d) - sum(self.s))
                self.c.append([0 for _ in range(len(self.c[0]))])
            if sum(self.s) > sum(self.d):
                self.d.append(sum(self.s) - sum(self.d))
                for i in range(len(self.c)):
                    self.c[i].append(0)

    def get_row_diff(self, row):
        st = sorted(deepcopy(self.c[row]))
        return st[1] - st[0]

    def get_col_diff(self, col):
        cl = sorted([x[col] for x in self.c])
        return cl[1] - cl[0]

    def solve(self):
        diffs = {
            "c": {},
            "r": {}
        }
        for i in range(len(self.c)):
            diffs["r"][i] = max(0, self.get_row_diff(i))

        for i in range(len(self.c[0])):
            diffs["c"][i] = max(0, self.get_col_diff(i))

        row_diff_max = 0
        row_diff = None
        for index in diffs["r"]:
            if diffs["r"][index] > row_diff_max:
                row_diff_max = diffs["r"][index]
                row_diff = (index, row_diff_max)

        col_diff_max = 0
        col_diff = None
        for index in diffs["c"]:
            if diffs["c"][index] > col_diff_max:
                col_diff_max = diffs["c"][index]
                col_diff = (index, col_diff_max)
        if row_diff[1] >= col_diff[1]:
            victim_row = row_diff[0]
            victim_column = self.c[victim_row].index(min(self.c[victim_row]))
            mini = min(self.s[victim_row], self.d[victim_column])
            elim_row = victim_row if mini == self.s[victim_row] else None
            elim_col = victim_column if mini == self.d[victim_column] else None
            self.res_matrix[victim_row][victim_column] = mini * self.c[victim_row][victim_column]
            self.res += mini * self.c[victim_row][victim_column]
            if elim_row is not None:
                for i in range(len(self.c[elim_row])):
                    self.c[elim_row][i] = float('inf')
            if elim_col is not None:
                for i in range(len(self.c)):
                    self.c[i][elim_col] = float('inf')
            self.s[victim_row] -= mini
            self.d[victim_column] -= mini
        else:
            victim_column = col_diff[0]
            victim_row = [x[victim_column] for x in self.c].index(min([x[victim_column] for x in self.c]))
            mini = min(self.s[victim_row], self.d[victim_column])
            elim_row = victim_row if mini == self.s[victim_row] else None
            elim_col = victim_column if mini == self.d[victim_column] else None
            self.res_matrix[victim_row][victim_column] = mini * self.c[victim_row][victim_column]
            self.res += mini * self.c[victim_row][victim_column]
            if elim_row is not None:
                for i in range(len(self.c[elim_row])):
                    self.c[elim_row][i] = float('inf')
            if elim_col is not None:
                for i in range(len(self.c)):
                    self.c[i][elim_col] = float('inf')
            self.s[victim_row] -= mini
            self.d[victim_column] -= mini
        if sum(self.s) == 0 and sum(self.d) == 0:
            self.get_info()
            return
        self.solve()

    def get_info(self):
        print("Vogel obtained optimal solution")
        print("Here is the obtained matrix:")
        for r in self.res_matrix:
            print(r)
        print("\nThe Total Transportation Cost:", self.res, "\n")


class Russell:
    def __init__(self, s: list = None, c: list = None, d: list = None):
        self.s = np.array(s, float)
        self.c = np.array(c, float)
        self.d = np.array(d, float)

    def solve(self):
        cost = np.array(self.c, float)
        supply = np.array(self.s, float)
        demand = np.array(self.d, float)
        row_max = np.zeros(cost.shape[0])
        column_max = np.zeros(cost.shape[1])
        ans_matrix = np.zeros(cost.shape)

        for i in range(row_max.shape[0]):
            row_max[i] = cost[i][np.argmax(cost, 1)[i]]
        for i in range(column_max.shape[0]):
            column_max[i] = cost[np.argmax(cost, 0)[i]][i]
        for i in range(cost.shape[0]):
            for j in range(cost.shape[1]):
                cost[i][j] = row_max[i] + column_max[j] - cost[i][j]

        # Check by counter in case if the method is over
        cost_nonzeros = np.count_nonzero(cost)
        while cost_nonzeros:
            i, j = np.unravel_index(np.argmax(cost), cost.shape)
            if supply[i] > 0:
                if demand[j] > 0:
                    ans_matrix[i][j] = min(supply[i], demand[j])
                    supply[i] -= ans_matrix[i][j]
                    demand[j] -= ans_matrix[i][j]
            cost[i][j] = 0
            cost_nonzeros -= 1

        answer = 0
        for i in range(cost.shape[0]):
            for j in range(cost.shape[1]):
                answer += self.c[i][j] * ans_matrix[i][j]

        print("Russel algorithm completed.\nHere is the obtained matrix:")
        print(ans_matrix)
        print("\nThe Total Transportation Cost:", answer, "\n\n")
