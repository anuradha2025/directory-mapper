#!/usr/bin/env python3
"""
Screenshot demo script for Directory Mapper GUI.
This script shows the GUI and takes a screenshot for demonstration.
"""

import tkinter as tk
from directory_mapper_gui import DirectoryMapperGUI
import os

def demo_gui():
    """Create and display the GUI for screenshot."""
    root = tk.Tk()
    app = DirectoryMapperGUI(root)
    
    # Set a demo directory path to show functionality
    app.directory_path.set("/tmp/testdir")
    app.update_gitignore_status()
    
    # Add some demo content to the output area
    demo_content = """
|_testdir
    |_test.txt
    |_subdir
        |_sub.txt
        |_another_file.py
    |_config
        |_settings.json
        |_database.db"""
    
    app.output_text.insert(1.0, demo_content.strip())
    app.save_btn.config(state="normal")
    app.status_bar.config(text="Demo: Directory map generated for testdir (8 items)")
    
    # Take screenshot after a brief delay
    root.after(1000, lambda: take_screenshot(root))
    
    root.mainloop()

def take_screenshot(root):
    """Take a screenshot of the GUI window."""
    try:
        import PIL.ImageGrab as ImageGrab
        
        # Get window position and size
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        x1 = x + root.winfo_width()
        y1 = y + root.winfo_height()
        
        # Take screenshot
        img = ImageGrab.grab(bbox=(x, y, x1, y1))
        img.save('/home/runner/work/directory-mapper/directory-mapper/gui_screenshot.png')
        print("Screenshot saved to gui_screenshot.png")
        
    except ImportError:
        print("PIL not available for screenshot")
    except Exception as e:
        print(f"Screenshot failed: {e}")
    
    # Close after screenshot
    root.after(2000, root.quit)

if __name__ == "__main__":
    demo_gui()