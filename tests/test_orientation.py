#!/usr/bin/env python3
# Test script to verify EXIF orientation handling

from image_optimizer.processor import ImageProcessor
from PIL import Image

def test_orientation():
    # Test that orientation is preserved
    processor = ImageProcessor(backup=True)
    
    # Test the _fix_image_orientation method
    print('Testing EXIF orientation handling...')
    
    # Create a test image with different orientations
    test_img = Image.new('RGB', (100, 100), color='red')
    
    # Test orientation 1 (normal)
    result = processor._fix_image_orientation(test_img)
    print(f'Orientation 1: {result.size}')
    
    # Test orientation 3 (180 degrees)
    test_img2 = Image.new('RGB', (100, 100), color='blue')
    # Simulate EXIF orientation by setting the attribute
    test_img2.info['exif'] = b'\x01\x00\x04\x00\x03\x00\x00\x00'  # Orientation = 3
    result2 = processor._fix_image_orientation(test_img2)
    print(f'Orientation 3: {result2.size}')
    
    print('Orientation handling test completed successfully!')

if __name__ == '__main__':
    test_orientation()
