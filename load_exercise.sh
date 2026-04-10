#!/bin/bash

# Define the pattern for exercise files
EXERCISES=(exercise_*.py)

# Check if any exercises exist
if [ ! -e "${EXERCISES[0]}" ]; then
    echo "Error: No exercise files found in the current directory."
    exit 1
fi

echo "------------------------------------------"
echo "   Course Exercise Loader"
echo "------------------------------------------"
echo "Please choose an exercise to run:"

# Create the interactive menu
PS3="Enter the number of your choice (or 'q' to quit): "

select file in "${EXERCISES[@]}"; do
    if [[ $REPLY == "q" ]]; then
        echo "Exiting..."
        break
    elif [[ -n $file ]]; then
        echo "------------------------------------------"
        echo "Loading $file with marimo..."
        echo "------------------------------------------"
        
        # Execute the command
        uv run marimo run "$file" --headless
        break
    else
        echo "Invalid selection. Please try again."
    fi
done
