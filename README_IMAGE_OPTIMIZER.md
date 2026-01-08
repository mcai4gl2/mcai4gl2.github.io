# Image Optimizer for Hugo Blog

A Python utility to resize and optimize images for Hugo static sites. This tool generates responsive image sizes and WebP versions while preserving the original folder structure.

## Features

- **Responsive Image Generation**: Creates multiple sizes (400px, 800px, 1200px) for different devices
- **Format Optimization**: Generates WebP versions for better compression
- **Smart Content Detection**: Automatically optimizes photos vs screenshots differently
- **Safe Operations**: Backups originals by default with dry-run capability
- **Batch Processing**: Process entire folders with parallel execution
- **Detailed Analysis**: Analyze image sizes and potential savings

## Installation

### Option 1: Full Version (requires Pillow, Click, tqdm)

```bash
pip install -e .
```

Or install dependencies manually:
```bash
pip install Pillow click tqdm
```

### Option 2: Minimal Version (no dependencies)

Use the included `image_optimizer_minimal.py` script which works with Python's built-in libraries.

## Usage

### Full Version Commands

```bash
# Analyze images in a folder
image-optimizer analyze static/meat

# Optimize a single image
image-optimizer optimize static/meat/first.jpg

# Process entire folder
image-optimizer batch static/meat --sizes 400,800,1200 --quality 85

# Preview what would be done
image-optimizer batch static/ --dry-run

# Generate only specific sizes
image-optimizer batch static/meat --sizes 800,1200

# Skip WebP generation
image-optimizer batch static/meat --no-webp

# Don't backup originals
image-optimizer batch static/meat --no-backup
```

### Minimal Version Commands

```bash
# Check dependencies
python3 image_optimizer_minimal.py check-deps

# Analyze images
python3 image_optimizer_minimal.py analyze static/meat

# Optimize with ImageMagick (if available)
python3 image_optimizer_minimal.py optimize static/meat/first.jpg
```

## Output Structure

The optimizer creates size-specific folders for each image:

```
static/
├── meat/
│   ├── first.jpg                 # Original
│   ├── first_400px/
│   │   └── first.jpg            # 400px version
│   ├── first_800px/
│   │   └── first.jpg            # 800px version
│   ├── first_800px/
│   │   └── first.webp           # 800px WebP version
│   └── first_1200px/
│       └── first.jpg            # 1200px version
```

## Configuration

Default settings can be modified in `image_optimizer/config.py`:

- **Default sizes**: [400, 800, 1200] pixels
- **Quality settings**: Different for photos vs screenshots
- **Backup folder**: `.image_optimizer_backup`

## Example Results

For your current meat folder images:

- **Before**: 5 files, 15.5 MB total
- **After optimization**: Estimated savings of ~9.3 MB (60% reduction)
- **Generated**: Multiple responsive sizes for better performance

## Integration with Hugo

The optimized images maintain the same URL structure, so your existing markdown references continue to work:

```markdown
![first](/meat/first.jpg)  # Still works
```

For responsive images, you can update your markdown to use the new sizes:

```markdown
<img srcset="/meat/first_400px/first.jpg 400w,
             /meat/first_800px/first.jpg 800w,
             /meat/first_1200px/first.jpg 1200w"
     sizes="(max-width: 400px) 400px, (max-width: 800px) 800px, 1200px"
     src="/meat/first_1200px/first.jpg"
     alt="First image">
```

## Troubleshooting

### Dependencies Not Available

If you can't install Pillow, use the minimal version with ImageMagick:

```bash
# Install ImageMagick on Ubuntu/Debian
sudo apt install imagemagick

# Use minimal optimizer
python3 image_optimizer_minimal.py optimize static/meat/first.jpg
```

### Permission Issues

Make sure you have write permissions to the static folder and backup location.

### Large Files Processing

For very large folders, adjust the worker count:

```bash
image-optimizer batch static/ --workers 8
```

## Development

To extend the utility:

1. Modify `image_optimizer/config.py` for default settings
2. Add new processors in `image_optimizer/processor.py`
3. Extend CLI commands in `image_optimizer/cli.py`