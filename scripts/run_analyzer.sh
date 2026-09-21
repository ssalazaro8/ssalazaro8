#!/bin/bash

# GitHub Profile Analyzer - Bash Script for Linux/macOS

set -e

echo ""
echo "=========================================="
echo "  GitHub Profile Statistics Analyzer"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[INFO] Python found: $(python3 --version)"

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo ""
    echo "[WARNING] GitHub CLI (gh) is not installed"
    echo "[INFO] Install it from: https://cli.github.com/"
    echo ""
    echo "Installation commands:"
    echo "  macOS: brew install gh"
    echo "  Ubuntu/Debian: curl -fsSLo /tmp/gh-releases.sh https://cli.github.com/linux_setup.sh && sudo bash /tmp/gh-releases.sh"
    echo "  Arch: pacman -S github-cli"
    exit 1
fi

echo "[INFO] GitHub CLI found: $(gh --version)"

# Run the analyzer
echo ""
echo "[INFO] Running analyzer..."
echo "=========================================="
echo ""

cd "$(dirname "$0")"
python3 analyzer.py

echo ""
echo "=========================================="
echo "[SUCCESS] Statistics updated successfully!"
echo "[INFO] Open ../index.html to view the dashboard"
echo "=========================================="
echo ""
