#!/usr/bin/env python
import subprocess
import sys
import time
from pynput import keyboard
import threading
# Global variables
game_window_id = None
terminal_window_id = None
listener = None
def on_f12_press(key):
    global terminal_window_id
    
    if key == keyboard.Key.f12 and terminal_window_id:
        # Switch to the terminal window when F12 is pressed
        subprocess.run(['xdotool', 'windowactivate', terminal_window_id])
        return True
def start_keyboard_listener():
    global listener
    # Start keyboard listener in a non-blocking way
    listener = keyboard.Listener(on_press=on_f12_press)
    listener.start()
def yup():
    AAm = -0.23709
    AAb = 1001.525
    
    global game_window_id, terminal_window_id
    
    # First-time setup to capture window IDs
    if game_window_id is None:
        # First capture the terminal window ID
        result = subprocess.run(['xdotool', 'getactivewindow'], capture_output=True, text=True)
        terminal_window_id = result.stdout.strip()
        print(f"Terminal window ID saved: {terminal_window_id}")
        
        print("\n--- SETUP ---")
        print("We need to capture your game window ID.")
        print("1. After pressing Enter here, you'll have 5 seconds to switch to your game")
        print("2. Make sure your game window is active/focused within that time")
        input("Press Enter to start the 5-second countdown...")
        
        print("Switching to game in:")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        
        # Get the active window ID (should be the game now)
        result = subprocess.run(['xdotool', 'getactivewindow'], capture_output=True, text=True)
        game_window_id = result.stdout.strip()
        
        # Activate the terminal window again
        subprocess.run(['xdotool', 'windowactivate', terminal_window_id])
        
        print(f"\nGame window ID saved: {game_window_id}")
        print("--- SETUP COMPLETE ---\n")
        print("Now, whenever you need to calculate artillery:")
        print("1. Press F12 in your game to switch to this calculator")
        print("2. Enter the distance")
        print("3. It will automatically switch back to your game")
        print("")
        
        # Start the keyboard listener after we have both window IDs
        start_keyboard_listener()
    try:
        dist = input("Enter Artillery distance (or 'q' to quit): ")
        
        if dist.lower() == 'q':
            if listener:
                listener.stop()
            print("Exiting artillery calculator...")
            sys.exit(0)
        
        # Calculate mil and round to the nearest 10th (1 decimal place)
        mil = AAm * float(dist) + AAb
        rounded_mil = round(mil, 1)  # Round to 1 decimal place (10th)
        
        print('DISTANCE ENT:    ', dist)
        print("++++++")
        print('MILS TO TGT:     ', rounded_mil)  # Display the rounded value
        print("++++++")
        print("")
        
        # Switch back to game window after showing the result
        print("Switching back to game...")
        subprocess.run(['xdotool', 'windowactivate', game_window_id])
        
    except ValueError:
        print("Invalid input. Please enter a number.")
        # Still switch back to game even on error
        print("Switching back to game...")
        subprocess.run(['xdotool', 'windowactivate', game_window_id])
    # Call yup again (after a short delay to ensure window switching completes)
    time.sleep(0.5)
    yup()
# Start the artillery calculator
print("HLL Artillery Calculator")
print("=======================")
print("This script will help you calculate artillery settings and automatically")
print("switch back to your game after each calculation.")
yup()
