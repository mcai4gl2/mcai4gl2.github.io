"""
Unit tests for CLI interface - simplified version
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner

from image_optimizer.cli import main


class TestCLISimple(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.runner = CliRunner()
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_cli_version(self):
        """Test version command"""
        result = self.runner.invoke(main, ['version'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Image Optimizer v1.0.0', result.output)
    
    def test_cli_help(self):
        """Test help command"""
        result = self.runner.invoke(main, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Image Optimizer for Hugo Blogs', result.output)
    
    def test_cli_analyze_nonexistent_folder(self):
        """Test analyze command with non-existent folder"""
        result = self.runner.invoke(main, ['analyze', 'nonexistent_folder'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('Error:', result.output)
    
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
        # Create a dummy file for testing
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("not an image")
        
        result = self.runner.invoke(main, [
            'optimize', str(test_file),
            '--sizes', 'invalid'
        ])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('Error:', result.output)
    
    def test_cli_analyze_dry_run(self):
        """Test analyze command with dry run (should work without images)"""
        # Create empty folder
        empty_folder = Path(self.temp_dir) / "empty"
        empty_folder.mkdir()
        
        result = self.runner.invoke(main, ['analyze', str(empty_folder)])
        self.assertEqual(result.exit_code, 0)
        # Check for any indication of empty analysis
        self.assertIn('Total files: 0', result.output)


if __name__ == '__main__':
    unittest.main()