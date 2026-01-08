"""
Command-line interface for image optimizer
"""

import click
import sys
from pathlib import Path

from .processor import ImageProcessor
from .batch import BatchProcessor
from .utils import format_file_size


@click.group()
@click.version_option(version="1.0.0")
def main():
    """Image Optimizer for Hugo Blogs
    
    A utility to resize and optimize images for Hugo static sites.
    Generates responsive image sizes and WebP versions.
    """
    pass


@main.command()
@click.argument("image_path", type=click.Path(exists=True))
@click.option("--sizes", "-s", default="400,800,1200", 
              help="Comma-separated list of widths to generate (default: 400,800,1200)")
@click.option("--quality", "-q", type=int, help="Override quality (0-100)")
@click.option("--webp/--no-webp", default=True, help="Generate WebP versions")
@click.option("--backup/--no-backup", default=True, help="Backup original files")
@click.option("--backup-folder", default=".image_optimizer_backup", 
              help="Backup folder name")
@click.option("--dry-run", is_flag=True, help="Show what would be done without making changes")
def optimize(image_path, sizes, quality, webp, backup, backup_folder, dry_run):
    """Optimize a single image file"""
    
    # Parse sizes
    try:
        size_list = [int(s.strip()) for s in sizes.split(",")]
    except ValueError:
        click.echo("Error: Sizes must be comma-separated integers", err=True)
        sys.exit(1)
    
    try:
        processor = ImageProcessor(backup=backup, backup_folder=backup_folder)
        
        if dry_run:
            click.echo("DRY RUN MODE - No files will be modified\n")
        
        result = processor.process_image(
            image_path, 
            sizes=size_list,
            quality=quality,
            generate_webp=webp,
            dry_run=dry_run
        )
        
        # Display results
        click.echo(f"\nProcessed: {result['original_path']}")
        click.echo(f"Original size: {format_file_size(result['original_size'])}")
        
        if result["backup_created"]:
            click.echo(f"Backup created: {backup_folder}")
        
        if result["outputs"]:
            click.echo(f"\nGenerated {len(result['outputs'])} output files:")
            for output in result["outputs"]:
                size_str = f"{output['size'][0]}x{output['size'][1]}"
                click.echo(f"  {output['path']} ({size_str}, {output['format'].upper()}, {format_file_size(output['file_size'])})")
        
        if not dry_run:
            stats = processor.get_stats()
            if stats["processed"] > 0:
                reduction = stats["size_reduction_percent"]
                click.echo(f"\nSize reduction: {reduction:.1f}%")
    
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument("folder_path", type=click.Path(exists=True))
@click.option("--sizes", "-s", default="400,800,1200", 
              help="Comma-separated list of widths to generate (default: 400,800,1200)")
@click.option("--quality", "-q", type=int, help="Override quality (0-100)")
@click.option("--webp/--no-webp", default=True, help="Generate WebP versions")
@click.option("--backup/--no-backup", default=True, help="Backup original files")
@click.option("--backup-folder", default=".image_optimizer_backup", 
              help="Backup folder name")
@click.option("--recursive/--no-recursive", default=True, help="Process subfolders")
@click.option("--workers", "-w", default=4, help="Number of parallel workers")
@click.option("--dry-run", is_flag=True, help="Show what would be done without making changes")
def batch(folder_path, sizes, quality, webp, backup, backup_folder, recursive, workers, dry_run):
    """Process all images in a folder"""
    
    # Parse sizes
    try:
        size_list = [int(s.strip()) for s in sizes.split(",")]
    except ValueError:
        click.echo("Error: Sizes must be comma-separated integers", err=True)
        sys.exit(1)
    
    try:
        batch_processor = BatchProcessor(max_workers=workers, backup=backup, backup_folder=backup_folder)
        
        if dry_run:
            click.echo("DRY RUN MODE - No files will be modified\n")
        
        results = batch_processor.process_folder(
            folder_path,
            recursive=recursive,
            sizes=size_list,
            quality=quality,
            generate_webp=webp,
            dry_run=dry_run
        )
        
        # Print summary
        batch_processor.print_summary()
        
        if dry_run:
            click.echo("\nDRY RUN COMPLETED - No files were modified")
    
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument("folder_path", type=click.Path(exists=True))
@click.option("--recursive/--no-recursive", default=True, help="Analyze subfolders")
def analyze(folder_path, recursive):
    """Analyze images in a folder without processing"""
    
    try:
        batch_processor = BatchProcessor()
        analysis = batch_processor.analyze_folder(folder_path, recursive=recursive)
        
        batch_processor.print_analysis(analysis)
        
        # Provide recommendations
        if analysis["size_breakdown"]["large"] > 0:
            click.echo(f"\n--- Recommendations ---")
            click.echo(f"Found {analysis['size_breakdown']['large']} large files (>1MB)")
            click.echo("Consider optimizing these files for better web performance")
            click.echo("Run: image-optimizer batch --dry-run " + str(folder_path))
    
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
def version():
    """Show version information"""
    click.echo("Image Optimizer v1.0.0")
    click.echo("A utility for optimizing images in Hugo blogs")


if __name__ == "__main__":
    main()
