import pygame
import pickle
import neat
import os
import matplotlib.pyplot as plt
import numpy as np

pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600
STAT_FONT = pygame.font.SysFont("comicsans", 20)
BIG_FONT = pygame.font.SysFont("comicsans", 40)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("AI Analyzer")

class AIAnalyzer:
    def __init__(self):
        self.best_network = None
        self.config = None
        self.stats = None
        self.current_view = "main"  # main, network, stats
        
    def load_best_ai(self):
        """Load the best trained AI"""
        try:
            with open("best.pickle", "rb") as f:
                self.best_network = pickle.load(f)
            print("Loaded best AI successfully!")
            return True
        except Exception as e:
            print(f"No trained AI found or error loading: {e}")
            return False
    
    def load_config(self):
        """Load NEAT configuration"""
        try:
            local_dir = os.path.dirname(__file__)
            config_path = os.path.join(local_dir, "config-feedforward.txt")
            self.config = neat.config.Config(
                neat.DefaultGenome,
                neat.DefaultReproduction,
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation,
                config_path,
            )
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    def analyze_network(self):
        """Analyze the neural network structure"""
        if not self.best_network:
            return "No AI loaded - Train an AI first!"
        
        if not self.config:
            return "Configuration not loaded!"
        
        try:
            # Detect number of inputs by testing the network
            try:
                # Try 3 inputs first (new simplified version)
                test_inputs_3 = [0.5, 0.3, 0.1]
                output_3 = self.best_network.activate(test_inputs_3)
                input_nodes = 3
                input_description = "(Bird Y, Distance to Pipe, Velocity)"
            except:
                try:
                    # Try 6 inputs (previous version)
                    test_inputs_6 = [0.5, 0.3, 0.1, 0.2, 0.4, 0.6]
                    output_6 = self.best_network.activate(test_inputs_6)
                    input_nodes = 6
                    input_description = "(Bird Y, Pipe Distances, Velocity, Pipe Gap)"
                except:
                    # Try 7 inputs (enhanced version)
                    test_inputs_7 = [0.5, 0.3, 0.1, 0.2, 0.4, 0.6, 0.7]
                    output_7 = self.best_network.activate(test_inputs_7)
                    input_nodes = 7
                    input_description = "(Enhanced with difficulty)"
            
            output_nodes = 1
            
            # Use the appropriate output
            if input_nodes == 3:
                sample_output = output_3[0]
            elif input_nodes == 6:
                sample_output = output_6[0]
            else:
                sample_output = output_7[0]
            
            analysis = f"""Neural Network Analysis:
Input Nodes: {input_nodes} {input_description}
Output Nodes: {output_nodes} (Jump Decision)
Network Type: FeedForward
Sample Output: {sample_output:.3f}
Status: Ready for Analysis"""
            return analysis
        except Exception as e:
            return f"Error analyzing network: {e}"
    
    def visualize_network(self):
        """Create a visual representation of the network"""
        if not self.best_network or not self.config:
            return
        
        try:
            # Detect number of inputs
            try:
                test_inputs_3 = [0.5, 0.3, 0.1]
                self.best_network.activate(test_inputs_3)
                input_nodes = 3
                input_labels = ["Bird Y", "Pipe Dist", "Velocity"]
            except:
                try:
                    test_inputs_6 = [0.5, 0.3, 0.1, 0.2, 0.4, 0.6]
                    self.best_network.activate(test_inputs_6)
                    input_nodes = 6
                    input_labels = ["Bird Y", "Pipe Bottom", "Pipe Top", "Velocity", "Pipe Dist", "Gap Center"]
                except:
                    test_inputs_7 = [0.5, 0.3, 0.1, 0.2, 0.4, 0.6, 0.7]
                    self.best_network.activate(test_inputs_7)
                    input_nodes = 7
                    input_labels = ["Bird Y", "Pipe Bottom", "Pipe Top", "Velocity", "Pipe Dist", "Gap Center", "Difficulty"]
            
            # Create a simple network visualization
            WIN.fill((0, 0, 0))
            
            # Draw title
            title = BIG_FONT.render(f"Neural Network Visualization ({input_nodes} Inputs)", 1, (255, 255, 255))
            WIN.blit(title, (WIN_WIDTH//2 - title.get_width()//2, 20))
            
            # Draw simplified network
            node_positions = {}
            
            # Input nodes (left side)
            input_y_start = 100
            input_spacing = min(60, 400 // input_nodes)  # Adjust spacing based on number of inputs
            
            for i in range(input_nodes):
                y = input_y_start + i * input_spacing
                node_positions[f"input_{i}"] = (150, y)
                pygame.draw.circle(WIN, (0, 255, 0), (150, y), 20)
                
                # Truncate label if too long
                label = input_labels[i] if i < len(input_labels) else f"Input {i+1}"
                if len(label) > 8:
                    label = label[:8] + "..."
                text = STAT_FONT.render(label, 1, (255, 255, 255))
                WIN.blit(text, (50, y-10))
            
            # Output node (right side)
            output_y = 200
            node_positions["output_0"] = (650, output_y)
            pygame.draw.circle(WIN, (255, 0, 0), (650, output_y), 25)
            text = STAT_FONT.render("JUMP", 1, (255, 255, 255))
            WIN.blit(text, (680, output_y-10))
            
            # Draw connections (simplified)
            for i in range(input_nodes):
                start_pos = node_positions[f"input_{i}"]
                end_pos = node_positions["output_0"]
                pygame.draw.line(WIN, (255, 255, 255), start_pos, end_pos, 2)
            
            # Network info
            info_text = [
                f"Network Configuration:",
                f"• {input_nodes} Input Nodes",
                f"• 1 Output Node (Jump Decision)",
                "",
                "Input Parameters:"
            ]
            
            # Add input descriptions
            for i, label in enumerate(input_labels):
                info_text.append(f"• {label}")
            
            # Limit display to fit screen
            max_lines = 15
            if len(info_text) > max_lines:
                info_text = info_text[:max_lines-1] + ["..."]
            
            for i, text in enumerate(info_text):
                color = (255, 255, 0) if i == 0 else (200, 200, 200)
                rendered_text = STAT_FONT.render(text, 1, color)
                WIN.blit(rendered_text, (50, 450 + i * 20))
            
            # Instructions
            instructions = [
                "Press ESC to return to main menu",
                "Press A to analyze network",
                "Press P to plot training stats"
            ]
            
            for i, instruction in enumerate(instructions):
                text = STAT_FONT.render(instruction, 1, (150, 150, 150))
                WIN.blit(text, (50, 550 + i * 25))
            
            pygame.display.update()
            
        except Exception as e:
            print(f"Error in visualization: {e}")
    
    def plot_training_stats(self):
        """Plot training statistics if available"""
        try:
            if os.path.exists("training_stats.json"):
                import json
                with open("training_stats.json", "r") as f:
                    stats = json.load(f)
                
                plt.figure(figsize=(12, 8))
                
                # Plot fitness over generations
                plt.subplot(2, 2, 1)
                plt.plot(stats['generations'], stats['best_fitness'], 'b-', label='Best Fitness')
                plt.plot(stats['generations'], stats['avg_fitness'], 'r-', label='Average Fitness')
                plt.xlabel('Generation')
                plt.ylabel('Fitness')
                plt.title('Fitness Over Generations')
                plt.legend()
                plt.grid(True)
                
                plt.tight_layout()
                plt.show()
                return "Training stats plotted successfully!"
            else:
                return "No training statistics found. Run enhanced AI training first."
        except Exception as e:
            return f"Error plotting stats: {e}"

def draw_main_menu():
    """Draw the main analyzer menu"""
    WIN.fill((0, 0, 0))
    
    # Title
    title = BIG_FONT.render("AI Analyzer", 1, (255, 255, 255))
    WIN.blit(title, (WIN_WIDTH//2 - title.get_width()//2, 50))
    
    # AI Status
    if analyzer.best_network:
        status = "AI Status: Loaded ✓"
        status_color = (0, 255, 0)
    else:
        status = "AI Status: Not Found ✗"
        status_color = (255, 0, 0)
    
    status_text = STAT_FONT.render(status, 1, status_color)
    WIN.blit(status_text, (50, 120))
    
    # Controls
    controls = [
        "Controls:",
        "V - Visualize Network",
        "A - Analyze Network", 
        "P - Plot Training Stats",
        "ESC - Return to Menu"
    ]
    
    for i, control in enumerate(controls):
        color = (255, 255, 0) if i == 0 else (200, 200, 200)
        text = STAT_FONT.render(control, 1, color)
        WIN.blit(text, (50, 180 + i * 30))
    
    # Network Analysis
    if analyzer.best_network:
        analysis = analyzer.analyze_network()
        lines = analysis.split('\n')
        for i, line in enumerate(lines):
            text = STAT_FONT.render(line, 1, (150, 255, 150))
            WIN.blit(text, (50, 350 + i * 25))
    
    pygame.display.update()

def main():
    global analyzer
    analyzer = AIAnalyzer()
    
    # Load AI and config
    analyzer.load_best_ai()
    analyzer.load_config()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if analyzer.current_view == "network":
                        analyzer.current_view = "main"
                    else:
                        running = False
                elif event.key == pygame.K_v:
                    analyzer.current_view = "network"
                elif event.key == pygame.K_a:
                    print(analyzer.analyze_network())
                elif event.key == pygame.K_p:
                    result = analyzer.plot_training_stats()
                    print(result)
        
        # Draw appropriate view
        if analyzer.current_view == "main":
            draw_main_menu()
        elif analyzer.current_view == "network":
            analyzer.visualize_network()
    
    pygame.quit()

if __name__ == "__main__":
    main()
