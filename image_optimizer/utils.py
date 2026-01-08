"""
Utility functions for image processing
"""

import os
from pathlib import Path
from PIL import Image
import numpy as np

from .config import SUPPORTED_FORMATS, QUALITY_SETTINGS


def is_image_file(file_path):
    """Check if file is a supported image format"""
    return Path(file_path).suffix.lower() in SUPPORTED_FORMATS["input"]


def detect_content_type(image_path):
    """
    Detect image content type: photo, screenshot, or graphic
    Based on image characteristics and file properties
    """
    try:
        with Image.open(image_path) as img:
            # Get image properties
            width, height = img.size
            mode = img.mode
            format_name = img.format.lower() if img.format else ""
            
            # Convert to numpy array for analysis
            img_array = np.array(img)
            
            # Simple heuristic for content detection
            if format_name == "jpeg":
                # JPEG files are typically photos
                return "photo"
            elif format_name == "png":
                # PNG could be screenshot or graphic
                # Check for transparency (common in screenshots/graphics)
                if mode == "RGBA" and np.any(img_array[:, :, 3] < 255):
                    return "graphic"
                
                # Check for high contrast (common in screenshots)
                if len(img_array.shape) == 3:
                    # Calculate contrast
                    std_dev = np.std(img_array)
                    if std_dev > 50:  # High contrast suggests screenshot
                        return "screenshot"
                
                return "graphic"
            elif format_name == "gif":
                return "graphic"
            else:
                # Default to photo for unknown formats
                return "photo"
    except Exception:
        # Default to photo if detection fails
        return "photo"


def calculate_output_sizes(original_size, target_sizes):
    """
    Calculate output dimensions maintaining aspect ratio
    """
    width, height = original_size
    aspect_ratio = width / height
    
    output_sizes = {}
    
    for target_width in target_sizes:
        if width > target_width:
            new_height = int(target_width / aspect_ratio)
            output_sizes[target_width] = (target_width, new_height)
        else:
            # Don't upscale images
            output_sizes[target_width] = (width, height)
    
    return output_sizes


def get_quality_settings(content_type, output_format):
    """Get quality settings based on content type and output format"""
    content_settings = QUALITY_SETTINGS.get(content_type, QUALITY_SETTINGS["photo"])
    return content_settings.get(output_format.lower(), 85)


def create_backup_path(original_path, backup_folder):
    """Create backup path for original file"""
    original_path = Path(original_path)
    backup_path = Path(backup_folder) / original_path.relative_to(original_path.anchor)
    
    # Create backup directory structure
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    
    return backup_path


def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"


def get_file_size(file_path):
    """Get file size in bytes"""
    return os.path.getsize(file_path)


def calculate_size_reduction(original_size, optimized_size):
    """Calculate percentage size reduction"""
    if original_size == 0:
        return 0
    return ((original_size - optimized_size) / original_size) * 100