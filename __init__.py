"""
ComfyUI Contact Sheet Image Loader

A custom node for ComfyUI that allows loading images from a folder by displaying
the 8 most recent images as thumbnails in a contact sheet format.
"""

from .contact_sheet_loader import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
