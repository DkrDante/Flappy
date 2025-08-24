import pygame
import os
import subprocess
import sys

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("comicsans", 30)
TITLE_FONT = pygame.font.SysFont("comicsans", 60)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird - Main Menu")

# Load background
bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900)
)

class MenuItem:
    def __init__(self, text, description, command, key):
        self.text = text
        self.description = description
        self.command = command
        self.key = key

class MainMenu:
    def __init__(self):
        self.selected_option = 0
        self.menu_items = [
            MenuItem("Human Mode", "Play Flappy Bird yourself", "human_mode.py", "1"),
            MenuItem("AI Training", "Train AI using NEAT algorithm", "flappy_bird.py", "2"),
            MenuItem("AI Analyzer", "Analyze and visualize AI networks", "ai_analyzer.py", "3"),
            MenuItem("Leaderboard", "View high scores and statistics", "leaderboard.py", "4"),
            MenuItem("Settings", "Configure game options", "settings.py", "5"),
            MenuItem("Exit", "Close the game", "exit", "6")
        ]
    
    def draw_menu(self):
        WIN.blit(bg_img, (0, 0))
        
        # Title
        title = TITLE_FONT.render("FLAPPY BIRD", 1, (255, 255, 255))
        WIN.blit(title, (WIN_WIDTH//2 - title.get_width()//2, 60))
        
        subtitle = SMALL_FONT.render("Enhanced Edition", 1, (200, 200, 200))
        WIN.blit(subtitle, (WIN_WIDTH//2 - subtitle.get_width()//2, 130))
        
        # Menu options with better spacing
        for i, item in enumerate(self.menu_items):
            # Calculate position with better spacing
            y_pos = 180 + i * 85  # Increased spacing between items
            
            # Highlight selected option
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            bg_color = (50, 50, 50) if i == self.selected_option else (0, 0, 0)
            
            # Draw background for selected item
            if i == self.selected_option:
                pygame.draw.rect(WIN, bg_color, (40, y_pos - 5, WIN_WIDTH - 80, 75))
                pygame.draw.rect(WIN, (255, 255, 0), (40, y_pos - 5, WIN_WIDTH - 80, 75), 3)
            
            # Draw option text
            option_text = f"{item.key}. {item.text}"
            text = STAT_FONT.render(option_text, 1, color)
            WIN.blit(text, (60, y_pos))
            
            # Draw description with better positioning
            desc = SMALL_FONT.render(item.description, 1, (200, 200, 200))
            WIN.blit(desc, (60, y_pos + 35))
        
        # Instructions at the bottom
        instructions = [
            "Use UP/DOWN arrows or number keys to navigate",
            "Press ENTER or SPACE to select",
            "Press ESC to exit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = SMALL_FONT.render(instruction, 1, (150, 150, 150))
            WIN.blit(text, (50, 680 + i * 25))
        
        pygame.display.update()
    
    def run_selected_option(self):
        """Run the selected menu option"""
        selected_item = self.menu_items[self.selected_option]
        
        if selected_item.command == "exit":
            return False
        
        try:
            print(f"Starting {selected_item.text}...")
            
            # Check if the file exists
            if not os.path.exists(selected_item.command):
                print(f"Error: {selected_item.command} not found!")
                return True
            
            # Launch the selected program
            if sys.platform.startswith('win'):
                # Windows
                subprocess.Popen([sys.executable, selected_item.command])
            else:
                # macOS/Linux
                subprocess.Popen([sys.executable, selected_item.command])
            
            print(f"{selected_item.text} launched successfully!")
            
        except Exception as e:
            print(f"Error launching {selected_item.text}: {e}")
        
        return True
    
    def handle_input(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.run_selected_option()
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]:
                    # Number key selection
                    key_pressed = str(event.key - pygame.K_0)
                    for i, item in enumerate(self.menu_items):
                        if item.key == key_pressed:
                            self.selected_option = i
                            return self.run_selected_option()
        
        return True

def main():
    menu = MainMenu()
    run = True
    
    print("Flappy Bird Enhanced Edition - Main Menu")
    print("Use arrow keys or number keys to navigate")
    print("Press ENTER or SPACE to select an option")
    
    while run:
        menu.draw_menu()
        run = menu.handle_input()
    
    pygame.quit()
    print("Goodbye! Thanks for playing Flappy Bird!")
    quit()

if __name__ == "__main__":
    main()
