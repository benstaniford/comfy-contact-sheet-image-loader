# ComfyUI Contact Sheet Image Loader

A custom ComfyUI node that displays the 8 most recent images from a folder as thumbnails in a horizontal contact sheet format, allowing you to easily select and load one of them.

## Features

- **Visual Selection**: Shows up to 8 thumbnails of the most recent images in a folder
- **Automatic Sorting**: Images are automatically sorted by modification time (newest first)
- **Flexible Selection**: Choose any of the 8 displayed images using a simple 1-8 selector
- **Refreshable**: Update the thumbnail view by changing the trigger value
- **Efficient Caching**: Thumbnails are cached for better performance
- **Multiple Formats**: Supports JPG, JPEG, PNG, BMP, TIFF, and WEBP images

## Quick Start

1. Copy this folder to your ComfyUI `custom_nodes` directory
2. Restart ComfyUI
3. Add the "Contact Sheet Image Loader" node to your workflow
4. Set the folder path and start browsing your images!

## Node Parameters

- **folder_path**: Path to folder containing your images
- **source**: Connect any output here to refresh thumbnails (required)
- **selected_image**: Which image to load (1-8, left to right)
- **thumbnail_size**: Size of thumbnails in pixels (64-512)

## Outputs

- **contact_sheet**: Visual contact sheet showing up to 8 thumbnails
- **image**: The selected image tensor
- **mask**: Corresponding mask (useful for further processing)
- **filename**: Name of the selected file

## Use Cases

- Quickly browse and select from recent AI-generated images
- Preview images from output folders before loading
- Create workflows that process the most recent images
- Build image selection interfaces for batch processing

See [USAGE.md](USAGE.md) for detailed installation and usage instructions.
