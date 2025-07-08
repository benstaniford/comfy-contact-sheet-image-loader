#!/usr/bin/env python3
"""
Test script for Contact Sheet Image Loader

This script can be used to test the basic functionality of the node
outside of ComfyUI for development purposes.
"""

import os
import sys
import tempfile
import numpy as np
from PIL import Image

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from contact_sheet_loader import ContactSheetImageLoader

def create_test_images(folder_path, count=10):
    """Create test images for testing purposes."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (128, 128, 128), # Gray
        (255, 128, 0),  # Orange
        (128, 0, 255),  # Purple
        (0, 128, 255),  # Sky Blue
    ]
    
    for i in range(count):
        color = colors[i % len(colors)]
        img = Image.new('RGB', (200, 200), color)
        
        # Add some text to identify the image
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        text = f"Image {i+1}"
        draw.text((10, 10), text, fill=(255, 255, 255), font=font)
        
        filename = f"test_image_{i+1:02d}.png"
        filepath = os.path.join(folder_path, filename)
        img.save(filepath)
        
        print(f"Created: {filepath}")

def test_node():
    """Test the Contact Sheet Image Loader node."""
    print("Testing Contact Sheet Image Loader...")
    
    # Create a temporary directory with test images
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Using temporary directory: {temp_dir}")
        
        # Create test images
        create_test_images(temp_dir, 10)
        
        # Initialize the node
        loader = ContactSheetImageLoader()
        
        # Test getting recent images
        recent_images = loader.get_recent_images(temp_dir, 8)
        print(f"Found {len(recent_images)} recent images:")
        for i, img_path in enumerate(recent_images, 1):
            print(f"  {i}: {os.path.basename(img_path)}")
        
        # Test creating contact sheet
        contact_sheet = loader.create_contact_sheet(recent_images, 128)
        print(f"Contact sheet shape: {contact_sheet.shape}")
        
        # Test loading a specific image
        if recent_images:
            image, mask, filename = loader.load_selected_image(recent_images, 1)
            print(f"Loaded image: {filename}")
            print(f"Image shape: {image.shape}")
            print(f"Mask shape: {mask.shape}")
            
            # Test the main function
            try:
                result = loader.load_image(temp_dir, 1, 1, 128)
                print(f"Main function result types: {[type(r) for r in result]}")
                print(f"Image tensor shape: {result[0].shape}")
                print(f"Mask tensor shape: {result[1].shape}")
                print(f"Filename: {result[2]}")
            except Exception as e:
                print(f"Error in main function: {e}")
        
        print("Test completed!")

if __name__ == "__main__":
    test_node()
