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
board = [[EMPTY for y in range(HEIGHT)] for x in range(WIDTH)]

# Player class
class Player:
    def __init__(self, player_num, start_pos):
        self.player_num = player_num
        self.pos = start_pos
        self.bombs = 3
        self.alive = True
        with lock:
            board[self.pos[0]][self.pos[1]] = PLAYER

    # The method to run on the player thread
    def run(self):
        while self.alive:
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
                    with lock:
                        board[self.pos[0]][self.pos[1]] = BOMB
                        print("Bomb placed on ", self.pos[0], ", ", self.pos[1])
                    

    # Method called when the player is hit by an explosion
    def die(self):
        self.alive = False
        print("Player ", self.player_num, " died")
        with lock:
            board[self.pos[0]][self.pos[1]] = EMPTY
        

    # Method for moving players
    def move(self, dir):
        #Move left
        if dir == 0:
            if self.pos[1] == 0 or (board[self.pos[0]][self.pos[1] - 1] != EMPTY):
                print("Can't move there")
            else:    
                self.pos[1] -= 1
                with lock:
                    board[self.pos[0]][self.pos[1] + 1] = EMPTY
                    board[self.pos[0]][self.pos[1]] = PLAYER

        
        #Move right
        elif dir == 1:
            if self.pos[1] == 9 or (board[self.pos[0]][self.pos[1] + 1] != EMPTY):
                print("Can't move there")
            else:
                self.pos[1] += 1
                with lock:
                    board[self.pos[0]][self.pos[1] - 1] = EMPTY
                    board[self.pos[0]][self.pos[1]] = PLAYER   
                

        #Move up
        elif dir == 2:
            if self.pos[0] == 0 or (board[self.pos[0] - 1][self.pos[1]] != EMPTY):
                print("Can't move there")
            else:
                self.pos[0] -= 1
                with lock:
                    board[self.pos[0] + 1][self.pos[1]] = EMPTY
                    board[self.pos[0]][self.pos[1]] = PLAYER
                
        
        #Move down
        elif dir == 3:
            if self.pos[0] == 9 or (board[self.pos[0] + 1][self.pos[1]] != EMPTY):
                print("Can't move there")
            else:    
                self.pos[0] += 1
                with lock:
                    board[self.pos[0] - 1][self.pos[1]] = EMPTY
                    board[self.pos[0]][self.pos[1]] = PLAYER
                
        else:print("Can't move there")
        print(self.pos)

def print_board():
    row = ""
    for i in range(HEIGHT):
        for j in range(WIDTH):
            row += str("|")
            if board[i][j] == EMPTY:
                row += str(" ")
            elif board[i][j] == PLAYER:
                row += str("P")
            elif board[i][j] == BOMB:
                row += str("B")
        row += "|"
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

    # Waiting for game to end
    for thread in threads:
        thread.join()                  

if __name__ == "__main__":
    main()