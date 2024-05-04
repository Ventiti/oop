# Object-Oriented Programming ( OOP ) Coursework
A project for creating and documenting a system based on the analysis of functional requirements and the principles of object-oriented programming using the Python programming language.

<h1>Introduction</h1>
<h2>What is your application ?</h2>

<p>The project is a platform game ( Similar to Mario ) where you can place your own platform.</p>

<h2>How to run the program ?</h2>

<p>Just click on run and the program will run automatically.</p>

<h2>How to use the program ?</h2>

<p>When the program starts, you can move your character using the arrow keys.<br>
To place a block, right-click; to remove it, left-click. (If the block is placed or removed too close or too far from the player, it won't work.)<br>
You can place a monster wherever you want by doing a middle mouse click.<br>
To delete all monsters, press the R key.</p>

<h1>Body</h1>

<h2>Explain how the program covers (implements) functional requirements</h2>

<h3>4 OOP pillars, their meaning, and usage (in code and overall)</h3>
<h4>Encapsulation</h4>

```PYTHON
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
```
<p>The class "ConfigManager" contains two protected arguments.</p>

<h4>Data abstraction and Polymorphism</h4>

```PYTHON
class Entity(ABC):

    def __init__(self, name, health, coordinates):
        pass

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
        pass

    def move(self, position, tilemap):
        pass


    def damage(self):
        pass
    
    def draw(self, materials, window, window_size, pixel):
        pass
    
    def update(self, tilemap):
        pass
            
class Monster(Entity):

    def __init__(self, health, coordinates, sprite):
        pass

    def move(self, position, tilemap):
        pass

    def damage(self):
        pass
    
    def draw(self, materials, window, window_size, pixel):
        pass
    
    def update(self, tilemap):
        pass
```
<p>The class "Player" and "Monster" inherit from the abstract class "Entity".</p>

<h4>Inheritance</h4>

```PYTHON
class TileMap:
    
    def __init__(self,size,pixel):
        pass
                
    def draw(self, materials, window, window_size):
        pass
                    
class Level(TileMap):
    
    def __init__(self, size, pixel, monsters, spawnpoint, endpoints):
        pass
        
    def update(self, player):
        pass
    
    def draw(self, materials, window, window_size):
        pass
```
<p>The class "Level" inherit from the class "TileMap".</p>

<h3>Use at least 2 design patterns</h3>
<h4>Singleton</h4>

<p>The Singleton design pattern is a creational pattern that ensures a class has only one instance and provides a global point of access to that instance. In Python, the Singleton pattern can be implemented using various approaches. One common approach is to use a class variable to store the instance and a class method to access it.</p>

```PYTHON
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
```

<p>This pattern ensures that only one instance of the class is created throughout the program's execution, making it suitable for scenarios where exactly one instance of a class is needed, such as managing shared resources or configuration settings.</p>

<h4>Wrapper</h4>

<p>The Wrapper design pattern, also known as the Adapter pattern, is a structural pattern that allows incompatible interfaces to work together. In Python, the Wrapper pattern is often used to adapt the interface of one class to another interface expected by the client code.</p>

```PYTHON
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
```

<p>The Wrapper pattern allows you to use existing classes with incompatible interfaces in your codebase without the need for modifications, thus promoting code reusability and flexibility.</p>

<h3>Reading from file & writing to file</h3>

<p>When the program is closed, it automatically saves the game state in the "level.pkl" file. Upon restarting, the program reloads the game state from this file, allowing the player to resume from where they left off. This functionality ensures that progress is preserved even if the program is closed unexpectedly.</p>

<h2>Results and Summary</h2>

<p>- Implementing a Mario-like game in Python posed several challenges, such as collision detection with enemies.<br>
- Implementing game features such as enemy behavior was an enjoyable experience.<br>
- Despite these challenges, overcoming them resulted in a rewarding learning experience, increasing my skills in game development, problem-solving, and Python programming.</p>
<h4>How it would be possible to extend your application ?</h4>
<p>- Implementing a multi-level feature could be a great idea.<br>
- Implementing more enemies and bosses.<br>
- Implementing a menu to select level to load.</p>
