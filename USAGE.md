# Installation and Usage Guide

## Installation

1. **Clone or download this repository** to your ComfyUI custom nodes directory:
   ```bash
   cd /path/to/ComfyUI/custom_nodes/
   git clone https://github.com/yourusername/comfy-contact-sheet-image-loader.git
   ```

2. **Restart ComfyUI** - The node will be automatically loaded.

## Usage

### Node Inputs

- **folder_path**: Path to the folder containing images you want to browse
- **trigger**: Change this value to refresh the thumbnail cache (increment by 1)
- **selected_image**: Select which image to load (1-8, corresponding to the contact sheet positions)
- **thumbnail_size**: Size of thumbnails in pixels (64-512, default: 128)

### Node Outputs

- **image**: The selected image as a tensor
- **mask**: A corresponding mask (white/fully visible by default)
- **filename**: The filename of the selected image

### How to Use

1. Add the "Contact Sheet Image Loader" node to your workflow
2. Set the `folder_path` to point to your images folder
3. The node will automatically load the 8 most recent images (by modification time)
4. Use the `selected_image` parameter to choose which image to load (1 = leftmost/newest, 8 = rightmost/oldest)
5. To refresh the thumbnails after new images are added, increment the `trigger` value

### Notes

- Images are sorted by modification time (newest first)
- Supports common image formats: JPG, JPEG, PNG, BMP, TIFF, WEBP
- If fewer than 8 images exist, only the available images will be shown
- Thumbnails maintain aspect ratio and are centered in square frames
- The contact sheet is displayed horizontally with 8 thumbnail slots

## Troubleshooting

- **No images showing**: Check that the folder path is correct and contains supported image files
- **Images not updating**: Increment the `trigger` value to force a refresh
- **Performance issues**: Reduce `thumbnail_size` if working with many large images

## Technical Details

The node creates a horizontal contact sheet showing up to 8 thumbnails of the most recent images in the specified folder. The thumbnails are cached for performance, and the cache is invalidated when the folder path or trigger value changes.
