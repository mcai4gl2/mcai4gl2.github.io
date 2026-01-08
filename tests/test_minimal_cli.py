"""
Unit tests for minimal CLI
"""

import unittest
import tempfile
import shutil
import sys
from pathlib import Path

# Add parent directory to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent))

from image_optimizer_minimal import main as minimal_main


class TestMinimalCLI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test images
        self.create_test_files()
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def create_test_files(self):
        """Create test files"""
        self.test_folder = Path(self.temp_dir) / "test_images"
        self.test_folder.mkdir()
        
        # Create dummy image files
        for i in range(3):
            image_path = self.test_folder / f"test_image_{i}.jpg"
            image_path.write_text(f"dummy image content {i}")
    
    def test_minimal_check_deps(self):
        """Test minimal CLI check-deps command"""
        original_argv = sys.argv
        
        try:
            sys.argv = ['image_optimizer_minimal.py', 'check-deps']
            # Capture output
            from io import StringIO
            import contextlib
            
            f = StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    minimal_main()
                except SystemExit:
                    pass
            
            output = f.getvalue()
            # Check if dependency check was performed
            self.assertTrue(len(output) > 0)
        finally:
            sys.argv = original_argv
    
    def test_minimal_analyze(self):
        """Test minimal CLI analyze command"""
        original_argv = sys.argv
        
        try:
            sys.argv = ['image_optimizer_minimal.py', 'analyze', str(self.test_folder)]
            
            from io import StringIO
            import contextlib
            
            f = StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    minimal_main()
                except SystemExit:
                    pass
            
            output = f.getvalue()
            # Check if analysis was performed
            self.assertIn('Image Analysis', output)
            self.assertIn('Total files:', output)
        finally:
            sys.argv = original_argv
    
    def test_minimal_analyze_nonexistent(self):
        """Test minimal CLI analyze with non-existent folder"""
        original_argv = sys.argv
        
        try:
            sys.argv = ['image_optimizer_minimal.py', 'analyze', 'nonexistent']
            
            from io import StringIO
            import contextlib
            
            f = StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    minimal_main()
                except SystemExit:
                    pass
            
            output = f.getvalue()
            # Check if error was handled
            self.assertIn('Error:', output)
        finally:
            sys.argv = original_argv
    
    def test_minimal_unknown_command(self):
        """Test minimal CLI with unknown command"""
        original_argv = sys.argv
        
        try:
            sys.argv = ['image_optimizer_minimal.py', 'unknown_command']
            
            from io import StringIO
            import contextlib
            
            f = StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    minimal_main()
                except SystemExit:
                    pass
            
            output = f.getvalue()
            # Check if unknown command was handled
            self.assertIn('Unknown command', output)
        finally:
            sys.argv = original_argv


if __name__ == '__main__':
    unittest.main()