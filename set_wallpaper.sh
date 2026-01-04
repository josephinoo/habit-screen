#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <path_to_wallpaper>"
  exit 1
fi

WALLPAPER_PATH=$(realpath "$1")

echo "Setting wallpaper to: $WALLPAPER_PATH"

osascript -e "tell application \"System Events\" to set picture of every desktop to POSIX file \"$WALLPAPER_PATH\""

if [ $? -eq 0 ]; then
  echo "Wallpaper set successfully via bash script."
else
  echo "Failed to set wallpaper."
  exit 1
fi
