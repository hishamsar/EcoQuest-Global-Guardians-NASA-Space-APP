import pygame
from pygame.locals import *
import random
import time
import json

# Initialize Pygame and the mixer for sound effects
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("EcoQuest: Global Guardians")

# Load images with error handling
def load_images():
    try:
        return {key: pygame.image.load(f"assets/{key}.png") for key in [
            "urban_background", "ocean_background", "forest_background", 
            "tree", "plastic_bottle", "scoreboard", "correct", 
            "incorrect", "recycle_bin", "animal_habitat", 
            "game_over","menu_background", "community_challenge","waste"]}
    except pygame.error as e:
        print(f"Failed to load images: {e}")
        return {}

# Load sound effects with error handling
def load_sounds():
    try:
        return {
            "correct": pygame.mixer.Sound("assets/correct_sound.wav"),
            "incorrect": pygame.mixer.Sound("assets/incorrect_sound.wav"),
            "background_music": pygame.mixer.Sound("assets/background_music.wav"),
            "item_collect": pygame.mixer.Sound("assets/item_collect.wav"),
            "level_up": pygame.mixer.Sound("assets/level_up.wav"),
            "challenge_complete": pygame.mixer.Sound("assets/challenge_complete.wav")
        }
    except pygame.error as e:
        print(f"Failed to load sounds: {e}")
        return {}

# Constants for colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT_COLOR = (255, 255, 197)
DARK_BLUE = (0, 0, 128)

