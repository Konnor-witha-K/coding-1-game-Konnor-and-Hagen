# Write your game here

import curses
import emoji

game_data = {
    "room_1_width": 8, 
    "room_1_height": 7, 
    'player': {"x": 4, "y": 6, "score": 0},
    'door_pos': {"x": 7, "y": 2},
    'collectibles': [
        {"x": 1, "y": 1, "collected": False},
    ],
    'obstacles': [
        {"x": 1, "y": 2},
        {"x": 4, "y": 1}
    ],

    'room1_walls': [
        {"x": 0, "y": 0},
        {"x": 1, "y": 0},
        {"x": 2, "y": 0},
        {"x": 3, "y": 0},
        {"x": 4, "y": 0},
        {"x": 5, "y": 0},
        {"x": 6, "y": 0},
        {"x": 7, "y": 0},
        {"x": 0, "y": 1},
        {"x": 0, "y": 2},
        {"x": 0, "y": 3},
        {"x": 0, "y": 4},
        {"x": 0, "y": 5},
        {"x": 0, "y": 6},
        {"x": 7, "y": 0},
        {"x": 7, "y": 1},
        {"x": 7, "y": 2},
        {"x": 7, "y": 3},
        {"x": 7, "y": 4},
        {"x": 7, "y": 5},
        {"x": 7, "y": 6}
    ],

    # ASCII Icons 
    'wizard': "\U0001F9D9", #🧙
    'obstacle': "\U0001FAA8 ", #🪨
    'door_key': emoji.emojize(":old_key: "), #🗝️
    'room_door': "\U0001F6AA", #🚪
    'empty': "  "
}

def draw_board(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, -1)

    stdscr.clear()
    for y in range(game_data['room_1_height']):
        row = ""
        for x in range(game_data['room_1_width']):
            # Player
            if x == game_data['player']['x'] and y == game_data['player']['y']:
                row += game_data['wizard']
            # Door
            elif x == game_data['door_pos']['x'] and y == game_data['door_pos']['y']:
                row += game_data['room_door']
            # Obstacles
            elif any(o['x'] == x and o['y'] == y for o in game_data['obstacles']):
                row += game_data['obstacle']
            # Walls
            elif any(p['x'] == x and p['y'] == y for p in game_data['room1_walls']):
                row += game_data['obstacle']
            # Key
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['door_key']
            else:
                row += game_data['empty']
        stdscr.addstr(y, 0, row, curses.color_pair(1))

    stdscr.addstr(game_data['room_1_height'] + 1, 0,
                  f"Moves Survived: {game_data['player']['score']}",
                  curses.color_pair(1))
    stdscr.addstr(game_data['room_1_height'] + 2, 0,
                  "Move with W/A/S/D, Q to quit",
                  curses.color_pair(1))
    stdscr.refresh()


def move_player(key):
    x = game_data['player']['x']
    y = game_data['player']['y']

    new_x, new_y = x, y
    key = key.lower()

    if key == "w" and y > 0:
        new_y -= 1
    elif key == "s" and y < game_data['room_1_height'] - 1:
        new_y += 1
    elif key == "a" and x > 0:
        new_x -= 1
    elif key == "d" and x < game_data['room_1_width'] - 1:
        new_x += 1
    else:
        return  # Invalid key or move off board

    # Update position and increment score
    game_data['player']['x'] = new_x
    game_data['player']['y'] = new_y
    game_data['player']['score'] += 1

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)

    draw_board(stdscr)

    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None

        if key:
            if key.lower() == "q":
                break

            move_player(key)
            draw_board(stdscr)

curses.wrapper(main)
# Good Luck!