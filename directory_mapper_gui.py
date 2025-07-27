#!/usr/bin/env python3
"""
Directory Mapper GUI - A Tkinter-based interface for the directory mapping tool.

This GUI provides an easy-to-use interface for generating directory structure maps
with optional .gitignore exclusion support.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from dirmap import map_directory, read_gitignore


class DirectoryMapperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Mapper")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Variables
        self.directory_path = tk.StringVar()
        self.exclude_gitignore = tk.BooleanVar(value=True)
        self.output_text = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the main user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Directory selection section
        dir_frame = ttk.LabelFrame(main_frame, text="Directory Selection", padding="5")
        dir_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        dir_frame.columnconfigure(1, weight=1)
        
        # Directory path input
        ttk.Label(dir_frame, text="Directory Path:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.directory_path, width=50)
        self.dir_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Browse button
        self.browse_btn = ttk.Button(dir_frame, text="Browse...", command=self.browse_directory)
        self.browse_btn.grid(row=0, column=2, sticky=tk.W)
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Gitignore checkbox
        self.gitignore_check = ttk.Checkbutton(
            options_frame, 
            text="Exclude files and folders from .gitignore file",
            variable=self.exclude_gitignore
        )
        self.gitignore_check.grid(row=0, column=0, sticky=tk.W)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        button_frame.columnconfigure(0, weight=1)
        
        # Generate button
        self.generate_btn = ttk.Button(
            button_frame, 
            text="Generate Directory Map", 
            command=self.generate_map
        )
        self.generate_btn.grid(row=0, column=0, sticky=tk.W)
        
        # Save button
        self.save_btn = ttk.Button(
            button_frame, 
            text="Save to File", 
            command=self.save_to_file,
            state="disabled"
        )
        self.save_btn.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Clear button
        self.clear_btn = ttk.Button(
            button_frame, 
            text="Clear Output", 
            command=self.clear_output
        )
        self.clear_btn.grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Directory Structure", padding="5")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Text widget with scrollbar
        self.output_text = scrolledtext.ScrolledText(
            output_frame, 
            wrap=tk.NONE, 
            width=80, 
            height=20,
            font=("Courier New", 10)
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(
            title="Select Directory to Map",
            initialdir=os.getcwd()
        )
        if directory:
            self.directory_path.set(directory)
            self.update_gitignore_status()
    
    def update_gitignore_status(self):
        """Update the gitignore checkbox based on whether .gitignore exists."""
        path = self.directory_path.get()
        if path and os.path.isdir(path):
            gitignore_path = os.path.join(path, ".gitignore")
            if os.path.exists(gitignore_path):
                self.gitignore_check.config(state="normal")
                self.status_bar.config(text=f".gitignore found in {os.path.basename(path)}")
            else:
                self.gitignore_check.config(state="disabled")
                self.status_bar.config(text=f"No .gitignore found in {os.path.basename(path)}")
        else:
            self.gitignore_check.config(state="normal")
            self.status_bar.config(text="Ready")
    
    def generate_map(self):
        """Generate the directory map in a separate thread."""
        path = self.directory_path.get().strip()
        
        if not path:
            messagebox.showerror("Error", "Please select a directory path.")
            return
            
        if not os.path.isdir(path):
            messagebox.showerror("Error", f"'{path}' is not a valid directory.")
            return
        
        # Disable controls during generation
        self.set_controls_state("disabled")
        self.status_bar.config(text="Generating directory map...")
        
        # Run mapping in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self._generate_map_thread, args=(path,))
        thread.daemon = True
        thread.start()
    
    def _generate_map_thread(self, path):
        """Generate map in separate thread."""
        try:
            exclude_ignore = self.exclude_gitignore.get()
            tree_content = map_directory(path, exclude_ignore)
            
            # Update GUI in main thread
            self.root.after(0, self._update_output, tree_content, path)
            
        except Exception as e:
            error_msg = f"Error generating directory map: {str(e)}"
            self.root.after(0, self._show_error, error_msg)
    
    def _update_output(self, tree_content, path):
        """Update the output text widget with generated content."""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, tree_content)
        
        # Enable save button
        self.save_btn.config(state="normal")
        
        # Re-enable controls
        self.set_controls_state("normal")
        
        # Update status
        self.status_bar.config(
            text=f"Directory map generated for {os.path.basename(path)} ({len(tree_content.splitlines())} items)"
        )
    
    def _show_error(self, error_msg):
        """Show error message and re-enable controls."""
        messagebox.showerror("Error", error_msg)
        self.set_controls_state("normal")
        self.status_bar.config(text="Error occurred during generation")
    
    def set_controls_state(self, state):
        """Enable or disable control buttons."""
        self.generate_btn.config(state=state)
        self.browse_btn.config(state=state)
        self.dir_entry.config(state=state)
        if state == "disabled":
            self.save_btn.config(state="disabled")
    
    def save_to_file(self):
        """Save the current output to a file."""
        content = self.output_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No content to save.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Directory Map",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="directory_map.txt"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(content + '\n')
                messagebox.showinfo("Success", f"Directory map saved to {filename}")
                self.status_bar.config(text=f"Saved to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def clear_output(self):
        """Clear the output text widget."""
        self.output_text.delete(1.0, tk.END)
        self.save_btn.config(state="disabled")
        self.status_bar.config(text="Output cleared")


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = DirectoryMapperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()