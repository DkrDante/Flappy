import pygame
import json
import os
from datetime import datetime

pygame.font.init()

WIN_WIDTH = 600
WIN_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("comicsans", 30)
TITLE_FONT = pygame.font.SysFont("comicsans", 50)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Leaderboard")

# Load background
bg_img = pygame.transform.scale(
    pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha(), (600, 900)
)

class Leaderboard:
    def __init__(self):
        self.leaderboard_file = "leaderboard.json"
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Load scores from file"""
        try:
            with open(self.leaderboard_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_scores(self):
        """Save scores to file"""
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.scores, f, indent=2)
    
    def add_score(self, score, player_name="Player", mode="Human"):
        """Add a new score to the leaderboard"""
        new_score = {
            "score": score,
            "player": player_name,
            "mode": mode,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "timestamp": datetime.now().timestamp()
        }
        
        self.scores.append(new_score)
        # Sort by score (highest first)
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Keep only top 10 scores
        self.scores = self.scores[:10]
        self.save_scores()
    
    def get_top_scores(self, limit=10):
        """Get top scores"""
        return self.scores[:limit]
    
    def get_player_best(self, player_name):
        """Get best score for a specific player"""
        player_scores = [s for s in self.scores if s["player"] == player_name]
        if player_scores:
            return max(player_scores, key=lambda x: x["score"])
        return None
    
    def get_mode_scores(self, mode):
        """Get scores for a specific mode"""
        return [s for s in self.scores if s["mode"] == mode]

class LeaderboardDisplay:
    def __init__(self):
        self.leaderboard = Leaderboard()
        self.current_mode = "All"
        self.modes = ["All", "Human", "AI"]
    
    def draw_leaderboard(self):
        WIN.blit(bg_img, (0, 0))
        
        # Title
        title = TITLE_FONT.render("LEADERBOARD", 1, (255, 255, 255))
        WIN.blit(title, (WIN_WIDTH//2 - title.get_width()//2, 30))
        
        # Mode selector
        mode_text = STAT_FONT.render(f"Mode: {self.current_mode}", 1, (255, 255, 0))
        WIN.blit(mode_text, (50, 100))
        
        # Get scores based on current mode
        if self.current_mode == "All":
            scores = self.leaderboard.get_top_scores()
        else:
            scores = self.leaderboard.get_mode_scores(self.current_mode)
        
        # Draw scores
        if scores:
            # Header
            header_y = 150
            rank_text = SMALL_FONT.render("Rank", 1, (255, 255, 0))
            score_text = SMALL_FONT.render("Score", 1, (255, 255, 0))
            player_text = SMALL_FONT.render("Player", 1, (255, 255, 0))
            mode_text = SMALL_FONT.render("Mode", 1, (255, 255, 0))
            date_text = SMALL_FONT.render("Date", 1, (255, 255, 0))
            
            WIN.blit(rank_text, (50, header_y))
            WIN.blit(score_text, (120, header_y))
            WIN.blit(player_text, (200, header_y))
            WIN.blit(mode_text, (300, header_y))
            WIN.blit(date_text, (380, header_y))
            
            # Score entries
            for i, score_data in enumerate(scores):
                y = header_y + 40 + i * 35
                
                # Rank
                rank = SMALL_FONT.render(f"{i+1}.", 1, (255, 255, 255))
                WIN.blit(rank, (50, y))
                
                # Score
                score = SMALL_FONT.render(str(score_data["score"]), 1, (255, 255, 255))
                WIN.blit(score, (120, y))
                
                # Player name
                player = SMALL_FONT.render(score_data["player"][:10], 1, (255, 255, 255))
                WIN.blit(player, (200, y))
                
                # Mode
                mode = SMALL_FONT.render(score_data["mode"], 1, (255, 255, 255))
                WIN.blit(mode, (300, y))
                
                # Date
                date = SMALL_FONT.render(score_data["date"][:10], 1, (255, 255, 255))
                WIN.blit(date, (380, y))
        else:
            no_scores = STAT_FONT.render("No scores yet!", 1, (255, 255, 255))
            WIN.blit(no_scores, (WIN_WIDTH//2 - no_scores.get_width()//2, 300))
        
        # Instructions
        instructions = [
            "Press LEFT/RIGHT to change mode",
            "Press ESC to exit",
            "Press R to refresh"
        ]
        
        for i, instruction in enumerate(instructions):
            text = SMALL_FONT.render(instruction, 1, (200, 200, 200))
            WIN.blit(text, (50, 700 + i * 25))
        
        pygame.display.update()
    
    def change_mode(self, direction):
        """Change the current mode filter"""
        current_index = self.modes.index(self.current_mode)
        new_index = (current_index + direction) % len(self.modes)
        self.current_mode = self.modes[new_index]

def main():
    display = LeaderboardDisplay()
    run = True
    
    while run:
        display.draw_leaderboard()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    display.change_mode(-1)
                elif event.key == pygame.K_RIGHT:
                    display.change_mode(1)
                elif event.key == pygame.K_r:
                    display.leaderboard = Leaderboard()  # Reload
                elif event.key == pygame.K_ESCAPE:
                    run = False
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
