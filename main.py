import pygame
import pickle
import math
from abc import ABC, abstractmethod

pygame.init()
background_colour = (255,255,255)
(width, height) = (32, 23)

def distance(a, b):
    return math.sqrt(((a[0]+0.5-b[0])**2)+((a[1]+0.5-b[1])**2))

class TileMap:
    
    def __init__(self,size,pixel):
        self.size = size
        self.tiles = []
        self.pixel = pixel
        
        for x in range(size[0]):
            self.tiles.append([])
            for y in range(size[1]):
                if ( x == 0
                        or y == 0
                        or x == size[0]-1
                        or y == size[1] -1):
                    self.tiles[x].append(1)
                else:
                    self.tiles[x].append(0)
                
    def draw(self, materials, window, window_size):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if (x >= 0
                        and x < self.size[0]
                        and y >= 0
                        and y < self.size[1]
                        and self.tiles[x][y] > 0):
                    window.display(materials[self.tiles[x][y]],
                                (x*self.pixel, y*self.pixel))
                    
class Level(TileMap):
    
    def __init__(self, size, pixel, monsters, spawnpoint, endpoints):
        super().__init__(size, pixel)
        self.monsters = monsters
        self.spawnpoint = spawnpoint
        self.endpoints = endpoints
        
    def update(self, player):
        
        for i in self.monsters:
            if ((i.coordinates[0] <= player.coordinates[0] <= (i.coordinates[0]+1)
                and i.coordinates[1] <= player.coordinates[1] <= (i.coordinates[1]+1))
                or (i.coordinates[0] <= player.coordinates[0]+0.9 <= (i.coordinates[0]+1)
                and i.coordinates[1] <= player.coordinates[1] <= (i.coordinates[1]+1))
                or (i.coordinates[0] <= player.coordinates[0] <= (i.coordinates[0]+1)
                and i.coordinates[1] <= player.coordinates[1]+0.9 <= (i.coordinates[1]+1))
                or (i.coordinates[0] <= player.coordinates[0]+0.9 <= (i.coordinates[0]+1)
                and i.coordinates[1] <= player.coordinates[1]+0.9 <= (i.coordinates[1]+1))):
                
                player.damage()
          
        for i in self.endpoints:
            if (int(player.coordinates[0]) == i[0] and int(player.coordinates[1]) == i[1]):
                return True
            
        return False
    
    def draw(self, materials, window, window_size):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if (x >= 0
                        and x < self.size[0]
                        and y >= 0
                        and y < self.size[1]
                        and self.tiles[x][y] > 0):
                    window.display(materials[self.tiles[x][y]],
                                (x*self.pixel, y*self.pixel))
        for i in self.endpoints:
            window.display(materials[2], (i[0]*self.pixel, i[1]*self.pixel - 16))
        
        window.display(materials[2], (int(self.spawnpoint[0]*self.pixel), int(self.spawnpoint[1]*self.pixel - 16)))
                    
                
class Graphics:
    
    def __init__(self,name,size,tile_size):
        self.window = pygame.display.set_mode((size[0]*tile_size,size[1]*tile_size))
        pygame.display.set_caption(name)
        self.window.fill(background_colour)
        pygame.display.flip()
        
    def display(self, material, coord):
        self.window.blit(material,coord)
    
    def draw(self, tilemap, player):
        config_manager = ConfigManager()
        self.window.fill(background_colour)
        self.display(config_manager.get_param_value("Materials")[4],(0,0))
        
        
        tilemap.draw(config_manager.get_param_value("Materials"),
                          self,
                          config_manager.get_param_value("Size"))
        
        player.draw(config_manager.get_param_value("Materials"),
                         self,
                         config_manager.get_param_value("Size"),
                         config_manager.get_param_value("Pixel"))
        
        for i in tilemap.monsters:
            i.draw(config_manager.get_param_value("Materials"),
                         self,
                         config_manager.get_param_value("Size"),
                         config_manager.get_param_value("Pixel"))
        
        pygame.display.flip()
        
                

