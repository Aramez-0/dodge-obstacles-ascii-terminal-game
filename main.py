import random
import os
import re
from pathlib import Path
import json

# i could add a save file to this. is there a point though

class game_settings:

	def __init__(self):
		self.board_width = 25
		self.board_length = 10
		self.obstacle_size = [8, 9]
		self.obstacle_gaps = 2
		self.obstacle_frequency = [3, 5]
		self.obstacles = []
		self.prints_without_obstacles = 0
		self.player_lives = 1
		self.points = 0
		self.automatic_save_data = False

		self.board_width_points = 10
		self.board_length_points = 10
		self.obstacle_size_points = 10
		self.obstacle_gaps_points = 10
		self.obstacle_frequency_points = 10
		self.player_lives_points = 10
		p = Path("save_data.json")
		while True:
			try:
				with p.open() as f:
					try:
						data = json.load(f)
					except json.JSONDecodeError:
						data = {}
					for key, value in data.items():
							setattr(self, key, value)
				break
			except FileNotFoundError:
				with p.open("w") as f:
					json.dump({}, f)

	def upgrade(self, u: str):
		match u:
			case "Board Width":
				if self.points >= self.board_width_points:
					self.board_width += 1
					self.points -= self.board_width_points
					self.board_width_points += 10
			case "Board Length":
				if self.points >= self.board_length_points:
					self.board_length += 1
					self.points -= self.board_length_points
					self.board_length_points += 10
			case "Obstacle Size":
				if self.points >= self.obstacle_size_points:
					if self.obstacle_size[0] > self.board_width / 2: self.obstacle_size = [size - 1 for size in self.obstacle_size]
					self.points -= self.obstacle_size_points
					self.obstacle_size_points += 10
			case "Obstacle Gaps":
				if self.points >= self.obstacle_gaps_points:
					self.obstacle_gaps += 1
					self.points -= self.obstacle_gaps_points
					self.obstacle_gaps_points += 10
			case "Obstacle Frequency":
				if self.points >= self.obstacle_frequency_points:
					if self.obstacle_frequency[0] > 0: self.obstacle_frequency = [freq - 1 for freq in self.obstacle_frequency]
					self.points -= self.obstacle_frequency_points
					self.obstacle_frequency_points += 10
			case "Player Lives":
				if self.points >= self.player_lives_points:
					self.player_lives += 1
					self.points -= self.player_lives_points
					self.player_lives_points += 10

settings = game_settings()

class player:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.lives = settings.player_lives

	def lose_lives(self, amount = 1) -> str:
		self.lives -= amount
		if self.lives <= 0:
			return "dead\n"
		else:
			return "hit\n"

def save_game():
	p = Path("save_data.json")
	with p.open("w") as f:
		data = {
			"board_width": settings.board_width,
			"board_length": settings.board_length,
			"obstacle_size": [settings.obstacle_size[0], settings.obstacle_size[1]],
			"obstacle_gaps": settings.obstacle_gaps,
			"obstacle_frequency": [settings.obstacle_frequency[0], settings.obstacle_frequency[1]],
			"player_lives": settings.player_lives,
			"points": settings.points,
			"board_width_points": settings.board_width_points,
			"board_length_points": settings.board_length_points,
			"obstacle_size_points": settings.obstacle_size_points,
			"obstacle_gaps_points": settings.obstacle_gaps_points,
			"obstacle_frequency_points": settings.obstacle_frequency_points,
			"player_lives_points": settings.player_lives_points,
			"automatic_save_data": settings.automatic_save_data,
		}
		json.dump(data, f)

def to_snake_case(text):
    text = re.sub(r'[^a-zA-Z0-9_]', ' ', text)
    text = re.sub(r'((?<=[a-z0-9])(?=[A-Z]))', r'_\1', text)
    text = re.sub(r'[\s_]+', '_', text)
    return text.lower().strip('_')

