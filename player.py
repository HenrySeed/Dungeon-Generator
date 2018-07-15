import curses
import time

class Cursor():
    def __init__(self):
        self.visible = False
        self.sprite = '+'
        self.timer = 5
        self.x = -1
        self.y = -1

        # max distance cursor can be from player
        self.dist = 1


    def update(self, key, player):
        if key == " ":
            if self.visible:
                self.visible = False
            else:
                self.visible = True

        if self.visible:
            new_x = self.x
            new_y = self.y

            if key == 'w': new_y -= 1
            if key == 's': new_y += 1
            if key == 'a': new_x -= 1
            if key == 'd': new_x += 1

            if new_x <= self.dist and new_x >= (-1*self.dist) and new_y <= self.dist and new_y >= (-1*self.dist):
                self.x = new_x
                self.y = new_y


    def draw(self, win, player):
        if self.visible:
            win.addstr(player.y + self.y, player.x + self.x, self.sprite, curses.color_pair(9))


class Player():
    def __init__(self, x=40, y=10):
        self.origional_x = x
        self.origional_y = y
        self.x = x;
        self.y = y;

        self.v_speed = 1
        self.h_speed = 1

        self.sprite = "@"

        self.direc = 0

        self.cursor = Cursor()


    def update(self, key, objects):

        new_pos = [self.x, self.y]
        new_direc = self.direc

        if not self.cursor.visible:
            if key == 'w':
                new_pos = [self.x, self.y - self.v_speed]
                new_direc = 0
            if key == 's':
                new_pos = [self.x, self.y + self.v_speed]
                new_direc = 2
            if key == 'a':
                new_pos = [self.x - self.h_speed, self.y]
                new_direc = 3
            if key == 'd':
                new_pos = [self.x + self.h_speed, self.y]
                new_direc = 1          

        collided = False
        for obj in objects:
            try:
                if obj.check_collision(new_pos):
                    # the player has collided
                    collided = True
                    break
            except:
                pass

        self.cursor.update(key, self)

        if not collided:
            self.direc = new_direc
            self.x = new_pos[0]
            self.y = new_pos[1]


    def draw(self, win):

        self.cursor.draw(win, self)

        win.addstr(0, 0, 'Player x: {}  y: {}  Direction: {}'.format(self.x, self.y, self.direc))
        win.addstr(self.y, self.x, self.sprite, curses.color_pair(10))

    def reset(self):
        self.x = self.origional_x;
        self.y = self.origional_y;