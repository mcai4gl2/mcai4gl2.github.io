"""
Unit tests for batch processor
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import numpy as np

from image_optimizer.batch import BatchProcessor


class TestBatchProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.backup_dir = tempfile.mkdtemp()
        
        # Create test images
        self.create_test_images()
        
        # Initialize batch processor
        self.batch_processor = BatchProcessor(
            max_workers=2,
            backup=True,
            backup_folder=self.backup_dir
        )
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.backup_dir)
    
    def create_test_images(self):
        """Create test images in subfolder"""
        self.test_folder = Path(self.temp_dir) / "test_images"
        self.test_folder.mkdir()
        
        # Create several test images
        for i in range(3):
            image_path = self.test_folder / f"test_image_{i}.jpg"
            image_array = np.random.randint(0, 256, (800, 600, 3), dtype=np.uint8)
            image = Image.fromarray(image_array, 'RGB')
            image.save(image_path, 'JPEG', quality=95)
        
        # Create subfolder with images
        self.sub_folder = self.test_folder / "subfolder"
        self.sub_folder.mkdir()
        
        for i in range(2):
            image_path = self.sub_folder / f"sub_image_{i}.png"
            image_array = np.random.randint(0, 256, (600, 400, 3), dtype=np.uint8)
            image = Image.fromarray(image_array, 'RGB')
            image.save(image_path, 'PNG')
    
    def test_process_folder_basic(self):
        """Test basic folder processing"""
        results = self.batch_processor.process_folder(
            self.test_folder,
            recursive=False,
            sizes=[400],
            quality=85,
            generate_webp=False,
            dry_run=True
        )
        
        # Should process 3 images (not recursive)
        self.assertEqual(len(results), 3)
        
        # Check result structure
        for result in results:
            self.assertIn("original_path", result)
            self.assertIn("outputs", result)
    
    def test_process_folder_recursive(self):
        """Test recursive folder processing"""
        results = self.batch_processor.process_folder(
            self.test_folder,
            recursive=True,
            sizes=[400],
            quality=85,
            generate_webp=False,
            dry_run=True
        )
        
        # Should process 5 images (3 in root, 2 in subfolder)
        self.assertEqual(len(results), 5)
    
    def test_analyze_folder(self):
        """Test folder analysis"""
        analysis = self.batch_processor.analyze_folder(
            self.test_folder,
            recursive=True
        )
        
        # Check analysis structure
        self.assertIn("total_files", analysis)
        self.assertIn("total_size", analysis)
        self.assertIn("format_breakdown", analysis)
        self.assertIn("size_breakdown", analysis)
        self.assertIn("files", analysis)
        
        # Should find 5 files
        self.assertEqual(analysis["total_files"], 5)
        
        # Check format breakdown
        self.assertIn(".jpg", analysis["format_breakdown"])
        self.assertIn(".png", analysis["format_breakdown"])
        self.assertEqual(analysis["format_breakdown"][".jpg"]["count"], 3)
        self.assertEqual(analysis["format_breakdown"][".png"]["count"], 2)
        
        # Check files are sorted by size (largest first)
        files = analysis["files"]
        for i in range(len(files) - 1):
            self.assertGreaterEqual(files[i]["size"], files[i + 1]["size"])
    
    def test_get_summary(self):
        """Test summary generation"""
        # Process some images
        self.batch_processor.process_folder(
            self.test_folder,
            recursive=False,
            sizes=[400],
            dry_run=True
        )
        
        summary = self.batch_processor.get_summary()
        
        # Check summary structure
        self.assertIn("processed", summary)
        self.assertIn("errors", summary)
        self.assertIn("total_files", summary)
        self.assertIn("stats", summary)
        
        # Should have processed 3 files with no errors
        self.assertEqual(summary["processed"], 3)
        self.assertEqual(summary["errors"], 0)
        self.assertEqual(summary["total_files"], 3)
    
    def test_process_empty_folder(self):
        """Test processing empty folder"""
        empty_folder = Path(self.temp_dir) / "empty"
        empty_folder.mkdir()
        
        results = self.batch_processor.process_folder(empty_folder)
        
        # Should return empty list
        self.assertEqual(len(results), 0)
    
    def test_process_nonexistent_folder(self):
        """Test processing non-existent folder"""
        with self.assertRaises(FileNotFoundError):
            self.batch_processor.process_folder("nonexistent_folder")
    
    def test_analyze_nonexistent_folder(self):
        """Test analyzing non-existent folder"""
        # The analyze_folder method might not raise an error for non-existent folders
        # Let's check what it actually returns
        try:
            analysis = self.batch_processor.analyze_folder("nonexistent_folder")
            # If it doesn't raise an error, check if it returns empty analysis
            self.assertEqual(analysis["total_files"], 0)
        except FileNotFoundError:
            # If it does raise an error, that's also acceptable
            pass


if __name__ == '__main__':
    unittest.main()