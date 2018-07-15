import curses
from player import *
from dungeonGen import *
import os


def main(win):
    # Uses default terminal colours
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, i, -1);

    # Set up new player

    # sets sursor to invisible
    curses.curs_set(0)

    win.nodelay(True)
    key = ""
    win.clear() 

    # sets the demo so that the dungeon is the size of the given terminal
    rows, columns = os.popen('stty size', 'r').read().split() 
    width = int(columns) - 3
    height = int(rows) - 3

    dun = Dungeon(width, height)
    player = Player(int(width/2), int(height/2)+2)
    objects = [dun]


    win.addstr(key) 
    player.draw(win) 
    dun.draw(win) 
    win.addstr(2, 0, "Key: ") 

    while 1:          
        try:                 
            key = win.getkey() 

            if key in ['w', 's', 'a', 'd', 'W', 'A', 'S', 'D', ' ']:
                player.update(key, objects)

            if key == "q":
                return

            if key == "r":
                dun.make_dungeon()
                player.reset()  

            if key == "f":
                player.attack(win)       

            win.clear()  

            player.draw(win)
            dun.draw(win)
            win.addstr(2, 0, "Key: " + str(key))
            

            if key == os.linesep:
                break         

        except Exception as e:
            # No input   
            pass         

curses.wrapper(main)