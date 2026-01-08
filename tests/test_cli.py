"""
Unit tests for CLI interface
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner
from PIL import Image
import numpy as np

from image_optimizer.cli import main
from image_optimizer_minimal import main as minimal_main


class TestCLI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.runner = CliRunner()
        
        # Create test images
        self.create_test_images()
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def create_test_images(self):
        """Create test images"""
        self.test_folder = Path(self.temp_dir) / "test_images"
        self.test_folder.mkdir()
        
        # Create a test image
        image_path = self.test_folder / "test.jpg"
        image_array = np.random.randint(0, 256, (800, 600, 3), dtype=np.uint8)
        image = Image.fromarray(image_array, 'RGB')
        image.save(image_path, 'JPEG', quality=95)
    
    def test_cli_version(self):
        """Test version command"""
        result = self.runner.invoke(main, ['version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Image Optimizer v1.0.0', result.output)
    
    def test_cli_analyze(self):
        """Test analyze command"""
        result = self.runner.invoke(main, ['analyze', str(self.test_folder)])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Image Analysis', result.output)
        self.assertIn('Total files:', result.output)
    
    def test_cli_optimize_dry_run(self):
        """Test optimize command with dry run"""
        image_path = self.test_folder / "test.jpg"
        result = self.runner.invoke(main, [
            'optimize', str(image_path),
            '--dry-run'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('DRY RUN MODE', result.output)
    
    def test_cli_batch_dry_run(self):
        """Test batch command with dry run"""
        result = self.runner.invoke(main, [
            'batch', str(self.test_folder),
            '--dry-run'
        ])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('DRY RUN MODE', result.output)
    
    def test_cli_optimize_nonexistent_file(self):
        """Test optimize command with non-existent file"""
        result = self.runner.invoke(main, ['optimize', 'nonexistent.jpg'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('Error:', result.output)
    
    def test_cli_batch_nonexistent_folder(self):
        """Test batch command with non-existent folder"""
        result = self.runner.invoke(main, ['batch', 'nonexistent_folder'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('Error:', result.output)
    
    def test_cli_invalid_sizes(self):
        """Test invalid sizes parameter"""
        image_path = self.test_folder / "test.jpg"
        result = self.runner.invoke(main, [
            'optimize', str(image_path),
            '--sizes', 'invalid'
        ])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('Error:', result.output)


class TestMinimalCLI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test images
        self.create_test_images()
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def create_test_images(self):
        """Create test images"""
        self.test_folder = Path(self.temp_dir) / "test_images"
        self.test_folder.mkdir()
        
        # Create a test image
        image_path = self.test_folder / "test.jpg"
        image_array = np.random.randint(0, 256, (800, 600, 3), dtype=np.uint8)
        image = Image.fromarray(image_array, 'RGB')
        image.save(image_path, 'JPEG', quality=95)
    
    def test_minimal_analyze(self):
        """Test minimal CLI analyze command"""
        import sys
        original_argv = sys.argv
        
        try:
            sys.argv = ['image_optimizer_minimal.py', 'analyze', str(self.test_folder)]
            minimal_main()
        except SystemExit:
            pass  # Expected behavior
        finally:
            sys.argv = original_argv
    
    def test_minimal_check_deps(self):
        """Test minimal CLI check-deps command"""
        import sys
        original_argv = sys.argv
        
        try:
            sys.argv = ['image_optimizer_minimal.py', 'check-deps']
            minimal_main()
        except SystemExit:
            pass  # Expected behavior
        finally:
            sys.argv = original_argv


if __name__ == '__main__':
    unittest.main()