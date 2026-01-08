from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image-optimizer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "image-optimizer=image_optimizer.cli:main",
        ],
    },
    author="Blog Image Optimizer",
    description="Image optimization utility for Hugo blogs",
    long_description="A Python utility to resize and optimize images for Hugo static sites",
    long_description_content_type="text/plain",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)