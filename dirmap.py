import os
import fnmatch


def read_gitignore(gitignore_path):
    """Read .gitignore and return patterns to ignore."""
    ignore_patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            for line in gitignore_file:
                # Ignore comments and empty lines
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_patterns.append(line)
    return ignore_patterns


def is_ignored(path, ignore_patterns, base_path):
    """Check if a file or directory should be ignored based on the .gitignore patterns."""
    relative_path = os.path.relpath(path, base_path).replace(os.sep, "/")
    for pattern in ignore_patterns:
        # Handle patterns with leading '/'
        if pattern.startswith("/"):
            pattern = pattern[1:]
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(
            relative_path, os.path.join("**", pattern).replace(os.sep, "/")
        ):
            return True
    return False


def map_directory(start_path, exclude_ignore=True, output_file=None):
    """
    Map the directory structure to 'directory_map.txt', optionally excluding
    files/folders from .gitignore.
    Returns the directory structure as a string.
    """
    if output_file is None:
        output_file = os.path.join(os.getcwd(), "directory_map.txt")
    
    gitignore_path = os.path.join(start_path, ".gitignore")

    # Decide which patterns to use
    if exclude_ignore and os.path.exists(gitignore_path):
        ignore_patterns = read_gitignore(gitignore_path)
    else:
        ignore_patterns = []

    directory_tree = []
    
    for root, dirs, files in os.walk(start_path):
        # Filter directories and files based on ignore patterns
        dirs[:] = [
            d
            for d in dirs
            if not is_ignored(os.path.join(root, d), ignore_patterns, start_path)
        ]
        files = [
            file
            for file in files
            if not is_ignored(os.path.join(root, file), ignore_patterns, start_path)
        ]

        # Calculate indentation
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        directory_tree.append(f"{indent}|_{os.path.basename(root)}")
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            directory_tree.append(f"{sub_indent}|_{file}")

    # Write to file
    tree_content = "\n".join(directory_tree) + "\n"
    with open(output_file, "w") as f:
        f.write(tree_content)

    print(f"Directory structure has been written to {output_file}")
    return tree_content


if __name__ == "__main__":
    directory_path = input("Enter the directory path: ").strip()
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a valid directory.")
        exit(1)

    # Check for .gitignore and ask user whether to exclude
    gitignore_path = os.path.join(directory_path, ".gitignore")
    exclude_ignore = True
    if os.path.exists(gitignore_path):
        answer = (
            input("Exclude files and folders from the .gitignore file? [Y/n]: ")
            .strip()
            .lower()
        )
        if answer and answer[0] == "n":
            exclude_ignore = False

    map_directory(directory_path, exclude_ignore)
