#!/bin/bash

# Melius Global Installer
# This script installs Melius directly from GitHub without needing PyPI.

set -e

echo "🚀 Installing Melius AI Agent..."

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install it first."
    exit 1
fi

# 2. Create Melius Directory
INSTALL_DIR="$HOME/.melius"
mkdir -p "$INSTALL_DIR"

# 3. Clone/Update Source
if [ -d "$INSTALL_DIR/source" ]; then
    echo "🔄 Updating Melius source code..."
    cd "$INSTALL_DIR/source" && git pull origin main
else
    echo "📥 Downloading Melius source code..."
    git clone https://github.com/appointeasedev-oss/melius-source-code.git "$INSTALL_DIR/source"
fi

# 4. Install Dependencies
echo "📦 Installing dependencies..."
pip3 install -e "$INSTALL_DIR/source" --quiet

# 5. Create Alias
SHELL_RC="$HOME/.bashrc"
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
fi

if ! grep -q "alias melius=" "$SHELL_RC"; then
    echo "alias melius='python3 $INSTALL_DIR/source/src/melius/cli/main.py'" >> "$SHELL_RC"
    echo "✅ Alias 'melius' added to $SHELL_RC"
fi

echo "🎉 Melius is installed! Restart your terminal or run 'source $SHELL_RC' to start."
echo "👉 Run 'melius --help' to see available commands."
