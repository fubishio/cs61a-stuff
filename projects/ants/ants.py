"""The ants module implements game logic for Ants Vs. SomeBees."""

import random
import sys
from ucb import main, interact, trace
from collections import OrderedDict


################
# Core Classes #
################


class Place:
    """A Place holds insects and has an exit to another Place."""

    def __init__(self, name, exit=None):
        """Create a Place with the given exit.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        if self.exit is not None:                   # check if the place has an exit
            self.exit.entrance = self               # set the exit's entrance to the place

    def add_insect(self, insect):
        """Add an Insect to this Place.

        There can be at most one Ant in a Place, unless exactly one of them is
        a BodyguardAnt (Phase 4), in which case there can be two. If add_insect
        tries to add more Ants than is allowed, an assertion error is raised.

        There can be any number of Bees in a Place.
        """
        if insect.is_ant:
            # Phase 4: Special handling for BodyguardAnt
            if (self.ant is not None) and self.ant.can_contain(insect):         # check if there is an ant and if that ant can contain insect
                self.ant.contain_ant(insect)                                    # if so, that ant's ant is insect
            elif (self.ant is not None) and insect.can_contain(self.ant):       # check if there is an ant and if insect can contain that ant
                insect.contain_ant(self.ant)                                    # if so, that insect's ant is that ant
                self.ant = insect                                               # that place's ant is insect
            else:
                assert self.ant is None, 'Two ants in {0}'.format(self)
                self.ant = insect
        else:
            self.bees.append(insect)
        insect.place = self

    def remove_insect(self, insect):
        """Remove an Insect from this Place."""
        if insect.is_ant:                           
            if insect.container and (insect.ant != None):       # check if insect has an ant
                self.ant = insect.ant                           # set the place's ant to that ant
            else:
                assert self.ant == insect, '{0} is not in {1}'.format(insect, self)
                # Phase 4: Special handling for QueenAnt
                if type(self.ant) != QueenAnt or (type(self.ant) == QueenAnt) and (self.ant != self.ant.queens[0]):   # checks if ant is not a QueenAnt or the true QueenAnt
                    self.ant = None                                                                                   # remove the ant
        else:
            self.bees.remove(insect)

        insect.place = None

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has armor and a Place."""

    is_ant = False
    watersafe = False

    def __init__(self, armor, place=None):
        """Create an Insect with an armor amount and a starting Place."""
        self.armor = armor
        self.place = place  # set by Place.add_insect and Place.remove_insect

    def reduce_armor(self, amount):
        """Reduce armor by amount, and remove the insect from its place if it
        has no armor remaining.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_armor(2)
        >>> test_insect.armor
        3
        """
        self.armor -= amount
        if self.armor <= 0:
            print('{0} ran out of armor and expired'.format(self))
            self.place.remove_insect(self)

    def action(self, colony):
        """The action performed each turn.

        colony -- The AntColony, used to access game state information.
        """

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.armor, self.place)


class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    watersafe = True

    def sting(self, ant):
        """Attack an Ant, reducing the Ant's armor by 1."""
        ant.reduce_armor(1)

    def move_to(self, place):
        """Move from the Bee's current Place to a new Place."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""    # ...or if there is an ant and its blocks_path attribute is True
        # Phase 3: Special handling for NinjaAnt
        return (self.place.ant is not None) and (self.place.ant.blocks_path)   

    def action(self, colony):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        colony -- The AntColony, used to access game state information.
        """
        if self.blocked():
            self.sting(self.place.ant)
        elif self.place is not colony.hive and self.armor > 0:
            self.move_to(self.place.exit)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    is_ant = True
    implemented = False  # Only implemented Ant classes should be instantiated
    damage = 0
    food_cost = 0           # default value of food_cost for an Ant
    blocks_path = True      # determines whether or not an ant will block a bee (default is True)
    container = False       # determines whether or not an ant can contain another ant (default is False)

    def __init__(self, armor=1):
        """Create an Ant with an armor quantity."""
        Insect.__init__(self, armor)

    def can_contain(self, other):
        """One ant can contain another if and only if 
        1) it is a container, 
        2) it doesn't contain another ant already, and 
        3) the other ant is not a container
        """
        return self.container and (self.ant is None) and (not other.container)


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    implemented = True
    food_cost = 2

    def action(self, colony):
        """Produce 1 additional food for the colony.

        colony -- The AntColony, used to access game state information.
        """
        colony.food += 1


