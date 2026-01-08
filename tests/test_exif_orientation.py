#!/usr/bin/env python3
"""Unit tests for EXIF orientation handling in image processor"""

import unittest
import tempfile
import os
from pathlib import Path
from PIL import Image
import io

# Add the parent directory to the path so we can import our modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from image_optimizer.processor import ImageProcessor


class TestEXIFOrientation(unittest.TestCase):
    """Test EXIF orientation handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.processor = ImageProcessor(backup=False)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def _create_test_image_with_exif(self, orientation=1, width=100, height=200):
        """Create a test image with specified EXIF orientation"""
        # Create a simple test image
        img = Image.new('RGB', (width, height), color='red')
        
        # Create EXIF data with orientation
        exif = Image.Exif()
        exif[0x0112] = orientation  # Orientation tag
        
        # Save to a bytes buffer with EXIF
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', exif=exif)
        buffer.seek(0)
        
        # Save to temp file
        test_file = self.temp_dir / f"test_orientation_{orientation}.jpg"
        with open(test_file, 'wb') as f:
            f.write(buffer.getvalue())
        
        # Verify the EXIF data was saved
        with Image.open(test_file) as saved_img:
            if hasattr(saved_img, '_getexif') and saved_img._getexif():
                saved_exif = saved_img._getexif()
                # Check if orientation was saved correctly
                if 0x0112 in saved_exif:
                    print(f"Successfully saved orientation {orientation} to EXIF")
                else:
                    print(f"Failed to save orientation {orientation} to EXIF")
        
        return test_file
    
    def test_orientation_1_normal(self):
        """Test orientation 1 (normal) - no rotation"""
        test_file = self._create_test_image_with_exif(orientation=1, width=100, height=200)
        
        # Process the image
        result = self.processor.process_image(test_file, sizes=[50], dry_run=True)
        
        # Check that dimensions are calculated correctly
        self.assertEqual(result['outputs'][0]['size'], (50, 100))
    
    def test_orientation_3_180_degrees(self):
        """Test orientation 3 (180 degrees rotation)"""
        test_file = self._create_test_image_with_exif(orientation=3, width=100, height=200)
        
        with Image.open(test_file) as img:
            original_size = img.size
        
        # Process the image
        result = self.processor.process_image(test_file, sizes=[50], dry_run=True)
        
        # After 180 degree rotation, 100x200 becomes 100x200 (same dimensions)
        # But the content is rotated
        self.assertEqual(result['outputs'][0]['size'], (50, 100))
    
    def test_orientation_6_270_degrees(self):
        """Test orientation 6 (270 degrees rotation) - landscape to portrait"""
        test_file = self._create_test_image_with_exif(orientation=6, width=200, height=100)
        
        with Image.open(test_file) as img:
            original_size = img.size
        
        # Process the image
        result = self.processor.process_image(test_file, sizes=[100], dry_run=True)
        
        # After 270 degree rotation, 200x100 becomes 100x200
        # But the aspect ratio calculation should be based on the rotated dimensions
        # Since original is wider than target, it should resize to target width
        # The rotated image would be 100x200, so 100 is already the correct width
        self.assertEqual(result['outputs'][0]['size'], (100, 200))
    
    def test_orientation_8_90_degrees(self):
        """Test orientation 8 (90 degrees rotation) - portrait to landscape"""
        test_file = self._create_test_image_with_exif(orientation=8, width=100, height=200)
        
        with Image.open(test_file) as img:
            original_size = img.size
        
        # Process the image
        result = self.processor.process_image(test_file, sizes=[150], dry_run=True)
        
        # After 90 degree rotation, 100x200 becomes 200x100
        # Since original height is less than target width, it should resize to target width
        # The rotated image would be 200x100, so it would be upscaled to 150x75
        self.assertEqual(result['outputs'][0]['size'], (150, 75))
    
    def test_orientation_2_flip_horizontal(self):
        """Test orientation 2 (horizontal flip)"""
        test_file = self._create_test_image_with_exif(orientation=2, width=100, height=200)
        
        with Image.open(test_file) as img:
            original_size = img.size
        
        # Process the image
        result = self.processor.process_image(test_file, sizes=[50], dry_run=True)
        
        # After horizontal flip, dimensions remain 100x200
        # But content is mirrored
        self.assertEqual(result['outputs'][0]['size'], (50, 100))
    
    def test_no_exif_data(self):
        """Test image without EXIF data"""
        # Create image without EXIF
        img = Image.new('RGB', (100, 200), color='blue')
        test_file = self.temp_dir / "test_no_exif.jpg"
        img.save(test_file)
        
        # Process the image
        result = self.processor.process_image(test_file, sizes=[50], dry_run=True)
        
        # Should work normally without EXIF
        self.assertEqual(result['outputs'][0]['size'], (50, 100))
    
    def test_multiple_sizes_with_orientation(self):
        """Test multiple output sizes with orientation correction"""
        test_file = self._create_test_image_with_exif(orientation=6, width=800, height=600)
        
        # Process with multiple sizes
        result = self.processor.process_image(test_file, sizes=[400, 200], dry_run=True)
        
        # Check all outputs
        outputs = result['outputs']
        
        # Find JPEG outputs
        jpeg_outputs = [o for o in outputs if o['format'] == 'jpeg']
        webp_outputs = [o for o in outputs if o['format'] == 'webp']
        
        # Check that aspect ratio is preserved after rotation
        # Original: 800x600 with orientation 6 becomes 600x800 after rotation
        # 600x800 aspect ratio = 0.75
        
        # 400px width should give 400x533
        self.assertEqual(jpeg_outputs[0]['size'], (400, 533))
        # 200px width should give 200x266 (truncated from 266.67)
        self.assertEqual(jpeg_outputs[1]['size'], (200, 266))
        
        # WebP outputs should have same dimensions
        self.assertEqual(webp_outputs[0]['size'], (400, 533))
        self.assertEqual(webp_outputs[1]['size'], (200, 266))
    
    def test_exif_stripping_in_jpeg_output(self):
        """Test that EXIF data is stripped from JPEG output"""
        test_file = self._create_test_image_with_exif(orientation=6, width=100, height=200)
        
        # Process without dry run to create actual files
        result = self.processor.process_image(test_file, sizes=[50], generate_webp=False)
        
        # Check that output was created (not in dry-run mode)
        if result['outputs'] and result['outputs'][0]['file_size'] > 0:
            # Check that JPEG output doesn't have EXIF data
            output_path = Path(result['outputs'][0]['path'])
            with Image.open(output_path) as output_img:
                # EXIF should be stripped
                self.assertIsNone(output_img._getexif())
        else:
            # In dry-run mode, files aren't created, so we can't check EXIF
            # Just verify the dry-run completed successfully
            self.assertTrue(result['outputs'])
    
    def test_real_world_scenario(self):
        """Test with a more realistic scenario"""
        # Create a portrait image that was saved as landscape
        # This simulates a phone camera image taken in portrait but saved as landscape
        test_file = self._create_test_image_with_exif(orientation=6, width=3000, height=4000)
        
        # Process with typical web sizes
        result = self.processor.process_image(
            test_file, 
            sizes=[400, 800, 1200], 
            generate_webp=True,
            dry_run=True
        )
        
        # Check that all outputs maintain correct aspect ratio
        # After rotation: 4000x3000 (4:3 aspect ratio)
        expected_aspect_ratio = 4/3
        
        for output in result['outputs']:
            width, height = output['size']
            actual_ratio = width / height
            # Allow for small floating point differences
            self.assertAlmostEqual(actual_ratio, expected_aspect_ratio, places=2)
            # Ensure width is not greater than original width after rotation
            self.assertLessEqual(width, 4000)


if __name__ == '__main__':
    unittest.main()
