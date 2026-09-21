# 🔧 Scripts Directory

This directory contains utility scripts for managing and analyzing your GitHub profile.

## 📋 Available Scripts

### `analyzer.py`
**Purpose:** Analyze all your repositories and extract statistics

**Usage:**
```bash
python3 analyzer.py
```

**Features:**
- ✅ Scans all local repositories
- ✅ Detects programming languages
- ✅ Identifies frameworks and tools
- ✅ Finds databases and technologies
- ✅ Generates `data/stats.json` with detailed metrics
- ✅ Provides console summary

**Output:** `../data/stats.json`

### `run_analyzer.bat` (Windows)
**Purpose:** Convenient wrapper script for Windows users

**Usage:**
```bash
run_analyzer.bat
```

Or simply double-click the file in Windows Explorer.

**Features:**
- Checks for Python installation
- Checks for GitHub CLI installation
- Automatically runs the analyzer
- Provides helpful error messages

### `run_analyzer.sh` (Linux/macOS)
**Purpose:** Convenient wrapper script for Linux/macOS users

**Usage:**
```bash
chmod +x run_analyzer.sh
./run_analyzer.sh
```

Or:
```bash
bash run_analyzer.sh
```

**Features:**
- Checks for Python 3 installation
- Checks for GitHub CLI installation
- Automatically runs the analyzer
- Provides installation instructions if needed

### `config.json`
**Purpose:** Configuration file for the analyzer

**Customizable:**
- Framework detection patterns
- Database detection patterns
- Programming languages
- Ignore directories and files
- Output settings
- Display preferences

**Usage:** Edit this file to customize analyzer behavior

## 🚀 Quick Start

### Windows
```bash
# Option 1: Double-click run_analyzer.bat
run_analyzer.bat

# Option 2: From command prompt
python scripts\analyzer.py
```

### Linux/macOS
```bash
# Make script executable
chmod +x scripts/run_analyzer.sh

# Run it
./scripts/run_analyzer.sh

# Or directly with Python
python3 scripts/analyzer.py
```

## 📊 Understanding the Output

After running the analyzer, you'll see output like:

```
==================================================
Analysis Complete!
==================================================
Total Repositories: 5
Top Language: JavaScript
Frameworks Found: 8
Databases Found: 4

Top Languages:
  - JavaScript: 2500
  - Python: 1800
  - TypeScript: 1500
```

The statistics are saved to `data/stats.json` in JSON format:

```json
{
  "username": "ssalazaro8",
  "totalRepos": 5,
  "totalCommits": 500,
  "languages": {
    "JavaScript": 2500,
    "Python": 1800,
    ...
  },
  "frameworks": ["React", "Django", "Express", ...],
  "databases": ["MongoDB", "PostgreSQL", ...],
  "topLanguage": "JavaScript",
  "mostUsedFramework": "React",
  "lastUpdated": "2024-09-20T12:00:00"
}
```

## 🔧 Troubleshooting

### Python not found
**Windows:**
- Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

**Linux/macOS:**
```bash
python3 --version
# If not installed:
# macOS: brew install python3
# Ubuntu: sudo apt-get install python3
```

### GitHub CLI not found
**Windows (Chocolatey):**
```bash
choco install gh
```

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
curl -fsSLo /tmp/gh-releases.sh https://cli.github.com/linux_setup.sh
sudo bash /tmp/gh-releases.sh
```

### "No modules named" error
The analyzer uses only Python standard library modules. If you see this error, ensure you're using Python 3.8+:

```bash
python3 --version
```

### Authentication failed
Re-authenticate with GitHub CLI:

```bash
gh auth logout
gh auth login
```

## 🎯 Customization

### Add a new framework

Edit `config.json`:

```json
{
  "frameworks": {
    "MyCategory": {
      "my-framework": ["my-framework", "pattern"]
    }
  }
}
```

Edit `analyzer.py` to detect it in repository files.

### Add a new database

Edit `config.json`:

```json
{
  "databases": {
    "my-database": ["my-database", "pattern"]
  }
}
```

### Add a new language

Edit `config.json`:

```json
{
  "languages": {
    "my-language": [".ext1", ".ext2"]
  }
}
```

### Change output location

Edit `analyzer.py` and modify the `save_stats()` method:

```python
analyzer.save_stats('custom/path/stats.json')
```

## 📚 API Reference

### GitHubAnalyzer Class

```python
analyzer = GitHubAnalyzer('your-username')

# Analyze repositories
stats = analyzer.analyze()

# Save results
analyzer.save_stats('output/path.json')
```

### Methods

- `get_repos()` - Fetch repositories using GitHub CLI
- `get_local_repos(path)` - Find local repositories
- `analyze_repo(path)` - Analyze a single repository
- `analyze()` - Analyze all repositories and compile stats
- `save_stats(file)` - Save statistics to JSON file

## 🤝 Contributing

Have improvements? Found a bug?

1. Edit the script
2. Test your changes
3. Submit a pull request

## 📝 License

These scripts are part of your GitHub profile project.

---

**Happy analyzing!** 🚀
