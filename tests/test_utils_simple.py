"""
Unit tests for utility functions - simplified version without external dependencies
"""

import unittest
import tempfile
import os
from pathlib import Path

from image_optimizer.utils import (
    is_image_file,
    calculate_output_sizes,
    get_quality_settings,
    format_file_size,
    calculate_size_reduction
)


class TestUtilsSimple(unittest.TestCase):
    
    def test_is_image_file(self):
        """Test image file detection"""
        # Test valid image files
        self.assertTrue(is_image_file("test.jpg"))
        self.assertTrue(is_image_file("test.jpeg"))
        self.assertTrue(is_image_file("test.png"))
        self.assertTrue(is_image_file("test.gif"))
        
        # Test invalid files
        self.assertFalse(is_image_file("test.txt"))
        self.assertFalse(is_image_file("test.pdf"))
        self.assertFalse(is_image_file("test"))
    
    def test_calculate_output_sizes(self):
        """Test output size calculation"""
        # Test with larger image
        original_size = (2000, 1000)  # 2:1 aspect ratio
        target_sizes = [400, 800, 1200]
        
        result = calculate_output_sizes(original_size, target_sizes)
        
        # Check that all target sizes are present
        self.assertEqual(len(result), 3)
        self.assertIn(400, result)
        self.assertIn(800, result)
        self.assertIn(1200, result)
        
        # Check aspect ratio is maintained
        for width, (new_width, new_height) in result.items():
            self.assertEqual(new_width, width)
            self.assertAlmostEqual(new_height, width * 0.5)
        
        # Test with smaller image (no upscaling)
        small_size = (300, 200)
        result = calculate_output_sizes(small_size, target_sizes)
        
        for width, dimensions in result.items():
            self.assertEqual(dimensions, small_size)
    
    def test_get_quality_settings(self):
        """Test quality settings retrieval"""
        # Test photo quality
        photo_jpeg_quality = get_quality_settings("photo", "jpeg")
        self.assertEqual(photo_jpeg_quality, 85)
        
        photo_webp_quality = get_quality_settings("photo", "webp")
        self.assertEqual(photo_webp_quality, 85)
        
        # Test screenshot quality
        screenshot_png_quality = get_quality_settings("screenshot", "png")
        self.assertEqual(screenshot_png_quality, 90)
        
        # Test graphic quality
        graphic_webp_quality = get_quality_settings("graphic", "webp")
        self.assertEqual(graphic_webp_quality, 95)
        
        # Test unknown content type (defaults to photo)
        unknown_quality = get_quality_settings("unknown", "jpeg")
        self.assertEqual(unknown_quality, 85)
    
    def test_format_file_size(self):
        """Test file size formatting"""
        # Test bytes
        self.assertEqual(format_file_size(512), "512 B")
        
        # Test kilobytes
        self.assertEqual(format_file_size(1024), "1.0 KB")
        self.assertEqual(format_file_size(1536), "1.5 KB")
        
        # Test megabytes
        self.assertEqual(format_file_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_file_size(2.5 * 1024 * 1024), "2.5 MB")
    
    def test_calculate_size_reduction(self):
        """Test size reduction calculation"""
        # Test 50% reduction
        reduction = calculate_size_reduction(1000, 500)
        self.assertEqual(reduction, 50.0)
        
        # Test 25% reduction
        reduction = calculate_size_reduction(1000, 750)
        self.assertEqual(reduction, 25.0)
        
        # Test no reduction
        reduction = calculate_size_reduction(1000, 1000)
        self.assertEqual(reduction, 0.0)
        
        # Test edge case (zero original size)
        reduction = calculate_size_reduction(0, 500)
        self.assertEqual(reduction, 0)


if __name__ == '__main__':
    unittest.main()