from typing import Union

from player import Player
from asteroid import Asteroid
from bullet import Bullet


Collideable = Union[Player, Asteroid, Bullet]
