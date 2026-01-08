"""
Image Optimizer for Hugo Blogs

A Python utility to resize and optimize images for Hugo static sites.
Generates responsive image sizes and WebP versions while preserving
the original folder structure and file organization.
"""

__version__ = "1.0.0"
__author__ = "Blog Image Optimizer"

# Lazy imports to avoid dependency issues during testing
def get_image_processor():
    """Get ImageProcessor class with lazy import"""
    from .processor import ImageProcessor
    return ImageProcessor

def get_batch_processor():
    """Get BatchProcessor class with lazy import"""
    from .batch import BatchProcessor
    return BatchProcessor

def get_utils():
    """Get utility functions with lazy import"""
    from .utils import detect_content_type, calculate_output_sizes
    return detect_content_type, calculate_output_sizes

__all__ = [
    "get_image_processor",
    "get_batch_processor",
    "get_utils"
]