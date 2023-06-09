import threading
import time
import random
import os
import pygame
from pygame.locals import (
    K_KP8,
    K_KP5,
    K_KP4,
    K_KP6,
    K_KP_PLUS,
    K_w,
    K_a,
    K_s,
    K_d,
    K_f,
    KEYDOWN,
    QUIT,
)

pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("DynaBlaster")

clock = pygame.time.Clock()


WIDTH = 10
HEIGHT = 10
EMPTY = 0
WALL = 1
PLAYER1 = 2
PLAYER2 = 3 
BOMB = 4
EXPLOSION = 5

# Players position
player1_pos = [1,1]
player2_pos = [WIDTH - 2, HEIGHT - 2]

# Bombs list
bombs = []

bomb_range = [-2, -1, 1, 2]

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
        self.bombs = 21
        self.alive = True
        with lock:
            if player_num == 1:
                board[self.pos[0]][self.pos[1]] = PLAYER1
            else:
                board[self.pos[0]][self.pos[1]] = PLAYER2

    # The method to run on the player thread
    def run(self):
        running = True                  

    # Method called when the player is hit by an explosion
    def die(self):
        self.alive = False
        print("Player ", self.player_num, " died")
        with lock:
            board[self.pos[0]][self.pos[1]] = EMPTY
            pygame.quit()
        
    def place(self, player):
        if player.bombs > 0:
                player.bombs -= 1
                with lock:
                    board[player.pos[0]][player.pos[1]] = BOMB
                    bomb = Bomb([player.pos[0], player.pos[1]])
        draw_board()
        return bomb

    # Method for moving players
    def move(self, playernum, dir):
        #Move left
        if dir == 0:
            if self.pos[1] == 0 or (board[self.pos[0]][self.pos[1] - 1] != EMPTY):
                print("Can't move there")
            else:    
                self.pos[1] -= 1
                with lock:
                    if board[self.pos[0]][self.pos[1] + 1] != BOMB: 
                        board[self.pos[0]][self.pos[1] + 1] = EMPTY
                    board[self.pos[0]][self.pos[1]] = playernum

        #Move right
        elif dir == 1:
            if self.pos[1] == 9 or (board[self.pos[0]][self.pos[1] + 1] != EMPTY):
                print("Can't move there")
            else:
                self.pos[1] += 1
                with lock:
                    if board[self.pos[0]][self.pos[1] - 1] != BOMB:
                        board[self.pos[0]][self.pos[1] - 1] = EMPTY
                    board[self.pos[0]][self.pos[1]] = playernum   
        #Move up
        elif dir == 2:
            if self.pos[0] == 0 or (board[self.pos[0] - 1][self.pos[1]] != EMPTY):
                print("Can't move there")
            else:
                self.pos[0] -= 1
                with lock:
                    if  board[self.pos[0] + 1][self.pos[1]] != BOMB:
                        board[self.pos[0] + 1][self.pos[1]] = EMPTY
                    board[self.pos[0]][self.pos[1]] = playernum
        #Move down
        elif dir == 3:
            if self.pos[0] == 9 or (board[self.pos[0] + 1][self.pos[1]] != EMPTY):
                print("Can't move there")
            else:    
                self.pos[0] += 1
                with lock:
                    if board[self.pos[0] - 1][self.pos[1]] != BOMB:
                        board[self.pos[0] - 1][self.pos[1]] = EMPTY
                    board[self.pos[0]][self.pos[1]] = playernum    
        else:
            print("Can't move there")
        draw_board()

class Bomb:
    def __init__(self, pos):
        self.pos = pos
        self.start = pygame.time.get_ticks()
        self.timer = 3000
        self.blast_timer = 1000
        self.live = True

    #Timer countdown on a bomb
    def countdown(self):
        current = pygame.time.get_ticks()
        if current - self.start >= self.timer:
            self.explosion()

    #Explosion of the bomb
    def explosion(self):
        while self.live:
            for i in bomb_range:
                if self.pos[0] + i >= HEIGHT - 1 or self.pos[1] + i >= WIDTH - 1:
                    continue
                if board[self.pos[0] + i][self.pos[1]] != EMPTY or board[self.pos[0]][self.pos[1] + i] != EMPTY:                  
                    print("xd")   
            with lock:
                board[self.pos[0]][self.pos[1]] = EMPTY
            self.live = False
        draw_board()


def draw_board():
    # Draw the game board
    for i in range(HEIGHT):
        for j in range(WIDTH):
            cell_x = j * (WINDOW_WIDTH // WIDTH)
            cell_y = i * (WINDOW_HEIGHT // HEIGHT)

            if board[i][j] == EMPTY:
                pygame.draw.rect(window, (255, 255, 255), (cell_x, cell_y, WINDOW_WIDTH // WIDTH, WINDOW_HEIGHT // HEIGHT))
            elif board[i][j] == PLAYER1:
                pygame.draw.rect(window, (0, 255, 0), (cell_x, cell_y, WINDOW_WIDTH // WIDTH, WINDOW_HEIGHT // HEIGHT))
            elif board[i][j] == PLAYER2:
                pygame.draw.rect(window, (0, 0, 255), (cell_x, cell_y, WINDOW_WIDTH // WIDTH, WINDOW_HEIGHT // HEIGHT))
            elif board[i][j] == BOMB:
                pygame.draw.rect(window, (255, 0, 0), (cell_x, cell_y, WINDOW_WIDTH // WIDTH, WINDOW_HEIGHT // HEIGHT))
            elif board[i][j] == EXPLOSION:
                pygame.draw.rect(window, (204, 102, 0), (cell_x, cell_y, WINDOW_WIDTH // WIDTH, WINDOW_HEIGHT // HEIGHT))
    pygame.display.flip()  # Update the window              

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

    board_thread = threading.Thread(target=draw_board)
    board_thread.start()
    threads.append(board_thread)

    # Waiting for game to end
    for thread in threads:
        thread.join()
    
    while True:
        for bomb in bombs:
            bomb.countdown()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_a:
                    player1.move(PLAYER1, 0)
                elif event.key == K_d:
                    player1.move(PLAYER1, 1)
                elif event.key == K_w:
                    player1.move(PLAYER1, 2)
                elif event.key == K_s:
                    player1.move(PLAYER1, 3)
                elif event.key == K_KP4:
                    player2.move(PLAYER2, 0)
                elif event.key == K_KP6:
                    player2.move(PLAYER2,1)
                elif event.key == K_KP8:
                    player2.move(PLAYER2,2)
                elif event.key == K_KP5:
                    player2.move(PLAYER2,3)
                elif event.key == K_f:
                    bomb = player1.place(player1)
                    bombs.append(bomb)
                elif event.key == K_KP_PLUS:
                    bomb = player2.place(player2)
                    bombs.append(bomb)
        pygame.display.update()

if __name__ == "__main__":
    main()