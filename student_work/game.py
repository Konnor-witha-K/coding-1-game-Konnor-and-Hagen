# Write your game here

import curses

game_data = {
    "room_1_width": 8, 
    "room_1_height": 7, 
    'player': {"x": 4, "y": 6},
    'door_pos': {"x": 7, "y": 2},
    'collectibles': [
        {"x": 1, "y": 1, "collected": False},
    ],
    'obstacles': [
        {"x": 1, "y": 2},
        {"x": 4, "y": 1}
    ],

    'walls': [
        {"x": 0, "y": 0},
        {"x": 1, "y": 0},
        {"x": 2, "y": 0},
    ],

    # ASCII Icons 
    'wizard': "\U0001F9D9", #🧙
    'obstacle': "\U0001FAA8 ", #🪨
    'door_key': "\U0001F5DD", #🗝️
    'room_door': "\U0001F6AA", #🚪
    'room_wall': "\U0001F9F1", #🧱
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
            elif any(p['x'] == x and p['y'] == y for p in game_data['walls']):
                row += game_data['room_wall']
            # Key
            elif any(c['x'] == x and c['y'] == y and not c['collected'] for c in game_data['collectibles']):
                row += game_data['door_key']
            else:
                row += game_data['empty']
        stdscr.addstr(y, 0, row, curses.color_pair(1))

    stdscr.refresh()
    stdscr.getkey()  # pause so player can see board



curses.wrapper(draw_board)
# Good Luck!