def random_or_none(s):
    """Return a random element of sequence s, or return None if s is empty."""
    if s:
        return random.choice(s)


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    food_cost = 4           # default value of food_cost for a ThrowerAnt
    min_range = 0           # default value of min_range for a ThrowerAnt
    max_range = 10          # default value of max_range for a ThrowerAnt

    def nearest_bee(self, hive):
        """Return the nearest Bee in a Place that is not the Hive, connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        next_place = self.place                                             # save location of ThrowerAnt
        min_index, max_index = 0, 0                                         # index variables (tells us if we've reached the right bounds)                         
        while next_place is not hive:                                       # check each location that is not hive
            if min_index != self.min_range:                                 # check if min_range is not 0
                next_place = next_place.entrance                            # iterate (location moves to next entrance)
                min_index += 1                                              # increment index variables
                max_index += 1                                          
            elif max_index == self.max_range or next_place.bees != []:      # check if max_range has been reached or there is(/are) bee(s)
                return random_or_none(next_place.bees)                      # return a random bee or None at the location
            else:
                next_place = next_place.entrance                            # iterate (location moves to next entrance)
                max_index += 1                                              # increment index variable (max_index)

    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its armor."""
        if target is not None:
            target.reduce_armor(self.damage)

    def action(self, colony):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee(colony.hive))


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees:
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, colony):
        exits = [p for p in colony.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(colony.time, []):
            bee.move_to(random.choice(exits))


class AntColony:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    queen -- the place where the queen resides
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, strategy, hive, ant_types, create_places, food=2):
        """Create an AntColony for simulating a game.

        Arguments:
        strategy -- a function to deploy ants to places
        hive -- a Hive full of bees
        ant_types -- a list of ant constructors
        create_places -- a function that creates the set of places
        """
        self.time = 0
        self.food = food
        self.strategy = strategy
        self.hive = hive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.configure(hive, create_places)

    def configure(self, hive, create_places):
        """Configure the places in the colony."""
        self.queen = Place('AntQueen')
        self.places = OrderedDict()
        self.bee_entrances = []
        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = hive
                self.bee_entrances.append(place)
        register_place(self.hive, False)
        create_places(self.queen, register_place)

    def simulate(self):
        """Simulate an attack on the ant colony (i.e., play the game)."""
        while len(self.queen.bees) == 0 and len(self.bees) > 0:
            self.hive.strategy(self)    # Bees invade
            self.strategy(self)         # Ants deploy
            for ant in self.ants:       # Ants take actions
                if ant.armor > 0:
                    ant.action(self)
            for bee in self.bees:       # Bees take actions
                if bee.armor > 0:
                    bee.action(self)
            self.time += 1
        if len(self.queen.bees) > 0:
            print('The ant queen has perished. Please try again.')
        else:
            print('All bees are vanquished. You win!')

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        constructor = self.ant_types[ant_type_name]
        if self.food < constructor.food_cost:
            print('Not enough food remains to place ' + ant_type_name)
        else:
            self.places[place_name].add_insect(constructor())
            self.food -= constructor.food_cost

    def remove_ant(self, place_name):
        """Remove an Ant from the Colony."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]

def interactive_strategy(colony):
    """A strategy that starts an interactive session and lets the user make
    changes to the colony.

    For example, one might deploy a ThrowerAnt to the first tunnel by invoking
    colony.deploy_ant('tunnel_0_0', 'Thrower')
    """
    print('colony: ' + str(colony))
    msg = '<Control>-D (<Control>-Z <Enter> on Windows) completes a turn.\n'
    interact(msg)

def start_with_strategy(args, strategy):
    """Reads command-line arguments and starts a game with those options."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Ants vs. SomeBees")
    parser.add_argument('-f', '--full', action='store_true',
                        help='loads a full layout and assault plan')
    parser.add_argument('-w', '--water', action='store_true',
                        help='loads a full layout with water')
    parser.add_argument('-i', '--insane', action='store_true',
                        help='loads a difficult assault plan')
    parser.add_argument('--food', type=int,
                        help='number of food to start with', default=2)
    args = parser.parse_args()

    assault_plan = make_test_assault_plan()
    layout = test_layout
    food = args.food
    if args.full:
        assault_plan = make_full_assault_plan()
        layout = dry_layout
    if args.water:
        layout = wet_layout
    if args.insane:
        assault_plan = make_insane_assault_plan()
    hive = Hive(assault_plan)
    AntColony(strategy, hive, ant_types(), layout, food).simulate()


