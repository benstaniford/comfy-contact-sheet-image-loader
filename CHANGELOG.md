# Changelog

All notable changes to the ComfyUI Contact Sheet Image Loader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-08

### Added
- Initial release of Contact Sheet Image Loader
- Support for displaying 8 most recent images as thumbnails
- Automatic sorting by modification time (newest first)
- Image selection via 1-8 integer selector
- Configurable thumbnail size (64-512 pixels)
- Support for multiple image formats (JPG, JPEG, PNG, BMP, TIFF, WEBP)
- Thumbnail caching for improved performance
- Trigger-based refresh mechanism
- Proper mask output for ComfyUI compatibility
- Filename output for reference

### Features
- **Visual Contact Sheet**: Horizontal layout showing up to 8 image thumbnails
- **Smart Caching**: Thumbnails are cached and only regenerated when needed
- **Flexible Input**: Works with any folder containing supported image files
- **ComfyUI Integration**: Properly integrated as a custom node with appropriate input/output types
- **Error Handling**: Graceful handling of missing files and unsupported formats

### Technical Details
- Written in Python with PyTorch tensor output
- Uses PIL for image processing and thumbnail generation
- Maintains aspect ratios while creating square thumbnails
- Supports batch processing through tensor operations
