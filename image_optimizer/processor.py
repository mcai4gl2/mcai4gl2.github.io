"""
Core image processing functionality
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageOps
import logging

from .utils import (
    detect_content_type, 
    calculate_output_sizes, 
    get_quality_settings,
    create_backup_path,
    format_file_size,
    get_file_size,
    calculate_size_reduction
)
from .config import DEFAULT_SIZES, BACKUP_FOLDER, SUPPORTED_FORMATS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageProcessor:
    """Core image processing class"""
    
    def __init__(self, backup=True, backup_folder=None):
        self.backup = backup
        self.backup_folder = backup_folder or BACKUP_FOLDER
        self.stats = {
            "processed": 0,
            "original_size": 0,
            "optimized_size": 0,
            "files_created": 0
        }
    
    def process_image(self, image_path, sizes=None, quality=None, generate_webp=True, dry_run=False):
        """
        Process a single image file
        
        Args:
            image_path: Path to the image file
            sizes: List of target widths to generate
            quality: Override quality setting (0-100)
            generate_webp: Whether to generate WebP versions
            dry_run: If True, only show what would be done
        
        Returns:
            Dictionary with processing results
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        if not image_path.suffix.lower() in SUPPORTED_FORMATS["input"]:
            raise ValueError(f"Unsupported image format: {image_path.suffix}")
        
        sizes = sizes or DEFAULT_SIZES
        
        results = {
            "original_path": str(image_path),
            "original_size": get_file_size(image_path),
            "outputs": [],
            "backup_created": False
        }
        
        # Detect content type for quality optimization
        content_type = detect_content_type(image_path)
        logger.info(f"Processing {image_path.name} (detected as: {content_type})")
        
        # Create backup if needed
        if self.backup and not dry_run:
            backup_path = create_backup_path(image_path, self.backup_folder)
            shutil.copy2(image_path, backup_path)
            results["backup_created"] = True
            logger.info(f"Created backup: {backup_path}")
        
        # Process the image
        try:
            with Image.open(image_path) as img:
                # Apply EXIF orientation FIRST before any calculations
                img = self._fix_image_orientation(img)
                corrected_size = img.size
                
                output_sizes = calculate_output_sizes(corrected_size, sizes)
                
                # Generate responsive sizes
                for width, dimensions in output_sizes.items():
                    output_path = self._create_output_path(image_path, width, "jpg")
                    
                    if not dry_run:
                        self._save_resized_image(
                            img, dimensions, output_path, "jpeg", 
                            quality, content_type
                        )
                    
                    output_info = {
                        "path": str(output_path),
                        "size": dimensions,
                        "format": "jpeg",
                        "file_size": 0 if dry_run else get_file_size(output_path)
                    }
                    results["outputs"].append(output_info)
                
                # Generate WebP versions
                if generate_webp:
                    for width, dimensions in output_sizes.items():
                        output_path = self._create_output_path(image_path, width, "webp")
                        
                        if not dry_run:
                            self._save_resized_image(
                                img, dimensions, output_path, "webp", 
                                quality, content_type
                            )
                        
                        output_info = {
                            "path": str(output_path),
                            "size": dimensions,
                            "format": "webp",
                            "file_size": 0 if dry_run else get_file_size(output_path)
                        }
                        results["outputs"].append(output_info)
                
                # Update statistics
                if not dry_run:
                    self._update_stats(results)
                
                return results
                
        except Exception as e:
            logger.error(f"Error processing {image_path}: {str(e)}")
            raise
    
    def _create_output_path(self, original_path, width, format_ext):
        """Create output path for resized image"""
        original_path = Path(original_path)
        
        # Create size-specific folder
        size_folder = original_path.parent / f"{original_path.stem}_{width}px"
        size_folder.mkdir(exist_ok=True)
        
        # Create output filename
        output_name = f"{original_path.stem}.{format_ext}"
        output_path = size_folder / output_name
        
        return output_path
    
    def _fix_image_orientation(self, img):
        """Fix image orientation based on EXIF data"""
        try:
            # Check if image has EXIF data
            if hasattr(img, '_getexif') and img._getexif() is not None:
                exif = img._getexif()
                
                # Get orientation tag (0x0112)
                orientation = exif.get(0x0112, 1)
                
                # Apply rotation based on orientation
                if orientation == 3:
                    img = img.rotate(180, expand=True)
                elif orientation == 6:
                    img = img.rotate(270, expand=True)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)
                elif orientation in [2, 4, 5, 7]:
                    # Handle mirrored orientations
                    if orientation == 2:
                        img = ImageOps.mirror(img)
                    elif orientation == 4:
                        img = img.rotate(180, expand=True)
                        img = ImageOps.mirror(img)
                    elif orientation == 5:
                        img = img.rotate(90, expand=True)
                        img = ImageOps.mirror(img)
                    elif orientation == 7:
                        img = img.rotate(270, expand=True)
                        img = ImageOps.mirror(img)
                
                logger.debug(f"Applied EXIF orientation correction: {orientation}")
            
        except Exception as e:
            logger.warning(f"Could not process EXIF orientation: {str(e)}")
        
        return img
    
    def _save_resized_image(self, img, dimensions, output_path, format_ext, quality_override, content_type):
        """Save resized image with appropriate settings"""
        # Handle EXIF orientation to preserve rotation
        img = self._fix_image_orientation(img)
        
        # Resize image
        resized_img = img.resize(dimensions, Image.Resampling.LANCZOS)
        
        # Determine quality
        if quality_override:
            quality = quality_override
        else:
            quality = get_quality_settings(content_type, format_ext)
        
        # Save with appropriate settings
        save_kwargs = {"optimize": True}
        
        if format_ext.lower() in ["jpeg", "jpg"]:
            save_kwargs.update({"quality": quality, "progressive": True})
        elif format_ext.lower() == "png":
            save_kwargs.update({"compress_level": 6})
        elif format_ext.lower() == "webp":
            save_kwargs.update({"quality": quality, "method": 6})
        
        # Ensure format is correct for PIL
        pil_format = "JPEG" if format_ext.lower() in ["jpeg", "jpg"] else format_ext.upper()
        
        # For JPEG, strip EXIF data to avoid orientation conflicts
        # The orientation has already been applied to the image pixels
        if pil_format == "JPEG":
            save_kwargs["exif"] = b""  # Strip EXIF data
        
        resized_img.save(output_path, format=pil_format, **save_kwargs)
        logger.info(f"Saved {output_path}")
    
    def _update_stats(self, results):
        """Update processing statistics"""
        self.stats["processed"] += 1
        self.stats["original_size"] += results["original_size"]
        
        for output in results["outputs"]:
            self.stats["optimized_size"] += output["file_size"]
            self.stats["files_created"] += 1
    
    def get_stats(self):
        """Get processing statistics"""
        if self.stats["original_size"] > 0:
            reduction = calculate_size_reduction(
                self.stats["original_size"], 
                self.stats["optimized_size"]
            )
        else:
            reduction = 0
        
        return {
            **self.stats,
            "size_reduction_percent": reduction,
            "original_size_formatted": format_file_size(self.stats["original_size"]),
            "optimized_size_formatted": format_file_size(self.stats["optimized_size"])
        }
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.stats = {
            "processed": 0,
            "original_size": 0,
            "optimized_size": 0,
            "files_created": 0
        }