###########
# Layouts #
###########

def wet_layout(queen, register_place, length=8, tunnels=3, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)

def dry_layout(queen, register_place, length=8, tunnels=3):
    """Register dry tunnels."""
    wet_layout(queen, register_place, length, tunnels, 0)

def test_layout(queen, register_place, length=8):
    """Register a single dry tunnel."""
    dry_layout(queen, register_place, length, 1)


#################
# Assault Plans #
#################


class AssaultPlan(dict):
    """The Bees' plan of attack for the Colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def __init__(self, bee_armor=3):
        self.bee_armor = bee_armor

    def add_wave(self, time, count):
        """Add a wave at time with count Bees that have the specified armor."""
        bees = [Bee(self.bee_armor) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    @property
    def all_bees(self):
        """Place all Bees in the hive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]

def make_test_assault_plan():
    return AssaultPlan().add_wave(2, 1).add_wave(3, 1)

def make_full_assault_plan():
    plan = AssaultPlan().add_wave(2, 1)
    for time in range(3, 15, 2):
        plan.add_wave(time, 1)
    return plan.add_wave(15, 8)

def make_insane_assault_plan():
    plan = AssaultPlan(4).add_wave(1, 2)
    for time in range(3, 15):
        plan.add_wave(time, 1)
    return plan.add_wave(15, 20)

##############
# Extensions #
##############

class Water(Place):
    """Water is a place that can only hold 'watersafe' insects."""

    def add_insect(self, insect):
        """Add insect if it is watersafe, otherwise reduce its armor to 0."""
        print('added', insect, insect.watersafe)
        Place.add_insect(self, insect)                  # always add insect                         
        if not insect.watersafe:                        # test if the insect is not watersafe
            insect.reduce_armor(insect.armor)           # reduce armor to 0


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    food_cost = 4           # default value of food_cost for FireAnt
    implemented = True

    def reduce_armor(self, amount):
        place = self.place                      # save FireAnt's place before it dies
        Insect.reduce_armor(self, amount)       # call the original reduce armor function
        for bee in place.bees[:]:               # damage each bee in FireAnt's place; use copy of list
            bee.reduce_armor(self.damage)       # reduce the each bee's armor by damage


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 4 places away."""

    name = 'Long'
    food_cost = 3           # default value of food_cost for LongThrower
    min_range = 4           # min_range is 4 rather than 0
    implemented = True


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees less than 3 places away."""

    name = 'Short'
    food_cost = 3           # default value of food_cost for ShortThrower   
    max_range = 2           # max_range is 2 rather than 10
    implemented = True


class WallAnt(Ant):
    """WallAnt does nothing but has a large armor value."""

    name = 'Wall'
    food_cost = 4           # default value of food_cost for WallAnt
    implemented = True

    def __init__(self):
        """Create a WallAnt with an armor quantity of 4."""
        Ant.__init__(self, 4)                             

