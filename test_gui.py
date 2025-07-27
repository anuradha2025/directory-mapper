#!/usr/bin/env python3
"""
Test script for Directory Mapper GUI functionality.

This script tests the GUI components without actually displaying the window.
"""

import os
import sys
import tempfile
import shutil

# Test the GUI module can be imported and initialized
def test_gui_import():
    """Test that GUI module can be imported."""
    try:
        import tkinter as tk
        from directory_mapper_gui import DirectoryMapperGUI
        print("✓ GUI module imports successfully")
        return True
    except Exception as e:
        print(f"✗ GUI import failed: {e}")
        return False

def test_dirmap_functionality():
    """Test the core directory mapping functionality."""
    try:
        from dirmap import map_directory, read_gitignore, is_ignored
        
        # Create a temporary test directory structure
        test_dir = tempfile.mkdtemp()
        
        # Create some test files and directories
        os.makedirs(os.path.join(test_dir, "subdir1"))
        os.makedirs(os.path.join(test_dir, "subdir2"))
        
        with open(os.path.join(test_dir, "file1.txt"), 'w') as f:
            f.write("test content")
        
        with open(os.path.join(test_dir, "subdir1", "file2.txt"), 'w') as f:
            f.write("test content 2")
            
        with open(os.path.join(test_dir, ".gitignore"), 'w') as f:
            f.write("*.log\n__pycache__/\n")
        
        # Test mapping without gitignore
        result1 = map_directory(test_dir, exclude_ignore=False)
        assert len(result1) > 0, "Map should return content"
        assert "file1.txt" in result1, "Should contain test file"
        
        # Test mapping with gitignore
        result2 = map_directory(test_dir, exclude_ignore=True)
        assert len(result2) > 0, "Map should return content with gitignore"
        
        # Test gitignore reading
        patterns = read_gitignore(os.path.join(test_dir, ".gitignore"))
        assert "*.log" in patterns, "Should read gitignore patterns"
        
        # Cleanup
        shutil.rmtree(test_dir)
        
        print("✓ Core directory mapping functionality works")
        return True
        
    except Exception as e:
        print(f"✗ Directory mapping test failed: {e}")
        return False

def test_gui_initialization():
    """Test GUI can be initialized without display."""
    try:
        import tkinter as tk
        from directory_mapper_gui import DirectoryMapperGUI
        
        # Create root window but don't show it
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Initialize the GUI
        app = DirectoryMapperGUI(root)
        
        # Test that key attributes exist
        assert hasattr(app, 'directory_path'), "GUI should have directory_path variable"
        assert hasattr(app, 'exclude_gitignore'), "GUI should have exclude_gitignore variable"
        assert hasattr(app, 'output_text'), "GUI should have output_text widget"
        assert hasattr(app, 'generate_map'), "GUI should have generate_map method"
        
        # Test variable initialization
        assert app.exclude_gitignore.get() == True, "Default should exclude gitignore"
        
        root.destroy()
        
        print("✓ GUI initialization test passed")
        return True
        
    except Exception as e:
        print(f"✗ GUI initialization test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("Running Directory Mapper Tests...")
    print("=" * 40)
    
    tests = [
        test_gui_import,
        test_dirmap_functionality,
        test_gui_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! GUI is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)