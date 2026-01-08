"""
Unit tests for configuration settings
"""

import unittest
from image_optimizer.config import (
    DEFAULT_SIZES,
    QUALITY_SETTINGS,
    LARGE_FILE_THRESHOLD,
    MEDIUM_FILE_THRESHOLD,
    SUPPORTED_FORMATS,
    BACKUP_FOLDER
)


class TestConfig(unittest.TestCase):
    
    def test_default_sizes(self):
        """Test default image sizes"""
        self.assertIsInstance(DEFAULT_SIZES, list)
        self.assertEqual(DEFAULT_SIZES, [400, 800, 1200])
        self.assertTrue(all(isinstance(size, int) for size in DEFAULT_SIZES))
    
    def test_quality_settings(self):
        """Test quality settings structure"""
        self.assertIsInstance(QUALITY_SETTINGS, dict)
        
        # Check required content types
        self.assertIn("photo", QUALITY_SETTINGS)
        self.assertIn("screenshot", QUALITY_SETTINGS)
        self.assertIn("graphic", QUALITY_SETTINGS)
        
        # Check each content type has format settings
        for content_type, settings in QUALITY_SETTINGS.items():
            self.assertIsInstance(settings, dict)
            # Note: screenshot and graphic only have png/webp, not jpeg
            if content_type == "photo":
                self.assertIn("jpeg", settings)
                self.assertIn("webp", settings)
            else:
                self.assertIn("png", settings)
                self.assertIn("webp", settings)
            
            # Check quality values are valid
            for format_name, quality in settings.items():
                self.assertIsInstance(quality, int)
                self.assertGreaterEqual(quality, 0)
                self.assertLessEqual(quality, 100)
    
    def test_file_thresholds(self):
        """Test file size thresholds"""
        self.assertIsInstance(LARGE_FILE_THRESHOLD, int)
        self.assertIsInstance(MEDIUM_FILE_THRESHOLD, int)
        self.assertGreater(LARGE_FILE_THRESHOLD, MEDIUM_FILE_THRESHOLD)
        self.assertEqual(LARGE_FILE_THRESHOLD, 1024 * 1024)  # 1MB
        self.assertEqual(MEDIUM_FILE_THRESHOLD, 500 * 1024)  # 500KB
    
    def test_supported_formats(self):
        """Test supported image formats"""
        self.assertIsInstance(SUPPORTED_FORMATS, dict)
        self.assertIn("input", SUPPORTED_FORMATS)
        self.assertIn("output", SUPPORTED_FORMATS)
        
        # Check input formats
        input_formats = SUPPORTED_FORMATS["input"]
        self.assertIsInstance(input_formats, list)
        self.assertIn(".jpg", input_formats)
        self.assertIn(".jpeg", input_formats)
        self.assertIn(".png", input_formats)
        self.assertIn(".gif", input_formats)
        
        # Check output formats
        output_formats = SUPPORTED_FORMATS["output"]
        self.assertIsInstance(output_formats, list)
        self.assertIn(".jpg", output_formats)
        self.assertIn(".png", output_formats)
        self.assertIn(".webp", output_formats)
    
    def test_backup_folder(self):
        """Test backup folder setting"""
        self.assertIsInstance(BACKUP_FOLDER, str)
        self.assertEqual(BACKUP_FOLDER, ".image_optimizer_backup")
        self.assertTrue(BACKUP_FOLDER.startswith("."))


if __name__ == '__main__':
    unittest.main()