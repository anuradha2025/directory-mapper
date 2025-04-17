# Directory Mapper

A simple tool to generate a text-based map of any directory’s structure, with an optional `.gitignore`-based exclusion feature.

---

## 🚀 Features

- **Directory Tree Mapping**: Recursively walks through a given folder and outputs a neat, indented tree view into `directory_map.txt`.
- **Optional `.gitignore` Exclusion**: Detects a `.gitignore` file in the target folder and prompts you whether to exclude matching files/folders (default: **Yes**).
- **Standalone Executable**: Pre-built `.exe` available—no Python install required.

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/anuradha2025/directory-mapper.git
cd directory-mapper
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv/Scripts/activate  # Windows
```

### 3. Install Dependencies

This project uses only Python’s standard library; there are no extra dependencies.

---

## ⚙️ Usage

### A. Running from Source

```bash
python dirmap.py
```

1. **Enter the target directory path**, e.g. `C:/Projects/MyRepo`.
2. If a `.gitignore` file is present, you’ll be asked:

   > Exclude files and folders from the .gitignore file? [Y/n]

   - **Y** (default): Patterns from `.gitignore` will be honored.
   - **N**: All files/folders will be included.

3. After completion, check `directory_map.txt` in your current working directory for the tree output.

### B. Running the Standalone Executable

1. Download the latest `dirmap.exe` from the [Releases](https://github.com/anuradha2025/directory-mapper/releases) page.
2. Double-click or run in a console:
   ```bash
   ./dirmap.exe
   ```
3. Follow the same prompts as above.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Commit your changes: `git commit -am "Add feature X"`.
4. Push to your branch: `git push origin feature/my-feature`.
5. Open a Pull Request.

Please ensure your code follows PEP 8 styling.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## ✉️ Contact

Created and maintained by [Anuradha](https://github.com/anuradha2025). Feel free to open issues or reach out via GitHub.
