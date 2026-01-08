#!/usr/bin/env python3
"""
Minimal image optimizer without external dependencies
Uses Python's built-in libraries for basic image processing
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess
import json


def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import PIL
        print("✓ Pillow is available")
        return True
    except ImportError:
        print("✗ Pillow is not installed")
        print("To install dependencies, run:")
        print("  pip install Pillow click tqdm")
        print("Or on Ubuntu/Debian:")
        print("  sudo apt install python3-pil python3-click python3-tqdm")
        return False


def analyze_folder(folder_path, recursive=True):
    """Analyze images in a folder"""
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Error: Folder not found: {folder_path}")
        return
    
    # Find image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    image_files = []
    
    if recursive:
        for ext in image_extensions:
            image_files.extend(folder_path.rglob(f'*{ext}'))
            image_files.extend(folder_path.rglob(f'*{ext.upper()}'))
    else:
        for ext in image_extensions:
            image_files.extend(folder_path.glob(f'*{ext}'))
            image_files.extend(folder_path.glob(f'*{ext.upper()}'))
    
    if not image_files:
        print(f"No image files found in {folder_path}")
        return
    
    # Analyze files
    total_size = 0
    size_breakdown = {"small": 0, "medium": 0, "large": 0}
    format_breakdown = {}
    large_files = []
    
    for img_path in image_files:
        if img_path.is_file():
            size = img_path.stat().st_size
            total_size += size
            
            # Format breakdown
            ext = img_path.suffix.lower()
            if ext not in format_breakdown:
                format_breakdown[ext] = {"count": 0, "size": 0}
            format_breakdown[ext]["count"] += 1
            format_breakdown[ext]["size"] += size
            
            # Size breakdown
            size_mb = size / (1024 * 1024)
            if size_mb < 0.5:
                size_breakdown["small"] += 1
            elif size_mb < 1:
                size_breakdown["medium"] += 1
            else:
                size_breakdown["large"] += 1
                large_files.append((img_path, size_mb))
    
    # Print results
    print(f"\n=== Image Analysis ===")
    print(f"Folder: {folder_path}")
    print(f"Total files: {len(image_files)}")
    print(f"Total size: {total_size / (1024 * 1024):.1f} MB")
    
    print(f"\n--- Format Breakdown ---")
    for ext, info in sorted(format_breakdown.items()):
        print(f"{ext}: {info['count']} files ({info['size'] / (1024 * 1024):.1f} MB)")
    
    print(f"\n--- Size Breakdown ---")
    print(f"Small (< 500KB): {size_breakdown['small']} files")
    print(f"Medium (500KB-1MB): {size_breakdown['medium']} files")
    print(f"Large (> 1MB): {size_breakdown['large']} files")
    
    if large_files:
        print(f"\n--- Largest Files ---")
        large_files.sort(key=lambda x: x[1], reverse=True)
        for img_path, size_mb in large_files[:10]:
            rel_path = img_path.relative_to(folder_path)
            print(f"{rel_path}: {size_mb:.1f} MB")
    
    # Recommendations
    if size_breakdown["large"] > 0:
        print(f"\n--- Recommendations ---")
        print(f"Found {size_breakdown['large']} large files (>1MB)")
        print("These files should be optimized for better web performance")
        estimated_reduction = total_size * 0.6  # Estimate 60% reduction
        print(f"Potential savings: ~{estimated_reduction / (1024 * 1024):.1f} MB")
    
    return {
        "total_files": len(image_files),
        "total_size": total_size,
        "size_breakdown": size_breakdown,
        "format_breakdown": format_breakdown,
        "large_files": [(str(p.relative_to(folder_path)), s) for p, s in large_files]
    }


def create_backup(image_path, backup_folder):
    """Create backup of image file"""
    image_path = Path(image_path)
    backup_path = Path(backup_folder) / image_path.relative_to(image_path.anchor)
    
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(image_path, backup_path)
    
    return backup_path


def optimize_with_imagemagick(image_path, output_dir, sizes=None, quality=85):
    """Use ImageMagick for optimization if available"""
    if not sizes:
        sizes = [400, 800, 1200]
    
    image_path = Path(image_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if ImageMagick is available
    try:
        subprocess.run(['convert', '-version'], 
                      capture_output=True, check=True)
        imagemagick_available = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        imagemagick_available = False
    
    if not imagemagick_available:
        print("ImageMagick not available. Install with: sudo apt install imagemagick")
        return []
    
    results = []
    original_size = image_path.stat().st_size
    
    for width in sizes:
        # Create output filename
        output_name = f"{image_path.stem}_{width}px.jpg"
        output_path = output_dir / output_name
        
        # Run ImageMagick convert
        cmd = [
            'convert', str(image_path),
            '-resize', f'{width}>',  # Only resize if larger
            '-quality', str(quality),
            '-strip',  # Remove metadata
            str(output_path)
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            new_size = output_path.stat().st_size
            reduction = ((original_size - new_size) / original_size) * 100
            
            results.append({
                "path": str(output_path),
                "size": f"{width}px",
                "file_size": new_size,
                "size_reduction": reduction
            })
            
            print(f"  Created: {output_name} ({new_size / 1024:.1f} KB, {reduction:.1f}% reduction)")
            
        except subprocess.CalledProcessError as e:
            print(f"  Error processing {width}px: {e}")
    
    return results


def main():
    """Main CLI function"""
    if len(sys.argv) < 2:
        print("Usage: python3 image_optimizer_minimal.py <command> [options]")
        print("\nCommands:")
        print("  analyze <folder>    Analyze images in folder")
        print("  optimize <image>    Optimize a single image (requires ImageMagick)")
        print("  check-deps          Check if dependencies are available")
        return
    
    command = sys.argv[1]
    
    if command == "check-deps":
        check_dependencies()
    
    elif command == "analyze":
        if len(sys.argv) < 3:
            print("Usage: python3 image_optimizer_minimal.py analyze <folder>")
            return
        
        folder_path = sys.argv[2]
        recursive = "--recursive" in sys.argv or "-r" in sys.argv
        
        analyze_folder(folder_path, recursive)
    
    elif command == "optimize":
        if len(sys.argv) < 3:
            print("Usage: python3 image_optimizer_minimal.py optimize <image_path>")
            return
        
        image_path = sys.argv[2]
        
        if not Path(image_path).exists():
            print(f"Error: Image not found: {image_path}")
            return
        
        # Create backup
        backup_folder = ".image_optimizer_backup"
        backup_path = create_backup(image_path, backup_folder)
        print(f"Created backup: {backup_path}")
        
        # Create output directory
        output_dir = Path(image_path).parent / f"{Path(image_path).stem}_optimized"
        
        # Optimize
        print(f"Optimizing {image_path}...")
        results = optimize_with_imagemagick(image_path, output_dir)
        
        if results:
            print(f"\nOptimization complete! Created {len(results)} optimized versions.")
            print(f"Output directory: {output_dir}")
        else:
            print("Optimization failed.")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()