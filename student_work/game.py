# Write your game here

import curses
import random
import time
# may have type to install emojis with --> pip install emoji
import emoji

game_data = {
    "room_1_width": 8, 
    "room_1_height": 7, 
    'player': {"x": 4, "y": 6, "score": 0, "door1_unlocked": False},
    'enemy': {"x": 3, "y": 4},
    'door1_pos': [
        {"x": 7, "y": 2}
    ],
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
        {"x": 7, "y": 3},
        {"x": 7, "y": 4},
        {"x": 7, "y": 5},
        {"x": 7, "y": 6}
    ],

    # ASCII Icons 
    'wizard': emoji.emojize(":mage:"), #
    'obstacle': "\U0001FAA8 ", #🪨
    'door_key': emoji.emojize(":old_key: "), #🗝️
    'room_door': "\U0001F6AA", #🚪
    'cave_troll': "\U0001F9CC ", #🧌
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
            # Troll
            elif x == game_data['enemy']['x'] and y == game_data['enemy']['y']: 
                row += game_data['cave_troll']
            # Door
            elif any(o['x'] == x and o['y'] == y for o in game_data['door1_pos']):
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
                  f"Total Moves: {game_data['player']['score']}",
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
    
    # Check obstacle collision
    if any(o["x"] == new_x and o["y"] == new_y for o in game_data['obstacles']):
        return False
    # Wall Collision
    if any(o["x"] == new_x and o["y"] == new_y for o in game_data['room1_walls']):
        return False
    # Door Collision
    if game_data['player']['door1_unlocked'] == False:
        if any(o["x"] == new_x and o["y"] == new_y for o in game_data['door1_pos']):
            return False
    
    # Update position and increment score
    game_data['player']['x'] = new_x
    game_data['player']['y'] = new_y
    game_data['player']['score'] += 1

def check_collectibles():
    for c in game_data['collectibles']:
        if (not c["collected"] and
            game_data['player']["x"] == c["x"] and
            game_data['player']["y"] == c["y"]):

            c["collected"] = True
            game_data['player']['door1_unlocked'] = True

def move_troll():
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    random.shuffle(directions)
    ex, ey = game_data['enemy']['x'], game_data['enemy']['y']

    valid_moves = []

    for dx, dy in directions:
        new_x = ex + dx
        new_y = ey + dy
        # Inside board?
        if not (0 <= new_x < game_data['room_1_width'] and
                0 <= new_y < game_data['room_1_height']):
            continue        
        # Wall collision?
        if any(o["x"] == new_x and o["y"] == new_y
               for o in game_data['room1_walls']):
            continue
        # Door collision?
        if any(o["x"] == new_x and o["y"] == new_y
               for o in game_data['door1_pos']):
            continue
        # Rock collision?
        if any(o["x"] == new_x and o["y"] == new_y
               for o in game_data['obstacles']):
            continue

        valid_moves.append((new_x, new_y))

    # If there are valid moves, pick one
    if valid_moves:
        new_x, new_y = random.choice(valid_moves)
        game_data['enemy']["x"] = new_x
        game_data['enemy']["y"] = new_y

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

            move_troll()
            check_collectibles()

            draw_board(stdscr)
            time.sleep(0.2)  # Add a small delay for smoother gameplay

curses.wrapper(main)
# Good Luck!