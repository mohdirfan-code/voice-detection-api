#!/usr/bin/env bash
# Render build script - installs system dependencies

echo "Installing system dependencies..."

# Update package list
apt-get update

# Install ffmpeg for audio processing (required for MP3 support)
echo "Installing ffmpeg..."
apt-get install -y ffmpeg

# Verify installation
ffmpeg -version

echo "System dependencies installed successfully!"
