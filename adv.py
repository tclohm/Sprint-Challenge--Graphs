from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# MARK -- My import
from util import Stack

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

def reverse(direction):
    if direction is 'n':
        return 's'
    if direction is 's':
        return 'n'
    if direction is 'w':
        return 'e'
    if direction is 'e':
        return 'w'

# DEPTH First Traversal
def crawl():
    """
    print each node in depth order starting from our initial room
    """

    # stack will hold the path
    stack = Stack()
    # return our path
    moves = []
    # visited rooms, and determine if we hit a dead end
    visited = set()

    stack.push(player.current_room.id)

    while len(visited) < len(room_graph):
        # peek at room id, stack is holding path so we can't pop it. Thanks https://stackoverflow.com/questions/46801747/peek-stack-in-python-3
        room_id = stack.peek()

        visited.add(room_id)

        # grab the rooms details
        current_room = room_graph[room_id]
        print(current_room)
        
        # neighboring rooms
        neighboring_rooms = current_room[1]
        print(neighboring_rooms)

        # track if rooms have not been visited
        unknown = []

        # store the undiscovered rooms, got a little hacky using the items()
        for direction, neighbor_id in neighboring_rooms.items():
            print("has neighbor", neighbor_id, "been visited?")
            if neighbor_id not in visited:
                print("Not visited appending to unknown:", neighbor_id)
                unknown.append(neighbor_id)

        # move to the next room
        print("length of unknown:", len(unknown))
        if len(unknown) > 0:
            # grab next room
            next_room = unknown[0]
            print("next room in unknown being pushed to stack", next_room)
            stack.push(next_room)
        else:
            # remove current
            go_back = stack.pop()
            print("we've reached a deadend, popping off of stack:", go_back)
            next_room = stack.peek()

        # check out the rooms, if the neighbor_id is the next room append it to moves
        for direction, neighbor_id in neighboring_rooms.items():
            print("checking to see if neighbor_id", neighbor_id, "is equal too next_room", next_room)
            if neighbor_id == next_room:
                print("neigbor and next_room match! appending to moves", direction)
                moves.append(direction)

    return moves

traversal_path = crawl()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