class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place."""

    name = 'Ninja'
    damage = 1
    blocks_path = False         # Bee's pass through
    food_cost = 6               # default value of food_cost for NinjaAnt
    implemented = True

    def action(self, colony):
        """Damage all bees in its place."""
        for bee in self.place.bees[:]:              # modifies the armor of each bee in place
            bee.reduce_armor(self.damage)           # reduces the armor by damage attribute 


class ScubaThrower(ThrowerAnt):
    """A ThrowerAnt that is waterproof"""
    name = 'Scuba'
    watersafe = True            # is waterproof
    food_cost = 5               # default value of food_cost for ScubaThrower
    implemented = True


class HungryAnt(Ant):
    """HungryAnt will take three turns to digest a Bee in its place.
    While digesting, the HungryAnt can't eat another Bee.
    """
    name = 'Hungry'
    time_to_digest = 3          # default value of time_to_digest
    food_cost = 4               # default value of food_cost for HungryAnt
    implemented = True

    def __init__(self, digesting=0):
        """Create a HungryAnt with an armor quantity of 1."""
        Ant.__init__(self, 1)  
        self.digesting = digesting      # set digesting initially to 0     

    def eat_bee(self, bee):
        bee.reduce_armor(bee.armor)     # kill the bee

    def action(self, colony):    
        if self.place.bees != [] or self.digesting != 0:            # check if there is a bee in the same place or if digestion has been started
            if self.digesting == 0:                                 # if digestion has started (and there's a bee)
                self.eat_bee(random_or_none(self.place.bees))       # kill the bee
                if self.time_to_digest != 0:                        # increment only if time_to_digest is not 0
                    self.digesting += 1    
            elif self.digesting < self.time_to_digest:              # increment if digestion has not finished
                self.digesting += 1
            else:
                self.digesting = 0                                  # reset if digestion is finished


class BodyguardAnt(Ant):
    """BodyguardAnt provides protection to other Ants."""
    name = 'Bodyguard'
    container = True                # can contain another ant
    food_cost = 4                   # default value of food_cost for BodyguardAnt
    implemented = True

    def __init__(self):
        """Create a BodyguardAnt with an armor quantity of 2."""
        Ant.__init__(self, 2)       
        self.ant = None  # The Ant hidden in this bodyguard

    def contain_ant(self, ant):
        self.ant = ant              # set BodyguardAnt's ant to whatever ant given

    def action(self, colony):
        if self.ant != None:            # check if there BodyguardAnt contains another ant
            self.ant.action(colony)     # call the other ant's action method


class QueenPlace(Place):
    """A place that represents both places in which the bees find the queen.

    (1) The original colony queen location at the end of all tunnels, and
    (2) The place in which the QueenAnt resides.
    """
    def __init__(self, colony_queen, ant_queen):
        self.colony_queen = colony_queen                # set colony_queen instance to the colony_queen parameter
        self.ant_queen = ant_queen                      # set ant_queen instance to the ant_queen parameter

    @property
    def bees(self):
        return self.colony_queen.bees + self.ant_queen.bees     # a list of all bees in the same place as colony_queen and ant_queen


class QueenAnt(ScubaThrower):  
    """The Queen of the colony.  The game is over if a bee enters her place."""

    name = 'Queen'
    food_cost = 6               # default value of food_cost for QueenAnt
    queens = []                 # keeps track of all queens created
    implemented = True

    def __init__(self):
        """Create a QueenAnt with an armor quantity of 1."""
        ScubaThrower.__init__(self, 1)           
        self.double_ants = []           # keeps track of ants whose damage has been doubled
        QueenAnt.queens.append(self)    # adds each queen to a list of queens

    def action(self, colony):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.

        Impostor queens do only one thing: reduce their own armor to 0.
        """
        if self is not QueenAnt.queens[0]:                          # checks if the current queen is imposter                                                
            self.reduce_armor(self.armor)                           # kill imposter
            return None                                             # break action

        colony.queen = QueenPlace(colony.queen, self.place)         # allows two places to satisfy the end game condition 
        ScubaThrower.action(self, colony)                           # do the action of a regular ScubaThrower

        enter, exit = self.place, self.place                                                                        # index variables
        while enter is not None:                                                                                    # check all places right of QueenAnt
            if (enter is not self.place) and (enter.ant != None) and (enter.ant not in self.double_ants):           # checks if ants exist in each place
                if enter.ant.container and (enter.ant.ant != None) and (enter.ant.ant not in self.double_ants):     # checks if one ant contains another
                    enter.ant.ant.damage *= 2                                                                       # buff damage of contained ant
                    self.double_ants.append(enter.ant.ant)                                                          # add the ant to double_ants
                enter.ant.damage *= 2                                                                               # buff damage of ant (may be container)
                self.double_ants.append(enter.ant)                                                                  # add the ant to double_ants
            enter = enter.entrance                                                                                  # move to next place
        while exit is not None:                                                                                     # check all places left of QueenAnt    
            if (exit is not self.place) and (exit.ant != None) and (exit.ant not in self.double_ants):              # (see previous loop comments)
                if exit.ant.container and (exit.ant.ant != None) and (exit.ant.ant not in self.double_ants):        # ''
                    exit.ant.ant.damage *= 2                                                                        # ''    
                    self.double_ants.append(exit.ant.ant)                                                           # ''    
                exit.ant.damage *= 2                                                                                # ''
                self.double_ants.append(exit.ant)                                                                   # ''
            exit = exit.exit                                                                                        # ''
        if self.place.ant.container and (self.place.ant.ant is self) and (self.place.ant not in self.double_ants):  # check if the queen is contained    
            self.place.ant.damage *= 2                                                                              # buff damage of container
            self.double_ants.append(self.place.ant)                                                                 # add container to double_ants


