import threading
import time
import random

WIDTH = 10
HEIGHT = 10
EMPTY = 0
WALL = 1
PLAYER = 2
BOMB = 3
EXPLOSION = 4

# Players position
player1_pos = [1,1]
player2_pos = [WIDTH - 2, HEIGHT - 2]

# Threads list
threads = []

# Semaphore for synchronizing board access
lock = threading.Lock()


# Board initialization
board = [[EMPTY for y in range(WIDTH)] for x in range(HEIGHT)]

# Player class
class Player:
    def __init__(self, player_num, start_pos):
        self.player_num = player_num
        self.pos = start_pos
        self.bombs = 3
        self.alive = True

    # The method to run on the player thread
    def run(self):
        while self.alive:
            print_board()
            # Reading the player's movement from the keyboard
            if self.player_num == 1:
                key = input("Gracz 1: ")
            else:
                key = input("Gracz 2: ")

            #Inputs are left = 0, right = 1, up = 2, down = 3
            if key == "a":
                self.move(0)
            elif key == "d":
                self.move(1)
            elif key == "w":
                self.move(2)
            elif key == "s":
                self.move(3)
            elif key == ".":
                # Player places a bomb
                if self.bombs > 0:
                    self.bombs -= 1
                    lock.acquire()
                    board[self.pos[0]][self.pos[1]] = BOMB
                    print("Bomb placed on ", self.pos[0], ", ", self.pos[1])
                    lock.release()

    # Method called when the player is hit by an explosion
    def die(self):
        self.alive = False
        print("Player ", self.player_num, " died")
        lock.acquire()
        board[self.pos[0]][self.pos[1]] = EMPTY
        lock.release()

    # Method for moving players
    def move(self, dir):
        if dir == 0:
            if (board[self.pos[0] - 1][self.pos[1]] == EMPTY):
                self.pos[0] -= 1
                print(self.pos)
                lock.acquire()
                board[self.pos[0] - 1][self.pos[1]] = EMPTY
                board[self.pos[0]][self.pos[1]] = PLAYER
                lock.release
            else:
                print("Can't move there")
        elif dir == 1:
            if (board[self.pos[0] + 1][self.pos[1]] == EMPTY):
                self.pos[0] += 1
                print(self.pos)
                lock.acquire()
                board[self.pos[0] + 1][self.pos[1]] = EMPTY
                board[self.pos[0]][self.pos[1]] = PLAYER
                lock.release
            else:
                print("Can't move there")
        elif dir == 2:
            if (board[self.pos[0]][self.pos[1] - 1] == EMPTY):
                self.pos[1] -= 1
                print(self.pos)
                lock.acquire()
                board[self.pos[0]][self.pos[1] - 1] = EMPTY
                board[self.pos[0]][self.pos[1]] = PLAYER
                lock.release
            else:
                print("Can't move there")
        elif dir == 3:
            if (board[self.pos[0]][self.pos[1] + 1] == EMPTY):
                self.pos[1] += 1
                print(self.pos)
                lock.acquire()
                board[self.pos[0]][self.pos[1] + 1] = EMPTY
                board[self.pos[0]][self.pos[1]] = PLAYER
                lock.release
            else:
                print("Can't move there")
        else:print("Can't move there")

# Funkcja obsługująca bomby
def handle_bombs():
    while True:
        # Czekamy na wybuch bomby
        time.sleep(3)
        # Szukamy bomb na planszy
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if board[x][y] == BOMB:
                    # Bomb explosion
                    lock.acquire()
                    board[x][y] = EXPLOSION
                    lock.release()
                    # Ustalamy obszar eksplozji
                    explosion_area = get_explosion_area(x, y)
                    # Usuwamy eksplozję po 1 sekundzie
                    time.sleep(1)
                    lock.acquire()
                    board[x][y] = EMPTY
                    lock.release()
                    # Sprawdzamy, czy gracz został trafiony przez eksplozję
                    if player1.pos == (x, y):
                        player1.die()
                    elif player2.pos == (x, y):
                        player2.die()
                        
# Function returning the space after bomb explosion
def get_explosion_area(x, y):
    explosion_area = []
    # Searching to the right of the bomb
    for i in range(1, 4):
        if x + i >= WIDTH or board[x+i][y] == WALL:
            break
        explosion_area.append((x+i, y))
        if board[x+i][y] == PLAYER:
            break
    # Searching to the left of the bomb
    for i in range(1, 4):
        if x - i < 0 or board[x-i][y] == WALL:
            break
        explosion_area.append((x-i, y))
        if board[x-i][y] == PLAYER:
            break
    # Searching below the bomb
    for i in range(1, 4):
        if y + i >= HEIGHT or board[x][y+i] == WALL:
            break
        explosion_area.append((x, y+i))
        if board[x][y+i] == PLAYER:
            break
    # Searching above the bomb
    for i in range(1, 4):
        if y - i < 0 or board[x][y-i] == WALL:
            break
        explosion_area.append((x, y-i))
        if board[x][y-i] == PLAYER:
            break
    return explosion_area

def print_board():
    row = ""
    for i in range(WIDTH - 1):
        for j in range(HEIGHT - 1):
            row += str("|")
            if board[i][j] == EMPTY:
                row += str(" ")
            elif board[i][j] == PLAYER:
                row += str("P")
            elif board[i][j] == BOMB:
                row += str("B")
            
            if j == WIDTH - 1:
                row += str("|")
            print(row)
        row = ""

def main():

    # Creating players
    player1 = Player(1, player1_pos)
    player2 = Player(2, player2_pos)

    # Running players threads
    player1_thread = threading.Thread(target=player1.run)
    player1_thread.start()
    threads.append(player1_thread)

    player2_thread = threading.Thread(target=player2.run)
    player2_thread.start()
    threads.append(player2_thread)

    # Running bomb threads
    #bomb_thread = threading.Thread(target=handle_bombs)
    #bomb_thread.start()
    #threads.append(bomb_thread)

    # Waiting for game to end
    for thread in threads:
        thread.join()                  

if __name__ == "__main__":
    main()