class Entity(ABC):

    def __init__(self, name, health, coordinates):
        self.name = name
        self.health = health
        self.coordinates = coordinates
        self.gravity = True

    @abstractmethod
    def move(self, coordinates, tilemap):
        pass
    
    @abstractmethod
    def damage(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
class Player(Entity):

    def __init__(self, health, coordinates):
        super().__init__("Player", health, coordinates)
        self.jump = 0

    def move(self, position, tilemap):
        x = round(self.coordinates[0]+position[0],1)
        y = round(self.coordinates[1]+position[1],1)
        
        if (x >= 0
                and tilemap.tiles[int(x)][int(y)] == 0
                and y >= 0
                and tilemap.tiles[int(x)][int(y+0.9)] == 0
                and tilemap.tiles[int(x+0.9)][int(y)] == 0
                and tilemap.tiles[int(x+0.9)][int(y+0.9)] == 0):
            self.coordinates = (x,y)


    def damage(self):
        if (self.health > 0):
            self.health -= 1
        else:
            pygame.display.quit()
            pygame.quit()
            quit()
    
    def draw(self, materials, window, window_size, pixel):
        window.display(materials[0], (int(self.coordinates[0]*pixel), int(self.coordinates[1]*pixel)))
    
    def update(self, tilemap):
        keys = pygame.key.get_pressed()
        
        if (tilemap.tiles[int(self.coordinates[0])][int(self.coordinates[1]+1)] != 0 or tilemap.tiles[int(self.coordinates[0]+0.9)][int(self.coordinates[1]+1)] != 0):
            self.gravity = False
            self.jump = 0
        elif not keys[pygame.K_UP] or self.jump >= 22:
            self.gravity = True

        if self.gravity:
            self.move((0,0.1), tilemap)
        
        if keys[pygame.K_LEFT]:
            self.move((-0.1,0), tilemap)
        if keys[pygame.K_RIGHT]:
            self.move((0.1,0), tilemap)
        if keys[pygame.K_UP] and not self.gravity:
            self.move((0,-0.1), tilemap)
            self.jump += 1
        if keys[pygame.K_DOWN]:
            self.move((0,0.1), tilemap)
            
class Monster(Entity):

    def __init__(self, health, coordinates, sprite):
        super().__init__("Monster", health, coordinates)
        self.speed = -0.1
        self.sprite = sprite

    def move(self, position, tilemap):
        x = round(self.coordinates[0]+position[0],1)
        y = round(self.coordinates[1]+position[1],1)
        
        if (x >= 0
                and tilemap.tiles[int(x)][int(y)] == 0
                and y >= 0
                and tilemap.tiles[int(x)][int(y+0.9)] == 0
                and tilemap.tiles[int(x+0.9)][int(y)] == 0
                and tilemap.tiles[int(x+0.9)][int(y+0.9)] == 0):
            self.coordinates = (x,y)


    def damage(self):
        pass
    
    def draw(self, materials, window, window_size, pixel):
        window.display(materials[self.sprite], (int(self.coordinates[0]*pixel), int(self.coordinates[1]*pixel)))
    
    def update(self, tilemap):
        self.move((0,0.1), tilemap)
        
        x = round(self.coordinates[0]+self.speed,1)
        y = self.coordinates[1]
        if (x >= 0
                and tilemap.tiles[int(x)][int(y)] == 0
                and tilemap.tiles[int(x)][int(y+0.9)] == 0
                and tilemap.tiles[int(x+0.9)][int(y)] == 0
                and tilemap.tiles[int(x+0.9)][int(y+0.9)] == 0):
            self.move((self.speed,0), tilemap)
        else:
            self.speed *= -1

class ConfigManager:
    _instance = None
    _config = {}

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)

        for key, value in kwargs.items():
            cls._config[key] = value

        return cls._instance

    def set_param_value(cls, string, value):
        cls._config[string] = value

    def get_param_value(cls, string):
        return cls._config[string]
    
class Game:
    
    def __init__(self, name, size, materials, tile_size):
        self.config_manager = ConfigManager()
        #self.tilemap = TileMap(size,tile_size)
        #with open('level_monsters.pkl', 'rb') as file:
        #    self.monsters = pickle.load(file)
        self.monsters = []
        with open('level.pkl', 'rb') as file:
            #loaded_person = pickle.load(file)
            self.tilemap = pickle.load(file) #Level(size, tile_size, self.monsters, (2,5), [(30,21,"Test !")])
            
        
        self.player = Player(1,self.tilemap.spawnpoint)
        
        self.window = Graphics(name, size, tile_size)
        
        self.config_manager.set_param_value("Name", name)
        self.config_manager.set_param_value("Size", size)
        self.config_manager.set_param_value("Materials", materials)
        self.config_manager.set_param_value("Pixel", tile_size)
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if (x//self.tilemap.pixel < self.tilemap.size[0]
                        and y//self.tilemap.pixel < self.tilemap.size[1]
                        and 1 < distance(self.player.coordinates, ((x//self.tilemap.pixel), (y//self.tilemap.pixel))) < 4):
                    if event.button == 1:
                        self.tilemap.tiles[(x//self.tilemap.pixel)][(y//self.tilemap.pixel)] = 1
                    elif event.button == 3:
                        self.tilemap.tiles[(x//self.tilemap.pixel)][(y//self.tilemap.pixel)] = 0
                elif (x//self.tilemap.pixel < self.tilemap.size[0]
                        and y//self.tilemap.pixel < self.tilemap.size[1]
                        and 4 < distance(self.player.coordinates, ((x//self.tilemap.pixel), (y//self.tilemap.pixel)))
                        and event.button == 2):
                    self.tilemap.monsters.append(Monster(1, ((x//self.tilemap.pixel), (y//self.tilemap.pixel)), 3))
                    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.tilemap.monsters = []
            #self.player.coordinates = self.tilemap.spawnpoint
            
        self.player.update(self.tilemap)
        self.tilemap.update(self.player)
        for i in self.tilemap.monsters:
            i.update(self.tilemap)
        
        self.window.draw(self.tilemap, self.player)
        
        return True

mats = []
pixel = 16
game = Game("Test game !", (width, height), mats, pixel)
mats.append(pygame.transform.scale(pygame.image.load('player.png'), (pixel,pixel)))
mats.append(pygame.transform.scale(pygame.image.load('tile2.png'), (pixel,pixel)))
mats.append(pygame.image.load('sign.png'))
mats.append(pygame.transform.scale(pygame.image.load('bullet.png'), (pixel,pixel)))
mats.append(pygame.image.load('background.png'))
clock = pygame.time.Clock()

running = True
while running:
    running = game.update()
    clock.tick(75)
    
game.tilemap.spawnpoint = game.player.coordinates
with open('level.pkl', 'wb') as file:
    pickle.dump(game.tilemap, file)
    
pygame.display.quit()
pygame.quit()
quit()
        