class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'Remover'
    implemented = True

    def __init__(self):
        Ant.__init__(self, 0)


##################
# Status Effects #
##################

def make_slow(action):
    """Return a new action method that calls action every other turn.

    action -- An action method of some Bee
    """
    def new_action(colony):                 # create a function that takes colony as an argument
        if colony.time % 2 == 0:            # check if colony.time is even
            action(colony)                  # if so, do the action
            return None                     # end new_action 
    return new_action                       # return the function

def make_stun(action):
    """Return a new action method that does nothing.

    action -- An action method of some Bee
    """
    def new_action(colony):                 # create a function that takes colony as an argument
        return None                         # end new_action
    return new_action                       # return the function

def apply_effect(effect, bee, duration):
    """Apply a status effect to a Bee that lasts for duration turns."""
    original = bee.action                   # save the original action
    def new_action(colony):                 # create a function that takes colony as an argument
        nonlocal duration                   # allow access to duration within new_action
        if duration != 0:                   # check if duration is not 0
            effect(original)(colony)        # if so, run the effect on original and run the resulting action
            duration -= 1                   # increment duration
            return None                     # end new_action
        else:
            original(colony)                # run the action taking in colony as an argument
            bee.action = original           # reset the action to the original value
            return None                     # end new_action
    bee.action = new_action                 # set the action to the function
   

class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    food_cost = 4               # default value of food_cost for SlowThrower    
    implemented = True

    def throw_at(self, target):
        if target:
            apply_effect(make_slow, target, 3)


class StunThrower(ThrowerAnt):
    """ThrowerAnt that causes Stun on Bees."""

    name = 'Stun'
    food_cost = 6               # default value of food_cost for StunThrower
    implemented = True

    def throw_at(self, target):
        if target:
            apply_effect(make_stun, target, 1)

@main
def run(*args):
    start_with_strategy(args, interactive_strategy)
