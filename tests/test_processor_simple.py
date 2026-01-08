"""
Unit tests for image processor - simplified version
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from image_optimizer.processor import ImageProcessor


class TestImageProcessorSimple(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.backup_dir = tempfile.mkdtemp()
        
        # Initialize processor
        self.processor = ImageProcessor(backup=True, backup_folder=self.backup_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.backup_dir)
    
    def test_processor_initialization(self):
        """Test processor initialization"""
        self.assertTrue(self.processor.backup)
        self.assertEqual(self.processor.backup_folder, self.backup_dir)
        self.assertEqual(self.processor.stats["processed"], 0)
        self.assertEqual(self.processor.stats["files_created"], 0)
    
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
        # Initially should have zero stats
        stats = self.processor.get_stats()
        
        # Check stats structure
        self.assertIn("processed", stats)
        self.assertIn("original_size", stats)
        self.assertIn("optimized_size", stats)
        self.assertIn("files_created", stats)
        self.assertIn("size_reduction_percent", stats)
        
        # Should have processed 0 files initially
        self.assertEqual(stats["processed"], 0)
        self.assertEqual(stats["files_created"], 0)
    
    def test_reset_stats(self):
        """Test statistics reset"""
        # Reset stats
        self.processor.reset_stats()
        
        # Check stats are reset
        stats = self.processor.get_stats()
        self.assertEqual(stats["processed"], 0)
        self.assertEqual(stats["files_created"], 0)
        self.assertEqual(stats["original_size"], 0)
        self.assertEqual(stats["optimized_size"], 0)
    
    def test_no_backup_mode(self):
        """Test processing without backup"""
        processor = ImageProcessor(backup=False)
        self.assertFalse(processor.backup)
    
    def test_create_output_path(self):
        """Test output path creation"""
        original_path = Path(self.temp_dir) / "test_image.jpg"
        
        # Test creating output path
        output_path = self.processor._create_output_path(original_path, 400, "jpg")
        
        # Check path structure
        self.assertIn("test_image_400px", str(output_path))
        self.assertEqual(output_path.name, "test_image.jpg")
        self.assertEqual(output_path.suffix, ".jpg")
    
    def test_create_output_path_webp(self):
        """Test output path creation for WebP"""
        original_path = Path(self.temp_dir) / "test_image.jpg"
        
        # Test creating WebP output path
        output_path = self.processor._create_output_path(original_path, 800, "webp")
        
        # Check path structure
        self.assertIn("test_image_800px", str(output_path))
        self.assertEqual(output_path.name, "test_image.webp")
        self.assertEqual(output_path.suffix, ".webp")


if __name__ == '__main__':
    unittest.main()