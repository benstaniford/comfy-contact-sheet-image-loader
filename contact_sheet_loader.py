import os
import glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import torch
from typing import List, Tuple, Optional
import folder_paths

class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

class ContactSheetImageLoader:
    """
    A ComfyUI node that displays the 8 most recent images from a folder as thumbnails
    and allows selection of one image to load.
    """
    
    def __init__(self):
        self.thumbnail_cache = {}
        self.last_folder = None
        self.last_trigger = None
        self.last_rows = None
        self.cached_images = []
        
    @classmethod
    def INPUT_TYPES(cls):
        # Get ComfyUI's output directory as default
        try:
            default_folder = folder_paths.get_output_directory()
        except:
            default_folder = ""
            
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": default_folder, 
                    "multiline": False,
                    "tooltip": "Path to folder containing images"
                }),
                "selected_image": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 64,
                    "tooltip": "Select image 1-64 from the contact sheet"
                }),
                "thumbnail_size": ("INT", {
                    "default": 256,
                    "min": 64,
                    "max": 512,
                    "step": 16,
                    "tooltip": "Size of thumbnails in pixels"
                }),
                "rows": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 8,
                    "tooltip": "Number of rows (1=8 images, 2=16, ..., 8=64)"
                }),
                "load_trigger": (any_type, {}),
            },
        }
    
    RETURN_TYPES = ("IMAGE", "IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("contact_sheet", "image", "mask", "filename")
    FUNCTION = "load_image"
    CATEGORY = "image/loaders"
    OUTPUT_NODE = False
    
    def get_recent_images(self, folder_path: str, max_count: int = 64) -> List[str]:
        """Get the most recent image files from the specified folder."""
        if not os.path.exists(folder_path):
            return []
        
        # Common image extensions
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif', '*.webp']
        image_files = []
        
        for ext in extensions:
            pattern = os.path.join(folder_path, ext)
            image_files.extend(glob.glob(pattern, recursive=False))
            # Also check uppercase
            pattern = os.path.join(folder_path, ext.upper())
            image_files.extend(glob.glob(pattern, recursive=False))
        
        # Remove duplicates and sort by modification time (newest first)
        image_files = list(set(image_files))
        image_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        return image_files[:max_count]
    
    def create_thumbnail(self, image_path: str, size: int) -> Optional[np.ndarray]:
        """Create a thumbnail of the specified size."""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create thumbnail maintaining aspect ratio
                img.thumbnail((size, size), Image.Resampling.LANCZOS)
                
                # Create a square thumbnail with padding
                thumbnail = Image.new('RGB', (size, size), (128, 128, 128))
                
                # Center the image
                x = (size - img.width) // 2
                y = (size - img.height) // 2
                thumbnail.paste(img, (x, y))
                
                # Convert to numpy array and normalize
                thumbnail_array = np.array(thumbnail).astype(np.float32) / 255.0
                return thumbnail_array
                
        except Exception as e:
            print(f"Error creating thumbnail for {image_path}: {e}")
            return None
    
    def create_contact_sheet(self, image_paths: List[str], thumbnail_size: int, rows: int = 1) -> np.ndarray:
        """Create a contact sheet from the image paths with specified number of rows."""
        cols = 8  # Always 8 columns
        max_images = rows * cols
        
        if not image_paths:
            # Return a placeholder image
            placeholder = np.full((thumbnail_size * rows, thumbnail_size * cols, 3), 0.5, dtype=np.float32)
            return placeholder
        
        contact_sheet_height = thumbnail_size * rows
        contact_sheet_width = thumbnail_size * cols
        contact_sheet = np.full((contact_sheet_height, contact_sheet_width, 3), 0.3, dtype=np.float32)
        
        for i, image_path in enumerate(image_paths[:max_images]):
            if i >= max_images:
                break
                
            # Calculate row and column position
            row = i // cols
            col = i % cols
            
            thumbnail = self.create_thumbnail(image_path, thumbnail_size)
            if thumbnail is not None:
                # Convert back to PIL Image to add the number
                thumbnail_pil = Image.fromarray((thumbnail * 255).astype(np.uint8))
                
                # Add number to bottom right corner
                draw = ImageDraw.Draw(thumbnail_pil)
                number_text = str(i + 1)
                
                # Try to use a reasonable font size based on thumbnail size
                try:
                    font_size = max(12, thumbnail_size // 12)
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    # Fallback to default font if arial.ttf is not available
                    try:
                        font = ImageFont.load_default()
                    except:
                        font = None
                
                if font:
                    # Get text dimensions
                    bbox = draw.textbbox((0, 0), number_text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    # Position in bottom right corner with small padding
                    x = thumbnail_size - text_width - 4
                    y = thumbnail_size - text_height - 4
                    
                    # Draw background circle/rectangle for better visibility
                    padding = 2
                    draw.ellipse([x - padding, y - padding, x + text_width + padding, y + text_height + padding], 
                                fill=(0, 0, 0, 180))  # Semi-transparent black background
                    
                    # Draw the number in white
                    draw.text((x, y), number_text, font=font, fill=(255, 255, 255))
                
                # Convert back to numpy array
                thumbnail_with_number = np.array(thumbnail_pil).astype(np.float32) / 255.0
                
                # Calculate position in contact sheet
                y_start = row * thumbnail_size
                y_end = y_start + thumbnail_size
                x_start = col * thumbnail_size
                x_end = x_start + thumbnail_size
                
                contact_sheet[y_start:y_end, x_start:x_end, :] = thumbnail_with_number
        
        return contact_sheet
    
    def load_selected_image(self, image_paths: List[str], selected_index: int) -> Tuple[np.ndarray, np.ndarray, str]:
        """Load the selected image and create a mask."""
        if not image_paths or selected_index < 1 or selected_index > len(image_paths):
            # Return placeholder data
            placeholder_img = np.full((512, 512, 3), 0.5, dtype=np.float32)
            placeholder_mask = np.ones((512, 512), dtype=np.float32)
            return placeholder_img, placeholder_mask, "no_image"
        
        image_path = image_paths[selected_index - 1]  # Convert to 0-based index
        
        try:
            with Image.open(image_path) as img:
                # Convert to RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Convert to numpy array and normalize
                image_array = np.array(img).astype(np.float32) / 255.0
                
                # Create mask (white = fully visible)
                mask = np.ones((img.height, img.width), dtype=np.float32)
                
                filename = os.path.basename(image_path)
                return image_array, mask, filename
                
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            # Return placeholder data
            placeholder_img = np.full((512, 512, 3), 0.5, dtype=np.float32)
            placeholder_mask = np.ones((512, 512), dtype=np.float32)
            return placeholder_img, placeholder_mask, f"error_{os.path.basename(image_path)}"
    
    def load_image(self, folder_path: str, selected_image: int, thumbnail_size: int, rows: int, load_trigger=None):
        """Main function called by ComfyUI."""
        
        # Calculate max images based on rows
        max_images = rows * 8
        
        # Convert load_trigger to a comparable value (hash for tensors, direct value for others)
        if hasattr(load_trigger, 'shape') and hasattr(load_trigger, 'dtype'):  # It's a tensor
            source_key = hash(str(load_trigger.shape) + str(load_trigger.dtype) + str(load_trigger.sum().item() if load_trigger.numel() > 0 else 0))
        else:
            source_key = load_trigger
        
        # Check if we need to refresh the image list
        if (self.last_folder != folder_path or 
            self.last_trigger != source_key or 
            self.last_rows != rows or
            not self.cached_images):
            
            self.cached_images = self.get_recent_images(folder_path, max_images)
            self.last_folder = folder_path
            self.last_trigger = source_key
            self.last_rows = rows
        
        # Create the contact sheet
        contact_sheet = self.create_contact_sheet(self.cached_images, thumbnail_size, rows)
        
        # Load the selected image
        image, mask, filename = self.load_selected_image(self.cached_images, selected_image)
        
        # Convert to torch tensors with batch dimension
        contact_sheet_tensor = torch.from_numpy(contact_sheet).unsqueeze(0)  # Add batch dimension
        image_tensor = torch.from_numpy(image).unsqueeze(0)  # Add batch dimension
        mask_tensor = torch.from_numpy(mask).unsqueeze(0)    # Add batch dimension
        
        return (contact_sheet_tensor, image_tensor, mask_tensor, filename)

# Node mapping for ComfyUI
NODE_CLASS_MAPPINGS = {
    "ContactSheetImageLoader": ContactSheetImageLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ContactSheetImageLoader": "Contact Sheet Image Loader"
}
