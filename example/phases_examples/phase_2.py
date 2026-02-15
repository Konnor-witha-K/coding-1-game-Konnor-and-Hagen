# The goals for this phase include:
#  - Pick out some icons for your game
#  - Establish a starting position for each icon
#  - Pick a size for your playing space
#  - Print your playing space with starting position of each icon

# To make this work, you may have to type this into the terminal --> pip install curses
import curses

# Icons
# To find more icons go to https://emojipedia.org/
turtle = "\U0001F422"
eagle = "\U0001F985"
obstacle = "\U0001FAA8 "
leaf = "\U0001F343"
empty = "  "  # two spaces for alignment

# Board dimensions
width, height = 5, 5

# Icon positions
positions = {
    'player': (0, 0),
    'eagle': (4, 4),
    'obstacle': [(1, 2), (3, 1)],
    'leaf': [(2, 1)],
}

def draw_board(stdscr):
    # Initialize color support
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)

    stdscr.clear()
    for y in range(height):
        row = ""
        for x in range(width):
            if (x, y) == positions['player']:
                row += turtle
            elif (x, y) == positions['eagle']:
                row += eagle
            elif (x, y) in positions['obstacle']:
                row += obstacle
            elif (x, y) in positions['leaf']:
                row += leaf
            else:
                row += empty
        stdscr.addstr(y, 0, row, curses.color_pair(1))

    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(draw_board)
