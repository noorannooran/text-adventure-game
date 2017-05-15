import items, enemies, actions, world

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, the_player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjactent tiles"""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y -1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all available actions in this room"""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())

        return moves

    
class StartingRoom(MapTile):
    def intro_text(self):
        return
        """You find yourself in a cave with a flickering torch on the wall.
        You can make our four paths, each equally as dark and foreboding."""

    def modify_player(self,the_player):
        #Room has no action on player
        pass


class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return
        """You stumble, squinting into the light.
        Can it be?
        Yes! Sweet freedom
        Congratulations! You won the game!"""

    def modify_player(self, the_player):
        the_player.victory = True
        

class LootRoom(MapTile):
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x,y)

    def add_loot(self, the_player):
        the_player.inventory.append(self.item)

    def modify_player(self, the_player):
        self.add_loot(the_player)


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x,y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            if the_player.is_alive():
                print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))
            else:
                print("You are dead.")
                
    def available_actions(self):
        if self.enemy.is_alive():
            return[actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()
        
            
class EmptyCavePath(MapTile):
    def intro_text(self):
        return " Another unremarkable part of the cave. You must forge onward."

    def modify_player(self,the_player):
        #Room has no action on player
        pass


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x,y, enemies.GiantSpider())

    def intro_text(self):
        if self.enemy.is_alive():
            return "A giant spider jumps down from its web in front of you!"
        else:
            return "The corpse of a dead spider rots on the ground."


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x,y, enemies.Ogre())

    def intro_text(self):
        if self.enemy.is_alive():
            return
            """An ogre emerges from the shadows!"""
        else:
            return
            """A pool of blood starts to form beneath the corpse of the ogre."""


class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x,y,items.Dagger())

    def intro_text(self):
        return """
        You notice something shiny in the corner.
        It's a dagger! You pick it up."""


class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x,y, items.Gold(5))

    def intro_text(self):
        return
        """Something gleams in the darkness.
        it's gold! You pick it up."""
    

class Find10GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x,y, items.Gold(10))

    def intro_text(self):
        return
        """Something gleams in the darkness.
        "It's gold! You pick it up."""

        
class FindRockRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x,y, items.Rock())

    def intro_text(self):
        return
        """Your foot knocks against something in the darkness.
        "It's a rock.You bend over to pick it up."""


    
            
