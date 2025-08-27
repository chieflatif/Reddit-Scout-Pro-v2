#!/bin/bash

# Reddit Scout Pro - Setup Alias Script
# This creates a permanent alias to start the app easily

echo "🔧 Setting up Reddit Scout Pro alias..."

# Define the alias command
ALIAS_COMMAND="alias reddit-scout='cd \"/Users/martin/Reddit Scout Pro\" && ./start.sh'"

# Add to .zshrc (since you're using zsh)
if [ -f ~/.zshrc ]; then
    if ! grep -q "reddit-scout" ~/.zshrc; then
        echo "" >> ~/.zshrc
        echo "# Reddit Scout Pro - Easy startup" >> ~/.zshrc
        echo "$ALIAS_COMMAND" >> ~/.zshrc
        echo "✅ Added reddit-scout alias to ~/.zshrc"
    else
        echo "ℹ️  reddit-scout alias already exists in ~/.zshrc"
    fi
else
    echo "⚠️  ~/.zshrc not found, creating it..."
    echo "$ALIAS_COMMAND" > ~/.zshrc
    echo "✅ Created ~/.zshrc with reddit-scout alias"
fi

# Add to .bash_profile as backup (for bash users)
if [ -f ~/.bash_profile ]; then
    if ! grep -q "reddit-scout" ~/.bash_profile; then
        echo "" >> ~/.bash_profile
        echo "# Reddit Scout Pro - Easy startup" >> ~/.bash_profile
        echo "$ALIAS_COMMAND" >> ~/.bash_profile
        echo "✅ Added reddit-scout alias to ~/.bash_profile"
    fi
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Now you can start Reddit Scout Pro in 3 ways:"
echo ""
echo "1. 🎯 EASIEST (after restarting terminal):"
echo "   reddit-scout"
echo ""
echo "2. 🚀 DIRECT:"
echo "   cd \"/Users/martin/Reddit Scout Pro\" && ./start.sh"
echo ""
echo "3. 📘 MANUAL:"
echo "   cd \"/Users/martin/Reddit Scout Pro\" && poetry run streamlit run app.py"
echo ""
echo "⚠️  Please restart your terminal or run 'source ~/.zshrc' to activate the alias"
