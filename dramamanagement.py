import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Forgotten Kingdom - Extended Edition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_RED = (139, 0, 0)
TEXT_BACKGROUND_COLOR = (0, 0, 0, 180)

# Character constants
CHARACTER_WIDTH = 80
CHARACTER_HEIGHT = 100
CHARACTER_MARGIN = 50

# Load backgrounds for different scenes
backgrounds = {
    "village": pygame.transform.scale(pygame.image.load("village_background.png"), (WIDTH, HEIGHT)),
    "tavern": pygame.transform.scale(pygame.image.load("tavern_background.png"), (WIDTH, HEIGHT)),
    "forest": pygame.transform.scale(pygame.image.load("forest_background.png"), (WIDTH, HEIGHT)),
    "palace": pygame.transform.scale(pygame.image.load("palace_background.png"), (WIDTH, HEIGHT)),
    "cave": pygame.transform.scale(pygame.image.load("cave_background.png"), (WIDTH, HEIGHT)),
    "mountain": pygame.transform.scale(pygame.image.load("mountain_background.png"), (WIDTH, HEIGHT)),
    "temple": pygame.transform.scale(pygame.image.load("temple_background.png"), (WIDTH, HEIGHT)),
    "dungeon": pygame.transform.scale(pygame.image.load("dungeon_background.png"), (WIDTH, HEIGHT)),
    "library": pygame.transform.scale(pygame.image.load("library_background.png"), (WIDTH, HEIGHT)),
    "garden": pygame.transform.scale(pygame.image.load("garden_background.png"), (WIDTH, HEIGHT))
}

# Load character images for different states
character_states = {
    "normal": pygame.transform.scale(pygame.image.load("character.png"), (CHARACTER_WIDTH, CHARACTER_HEIGHT)),
    "battle": pygame.transform.scale(pygame.image.load("character_battle.png"), (CHARACTER_WIDTH, CHARACTER_HEIGHT)),
    "stealth": pygame.transform.scale(pygame.image.load("character_stealth.png"), (CHARACTER_WIDTH, CHARACTER_HEIGHT))
}

# Fonts
try:
    title_font = pygame.font.Font("medieval.ttf", 48)
    main_font = pygame.font.Font("medieval.ttf", 24)
except:
    title_font = pygame.font.SysFont("Arial", 48)
    main_font = pygame.font.SysFont("Arial", 24)

class GameState:
    def __init__(self):
        self.current_scene = "village"
        self.background = "village"
        self.inventory = []
        self.character_x = WIDTH - CHARACTER_WIDTH - CHARACTER_MARGIN
        self.character_y = HEIGHT - CHARACTER_HEIGHT - 100
        self.choices = []
        self.character_state = "normal"
        self.quest_progress = {
            "ancient_key": False,
            "magic_map": False,
            "crystal_shard": False,
            "sacred_text": False,
            "royal_seal": False
        }
        self.player_stats = {
            "health": 100,
            "gold": 50,
            "reputation": 0
        }

game_state = GameState()

def create_gradient_background(width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for y in range(height):
        alpha = min(180, int(y * 0.5 + 100))
        pygame.draw.rect(surface, (*BLACK, alpha), (0, y, width, 1))
    return surface

def display_text(text, y_offset=100, is_title=False, color=GOLD):
    lines = text.split("\n")
    font = title_font if is_title else main_font
    
    max_width = max(font.size(line)[0] for line in lines)
    total_height = len(lines) * 40
    
    background_surface = create_gradient_background(max_width + 40, total_height + 30)
    screen.blit(background_surface, (30, y_offset - 10))
    
    for i, line in enumerate(lines):
        glow_surface = font.render(line, True, LIGHT_BLUE)
        glow_surface.set_alpha(100)
        screen.blit(glow_surface, (42, y_offset + i * 40 + 2))
        
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (40, y_offset + i * 40))

def display_stats():
    stats_text = f"Health: {game_state.player_stats['health']} | Gold: {game_state.player_stats['gold']} | Reputation: {game_state.player_stats['reputation']}"
    text_surface = main_font.render(stats_text, True, GOLD)
    screen.blit(text_surface, (10, 10))

