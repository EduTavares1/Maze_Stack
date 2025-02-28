import pygame
import numpy as np
import csv
import random
import threading
from collections import deque

class Maze:

    WALL = 0
    HALL = 1
    PLAYER = 2
    PRIZE = 3
    
    def __init__(self):
        self.M = None 
        pygame.init()
    
    def load_from_csv(self, file_path: str):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.M = np.array([list(map(int, row)) for row in reader])
            
    def init_player(self):
        while True:
            posx = random.randint(2, 39)
            posy = random.randint(2, 39)
            if self.M[posx, posy] == Maze.HALL:
                self.init_pos_player = (posx, posy)
                self.M[posx, posy] = Maze.PLAYER
                break
        
        while True:
            posx = random.randint(2, 39)
            posy = random.randint(2, 39)
            if self.M[posx, posy] == Maze.HALL:
                self.M[posx, posy] = Maze.PRIZE
                self.prize_pos = (posx, posy)
                break
    def find_prize(self) -> bool:
        stack = deque()
        visited = set()
        stack.append(self.init_pos_player)
        
        while stack:
            x, y = stack.pop()
            
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            if self.M[x, y] == Maze.PRIZE:
                return True
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.M.shape[0] and 0 <= ny < self.M.shape[1]:
                    if self.M[nx, ny] in [Maze.HALL, Maze.PRIZE] and (nx, ny) not in visited:
                        stack.append((nx, ny))
        
        return False
    def run(self):
        th = threading.Thread(target=self._display)
        th.start()
    
    def _display(self, cell_size=15):
        rows, cols = self.M.shape
        width, height = cols * cell_size, rows * cell_size
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Labirinto")
    
        BLACK = (0, 0, 0)
        GRAY = (192, 192, 192)
        BLUE = (0, 0, 255)
        GOLD = (255, 215, 0)
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print("Finding prize...")
                        result = self.find_prize()
                        print("Prize found!" if result else "No path to prize.")
    
            screen.fill(BLACK)
    
            for y in range(rows):
                for x in range(cols):
                    if self.M[y, x] == Maze.WALL:
                        color = BLACK
                    elif self.M[y, x] == Maze.HALL:
                        color = GRAY
                    elif self.M[y, x] == Maze.PLAYER:
                        color = BLUE
                    elif self.M[y, x] == Maze.PRIZE:
                        color = GOLD
                        
                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
    
            pygame.display.flip()
