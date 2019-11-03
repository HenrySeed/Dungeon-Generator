from random import randint 

def drawPixel(win, x, y, val):
    win.addstr(y, x, val)



class Dungeon():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.fill = "#"
        self.empty = " "

        self.map = []
        for i in range(height):
            self.map.append([self.fill] * width)

        self.rendered_map = []
        for i in range(height):
            self.rendered_map.append([self.empty] * width)

        self.make_dungeon()
        self.make_dungeon()

        self.stats = ""


    ''' checks if a given point collides with the map'''
    def check_collision(self, pos):
        new_pos = [pos[0], pos[1]-2]
        # self.stats = "Tile = \"{}\" at pos {} ".format(self.get_point(new_pos), new_pos)
        return self.get_point(new_pos) == self.fill


    '''Checks the dungeon for validity, eg: blocks out of bounds'''
    def is_valid(self):

        for pix in self.map[0]:
            if pix != self.fill:
                return False
                
        for pix in self.map[-1]:
            if pix != self.fill:
                return False

        for row in range(self.height-2):
            for col in [0, -1]:
                if self.map[row+1][col] != self.fill:
                    return False

        return True


    '''returns true if the given pos falls on the map as a vertical wall'''
    def is_vert_wall(self, x, y):
        neighbours = self.get_neighbours([x, y])
        if (neighbours[3] == ' ' or neighbours[5] == " ") and (neighbours[1] == '#' and neighbours[7] == "#"):
            return True
        else:
            return False


    '''returns true if the given pos falls on the map as a horizontal wall'''
    def is_horoz_wall(self, x, y):
        neighbours = self.get_neighbours([x, y])
        if (neighbours[1] == ' ' or neighbours[7] == " ") and (neighbours[3] == '#' and neighbours[5] == "#"):
            return True
        else:
            return False


    '''returns true if the given pos falls on the map as a corner wall'''
    def is_corner(self, x, y):
        neighbours = self.get_neighbours([x, y])
        return "#" in neighbours and " " in neighbours


    '''returns true if the given pos falls on the map as next to a wall, horozontal or vertical'''
    def is_on_wall(self, x, y):
        neighbours = self.get_neighbours([x, y], self.rendered_map)
        if ('|' in neighbours or '-' in neighbours) and self.get_point([x, y]) == self.empty:
            return True
        else:
            return False


    '''Generated a dungeon, checks it for validity and renders it out with vertical and horozontal walls'''
    def make_dungeon(self):
        try:
            self.gen_dungeon()
            crashed = False
        except:
            crashed = True

        while not self.is_valid() or crashed:
            try:
                self.gen_dungeon()
                crashed = False
            except:
                crashed = True

        self.rendered_map = []
        for i in range(self.height):
            self.rendered_map.append([self.empty] * self.width)

        for row in range(self.height):
            for col in range(self.width):
                # renders points to self.rendered_map
                if self.map[row][col] == "#":
                    if self.is_vert_wall(col, row):
                        self.rendered_map[row][col] = "|"

                    elif self.is_horoz_wall(col, row):
                        self.rendered_map[row][col] = "-"

                    elif self.is_corner(col, row):
                        self.rendered_map[row][col] = "+"

                    # self.rendered_map[row][col] = "#"
                
                elif self.map[row][col] == " ":
                    self.rendered_map[row][col] = " "

                else:
                    self.rendered_map[row][col] = self.map[row][col]


    ''' Generate a dungeon, filling the self.map array'''
    def gen_dungeon(self):
        # reset map
        self.map = []
        for i in range(self.height):
            self.map.append([self.fill] * self.width)
        # start pos
        moves = 10
        direcs = [0, 1, 2, 3]

        for direc in direcs:
            pos = [int(self.width/2), int(self.height/2)]
            # draw a point where pos is currently
            self.drawPoint(pos[0], pos[1], self.empty)
            old_direc = 0
                
            for move in range(moves):
                # choose a direction and move randint(3, 10), making a corridor
                # numbers for N,E,S,W
                
                while direc == old_direc or old_direc % 2 == direc % 2:
                    direc = direcs[randint(0, 3)]

                pos = self.gen_corridor(pos, direc)
                pos = self.gen_room(pos)

                old_direc = direc
                direc = direcs[randint(0, 3)]


    '''Generate a Corridor from the given pos and direction'''
    def gen_corridor(self, pos, direc):

        if direc == 0 or direc == 2: length = randint(5, 8) # vertical paths are shorted due to ascii
        if direc == 1 or direc == 3: length = randint(9, 16)

        for pix in range(length):
            if direc == 0: pos = [pos[0], pos[1] - 1]
            if direc == 1: pos = [pos[0] + 1, pos[1]]
            if direc == 2: pos = [pos[0], pos[1] + 1]
            if direc == 3: pos = [pos[0] - 1, pos[1]]

            # draw a point where pos is currently
            self.drawPoint(pos[0], pos[1], self.empty)

        return pos


    '''Generate a room from the given position'''
    def gen_room(self, pos):
        width = randint(5, 9)
        height = randint(3, 6)

        center = [pos[0]-randint(1, width-1), pos[1]-randint(1, height-1)]

        for row in range(height):
            for col in range(width):
                self.drawPoint(center[0]+col, center[1]+row, self.empty)

        # self.gen_items(center, [center[0]+width, center[1]+height])

        return pos


    ''' Adds items to the Map in the given room'''
    def gen_items(self, top_leftPos, bottom_rightPos):
        min_items = 1
        max_items = 4
        possible_locations = []

        # find all suitable positions in the given room
        for row in range(top_leftPos[1], bottom_rightPos[1]):
            for col in range(top_leftPos[0], bottom_rightPos[0]):
                # if self.is_on_wall(col, row):
                possible_locations.append([col, row])

        num_items = randint(min_items, max_items)
        if len(possible_locations) <= num_items:
            num_items = len(possible_locations) - 1

        self.stats = possible_locations

        for item in range(0, num_items):
            # choose random coords along a wall
            loc = possible_locations[item]
            # possible_locations.remove(loc)
            self.drawPoint(loc[1], loc[0], "&")
        

    ''' makes a point on self.map'''
    def drawPoint(self, x, y, val):
        self.map[y][x] = val


    def get_point(self, pos, on_map=404):
        if on_map == 404: on_map = self.map
        try: 
            return on_map[pos[1]][pos[0]]
        except:
            return ""


    '''Checks if the point pos in self.map has val as a neighbour'''
    def get_neighbours(self, pos, on_map=404):
        if on_map == 404: on_map = self.map
        neighbours = []
        neighbours.append(self.get_point([pos[0]-1, pos[1]-1], on_map))
        neighbours.append(self.get_point([pos[0], pos[1]-1], on_map))
        neighbours.append(self.get_point([pos[0]+1, pos[1]-1], on_map))

        neighbours.append(self.get_point([pos[0]-1, pos[1]], on_map))
        neighbours.append(self.get_point([pos[0], pos[1]], on_map))
        neighbours.append(self.get_point([pos[0]+1, pos[1]], on_map))

        neighbours.append(self.get_point([pos[0]-1, pos[1]+1], on_map))
        neighbours.append(self.get_point([pos[0], pos[1]+1], on_map))
        neighbours.append(self.get_point([pos[0]+1, pos[1]+1], on_map))

        return neighbours


    '''Draws the rendered map with outline'''
    def draw(self, win):
        # draws stats about the current map on the given win
        win.addstr(1, 0, 'Dungeon: {}'.format(self.stats))

        # draws the rendered map on the given win
        x = 0
        y = 2
        for row in range(0, len(self.map)):
            for col in range(0, len(self.map[row])):
                if self.rendered_map[row][col] != ' ':
                    drawPixel(win, col+x, row+y, self.rendered_map[row][col])