def generate_obstacle():
	global settings
	obstacle = {
		"pos": 0,
		"size": random.choice(settings.obstacle_size),
		"gaps": []
	}
	for i in range(settings.obstacle_gaps):
		gap_num = random.randint(0, obstacle["size"])
		while gap_num in obstacle["gaps"]:
			gap_num = random.randint(0, obstacle["size"])
		obstacle["gaps"].append(gap_num)
	settings.obstacles.append(obstacle)

def print_board(current_player):
	os.system('cls' if os.name == 'nt' else 'clear')
	global settings
	message = ""
	if settings.prints_without_obstacles > settings.obstacle_frequency[0] and settings.prints_without_obstacles < settings.obstacle_frequency[1]:
		if random.randint(0, 2) == 0:
			generate_obstacle()
			settings.prints_without_obstacles = 0
	elif settings.prints_without_obstacles == settings.obstacle_frequency[1]:
		generate_obstacle()
		settings.prints_without_obstacles = 0
	else:
		settings.prints_without_obstacles += 1
	board = ""
	for i in range(settings.board_width):
		board += "#"
	board += "\n"
	for k in range(settings.board_length):
		for i in range(settings.board_width):
			ob_placed = False
			for j in settings.obstacles:
				if j["pos"] == i and not k in j["gaps"]:
					board += "#"
					ob_placed = True
			if k == current_player.x and i == current_player.y:
				if ob_placed:
					message += current_player.lose_lives()
				else:
					settings.points += 1
				board += "X"
			elif not ob_placed:
				board += "/"
		board += "\n"
	for i in range(settings.board_width):
		board += "#"
	print(board)
	print(message)
	for i in settings.obstacles:
		i["pos"] += 1
		if i["pos"] > settings.board_width:
			settings.obstacles.remove(i)
	player_input = input("Input: ")
	if player_input == "w" and current_player.x > 0:
		current_player.x -= 1
	elif player_input == "s" and current_player.x < settings.board_length - 1:
		current_player.x += 1
	elif player_input == "a" and current_player.y > 0:
		current_player.y -= 1
	elif player_input == "d" and current_player.y < settings.board_width - 1:
		current_player.y += 1
	player_input_handling(player_input)
	if current_player.lives <= 0:
		start_game()
	print_board(current_player)

def clear_board():
	global settings
	settings.prints_without_obstacles = 0
	settings.obstacles.clear()

def player_input_handling(p_input: str):
	global settings
	if p_input == "menu":
		menu()
	elif p_input == "start":
		start_game()
	elif p_input == "help":
		help()
	elif p_input == "exit" or p_input == "quit" or p_input == "q":
		if settings.automatic_save_data:
			save_game()
		exit()
	elif p_input == "save":
		save_game()
	elif p_input == "a_save":
		settings.automatic_save_data = not settings.automatic_save_data

def menu():
	os.system('cls' if os.name == 'nt' else 'clear')
	global settings
	upgrades = [
		"Player Lives",
		"Board Width",
		"Board Length",
		"Obstacle Size",
		"Obstacle Gaps",
		"Obstacle Frequency",
	]
	print("Points: " + str(settings.points))
	for i in range(len(upgrades)):
		print(f"{i + 1}.{upgrades[i]}: " + str(getattr(settings, to_snake_case(upgrades[i]) + "_points")) + "\n")
	player_input = input("Input: ")
	for i in range(len(upgrades)):
		if player_input == upgrades[i] or player_input == str(i + 1):
			settings.upgrade(upgrades[i])
	player_input_handling(player_input)
	menu()

def start_game():
	clear_board()
	current_player = player()
	print_board(current_player)

def help():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("# Type start to play the game")
	print("# Type w, a, s or d while playing the game to control the direction the X character moves on the next turn")
	print("# Type menu to access the game menu")
	print("# Type exit, quit or q to exit the program")
	print("# Type help to re-enter this screen")
	print("# Type save to save game data into save_data.json file")
	if settings.automatic_save_data:
		print(f"# Automatic data saving before program exit via exit command is turned on, type a_save to toggle it")
	else:
		print("# Automatic data saving before program exit via exit command is turned off, type a_save to toggle it")
	print("# Press enter key after typing a command to execute the command")
	player_input = input("Input: ")
	player_input_handling(player_input)
	help()

help()