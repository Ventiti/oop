# oop
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
