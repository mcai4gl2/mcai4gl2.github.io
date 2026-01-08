"""
Unit tests for image processor
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import numpy as np

from image_optimizer.processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.backup_dir = tempfile.mkdtemp()
        
        # Create test image
        self.test_image_path = self.create_test_image()
        
        # Initialize processor
        self.processor = ImageProcessor(backup=True, backup_folder=self.backup_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.backup_dir)
    
    def create_test_image(self):
        """Create a test image"""
        image_path = Path(self.temp_dir) / "test_image.jpg"
        
        # Create a simple test image
        image_array = np.random.randint(0, 256, (800, 600, 3), dtype=np.uint8)
        image = Image.fromarray(image_array, 'RGB')
        image.save(image_path, 'JPEG', quality=95)
        
        return image_path
    
    def test_process_image_basic(self):
        """Test basic image processing"""
        result = self.processor.process_image(
            self.test_image_path,
            sizes=[400, 800],
            quality=85,
            generate_webp=False,
            dry_run=False
        )
        
        # Check result structure
        self.assertIn("original_path", result)
        self.assertIn("original_size", result)
        self.assertIn("outputs", result)
        self.assertIn("backup_created", result)
        
        # Check that backup was created
        self.assertTrue(result["backup_created"])
        
        # Check that outputs were generated
        self.assertEqual(len(result["outputs"]), 2)  # 400px and 800px versions
        
        # Check output files exist
        for output in result["outputs"]:
            self.assertTrue(Path(output["path"]).exists())
            self.assertEqual(output["format"], "jpeg")
    
    def test_process_image_with_webp(self):
        """Test image processing with WebP generation"""
        result = self.processor.process_image(
            self.test_image_path,
            sizes=[400],
            quality=85,
            generate_webp=True,
            dry_run=False
        )
        
        # Should have both JPEG and WebP versions
        self.assertEqual(len(result["outputs"]), 2)
        
        formats = [output["format"] for output in result["outputs"]]
        self.assertIn("jpeg", formats)
        self.assertIn("webp", formats)
    
    def test_process_image_dry_run(self):
        """Test dry run mode"""
        result = self.processor.process_image(
            self.test_image_path,
            sizes=[400],
            generate_webp=True,  # This is the default
            dry_run=True
        )
        
        # Check that outputs were created (jpg and webp)
        self.assertEqual(len(result["outputs"]), 2)
        for output in result["outputs"]:
            self.assertEqual(output["file_size"], 0)
        
        # Check that backup was not created
        self.assertFalse(result["backup_created"])
        
        # Check that stats were not updated in dry run
        stats = self.processor.get_stats()
        self.assertEqual(stats["processed"], 0)
    
    def test_process_nonexistent_file(self):
        """Test processing non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.processor.process_image("nonexistent.jpg")
    
    def test_process_unsupported_format(self):
        """Test processing unsupported file format"""
        # Create a text file
        text_file = Path(self.temp_dir) / "test.txt"
        text_file.write_text("This is not an image")
        
        with self.assertRaises(ValueError):
            self.processor.process_image(text_file)
    
    def test_get_stats(self):
        """Test statistics tracking"""
        # Process an image
        self.processor.process_image(self.test_image_path, dry_run=False)
        
        stats = self.processor.get_stats()
        
        # Check stats structure
        self.assertIn("processed", stats)
        self.assertIn("original_size", stats)
        self.assertIn("optimized_size", stats)
        self.assertIn("files_created", stats)
        self.assertIn("size_reduction_percent", stats)
        
        # Should have processed 1 file
        self.assertEqual(stats["processed"], 1)
    
    def test_reset_stats(self):
        """Test statistics reset"""
        # Process an image
        self.processor.process_image(self.test_image_path, dry_run=True)
        
        # Reset stats
        self.processor.reset_stats()
        
        # Check stats are reset
        stats = self.processor.get_stats()
        self.assertEqual(stats["processed"], 0)
        self.assertEqual(stats["files_created"], 0)
    
    def test_no_backup_mode(self):
        """Test processing without backup"""
        processor = ImageProcessor(backup=False)
        
        result = processor.process_image(
            self.test_image_path,
            sizes=[400],
            dry_run=False
        )
        
        # Check that backup was not created
        self.assertFalse(result["backup_created"])


if __name__ == '__main__':
    unittest.main()