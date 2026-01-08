"""
Configuration settings for image optimization
"""

# Default responsive image sizes (width in pixels)
DEFAULT_SIZES = [400, 800, 1200]

# Quality settings for different image types
QUALITY_SETTINGS = {
    "photo": {
        "jpeg": 85,
        "webp": 85
    },
    "screenshot": {
        "png": 90,
        "webp": 90
    },
    "graphic": {
        "png": 95,
        "webp": 95
    }
}

# File size thresholds (in bytes)
LARGE_FILE_THRESHOLD = 1024 * 1024  # 1MB
MEDIUM_FILE_THRESHOLD = 500 * 1024   # 500KB

# Supported image formats
SUPPORTED_FORMATS = {
    "input": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "output": [".jpg", ".png", ".webp"]
}

# Backup folder name
BACKUP_FOLDER = ".image_optimizer_backup"