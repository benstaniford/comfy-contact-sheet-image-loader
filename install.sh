#!/bin/bash
# Installation script for ComfyUI Contact Sheet Image Loader

echo "Installing ComfyUI Contact Sheet Image Loader..."

# Check if ComfyUI directory exists
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/ComfyUI"
    echo "Please provide the path to your ComfyUI installation"
    exit 1
fi

COMFYUI_PATH="$1"
CUSTOM_NODES_PATH="$COMFYUI_PATH/custom_nodes"

if [ ! -d "$COMFYUI_PATH" ]; then
    echo "Error: ComfyUI directory not found at $COMFYUI_PATH"
    exit 1
fi

if [ ! -d "$CUSTOM_NODES_PATH" ]; then
    echo "Error: custom_nodes directory not found at $CUSTOM_NODES_PATH"
    exit 1
fi

# Create target directory
TARGET_DIR="$CUSTOM_NODES_PATH/comfy-contact-sheet-image-loader"

if [ -d "$TARGET_DIR" ]; then
    echo "Warning: Directory already exists at $TARGET_DIR"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
    rm -rf "$TARGET_DIR"
fi

# Copy files
echo "Copying files to $TARGET_DIR..."
mkdir -p "$TARGET_DIR"
cp -r * "$TARGET_DIR/"

echo "Installation completed!"
echo ""
echo "Next steps:"
echo "1. Restart ComfyUI"
echo "2. Look for 'Contact Sheet Image Loader' in the node menu under 'image/loaders'"
echo "3. See USAGE.md for detailed usage instructions"
echo ""
echo "Enjoy your new contact sheet image loader!"
