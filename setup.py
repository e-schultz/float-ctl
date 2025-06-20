"""
Setup script for floatctl CLI tool
"""

from setuptools import setup, find_packages

setup(
    name="floatctl",
    version="0.1.0",
    description="FLOAT command-line interface - lf1m daemon CLI wrapper",
    author="Evan",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "chromadb",
        "pathlib",
        "watchdog",
    ],
    entry_points={
        'console_scripts': [
            'floatctl=floatctl.cli:cli',
        ],
        # FLOAT Plugin Entry Points - Issue #14
        'float.pattern_detection': [
            'builtin=plugins.builtin_pattern_detector:BuiltinPatternDetector',
        ],
        # Future plugin capabilities
        'float.content_analysis': [
            # Placeholder for content analysis plugins
        ],
        'float.storage_backend': [
            # Placeholder for storage backend plugins
        ],
        'float.summarization': [
            'ollama=plugins.ollama_summarizer:OllamaSummarizerPlugin',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)