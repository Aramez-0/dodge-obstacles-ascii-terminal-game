import random
import os

# obstacles are being a dick right now

board_width = 25
board_length = 10
obstacle_size = [8, 9]
obstacle_gaps = 2
obstacle_frequency = [3, 5]
obstacles = []
prints_without_obstacles = 0
player_lives = 1

class player:

	x = 0
	y = 0
	lives = player_lives
	
	def lose_lives(self, amount = 1) -> str:
		self.lives -= 1
		if self.lives <= 0:
			return "dead\n"
		else:
			return "hit\n"

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

def print_board(current_player):
	os.system('cls' if os.name == 'nt' else 'clear')
	global prints_without_obstacles
	global obstacles
	message = ""
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
			ob_placed = False
			for j in obstacles:
				if j["pos"] == i and not k in j["gaps"]:
					board += "#"
					ob_placed = True
			if not ob_placed:
				board += "/"
			if k == current_player.x and i == current_player.y:
				if ob_placed:
					message += current_player.lose_lives()
				board += "X"
		board += "\n"
	for i in range(board_width):
		board += "#"
	print(board)
	print(message)
	for i in obstacles:
		i["pos"] += 1
		if i["pos"] > board_width:
			obstacles.remove(i)
	player_input = input("Input: ")
	if player_input == "s" and current_player.x < board_length:
		current_player.x += 1
	elif player_input == "w" and current_player.x >= 0:
		current_player.x -= 1
	elif player_input == "a" and current_player.y < board_width:
		current_player.y -= 1
	elif player_input == "d" and current_player.y >= 0:
		current_player.y += 1
	elif player_input == "exit" or player_input == "quit" or player_input == "q":
		exit()
	if current_player.lives <= 0:
		start_game()
	print_board(current_player)

def clear_board():
	prints_without_obstacles = 0
	obstacles.clear()

def start_game():
	clear_board()
	current_player = player()
	print_board(current_player)

start_game()