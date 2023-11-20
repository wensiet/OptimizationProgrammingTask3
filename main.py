from algorithm import transportation


def main():
    # s = [300, 400, 500]
    # c = [[3, 1, 7, 4], [2, 6, 5, 9], [8, 3, 3, 2]]
    # d = [250, 350, 400, 200]

    rows = int(input("Enter the number of constraints (supply): "))
    columns = int(input("Enter the number of x's (demands): "))
    d = []
    print("Enter the demand: ")
    for i in range(columns):
        d.append(int(input()))
    c = []
    print("Enter a matrix of coefficients of constraint function: ")
    for i in range(rows):
        temp = []
        for j in range(columns):
            temp.append(int(input()))
        c.append(temp)
    print("Enter the supply: ")
    s = []
    for i in range(rows):
        s.append(int(input()))

    russel = transportation.Russell(s, c, d)
    russel.solve()

    northwest = transportation.NorthWest(s, c, d)
    northwest.solve()

    vogel = transportation.Vogel(s, c, d)
    vogel.solve()


if __name__ == "__main__":
    main()