def handle_scene():
    screen.fill(BLACK)
    screen.blit(backgrounds[game_state.background], (0, 0))
    display_stats()
    
    scenes = {
        # Starting Area
        "village": {
            "title": "The Village of Eldermore",
            "text": "The peaceful village holds many secrets.\nWhere would you like to go?",
            "choices": [
                {"text": "Visit the ancient library (1)", "next_scene": "library", "background": "library"},
                {"text": "Head to the tavern (2)", "next_scene": "tavern", "background": "tavern"},
                {"text": "Explore the forest (3)", "next_scene": "forest", "background": "forest"}
            ]
        },
        
        # Library Branch
        "library": {
            "title": "The Ancient Library",
            "text": "Dusty tomes line the walls. An old sage notices your presence.",
            "choices": [
                {"text": "Ask about the forgotten kingdom (1)", "next_scene": "library_lore"},
                {"text": "Search for magical texts (2)", "next_scene": "library_search"}
            ]
        },
        
        "library_lore": {
            "title": "Kingdom's History",
            "text": "The sage tells of a kingdom lost to dark magic.\nA crystal shard might help restore it.",
            "choices": [
                {"text": "Seek the crystal shard (1)", "next_scene": "mountain", "background": "mountain"},
                {"text": "Return to village (2)", "next_scene": "village", "background": "village"}
            ]
        },
        
        # Tavern Branch
        "tavern": {
            "title": "The Rusty Barrel Tavern",
            "text": "The tavern is filled with mysterious characters.\nWhat catches your attention?",
            "choices": [
                {"text": "Approach the hooded merchant (1)", "next_scene": "merchant"},
                {"text": "Listen to the bard's tale (2)", "next_scene": "bard_tale"}
            ]
        },
        
        # Forest Branch
        "forest": {
            "title": "The Whispering Forest",
            "text": "Ancient trees loom overhead. You hear distant whispers.",
            "choices": [
                {"text": "Follow the hidden path (1)", "next_scene": "temple", "background": "temple"},
                {"text": "Investigate the cave (2)", "next_scene": "cave", "background": "cave"}
            ]
        },
        
        # Mountain Branch
        "mountain": {
            "title": "The Frost Peak",
            "text": "The bitter cold bites at your skin.\nThe crystal shard is said to be nearby.",
            "choices": [
                {"text": "Climb to the peak (1)", "next_scene": "peak_battle"},
                {"text": "Search the abandoned mine (2)", "next_scene": "mine_exploration"}
            ]
        },
        
        # Temple Branch
        "temple": {
            "title": "The Forgotten Temple",
            "text": "Ancient magic pulses through the air.\nThe temple holds many secrets.",
            "choices": [
                {"text": "Explore the inner sanctum (1)", "next_scene": "sanctum"},
                {"text": "Decipher the wall runes (2)", "next_scene": "temple_runes"}
            ]
        },
        
        # Palace Branch (unlocked after getting required items)
        "palace": {
            "title": "The Lost Palace",
            "text": "You finally reach the legendary palace.\nIts magic awaits restoration.",
            "choices": [
                {"text": "Use the crystal shard (1)", "next_scene": "palace_restoration"},
                {"text": "Search for more clues (2)", "next_scene": "palace_search"}
            ]
        }
    }
    
    # Add more scenes with their specific conditions and outcomes
    special_scenes = {
        "merchant": {
            "title": "The Mysterious Merchant",
            "text": "The merchant offers to trade valuable information\nfor 30 gold pieces.",
            "action": lambda: trade_with_merchant()
        },
        "peak_battle": {
            "title": "Battle at the Peak",
            "text": "A frost guardian protects the crystal shard!\nPrepare for battle!",
            "action": lambda: handle_battle("frost_guardian")
        },
        # Add more special scenes...
    }
    
    current = scenes.get(game_state.current_scene)
    if current:
        display_text(current["title"], 50, True)
        display_text(current["text"], 150)
        game_state.choices = current["choices"]
        if len(current["choices"]) > 2:  # Display third choice if exists
            display_text(current["choices"][2]["text"], HEIGHT - 90)
    
    # Display choices
    if hasattr(game_state, 'choices') and game_state.choices:
        for i, choice in enumerate(game_state.choices[:2]):  # Display first two choices
            text_surface = main_font.render(choice["text"], True, LIGHT_BLUE)
            screen.blit(text_surface, (50, HEIGHT - 150 + i * 40))
    
    # Draw character with animation
    hover_offset = abs(pygame.time.get_ticks() % 1000 - 500) / 50
    character_img = character_states[game_state.character_state]
    screen.blit(character_img, (game_state.character_x, game_state.character_y + hover_offset))
    
    pygame.display.flip()

def trade_with_merchant():
    if game_state.player_stats["gold"] >= 30:
        game_state.player_stats["gold"] -= 30
        game_state.quest_progress["magic_map"] = True
        return "merchant_success"
    return "merchant_failure"

def handle_battle(enemy_type):
    game_state.character_state = "battle"
    # Add battle mechanics here
    success = random.random() > 0.5
    game_state.character_state = "normal"
    if success:
        game_state.player_stats["reputation"] += 10
        return "battle_victory"
    game_state.player_stats["health"] -= 20
    return "battle_defeat"

def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and game_state.choices:
                    next_scene = game_state.choices[0]["next_scene"]
                    game_state.current_scene = next_scene
                    if "background" in game_state.choices[0]:
                        game_state.background = game_state.choices[0]["background"]
                elif event.key == pygame.K_2 and game_state.choices:
                    next_scene = game_state.choices[1]["next_scene"]
                    game_state.current_scene = next_scene
                    if "background" in game_state.choices[1]:
                        game_state.background = game_state.choices[1]["background"]
                elif event.key == pygame.K_3 and len(game_state.choices) > 2:
                    next_scene = game_state.choices[2]["next_scene"]
                    game_state.current_scene = next_scene
                    if "background" in game_state.choices[2]:
                        game_state.background = game_state.choices[2]["background"]

        handle_scene()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()