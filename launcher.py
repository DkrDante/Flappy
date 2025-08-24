#!/usr/bin/env python3
"""
Flappy Bird Enhanced Edition - Command Line Launcher
A simple alternative to the menu system for quick access to different modes.
"""

import os
import sys
import subprocess

def print_banner():
    print("=" * 50)
    print("🐦 FLAPPY BIRD ENHANCED EDITION 🐦")
    print("=" * 50)
    print()

def print_menu():
    print("Available Modes:")
    print("1. Human Mode - Play Flappy Bird yourself")
    print("2. AI Training - Train AI using NEAT algorithm")
    print("3. AI Analyzer - Analyze and visualize AI networks")
    print("4. Leaderboard - View high scores and statistics")
    print("5. Settings - Configure game options")
    print("6. Main Menu - Launch the graphical menu")
    print("0. Exit")
    print()

def launch_program(program_name, description):
    """Launch a Python program"""
    if not os.path.exists(program_name):
        print(f"❌ Error: {program_name} not found!")
        return False
    
    print(f"🚀 Launching {description}...")
    try:
        subprocess.run([sys.executable, program_name], check=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {description}: {e}")
        return False
    except KeyboardInterrupt:
        print(f"\n⏹️  {description} interrupted by user")
        return True

def main():
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == "0":
                print("👋 Goodbye! Thanks for playing Flappy Bird!")
                break
            elif choice == "1":
                launch_program("human_mode.py", "Human Mode")
            elif choice == "2":
                launch_program("flappy_bird.py", "AI Training")
            elif choice == "3":
                launch_program("ai_analyzer.py", "AI Analyzer")
            elif choice == "4":
                launch_program("leaderboard.py", "Leaderboard")
            elif choice == "5":
                launch_program("settings.py", "Settings")
            elif choice == "6":
                launch_program("menu.py", "Main Menu")
            else:
                print("❌ Invalid choice! Please enter a number between 0-6.")
            
            print()
            input("Press Enter to continue...")
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for playing Flappy Bird!")
            break
        except EOFError:
            print("\n👋 Goodbye! Thanks for playing Flappy Bird!")
            break

if __name__ == "__main__":
    main()
