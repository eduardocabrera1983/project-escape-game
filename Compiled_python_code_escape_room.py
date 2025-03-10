# ASCII Art Game Title
print("""
#######                                       ######
#        ####   ####    ##   #####  ######    #     #  ####   ####  #    #
#       #      #    #  #  #  #    # #         #     # #    # #    # ##  ##
#####    ####  #      #    # #    # #####     ######  #    # #    # # ## #
#            # #      ###### #####  #         #   #   #    # #    # #    #
#       #    # #    # #    # #      #         #    #  #    # #    # #    #
#######  ####   ####  #    # #      ######    #     #  ####   ####  #    #
""")

# Define rooms and items
couch = {"name": "couch", "type": "furniture"}
queen_bed = {"name": "queen bed", "type": "furniture"}
double_bed = {"name": "double bed", "type": "furniture"}
dresser = {"name": "dresser", "type": "furniture"}
piano = {"name": "piano", "type": "furniture"}

door_a = {"name": "door a", "type": "door"}
door_b = {"name": "door b", "type": "door"}
door_c = {"name": "door c", "type": "door"}
door_d = {"name": "door d", "type": "door"}

key_a = {"name": "key for door a", "type": "key", "target": door_a}
key_b = {"name": "key for door b", "type": "key", "target": door_b}
key_c = {"name": "key for door c", "type": "key", "target": door_c}
key_d = {"name": "key for door d", "type": "key", "target": door_d}

game_room = {"name": "game room", "type": "room"}
bed_room1 = {"name": "bedroom 1", "type": "room"}
bed_room2 = {"name": "bedroom 2", "type": "room"}
outside = {"name": "outside"}

all_rooms = [game_room, bed_room1, bed_room2, outside]
all_doors = [door_a, door_b, door_c, door_d]

# Define item-room relationships
object_relations = {
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "queen bed": [key_b],
    "double bed": [key_c],
    "dresser": [key_d],
    "bedroom 1": [door_a, door_b, door_c, queen_bed],
    "bedroom 2": [door_b],
    "outside": [door_d],
    "door a": [game_room, bed_room1],
    "door b": [bed_room1, outside],
    "door c": [bed_room1, outside]
}

# Initial game state
INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

def checkInventory():
    """Check and display collected keys."""
    if len(game_state['keys_collected']) != 0:
        print("You check your pockets. You have the following keys:")
        for item in game_state['keys_collected']:
            print(item['name'])
    else:
        print("Nothing in your pockets.")

def linebreak():
    """Print a line break for readability."""
    print("\n\n")

def start_game():
    """Start the game with an introductory message."""
    print("You wake up on a couch and find yourself in a strange house with no windows.")
    print("You don't remember why you are here. You feel some unknown danger approaching.")
    print("You must get out of the house, NOW!\n")
    play_room(game_state["current_room"])

def play_room(room):
    """Handle interactions in the current room."""
    game_state["current_room"] = room

    if room == game_state["target_room"]:
        print("Congrats! You escaped the house!")
        return

    print(f"You are now in {room['name']}")
    
    intended_action = input("What would you like to do? Type 'explore', 'examine' or 'inventory': ").strip().lower()
    
    if intended_action == "explore":
        explore_room(room)
        play_room(room)
    elif intended_action == "examine":
        examine_item(input("What would you like to examine? ").strip().lower())
    elif intended_action == "inventory":
        checkInventory()
        play_room(room)
    else:
        print("Not sure what you mean. Type 'explore', 'examine', or 'inventory'.")
        play_room(room)
    
    linebreak()

def explore_room(room):
    """List all items in the room."""
    explore_message = f"You explore the room. This is {room['name']}. You find "
    explore_message += ", ".join([item["name"] for item in object_relations[room["name"]]]) + "."
    print(explore_message)

def get_next_room_of_door(door, current_room):
    """Find the room on the other side of a door."""
    connected_rooms = object_relations[door["name"]]
    return connected_rooms[1] if connected_rooms[0] == current_room else connected_rooms[0]

def examine_item(item_name):
    """Examine an item and take action if needed."""
    current_room = game_state["current_room"]
    next_room = None
    output = None

    for item in object_relations[current_room["name"]]:
        if item["name"] == item_name:
            output = f"You examine {item_name}. "
            if item["type"] == "door":
                if any(key["target"] == item for key in game_state["keys_collected"]):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if item_name in object_relations and object_relations[item_name]:
                    found_item = object_relations[item_name].pop()
                    game_state["keys_collected"].append(found_item)
                    output += f"You find {found_item['name']}."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if output is None:
        print("The item you requested is not found in the current room.")

    if next_room and input("Do you want to go to the next room? Enter 'yes' or 'no': ").strip().lower() == 'yes':
        play_room(next_room)
    else:
        play_room(current_room)

def living_room():
    """Handle the living room interaction."""
    print("""Welcome to the living room.
    There is a dining table and three boxes: blue, yellow, and red.
    Choose a color.""")

    color = input().strip().lower()

    if color == "yellow":
        print("The door D is revealed.")

        if any(key["name"] == "key for door d" for key in game_state['keys_collected']):
            print("Congrats, you can open Door D!")
        else:
            print("You have missed Key D. You have to go back.")

# Initialize game state and start game
game_state = INIT_GAME_STATE.copy()
start_game()
