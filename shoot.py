import random
import math

# Set map extents
BOUNDARY_SW = [100.0, 100.0]
BOUNDARY_NE = [200.0, 200.0]

# The game board
class Game:
    def __init__(self):
        self.player_turn = 0
        self.round_e = 0.0
        self.round_n = 0.0
        self.round_el = 0.0
        self.players = []


# Define a player
class Player:
    def __init__(self):
        self.position_e = random.randrange(BOUNDARY_SW[0], BOUNDARY_NE[0], 1)
        self.position_n = random.randrange(BOUNDARY_SW[1], BOUNDARY_NE[1], 1)
        self.position_el = 0.0


# Do the math
class CalculateCoordinates:
    def __init__(self):
        self.round_val = 4
        self.working_coords = []
        self.bearing = 0.0
        self.distance_2d = 0.0
        self.distance_3d = 0.0
        self.delta_e = 0.0
        self.delta_n = 0.0
        self.delta_el = 0.0

    def seek_deltas(self):
        # difference between both sets of coordinates.
        if len(self.working_coords) > 1:
            self.delta_e = self.working_coords[1][0] - self.working_coords[0][0]
            self.delta_n = self.working_coords[1][1] - self.working_coords[0][1]
            self.delta_el = self.working_coords[1][2] - self.working_coords[0][2]
        else:
            quit("Not enough coords dude.")

    def create_deltas(self):
        # Creates deltas from bearing and distance
        self.delta_e = self.distance_2d * (math.sin(math.radians(self.bearing)))
        self.delta_n = self.distance_2d * (math.cos(math.radians(self.bearing)))

    def create_coordinates(self):
        # Create new coords from deltas.
        new_coord = [self.working_coords[0][0] + self.delta_e,\
                  self.working_coords[0][1] + self.delta_n,\
                  self.working_coords[0][2]]
        self.working_coords.append(new_coord)

    def seek_bearing(self):
        # A great big switch statement to determine the correct direction.
        if self.delta_e == 0 and self.delta_n > 0:
            self.bearing = 0.0
        elif self.delta_e == 0 and self.delta_n < 0:
            self.bearing = 180.0
        elif self.delta_e > 0 and self.delta_n == 0:
            self.bearing = 90.0
        elif self.delta_e < 0 and self.delta_n == 0:
            self.bearing = 270.0

        # Check for 45 degree variations.
        elif abs(self.delta_e) == abs(self.delta_n):
            if self.delta_e > 0 and self.delta_n > 0:
                self.bearing = 45.0
            elif self.delta_e > 0 > self.delta_n:
                self.bearing = 135.0
            elif self.delta_e < 0 and self.delta_n < 0:
                self.bearing = 225.0
            elif self.delta_n > 0 > self.delta_e:
                self.bearing = 315.0

        # Compute it out.
        elif self.delta_e > 0:
            self.bearing = math.degrees(math.atan(self.delta_e / self.delta_n))
        elif self.delta_e < 0 and self.delta_n < 0:
            self.bearing = math.degrees(math.atan(self.delta_e / self.delta_n)) + 180
        elif self.delta_n > 0 > self.delta_e:
            self.bearing = math.degrees(math.atan(self.delta_e / self.delta_n)) + 360

        # The final piece.
        if self.bearing < 0:
            self.bearing += 180

    def dist_2d(self):
        # Determine the distance. (2D)
        self.distance_2d = math.sqrt((self.delta_e ** 2 + self.delta_n ** 2))

    def dist_3d(self):
        # Determine the distance. (3D)
        self.distance_3d = math.sqrt(self.delta_e ** 2 + self.delta_n ** 2 + self.delta_el ** 2)

    def list_coords(self):
        # Send back the values.
        for i in self.working_coords:
            print("E: {e} N: {n} El: {el} ".format(
                e=round(i[0], self.round_val),
                n=round(i[1], self.round_val),
                el=round(i[2], self.round_val),
            ))

    def bdc(self):
        # Return bearing and distance derived from two sets of coordinates.
        self.seek_deltas()
        self.seek_bearing()
        self.dist_2d()
        self.dist_3d()

    def cbd(self):
        self.create_deltas()
        self.create_coordinates()


new_game = Game()
calcs = CalculateCoordinates()
number_players = 2
play_away = True

while number_players:
    new_game.players.append(Player())
    number_players -= 1

while play_away:
    calcs.working_coords = []
    player_now = new_game.player_turn
    if player_now == 0:
        player_next = player_now + 1
    else:
        player_next = player_now - 1

    print("player turn " + str(new_game.player_turn + 1))
    # new_game.player_turn = player_next
    player_now_coords = []
    player_next_coords = []

    player_now_coords.append(new_game.players[player_now].position_e)
    player_now_coords.append(new_game.players[player_now].position_n)
    player_now_coords.append(new_game.players[player_now].position_el)
    # print(player_now_coords)

    # Calculate round fall.
    fire_bearing = float(input("fire at bearing: "))
    fire_range = float(input("range: "))
    calcs.distance_2d = fire_range
    calcs.bearing = fire_bearing

    calcs.working_coords.append(player_now_coords)
    calcs.cbd()
    round_coords = [calcs.working_coords[1][0], calcs.working_coords[1][1], calcs.working_coords[1][2]]

    # Calculate bearing distance to target
    calcs.working_coords = []
    calcs.working_coords.append(round_coords)

    player_next_coords.append(new_game.players[player_next].position_e)
    player_next_coords.append(new_game.players[player_next].position_n)
    player_next_coords.append(new_game.players[player_next].position_el)

    calcs.working_coords.append(player_next_coords)

    calcs.bdc()

    print("round landed: ")
    print(str(round(calcs.distance_2d, 3)) + "m from target")
    print("at bearing " + str(round(calcs.bearing, 2)))

    if calcs.distance_2d <= 10.0:
        quit("CONGRATS YOU WON!")
    else:
        new_game.player_turn = player_next
