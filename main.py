import random
import os

# obstacles are being a dick right now

board_width = 25
board_length = 10
obstacle_size = [8, 9]
obstacle_gaps = 2
obstacle_frequency = [3, 5]
obstacles = []
player = {"x": 0, "y": 0}
prints_without_obstacles = 0

def generate_obstacle():
	obstacle = {
		"pos": 0,
		"size": random.choice(obstacle_size),
		"gaps": []
	}
	for i in range(obstacle_gaps):
		gap_num = random.randint(0, obstacle["size"])
		while gap_num in obstacle["gaps"]:
			gap_num = random.randint(0, obstacle["size"])
		obstacle["gaps"].append(gap_num)
	obstacles.append(obstacle)

def print_board():
	os.system('cls' if os.name == 'nt' else 'clear')
	global prints_without_obstacles
	global player
	global obstacles
	if prints_without_obstacles > obstacle_frequency[0] and prints_without_obstacles < obstacle_frequency[1]:
		if random.randint(0, 2) == 0:
			generate_obstacle()
			prints_without_obstacles = 0
	elif prints_without_obstacles == obstacle_frequency[1]:
		generate_obstacle()
		prints_without_obstacles = 0
	else:
		prints_without_obstacles += 1
	board = ""
	for i in range(board_width):
		board += "#"
	board += "\n"
	for k in range(board_length):
		for i in range(board_width):
			for j in obstacles:
				if j["pos"] == i and not i in j["gaps"]:
					board += "#"
			if k == player["x"] and i == player["y"]:
				board += "X"
		board += "\n"
	for i in range(board_width):
		board += "#"
	print(board)
	player_input = input("Input: ")
	if player_input == "s" and player["x"] < board_length:
		player["x"] += 1
	elif player_input == "w" and player["x"] >= 0:
		player["x"] -= 1
	elif player_input == "a" and player["y"] < board_width:
		player["y"] += 1
	elif player_input == "d" and player["y"] >= board_length:
		player["y"] -= 1
	elif player_input == "exit" or player_input == "quit" or player_input == "q":
		exit()
	for i in obstacles:
		i["pos"] += 1
		if i["pos"] > board_width:
			obstacles.remove(i)
	print_board()
print_board()