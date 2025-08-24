import pygame
import json
import os

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("comicsans", 30)
TITLE_FONT = pygame.font.SysFont("comicsans", 50)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Settings")

# Load background
bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900)
)

class Settings:
    def __init__(self):
        self.settings_file = "game_settings.json"
        self.default_settings = {
            "difficulty": "normal",
            "sound_enabled": True,
            "music_volume": 0.7,
            "sfx_volume": 0.8,
            "ai_population_size": 100,
            "ai_generations": 50,
            "ai_speed": 10,
            "show_lines": False,
            "auto_save": True
        }
        self.current_settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create default"""
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except:
            return self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to file"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.current_settings, f, indent=2)
    
    def get_setting(self, key):
        """Get a specific setting value"""
        return self.current_settings.get(key, self.default_settings.get(key))
    
    def set_setting(self, key, value):
        """Set a specific setting value"""
        self.current_settings[key] = value
        self.save_settings()

class SettingsMenu:
    def __init__(self):
        self.settings = Settings()
        self.selected_option = 0
        self.options = [
            ("Difficulty", ["easy", "normal", "hard"]),
            ("Sound", ["on", "off"]),
            ("Music Volume", ["0.3", "0.5", "0.7", "0.9"]),
            ("AI Population", ["50", "100", "150", "200"]),
            ("AI Speed", ["5", "10", "15", "20"]),
            ("Show Lines", ["on", "off"]),
            ("Auto Save", ["on", "off"])
        ]
    
    def draw_menu(self):
        WIN.blit(bg_img, (0, 0))
        
        # Title
        title = TITLE_FONT.render("SETTINGS", 1, (255, 255, 255))
        WIN.blit(title, (WIN_WIDTH//2 - title.get_width()//2, 50))
        
        # Settings options
        for i, (option_name, values) in enumerate(self.options):
            # Get current value
            if option_name == "Difficulty":
                current_value = self.settings.get_setting("difficulty")
            elif option_name == "Sound":
                current_value = "on" if self.settings.get_setting("sound_enabled") else "off"
            elif option_name == "Music Volume":
                current_value = str(self.settings.get_setting("music_volume"))
            elif option_name == "AI Population":
                current_value = str(self.settings.get_setting("ai_population_size"))
            elif option_name == "AI Speed":
                current_value = str(self.settings.get_setting("ai_speed"))
            elif option_name == "Show Lines":
                current_value = "on" if self.settings.get_setting("show_lines") else "off"
            elif option_name == "Auto Save":
                current_value = "on" if self.settings.get_setting("auto_save") else "off"
            
            # Highlight selected option
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            
            # Draw option name
            option_text = STAT_FONT.render(f"{option_name}: {current_value}", 1, color)
            WIN.blit(option_text, (50, 150 + i * 60))
            
            # Draw arrow indicators for selected option
            if i == self.selected_option:
                left_arrow = STAT_FONT.render("<", 1, (255, 255, 0))
                right_arrow = STAT_FONT.render(">", 1, (255, 255, 0))
                WIN.blit(left_arrow, (20, 150 + i * 60))
                WIN.blit(right_arrow, (WIN_WIDTH - 40, 150 + i * 60))
        
        # Instructions
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Use LEFT/RIGHT arrows to change values",
            "Press ENTER to save and exit",
            "Press ESC to exit without saving"
        ]
        
        for i, instruction in enumerate(instructions):
            text = STAT_FONT.render(instruction, 1, (200, 200, 200))
            WIN.blit(text, (50, 600 + i * 30))
        
        pygame.display.update()
    
    def change_value(self, direction):
        """Change the value of the selected setting"""
        option_name, values = self.options[self.selected_option]
        current_value = None
        
        # Get current value
        if option_name == "Difficulty":
            current_value = self.settings.get_setting("difficulty")
        elif option_name == "Sound":
            current_value = "on" if self.settings.get_setting("sound_enabled") else "off"
        elif option_name == "Music Volume":
            current_value = str(self.settings.get_setting("music_volume"))
        elif option_name == "AI Population":
            current_value = str(self.settings.get_setting("ai_population_size"))
        elif option_name == "AI Speed":
            current_value = str(self.settings.get_setting("ai_speed"))
        elif option_name == "Show Lines":
            current_value = "on" if self.settings.get_setting("show_lines") else "off"
        elif option_name == "Auto Save":
            current_value = "on" if self.settings.get_setting("auto_save") else "off"
        
        # Find current index and change
        try:
            current_index = values.index(current_value)
            new_index = (current_index + direction) % len(values)
            new_value = values[new_index]
            
            # Update setting
            if option_name == "Difficulty":
                self.settings.set_setting("difficulty", new_value)
            elif option_name == "Sound":
                self.settings.set_setting("sound_enabled", new_value == "on")
            elif option_name == "Music Volume":
                self.settings.set_setting("music_volume", float(new_value))
            elif option_name == "AI Population":
                self.settings.set_setting("ai_population_size", int(new_value))
            elif option_name == "AI Speed":
                self.settings.set_setting("ai_speed", int(new_value))
            elif option_name == "Show Lines":
                self.settings.set_setting("show_lines", new_value == "on")
            elif option_name == "Auto Save":
                self.settings.set_setting("auto_save", new_value == "on")
        except:
            pass

def main():
    menu = SettingsMenu()
    run = True
    
    while run:
        menu.draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu.selected_option = (menu.selected_option - 1) % len(menu.options)
                elif event.key == pygame.K_DOWN:
                    menu.selected_option = (menu.selected_option + 1) % len(menu.options)
                elif event.key == pygame.K_LEFT:
                    menu.change_value(-1)
                elif event.key == pygame.K_RIGHT:
                    menu.change_value(1)
                elif event.key == pygame.K_RETURN:
                    menu.settings.save_settings()
                    run = False
                elif event.key == pygame.K_ESCAPE:
                    run = False
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
