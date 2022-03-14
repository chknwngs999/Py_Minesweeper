import random
import time


class Button:
    def __init__(self, x, y):
        self.__marked = False
        self.__clicked = False
        self.__x = x
        self.__y = y
        self.__display = "⬜"

    def __str__(self):
        if lost and self in mines:
            if not self.__clicked:
                if self.__marked:
                    return "🚩"
                return "💣"
            return "💥"
        if self.__marked:
            return "🚩"
        elif self.__clicked:
            if self.around != 0:
                return " " + str(self.around)
            else:
                return "  "
        else:
            return "⬜"

    def onClick(self, click):
        self.__clicked = True
        if click == 'm':
            self.__marked = not self.__marked
            if self.__marked == False:
                self.__clicked = False
        elif self.around == 0 and board[self.__x][self.__y] not in mines:
            for i in range(self.__x-1, self.__x+2):
                for j in range(self.__y-1, self.__y+2):
                    if isValid(i, j):
                        if not board[i][j].__clicked and board[i][j] not in mines:
                            board[i][j].onClick("c")

    def isClicked(self):
        return self.__clicked


def isValid(x, y):
    return (x >= 0 and y >= 0) and (x < 10 and y < 10)


def countMines(button, x, y):
    count = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if isValid(i, j):
                if board[i][j] in mines:
                    count += 1

    if board[x][y] in mines:
        count -= 1
    return count


def checkWin():
    for x in range(10):
        for y in range(10):
            if board[x][y] not in mines:
                if board[x][y].isClicked() == False:
                    return False
    return True


def draw():
    print("   a b c d e f g h i j")
    for x in range(10):
        print(f"{x} " + "".join([board[x][y].__str__() for y in range(10)]))


lost = False

board = [[Button(x, y) for y in range(10)] for x in range(10)]
mines = []
minecounter = 0

while minecounter != 10:
    x, y = (random.randint(0, 9), random.randint(0, 9))
    if board[x][y] not in mines:
        mines.append(board[x][y])
        minecounter += 1
for x in range(10):
    for y in range(10):
        board[x][y].around = countMines(board[x][y], x, y)

print("""
Instructions: 3 character input
Character 1: m for mark / c for click
Character 2: Column letter (a-j)
Character 3: Row number (0-9)
""")
starttime = time.perf_counter()
while not lost:
    draw()

    try:
        given = tuple(input().lower().strip())

        if len(given) != 3 or given[0] not in "fmc":
            raise BaseException

        todo, col, row = tuple(given)

        col = ord(col)-97
        row = int(row)

        if not isValid(col, row):
            raise BaseException
    except:
        print("Invalid Input")
        continue

    board[row][col].onClick(todo)
    if board[row][col] in mines:
        lost = True
    if checkWin():
        break
# end timer
endtime = time.perf_counter()
elapsed = endtime-starttime

draw()
if lost:
    print("You lose...", end=" ")
else:
    print("You win!", end=" ")

print(f"That took {elapsed:.2f} seconds")

# todo - generate mines AFTER first click
# middle click - f=flag, c=click, m=middle click
# add gui
