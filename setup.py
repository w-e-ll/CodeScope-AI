#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import find_packages
from setuptools import setup


BASE_DIR = Path(__file__).parent

README_PATH = BASE_DIR / "README.md"


with open(
    README_PATH,
    "r",
    encoding="utf-8",
) as file:
    LONG_DESCRIPTION = file.read()


setup(
    name="codescope-ai",
    version="0.1.0",
    description=(
        "AI-powered code documentation assistant "
        "with Retrieval-Augmented Generation"
    ),
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Valentin Sheboldaev",
    python_requires=">=3.11",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.36.0",
        "openai>=1.35.0",
        "chromadb>=0.5.3",
        "python-dotenv>=1.0.1",
        "pyyaml>=6.0.1",
        "tiktoken>=0.7.0",
        "tenacity>=8.4.2",
        "numpy>=1.26.4",
    ],
    extras_require={
        "dev": [
            "pytest>=8.2.2",
            "pytest-cov>=5.0.0",
            "black>=24.4.2",
            "ruff>=0.5.0",
            "mypy>=1.10.1",
        ]
    },
    entry_points={
        "console_scripts": [
            "codescope-ai=codescope_ai.main:main",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
