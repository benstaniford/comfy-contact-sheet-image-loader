import os
import glob
import numpy as np
from PIL import Image
import torch
from typing import List, Tuple, Optional

class ContactSheetImageLoader:
    """
    A ComfyUI node that displays the 8 most recent images from a folder as thumbnails
    and allows selection of one image to load.
    """
    
    def __init__(self):
        self.thumbnail_cache = {}
        self.last_folder = None
        self.last_trigger = None
        self.cached_images = []
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {
                    "default": "", 
                    "multiline": False,
                    "tooltip": "Path to folder containing images"
                }),
                "trigger": ("*", {
                    "tooltip": "Connect any output here to refresh thumbnails"
                }),
                "selected_image": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 8,
                    "tooltip": "Select image 1-8 from the contact sheet"
                }),
                "thumbnail_size": ("INT", {
                    "default": 128,
                    "min": 64,
                    "max": 512,
                    "step": 16,
                    "tooltip": "Size of thumbnails in pixels"
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "filename")
    FUNCTION = "load_image"
    CATEGORY = "image/loaders"
    OUTPUT_NODE = False
    
    def get_recent_images(self, folder_path: str, max_count: int = 8) -> List[str]:
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
    
    def create_contact_sheet(self, image_paths: List[str], thumbnail_size: int) -> np.ndarray:
        """Create a horizontal contact sheet from the image paths."""
        if not image_paths:
            # Return a placeholder image
            placeholder = np.full((thumbnail_size, thumbnail_size * 8, 3), 0.5, dtype=np.float32)
            return placeholder
        
        contact_sheet_width = thumbnail_size * 8
        contact_sheet = np.full((thumbnail_size, contact_sheet_width, 3), 0.3, dtype=np.float32)
        
        for i, image_path in enumerate(image_paths[:8]):
            if i >= 8:
                break
                
            thumbnail = self.create_thumbnail(image_path, thumbnail_size)
            if thumbnail is not None:
                x_start = i * thumbnail_size
                x_end = x_start + thumbnail_size
                contact_sheet[:, x_start:x_end, :] = thumbnail
        
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
    
    def load_image(self, folder_path: str, trigger: int, selected_image: int, thumbnail_size: int):
        """Main function called by ComfyUI."""
        
        # Check if we need to refresh the image list
        if (self.last_folder != folder_path or 
            self.last_trigger != trigger or 
            not self.cached_images):
            
            self.cached_images = self.get_recent_images(folder_path, 8)
            self.last_folder = folder_path
            self.last_trigger = trigger
        
        # Load the selected image
        image, mask, filename = self.load_selected_image(self.cached_images, selected_image)
        
        # Convert to torch tensors with batch dimension
        image_tensor = torch.from_numpy(image).unsqueeze(0)  # Add batch dimension
        mask_tensor = torch.from_numpy(mask).unsqueeze(0)    # Add batch dimension
        
        return (image_tensor, mask_tensor, filename)

# Node mapping for ComfyUI
NODE_CLASS_MAPPINGS = {
    "ContactSheetImageLoader": ContactSheetImageLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ContactSheetImageLoader": "Contact Sheet Image Loader"
}
