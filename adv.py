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
traversal_path = []
room_path = []

accepted_direction = {'n', 's', 'w', 'e'}
direction = ["?"]
last_direction = '?'
direction_graph = {}

for room in world.rooms:
    dic = {}
    for e in world.rooms[room].get_exits():
        dic[e] = "?"
    direction_graph[room] = dic

recently_visited = set()
explored_rooms = set()

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
stack = Stack()
stack.push(player.current_room.id)

while len(explored_rooms) < len(room_graph):
    print(len(explored_rooms))

    direction_head = direction.pop()

    prev_room = player.current_room.id

    if direction_head in accepted_direction:
        player.travel(direction_head)
        traversal_path.append(direction_head)

        direction_graph[prev_room][direction_head] = player.current_room.id
        opposite = reverse(direction_head)
        direction_graph[player.current_room.id][opposite] = prev_room

    for exit in direction_graph[player.current_room.id]:

        if direction_graph[player.current_room.id][exit] not in recently_visited:
            if direction_graph[player.current_room.id][exit] == "?":
                direction = [exit]

    explored_rooms.add(player.current_room.id)

    path_back = traversal_path.copy()
    recently_visited = set()

    while len(path_back) > 0:
        forward_direction = path_back.pop()
        back_direction = reverse(forward_direction)

        avoid = False

        recently_visited.add(player.current_room.id)

        for move in direction_graph[player.current_room.id]:

            if direction_graph[player.current_room.id][move] == "?":
                avoid = True
                direction = [move]

        if avoid == False:

            if back_direction in accepted_direction:

                player.travel(back_direction)
                traversal_path.append(back_direction)



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