class EcoQuestGame:
    def __init__(self):
        self.running = True
        self.level = 0  
        self.player_score = 0
        self.environment_health = 1000
        self.current_environment = ["Urban", "Ocean", "Forest"]
        self.images = load_images()
        self.sounds = load_sounds()
        self.current_environment_name = self.current_environment[self.level]
        self.quest_active = False
        self.quest_message = ""
        self.educational_popups = []
        self.gloabe_data_entries = []
        self.leaderboard = self.load_leaderboard()
        self.exp = 0
        self.level_up_exp = 10 * (self.level + 1)
        
        # Quest management
        self.completed_quests = []
        self.current_quests = []
        
        # Mini-game selection
        self.mini_game_active = False
        
        # Start background music based on environment
        self.play_background_music()

    def play_background_music(self):
        """Play background music based on current environment."""
        if self.sounds["background_music"]:
            self.sounds["background_music"].play(-1)

    def load_leaderboard(self):
        """Load leaderboard from a JSON file."""
        try:
            with open('leaderboard.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_leaderboard(self):
        """Save leaderboard to a JSON file."""
        with open('leaderboard.json', 'w') as f:
            json.dump(self.leaderboard, f)

    def run(self):
        """Main game loop."""
        self.show_start_menu()
        while self.running:
            self.update()
            self.handle_events()
            self.render()
    def update(self):
        """Update game state."""
        if not self.mini_game_active:
            self.environment_health -= 0.1
            if self.environment_health <= 0:
                self.environment_health = 0
                self.game_over()
            

            # Change scenario if all quests are completed
            if not self.current_quests and (self.level % 3 == 0):
                self.environment_health = 1000
         
    def show_start_menu(self):
        """Display the start menu."""
        while True:
            screen.blit(self.images["menu_background"], (0, 0))
            font = pygame.font.Font(None, 74)
            title_text = font.render("EcoQuest: Global Guardians", True, DARK_BLUE)            
            start_text = font.render("Press Enter to Start", True, DARK_BLUE)
            pygame.draw.rect(screen, (211,211,211), (50, 100, 712, 43))
            screen.blit(title_text, (50, 100))
            pygame.draw.rect(screen, (211,211,211), (150, 238, 480, 43))
            screen.blit(start_text, (150, 238))

            
            # Level selection
            font=pygame.font.Font(None ,47)
            pygame.draw.rect(screen, (211,211,211), (230, 380, 300, 30))
            levels_text = font.render("Press T for Tutorial", True, DARK_BLUE)
            screen.blit(levels_text, (230, 380))
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return
                    elif event.key == K_t:
                        self.level = 0
                        self.show_tutorial()

    def show_tutorial(self):
        """Show tutorial."""
        while True:
            screen.blit(self.images["menu_background"], (0, 0))
            font = pygame.font.Font(None, 32)
            text = font.render("How to play:", True, FONT_COLOR)
            text_rect = text.get_rect(center=(400, 100))
            screen.blit(text, text_rect)
            
            # Show instruction
            instruction = """
            Q: Start Quest
            SPACE: Collect Item
            M: Play Mini Game
            L: Show Leaderboard
            E: Complete Quest
            R: Record globe data
            G: Display globe data
            P: Display community challenges
            """
            lines = instruction.strip().splitlines()
            y = 150
            rect = pygame.Rect(234, y - 15, 400, len(lines) * 30)
            pygame.draw.rect(screen, (211,211,211), rect)
            for i, line in enumerate(lines):
                text = font.render(line, True, FONT_COLOR)
                text_rect = text.get_rect(center=(400, y))
                screen.blit(text, text_rect)
                y += 30

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_b:
                        return
    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN) and (event.type == QUIT or event.key == K_ESCAPE):
                self.running = False

            elif event.type == KEYDOWN:
                self.process_key(event.key)
    def record_globe_data(self):
        """Record globe data collected by the player."""
        # Example of adding globe data entry
        entry = {
            "type": "Plastic Waste",
            "value": random.randint(1, 10),  # Randomly generated value for demonstration
            "location": self.current_environment_name
        }
        self.gloabe_data_entries.append(entry)
        print(f"Recorded data: {entry}")

    def display_globe_data(self):
        """Display globe data collected by the player."""
        globe_data_window = pygame.display.set_mode((800, 380))
        pygame.display.set_caption("Globe Data")
        globe_data_window.blit(self.images["community_challenge"], (0, 0))
        font = pygame.font.Font(None, 32)
        return_txt= font.render("Press B to return", True, DARK_BLUE)
        pygame.draw.rect(globe_data_window, (211,211,211), (300, 8, 180, 25))
        globe_data_window.blit(return_txt, (300, 10))
        globe_data_texts = [f"{entry['type']}: {entry['value']} at {entry['location']}" for entry in self.gloabe_data_entries]
        for index, entry in enumerate(globe_data_texts):
            globe_data_text = font.render(entry, True, (0, 0, 0))
            globe_data_window.blit(globe_data_text, (70, 60 + index * 30))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN and event.key == K_b:
                    pygame.display.set_mode((800, 600))
                    return
                     
    
    def show_leaderboard(self):
        """Show leaderboard on a new screen."""
        while True:
            screen.fill(WHITE)
            font = pygame.font.Font(None, 32)
            leaderboard_texts = [f"{name}: {score}" for name, score in sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)]
        
            for index, entry in enumerate(leaderboard_texts):
                leader_text = font.render(entry, True, (0, 0, 0))
                screen.blit(leader_text, (50, 50 + index * 30))

            return_button = font.render("Press B to return", True, DARK_BLUE)
            screen.blit(return_button, (50, 50 + len(leaderboard_texts) * 30 + 20))
        
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_b:
                        return  # Return to main game loop


    def process_key(self, key):
        """Process key inputs."""
        if key == K_q:
            self.start_quest()  
            total_points = self.player_score          
            player_name = "sky"   # Update leaderboard with player name
            if  total_points > self.leaderboard[player_name]:
                    self.leaderboard[player_name] = total_points
                    self.save_leaderboard()      
        elif key == K_SPACE:
            self.collect_item()
        elif key == K_m:
            self.start_mini_game() 
        elif key == K_l:  # Press L to show leaderboard
            self.show_leaderboard()
        elif key == K_e:  # Press E to complete the current quest
            self.complete_current_quest()
        elif key == K_r:
            self.record_globe_data()
        elif key == K_g:
            self.display_globe_data()
        elif key == K_p:
            self.display_community_challenges()
    
    def start_quests_in_order(self):
        """Sequentially run quests based on the current environment."""
        if self.level < 3:  # Urban
            urban_quests = [
                {"task": "Collect 3 recyclable items", "reward": 25, "completed": False, "minigame": "sort_trash_mini_game"},
                {"task": "Educate 3 friends about recycling", "reward": 50, "completed": False, "minigame": "recycling_quiz_mini_game"},
            ]
            return urban_quests

        elif self.level >= 3 and self.level < 6:  # Ocean
            ocean_quests = [
                {"task": "Help clean up the beach", "reward": 50, "completed": False},
                {"task": "Recognize plastic waste", "reward": 100, "completed": False}
            ]
            return ocean_quests

        elif self.level >= 6:  # Forest
            forest_quests = [
                {"task": "Find the Hidden Trees!", "reward": 100, "completed": False},
                {"task": "Identify wildlife habitats", "reward": 75, "completed": False},
            ]
            return forest_quests

    def start_quest(self):
        """Start a new quest and return the reward points."""

        # Start new quests based on level if current_quests is empty
        if not self.current_quests and all(quest["completed"] == False for quest in self.current_quests):
            self.current_quests = self.start_quests_in_order()
    
        # Assign the current quest message
        if self.current_quests:  # Check if there are any quests available
            current_quest = self.current_quests[0]  # Get the first quest in the list
            self.quest_message = f"Quest: {current_quest['task']}"  # Set the message for the current quest

            # If this quest is completed, remove it from the list
            if current_quest["completed"]:
                self.current_quests.pop(0)  # Remove completed quest
            
        
        
        # Check if all quests in the current environment are completed
        if all(quest["completed"] == True for quest in self.current_quests):
            if self.level > 6:
                self.quest_message = "Congratulations! You have completed all quests \n in the forest environment." 
                return  # Exit since no new quest will be started


    def complete_current_quest(self):        
        """Mark the current quest as complete. If the current quest is 'Collect 3 recyclable items', 
        it will increment a counter until it reaches 3, then it will mark the quest as complete, 
        add the reward points to the player score, play a sound, and start a new quest."""
        current_quest = self.current_quests[0]

        if current_quest["task"] == "Collect 3 recyclable items":
            times_completed = 0
        
            # Loop until we collect 3 recyclable items
            while times_completed < 3:
                if self.sort_trash_mini_game():  # Assume this returns True upon success
                    times_completed += 1
                    font=pygame.font.Font(None, 36)
                    txt_1=font.render(f"Successfully Collected Recyclable Items! Attempts so far: {times_completed}/3", True, FONT_COLOR)
                    screen.blit(txt_1, (50, 350))
                    pygame.display.flip()
                    pygame.time.delay(1200)


            # After achieving 3 successful attempts
            current_quest["completed"] = True
            self.exp += 10
            self.player_score += current_quest['reward']
            font=pygame.font.Font(None, 32)
            rew_txt__1=font.render(f"Completed Quest: {current_quest['task']}! You earned {current_quest['reward']} points.", True, FONT_COLOR)
            screen.blit(rew_txt__1, (50, 520))
            pygame.display.flip()
            pygame.time.delay(1200)
            self.sounds["correct"].play()
            self.current_quests.pop(0)
            self.quest_message = ""
            self.start_quest() 


                
        elif current_quest["task"] == "Educate 3 friends about recycling":
            times_completed = 0
        
            
            while times_completed < 3:
                if self.recycling_quiz_min_game():  # Assume this returns True upon success
                    times_completed += 1
                    font=pygame.font.Font(None, 36)
                    txt_2=font.render(f"Successfully educated Friend ! Attempts so far: {times_completed}/3", True, FONT_COLOR)
                    screen.blit(txt_2, (50, 350))
                    pygame.display.flip()
                    pygame.time.delay(1200)
                   


            # After achieving 3 successful attempts
            current_quest["completed"] = True
            self.exp += 10
            self.player_score += current_quest['reward']
            font=pygame.font.Font(None, 32)
            rew_txt_2=font.render(f"Completed Quest: {current_quest['task']}! You earned {current_quest['reward']} points.", True, FONT_COLOR)
            screen.blit(rew_txt_2, (10, 520))
            pygame.display.flip()
            pygame.time.delay(1200)
            self.sounds["correct"].play()
            self.current_quests.pop(1)
            self.quest_message = ""
            self.start_quest() 
        
        elif current_quest["task"] == "Help clean up the beach":
            times_completed = 0
        
            
            while times_completed < 3:
                if self.clean_beach_mini_game():  # Assume this returns True upon success
                    times_completed += 1
                    font=pygame.font.Font(None, 36)
                    txt_3=font.render(f"Successfully Cleaned ! Attempts so far: {times_completed}/3", True, FONT_COLOR)
                    screen.blit(txt_3, (50, 450))
                    pygame.display.flip()
                    pygame.time.delay(1200)



            # After achieving 3 successful attempts
            current_quest["completed"] = True
            self.exp += 75
            if self.exp > self.level_up_exp:
                self.level_up()
            self.player_score += current_quest['reward']
            font=pygame.font.Font(None, 32)
            rew_txt_3=font.render(f"Completed Quest: {current_quest['task']}! You earned {current_quest['reward']} points.", True, FONT_COLOR)
            screen.blit(rew_txt_3, (10, 540))
            pygame.display.flip()
            pygame.time.delay(1200)
            self.sounds["correct"].play()
            self.current_quests.pop(0)
            self.quest_message = ""
            self.start_quest() 
        
        elif current_quest["task"] == "Recognize plastic waste":
            times_completed = 0
        
            
            while times_completed < 1:
                if self.clean_neighborhood_mini_game():  # Assume this returns True upon success
                    times_completed += 1
                    font=pygame.font.Font(None, 36)
                    txt_4=font.render(f"Successfully Recognized ! Attempts so far: {times_completed}/1", True, FONT_COLOR)
                    screen.blit(txt_4, (50, 250))
                    pygame.display.flip()
                    pygame.time.delay(1200)
                   


            # After achieving 3 successful attempts
            current_quest["completed"] = True
            self.exp += 75
            if self.exp > self.level_up_exp:
                self.level_up()
            self.player_score += current_quest['reward']
            font=pygame.font.Font(None, 32)
            rew_txt_4=font.render(f"Completed Quest: {current_quest['task']}! You earned {current_quest['reward']} points.", True, FONT_COLOR)
            screen.blit(rew_txt_4, (10, 450))
            pygame.display.flip()
            pygame.time.delay(1200)
            self.sounds["correct"].play()
            self.current_quests.pop(1)
            self.quest_message = ""
            self.start_quest()
        
        elif current_quest["task"] == "Find the Hidden Trees!":
            times_completed = 0
        
            
            while times_completed < 1:
                if self.plant_trees_mini_game():  # Assume this returns True upon success
                    times_completed += 1
                    
                   


            # After achieving 3 successful attempts
            current_quest["completed"] = True
            self.exp += 75
            if self.exp > self.level_up_exp:
                self.level_up()
            self.player_score += current_quest['reward']
            font=pygame.font.Font(None, 32)
            self.sounds["correct"].play()
            self.current_quests.pop(0)
            self.quest_message = ""
            self.start_quest()
        
        elif current_quest["task"] == "Identify wildlife habitats":
            times_completed = 0
        
            
            while times_completed < 3:
                if self.match_habitat_mini_game():  # Assume this returns True upon success
                    times_completed += 1
                    font=pygame.font.Font(None, 36)
                    txt_6=font.render(f"Successfully Matched ! Attempts so far: {times_completed}/3", True, FONT_COLOR)
                    screen.blit(txt_6, (50, 350))
                    pygame.display.flip()
                    pygame.time.delay(1200)
                   


            # After achieving 3 successful attempts
            current_quest["completed"] = True
            self.exp += 85
            if self.exp > self.level_up_exp:
                self.level_up()
            self.player_score += current_quest['reward']
            font=pygame.font.Font(None, 32)
            rew_txt_6=font.render(f"Completed Quest: {current_quest['task']}! You earned {current_quest['reward']} points.", True, FONT_COLOR)
            screen.blit(rew_txt_6, (50, 520))
            pygame.display.flip()
            pygame.time.delay(1200)
            self.sounds["correct"].play()
            pygame.time.delay(2000)
            """Display game over message and final score."""
            screen.fill(RED)
            game_over_text=pygame.font.Font(None ,74).render("Game Over!" , True , WHITE)
            score_text=pygame.font.Font(None ,36).render(f"Final Score: {self.player_score}" , True , WHITE)

            screen.blit(game_over_text,(250 ,250))
            screen.blit(score_text,(300 ,350))
         
            pygame.display.flip()
            pygame.time.delay(3000)  
            self.running=False

    

    def plant_trees_mini_game(self):
        """Mini-game for planting trees in a local park with enhanced feedback."""
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Find the Hidden Trees!")
        background = self.images["forest_background"]
        screen.blit(background, (0, 0))
        pygame.display.flip()

        tree_image = self.images["tree"]
        tree_width, tree_height = tree_image.get_size()

        correct_answer_image = self.images["correct"]
        correct_answer_width, correct_answer_height = correct_answer_image.get_size()

        correct_answer_places = [(100, 100), (300, 200), (500, 300), (700, 400), (200, 500)]
        black_marker_image = pygame.Surface((10, 10))
        black_marker_image.fill((0, 0, 0))
        black_marker_width, black_marker_height = black_marker_image.get_size()

        placed_trees = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for place in correct_answer_places:
                        if place[0] < x < place[0] + tree_width and place[1] < y < place[1] + tree_height:
                            screen.blit(tree_image, place)
                            placed_trees.append(place)
                            pygame.display.flip()
                            if len(placed_trees) == len(correct_answer_places):
                                for place in correct_answer_places:
                                    screen.blit(correct_answer_image, (place[0] + (tree_width - correct_answer_width) // 2, place[1] + (tree_height - correct_answer_height) // 2))
                                pygame.display.flip()
                                pygame.time.delay(2000)
                                self.player_score += 100
                                self.exp += 10
                                if self.environment_health<1000:
                                    self.environment_health += 50
                                if self.exp >= self.level_up_exp:
                                    self.level_up()
                                    self.sounds["level_up"].play()
                                if self.sounds["correct"]:
                                    self.sounds["correct"].play()
                                pygame.display.set_mode((800, 600))
                                return True

    def clean_neighborhood_mini_game(self):
        """Mini-game for cleaning up the neighborhood with enhanced feedback."""
        correct_answer = True
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Clean up your enviorment")
        if self.level< 3:
            background = self.images["urban_background"]
        elif self.level >= 3:
            background = self.images["ocean_background"]
        elif self.level >= 6:
            background = self.images["forest_background"]
        screen.blit(background, (0, 0))
        pygame.display.flip()

        waste = []
        for _ in range(6):
            x = random.randint(10, 700)
            y = random.randint(250, 500)
            waste.append((x, y))
            screen.blit(self.images["waste"], (x, y))

        pygame.display.flip()

        while len(waste) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for w in waste[:]:
                        if w[0] < event.pos[0] < w[0] + 100 and w[1] < event.pos[1] < w[1] + 100:
                            waste.remove(w)
                            screen.blit(self.images["correct"], (w[0], w[1]))
                            pygame.display.flip()
                            if self.sounds["correct"]:
                                self.sounds["correct"].play()

        if correct_answer:
            self.player_score += 75
            self.exp += 10
            if self.environment_health<1000:
                self.environment_health += 50
            
            if self.exp >= self.level_up_exp:
                self.level_up()
                self.sounds["level_up"].play()
            return True

    def level_up(self):
        """Increase player level and give them experience points."""
        self.level += 1
        self.exp = 0
        self.level_up_exp = 10 * (self.level + 1)

        if self.level == 3:
            self.current_environment_name = "Ocean"
        elif self.level == 6:
            self.current_environment_name = "Forest"

        if self.environment_health<1000:
            self.environment_health += 50
        self.current_quests = self.start_quests_in_order()


    def collect_item(self):
        """Simulate collecting an item and update score."""
        point_value = random.randint(1, 2)
        self.player_score += point_value
        self.exp += point_value
        print(f"Collected an item! Score: {self.player_score}")
        self.sounds["item_collect"].play()
        if self.exp >= self.level_up_exp:
            self.level_up()
    
    def start_mini_game(self):
        """Start a randomly chosen mini-game with enhanced feedback."""
        previous_mini_game = None
    
        if self.level < 3:
            mini_game_choices = ["sort_trash", "recycling_quiz", "clean_up_neighborhood"]
        elif self.level >= 3 and self.level < 10:
            mini_game_choices = ["clean_up_neighborhood","clean_beach","match_habitat"]
        else:
            mini_game_choices = ["match_habitat", "clean_up_neighborhood", "plant_trees"]
    
        while True:
            mini_game_choice = random.choice(mini_game_choices)
            if mini_game_choice != previous_mini_game:
                break
    
        if mini_game_choice == "sort_trash":
            self.sort_trash_mini_game()
        elif mini_game_choice == "match_habitat":
            self.match_habitat_mini_game()
        elif mini_game_choice == "recycling_quiz":
            self.recycling_quiz_min_game()
        elif mini_game_choice == "clean_up_neighborhood":
            self.clean_neighborhood_mini_game()
        elif mini_game_choice == "plant_trees":
            self.plant_trees_mini_game()
        elif mini_game_choice == "clean_beach":
            self.clean_beach_mini_game()

    def clean_beach_mini_game(self):
        """Mini-game for cleaning up the beach by dragging plastic bottles to a recycling bin."""
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Clean up the beach")
        background = self.images["ocean_background"]
        screen.blit(background, (0, 0))
        pygame.display.flip()
        
        plastic_bottles = []
        for _ in range(1):
            x = random.randint(0, 700)
            y = random.randint(250, 500)
            plastic_bottles.append((x, y))
        
        recycle_bin = self.images["recycle_bin"]
        screen.blit(recycle_bin, (700, 250))
        
        while len(plastic_bottles) > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for bottle in plastic_bottles[:]:
                        if bottle[0] < event.pos[0] < bottle[0] + 100 and bottle[1] < event.pos[1] < bottle[1] + 100:
                            plastic_bottles.remove(bottle)
                            for y in range(bottle[1], 250, -1):
                                screen.blit(background, (0, 0))
                                screen.blit(recycle_bin, (700, 250))
                                screen.blit(self.images["plastic_bottle"], (700, y))
                                pygame.display.flip()
                                pygame.time.delay(10)
                            screen.blit(self.images["correct"], (350, 250))
                            pygame.display.flip()
                            pygame.time.delay(2000)
                            if self.environment_health<1000:
                                self.environment_health += 50
                            self.exp += 10
                            if self.exp >= self.level_up_exp:
                                self.level_up() 
                            if self.sounds["correct"]:
                                self.sounds["correct"].play()
                            return True
            for bottle in plastic_bottles:
                screen.blit(self.images["plastic_bottle"], bottle)
            pygame.display.flip()
        
        self.completed_quests.append({"task": "Help clean up the beach", "reward": 50, "completed": True,})






    def sort_trash_mini_game(self):
        """Mini-game for sorting trash items with improved feedback."""
        correct_items = ["plastic bottle", "glass", "paper", "cardboard", "battery", "newspaper", 
                     "magazine", "aluminum can", "steel can", "copper wire", "old computer", 
                     "old phone", "TV", "bicycle", "tire", "cement", "wood", "fabric", 
                     "leather", "ceramic", "porcelain"]

        print("Mini-Game: Give name of Recyclable Objects!")
        input_box = pygame.Rect(250, 300, 140, 32)
    
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        active = False
        text = ''
    
        font = pygame.font.Font(None, 32)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and active:
                    if event.key == K_RETURN:
                        if text.strip().lower() in correct_items:  # Normalize input for comparison
                            print("Correct! You earn extra points!")
                            points_awarded = 50
                            self.exp += 10
                            if self.environment_health < 1000:
                                self.environment_health += 50
                            self.player_score += points_awarded
                            if self.exp >= self.level_up_exp:
                                self.level_up()
                                self.sounds["level_up"].play()
                            if self.sounds["correct"]:
                                self.sounds["correct"].play()
                            screen.blit(self.images["correct"], (280, 380))
                            pygame.display.flip()
                            pygame.time.delay(2000) 
                            return True  # Indicate success
                        else:
                            print("Incorrect! Try again.")
                            if self.sounds["incorrect"]:
                                self.sounds["incorrect"].play()
                            screen.blit(self.images["incorrect"], (280, 380))
                            pygame.display.flip()
                            pygame.time.delay(2000) 
                            return False  # Indicate failure

                    elif event.key == K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            
                if event.type == MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
            
                color = color_active if active else color_inactive
            
                screen.fill(BLUE)
                txt_surface = font.render(text, True, color)
                width = max(200, txt_surface.get_width() + 10)
                input_box.w = width

                screen.blit(self.images["plastic_bottle"], (250, 100))
                instructions = font.render("Type Name of Recyclable item:", True, WHITE)
                screen.blit(instructions, (220, 250))  
            
                screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                pygame.draw.rect(screen, color, input_box, 2)

                pygame.display.flip()


    def match_habitat_mini_game(self):
       """Mini-game for matching animals to their habitats with enhanced feedback."""
       habitats = {
           "lion": "savannah",
           "penguin": "antarctica",
           "dolphin": "ocean",
           "elephant": "savannah",
           "giraffe": "savannah",
           "kangaroo": "grassland",
           "koala": "forest",
           "monkey": "rainforest",
           "polar bear": "arctic",
           "zebra": "savannah",
           "crocodile": "swamp",
           "tiger": "forest",
           "leopard": "forest",
           "chimpanzee": "rainforest",
           "gorilla": "rainforest",
           "rhinoceros": "savannah",
           "hippopotamus": "swamp",
           "wolf": "forest",
           "giant panda": "bamboo forest",
           "hyena": "savannah",
           "sloth": "rainforest",
           "flamingo": "coastal wetland"
       }
       animal = random.choice(list(habitats.keys()))
    
       print(f"Mini-Game: Where does the {animal} live?")
    
       input_box = pygame.Rect(250, 300, 140, 32)
       color_inactive = pygame.Color('lightskyblue3')
       color_active = pygame.Color('dodgerblue2')
       active = False
       text = ''
       font = pygame.font.Font(None, 32)

       while True:
           for event in pygame.event.get():
               if event.type == QUIT:
                   pygame.quit()
                   exit()
               if event.type == KEYDOWN and active:
                   if event.key == K_RETURN:
                       if text.lower() == habitats[animal]:
                           print("Correct! You earn extra points!")
                           points_awarded=50
                           self.exp += 10
                           if self.environment_health<1000:
                               self.environment_health += 50
                           self.player_score += points_awarded
                           if self.exp >= self.level_up_exp:
                               self.level_up()
                               self.sounds["level_up"].play()
                           if self.sounds["correct"]:
                               self.sounds["correct"].play()
                           screen.blit(self.images["correct"], (280, 380))
                           pygame.display.flip()
                           pygame.time.delay(2000)
                           return True 
                       else:
                           print("Incorrect! Try again.")
                           if self.sounds["incorrect"]:
                               self.sounds["incorrect"].play()
                           screen.blit(self.images["incorrect"], (280, 380))
                           pygame.display.flip()
                           pygame.time.delay(2000)
                           return False 
                       return 
                   elif event.key == K_BACKSPACE:
                       text=text[:-1]
                   else:
                       text += event.unicode
            
               if event.type == MOUSEBUTTONDOWN:
                   if input_box.collidepoint(event.pos):
                       active= not active
                   else:
                       active=False
            
               color=color_active if active else color_inactive
            
               screen.fill(BLUE)
               instructions=font.render(f"Where does the {animal} live? Type your answer:", True , WHITE)
               screen.blit(instructions , (200 ,250))  
               
               screen.blit(self.images["animal_habitat"], (250, 100))

               txt_surface=font.render(text , True , color)
               width=max(200 ,txt_surface.get_width()+10)
               input_box.w=width
            
               screen.blit(txt_surface , (input_box.x+5 ,input_box.y+5))
               pygame.draw.rect(screen ,color ,input_box ,2)

               pygame.display.flip()

    def recycling_quiz_min_game(self):
       """Mini-game quiz about recycling with improved questions and feedback."""
       questions_and_answers = {
           "What is the recycling symbol?": ["Triangle with arrows", "Circle with lines"],
           "Which of these items can be recycled?": ["Plastic bottles", "Food waste"],
           "What does recycling help reduce?": ["Waste", "Pollution"],
           "What is the purpose of recycling?": ["To reduce waste", "To conserve resources"],
           "What is the most recyclable material?": ["Paper", "Glass"],
           "What is the least recyclable material?": ["Plastic", "Metal"],
           "What is the most common recyclable material?": ["Paper", "Cardboard"],
           "What is the least common recyclable material?": ["Glass", "Metal"],
           "What is the most efficient way to recycle?": ["Sort recyclables by type", "Use a recycling bin"],
           "What is the least efficient way to recycle?": ["Mix all recyclables together", "Use a trash can"],
           "What is the most common recycling mistake?": ["Contamination", "Not recycling at all"],
           "What is the least common recycling mistake?": ["Not sorting", "Not rinsing recyclables"],
           "What is the most effective way to reduce waste?": ["Reduce", "Reuse"],
           "What is the least effective way to reduce waste?": ["Recycle", "Dispose of it properly"]
       }
       question, answers = random.choice(list(questions_and_answers.items()))

       input_box = pygame.Rect(250, 300, 140, 32)
       color_inactive = pygame.Color('lightskyblue3')
       color_active = pygame.Color('dodgerblue2')
    
       active = False
       text = ''
    
       font = pygame.font.Font(None, 32)

       while True:
           for event in pygame.event.get():
               if event.type == QUIT:
                   pygame.quit()
                   exit()
               if event.type == KEYDOWN and active:
                   correct_answer_index = answers.index([a for a in answers if a.lower() == questions_and_answers[question][0].lower()][0])
                   if event.key== K_RETURN:
                       if text.lower() == answers[correct_answer_index].lower():
                           print("Correct! You earn extra points!")
                           points_awarded=50
                           self.exp += 10
                           if self.environment_health<1000:
                                self.environment_health += 50
                           self.player_score += points_awarded
                           if self.exp >= self.level_up_exp:
                               self.level_up()
                               self.sounds["level_up"].play()
                           if self.sounds["correct"]:
                               self.sounds["correct"].play()
                           screen.blit(self.images["correct"], (280 ,380)) 
                           pygame.display.flip() 
                           pygame.time.delay(2000)
                           return True 
                       else:
                           print("Incorrect! Try again.")
                           if self.sounds["incorrect"]:
                               self.sounds["incorrect"].play()
                           screen.blit(self.images["incorrect"], (280 ,380))  
                           pygame.display.flip() 
                           pygame.time.delay(2000)
                           return False 
                        
                   elif event.key == K_BACKSPACE:
                       text=text[:-1]
                   else:
                       text += event.unicode
            
               if event.type == MOUSEBUTTONDOWN:
                   if input_box.collidepoint(event.pos):
                       active= not active
                   else:
                       active=False
            
               color=color_active if active else color_inactive
            
               screen.fill(BLUE)
               instructions=font.render(f"{question} Type your answer:", True , WHITE)
               screen.blit(self.images["plastic_bottle"], (250, 100))
               screen.blit(self.images["recycle_bin"], (300, 100))
               screen.blit(instructions , (60 ,250))  
            
               txt_surface=font.render(text , True , color)
               width=max(200 ,txt_surface.get_width()+10)
               input_box.w=width
            
               screen.blit(txt_surface , (input_box.x+5 ,input_box.y+5))
               pygame.draw.rect(screen ,color ,input_box ,2)

               # Refresh the display.
               pygame.display.flip()
    
    def community_challenges(self):
      """Start a community challenge and give rewards upon completion with enhanced feedback."""
      challenges=[
          {"challenge":"Reduce plastic waste by collecting litter in your area!"},
          {"challenge":"Plant trees in your local park!"},
          {"challenge":"Organize a local cleanup event!"},
          {"challenge":"Donate to local charities!"},
          {"challenge":"Plant trees in your local park!"},
      ]
      return challenges
    def display_community_challenges(self):
        """Display community challenges."""
        community_window = pygame.display.set_mode((800, 380))
        pygame.display.set_caption("Community challenge")
        community_window.blit(self.images["community_challenge"], (0, 0))
        font = pygame.font.Font(None, 30)
        return_1_txt= font.render("Press B to return", True, DARK_BLUE)
        pygame.draw.rect(community_window, (211,211,211), (300, 8, 180, 25))
        community_window.blit(return_1_txt, (300, 10))
        challenges= self.community_challenges()   
        challenge_texts = [f"{index+1}. {challenge['challenge']}" for index, challenge in enumerate(challenges)]
        for index, entry in enumerate(challenge_texts):
            globe_data_text = font.render(entry, True, (0, 0, 0))
            community_window.blit(globe_data_text, (75, 70 + index * 30))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN and event.key == K_b:
                    pygame.display.set_mode((800, 600))
                    return
    
    def render(self):
         """Render game graphics on the screen."""
         if not self.running:
             return

         screen.blit(self.images[self.current_environment_name.lower() + "_background"], (0 ,0))
         
         # Display quest message  at the top of the UI.
         font=pygame.font.Font(None ,40)
         quest_text=font.render(self.quest_message , True , FONT_COLOR)
         screen.blit(quest_text , (180 ,450))


         for index,popup in enumerate(self.educational_popups):
             popup_text=font.render(popup , True , FONT_COLOR)
             screen.blit(popup_text , (10 ,50 + index *30))

         # Display score and health info clearly at the bottom of the UI.
         self.display_info()
         pygame.display.flip()

    def display_info(self):
        """Display player's score, environmental health, and current level."""
        font=pygame.font.Font(None ,36)
        score_text=font.render(f"Score: {self.player_score}" , True , FONT_COLOR)
        health_text=font.render(f"Environmental Health: {self.environment_health:.1f}" , True , FONT_COLOR)
        level_text=font.render(f"Level: {self.level} exp:{self.exp}/{self.level_up_exp}" , True , FONT_COLOR)

        # Draw a background rectangle to enhance visibility of score and health info.
        if self.level < 3 :
            pygame.draw.rect(screen , (128,128,128) , (5 ,5 ,370 ,100))  
            pygame.draw.rect(screen , (128,128,128) , (5 ,540 ,230 ,50))  
            screen.blit(score_text,(10 ,10))
            screen.blit(health_text,(10 ,50))
            screen.blit(level_text,(10 ,550))
        elif self.level >= 3:
            pygame.draw.rect(screen , BLUE , (5 ,5 ,370 ,100))  
            pygame.draw.rect(screen , BLUE , (5 ,540 ,230 ,50))
            screen.blit(score_text,(10 ,10))
            screen.blit(health_text,(10 ,50))
            screen.blit(level_text,(10 ,550))
        elif self.level >=6:
            pygame.draw.rect(screen , (168,0,32) , (5 ,5 ,370 ,100))  
            pygame.draw.rect(screen , (168,0,32) , (5 ,540 ,230 ,50))
            screen.blit(score_text,(10 ,10))
            screen.blit(health_text,(10 ,50))
            screen.blit(level_text,(10 ,550))


    def game_over(self):
         """Display game over message and final score."""
         screen.fill(RED)
         game_over_text=pygame.font.Font(None ,74).render("Game Over!" , True , WHITE)
         score_text=pygame.font.Font(None ,36).render(f"Final Score: {self.player_score}" , True , WHITE)

         screen.blit(game_over_text,(250 ,250))
         screen.blit(score_text,(300 ,350))
         
         pygame.display.flip()
         pygame.time.delay(3000)  
         self.running=False

# Entry point.
if __name__=="__main__":
    game=EcoQuestGame()
    game.run()
    pygame.quit()
