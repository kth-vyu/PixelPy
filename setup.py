from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pixelpy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow>=9.0.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "mypy>=1.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    author="kth.vyu",
    author_email="kozyreva.k1@ya.ru",
    description="Библиотека для создания пиксельных изображений с настраиваемой сеткой и палитрой",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kth-vyu/PixelPy",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    keywords="image processing, pixel art, image manipulation, PIL, Pillow, pixelization",
    project_urls={
        "Bug Tracker": "https://github.com/kth-vyu/PixelPy/issues",
        "Documentation": "https://github.com/kth-vyu/PixelPy#readme",
        "Source Code": "https://github.com/kth-vyu/PixelPy",
    },
) 