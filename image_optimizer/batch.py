"""
Batch processing functionality for multiple images
"""

import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging

from .processor import ImageProcessor
from .utils import is_image_file, format_file_size, get_file_size

logger = logging.getLogger(__name__)


class BatchProcessor:
    """Batch processing class for multiple images"""
    
    def __init__(self, max_workers=4, **processor_kwargs):
        self.max_workers = max_workers
        self.processor = ImageProcessor(**processor_kwargs)
        self.results = []
    
    def process_folder(self, folder_path, recursive=True, **process_kwargs):
        """
        Process all images in a folder
        
        Args:
            folder_path: Path to the folder containing images
            recursive: Whether to process subfolders
            **process_kwargs: Arguments to pass to process_image()
        
        Returns:
            List of processing results
        """
        folder_path = Path(folder_path)
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        # Find all image files
        image_files = self._find_image_files(folder_path, recursive)
        
        if not image_files:
            logger.warning(f"No image files found in {folder_path}")
            return []
        
        logger.info(f"Found {len(image_files)} image files to process")
        
        # Process images in parallel
        self.results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(
                    self.processor.process_image, 
                    img_path, 
                    **process_kwargs
                ): img_path for img_path in image_files
            }
            
            # Process with progress bar
            with tqdm(total=len(image_files), desc="Processing images") as pbar:
                for future in as_completed(future_to_file):
                    img_path = future_to_file[future]
                    try:
                        result = future.result()
                        self.results.append(result)
                        pbar.set_postfix({
                            "file": img_path.name[:20],
                            "size": format_file_size(get_file_size(img_path))
                        })
                    except Exception as e:
                        logger.error(f"Failed to process {img_path}: {str(e)}")
                        # Add error result
                        self.results.append({
                            "original_path": str(img_path),
                            "error": str(e),
                            "outputs": []
                        })
                    finally:
                        pbar.update(1)
        
        return self.results
    
    def _find_image_files(self, folder_path, recursive):
        """Find all image files in folder"""
        image_files = []
        
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        for file_path in folder_path.glob(pattern):
            if file_path.is_file() and is_image_file(file_path):
                image_files.append(file_path)
        
        return sorted(image_files)
    
    def analyze_folder(self, folder_path, recursive=True):
        """
        Analyze images in a folder without processing
        
        Args:
            folder_path: Path to the folder containing images
            recursive: Whether to analyze subfolders
        
        Returns:
            Analysis results
        """
        folder_path = Path(folder_path)
        image_files = self._find_image_files(folder_path, recursive)
        
        analysis = {
            "total_files": len(image_files),
            "total_size": 0,
            "format_breakdown": {},
            "size_breakdown": {
                "small": 0,    # < 500KB
                "medium": 0,   # 500KB - 1MB
                "large": 0     # > 1MB
            },
            "files": []
        }
        
        for img_path in image_files:
            file_size = get_file_size(img_path)
            file_ext = img_path.suffix.lower()
            
            # Update total size
            analysis["total_size"] += file_size
            
            # Update format breakdown
            if file_ext not in analysis["format_breakdown"]:
                analysis["format_breakdown"][file_ext] = {"count": 0, "size": 0}
            analysis["format_breakdown"][file_ext]["count"] += 1
            analysis["format_breakdown"][file_ext]["size"] += file_size
            
            # Update size breakdown
            if file_size < 500 * 1024:  # < 500KB
                analysis["size_breakdown"]["small"] += 1
            elif file_size < 1024 * 1024:  # < 1MB
                analysis["size_breakdown"]["medium"] += 1
            else:
                analysis["size_breakdown"]["large"] += 1
            
            # Add file info
            analysis["files"].append({
                "path": str(img_path),
                "size": file_size,
                "size_formatted": format_file_size(file_size),
                "format": file_ext
            })
        
        # Sort files by size (largest first)
        analysis["files"].sort(key=lambda x: x["size"], reverse=True)
        
        return analysis
    
    def get_summary(self):
        """Get summary of batch processing results"""
        if not self.results:
            return {"processed": 0, "errors": 0}
        
        processed = sum(1 for r in self.results if "error" not in r)
        errors = sum(1 for r in self.results if "error" in r)
        
        stats = self.processor.get_stats()
        
        return {
            "processed": processed,
            "errors": errors,
            "total_files": len(self.results),
            "stats": stats
        }
    
    def print_analysis(self, analysis):
        """Print formatted analysis results"""
        print(f"\n=== Image Analysis ===")
        print(f"Total files: {analysis['total_files']}")
        print(f"Total size: {format_file_size(analysis['total_size'])}")
        
        print(f"\n--- Format Breakdown ---")
        for fmt, info in analysis["format_breakdown"].items():
            print(f"{fmt}: {info['count']} files ({format_file_size(info['size'])})")
        
        print(f"\n--- Size Breakdown ---")
        print(f"Small (< 500KB): {analysis['size_breakdown']['small']} files")
        print(f"Medium (500KB-1MB): {analysis['size_breakdown']['medium']} files")
        print(f"Large (> 1MB): {analysis['size_breakdown']['large']} files")
        
        if analysis["files"]:
            print(f"\n--- Largest Files ---")
            for file_info in analysis["files"][:5]:
                print(f"{file_info['path']}: {file_info['size_formatted']}")
    
    def print_summary(self):
        """Print formatted processing summary"""
        summary = self.get_summary()
        stats = summary["stats"]
        
        print(f"\n=== Processing Summary ===")
        print(f"Files processed: {summary['processed']}")
        print(f"Errors: {summary['errors']}")
        print(f"Total files: {summary['total_files']}")
        
        if summary["processed"] > 0:
            print(f"\n--- Size Optimization ---")
            print(f"Original total size: {stats['original_size_formatted']}")
            print(f"Optimized total size: {stats['optimized_size_formatted']}")
            print(f"Size reduction: {stats['size_reduction_percent']:.1f}%")
            print(f"Files created: {stats['files_created']}")