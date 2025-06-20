"""
Memory-Safe Plugin System Foundation for FLOAT

This module provides the base classes and interfaces for FLOAT's plugin architecture.
Designed to address the segfault issues from the previous plugin implementation by:

1. Using entry points instead of importlib.util.exec_module()
2. Providing clear interface contracts
3. Implementing defensive loading patterns
4. Maintaining backward compatibility

Issue #14: Memory-safe plugin architecture foundation
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime
import logging

class PluginError(Exception):
    """Base exception for plugin-related errors"""
    pass

class PluginLoadError(PluginError):
    """Raised when a plugin fails to load"""
    pass

class PluginValidationError(PluginError):
    """Raised when a plugin fails validation"""
    pass

class FloatPlugin(ABC):
    """
    Base class for all FLOAT plugins.
    
    Provides the fundamental interface that all plugins must implement.
    Includes metadata, validation, and lifecycle management.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique plugin name (should be filename-safe)"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version (semver format recommended)"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable plugin description"""
        pass
    
    @property
    def author(self) -> str:
        """Plugin author (optional)"""
        return "Unknown"
    
    @property
    def requires_float_version(self) -> str:
        """Minimum FLOAT version required (optional)"""
        return "3.1.0"
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """Complete plugin metadata"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'author': self.author,
            'requires_float_version': self.requires_float_version,
            'loaded_at': datetime.now().isoformat(),
            'plugin_type': self.__class__.__bases__[0].__name__ if self.__class__.__bases__ else 'FloatPlugin'
        }
    
    def validate(self) -> bool:
        """
        Validate plugin configuration and dependencies.
        Override in subclasses for custom validation.
        """
        # Basic validation
        if not self.name or not isinstance(self.name, str):
            raise PluginValidationError(f"Plugin name must be a non-empty string, got: {self.name}")
        
        if not self.version or not isinstance(self.version, str):
            raise PluginValidationError(f"Plugin version must be a non-empty string, got: {self.version}")
        
        # Name should be safe for filenames and module names
        if not self.name.replace('_', '').replace('-', '').isalnum():
            raise PluginValidationError(f"Plugin name must be alphanumeric (with _ and -): {self.name}")
        
        return True
    
    def initialize(self, config: Optional[Dict] = None, logger: Optional[logging.Logger] = None) -> bool:
        """
        Initialize plugin with configuration and logger.
        Override in subclasses for custom initialization.
        """
        self._config = config or {}
        self._logger = logger or logging.getLogger(f"float.plugin.{self.name}")
        return True
    
    def cleanup(self) -> bool:
        """
        Clean up plugin resources.
        Override in subclasses for custom cleanup.
        """
        return True

class PatternDetectorPlugin(FloatPlugin):
    """
    Base class for pattern detection plugins.
    
    Pattern detectors analyze content and extract FLOAT-specific patterns,
    signals, and metadata for enhanced content understanding.
    """
    
    @abstractmethod
    def detect_patterns(self, content: str, file_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Detect and extract patterns from content.
        
        Args:
            content: Text content to analyze
            file_path: Optional path to the source file
            
        Returns:
            Dictionary containing detected patterns, signals, and analysis results.
            Must include at least:
            - 'success': bool indicating if detection completed
            - 'patterns_found': int count of patterns detected
            - 'analysis_results': dict with detailed findings
        """
        pass
    
    @property
    def supported_patterns(self) -> List[str]:
        """List of pattern types this plugin can detect"""
        return []
    
    @property
    def pattern_confidence_threshold(self) -> float:
        """Minimum confidence score for pattern detection (0.0 to 1.0)"""
        return 0.5
    
    def get_pattern_summary(self, detection_results: Dict[str, Any]) -> str:
        """Generate human-readable summary of detected patterns"""
        patterns_found = detection_results.get('patterns_found', 0)
        return f"Detected {patterns_found} patterns using {self.name} v{self.version}"

class ContentAnalyzerPlugin(FloatPlugin):
    """
    Base class for content analysis plugins.
    
    Content analyzers perform deeper analysis of document structure,
    sentiment, topics, or other content characteristics.
    """
    
    @abstractmethod
    def analyze_content(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze content and return analysis results.
        
        Args:
            content: Text content to analyze
            metadata: File metadata and context
            
        Returns:
            Dictionary containing analysis results
        """
        pass
    
    @property
    def analysis_type(self) -> str:
        """Type of analysis this plugin performs"""
        return "general"

class StorageBackendPlugin(FloatPlugin):
    """
    Base class for storage backend plugins.
    
    Storage backends handle persistence of processed content,
    metadata, and search capabilities.
    """
    
    @abstractmethod
    def store_content(self, content: str, metadata: Dict[str, Any], collection: str) -> bool:
        """Store content with metadata in specified collection"""
        pass
    
    @abstractmethod
    def search_content(self, query: str, collection: Optional[str] = None, 
                      limit: int = 10) -> List[Dict[str, Any]]:
        """Search stored content and return results"""
        pass
    
    @property
    def supports_collections(self) -> bool:
        """Whether this backend supports multiple collections"""
        return True

class SummarizerPlugin(FloatPlugin):
    """
    Base class for content summarization plugins.
    
    Summarizers generate intelligent summaries of documents
    using various approaches (AI, rule-based, etc.).
    """
    
    @abstractmethod
    def summarize_content(self, content: str, file_metadata: Dict[str, Any], 
                         processing_hints: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate summary of content.
        
        Args:
            content: Text content to summarize
            file_metadata: File metadata and context
            processing_hints: Optional hints to guide summarization
            
        Returns:
            Dictionary containing summary and metadata
        """
        pass
    
    @property
    def max_content_length(self) -> int:
        """Maximum content length this summarizer can handle"""
        return 50000
    
    @property
    def supports_streaming(self) -> bool:
        """Whether this summarizer supports streaming/chunked content"""
        return False

# Plugin capability definitions
class PluginCapability:
    """Defines a specific capability that plugins can provide"""
    
    def __init__(self, name: str, description: str, interface_class: type):
        self.name = name
        self.description = description
        self.interface_class = interface_class

# Standard FLOAT plugin capabilities
FLOAT_CAPABILITIES = {
    'pattern_detection': PluginCapability(
        'pattern_detection',
        'Detect and extract FLOAT patterns from content',
        PatternDetectorPlugin
    ),
    'content_analysis': PluginCapability(
        'content_analysis', 
        'Analyze document structure and characteristics',
        ContentAnalyzerPlugin
    ),
    'storage_backend': PluginCapability(
        'storage_backend',
        'Persist and search processed content',
        StorageBackendPlugin
    ),
    'summarization': PluginCapability(
        'summarization',
        'Generate intelligent content summaries',
        SummarizerPlugin
    )
}

def get_plugin_interface(capability: str) -> Optional[type]:
    """Get the plugin interface class for a given capability"""
    cap = FLOAT_CAPABILITIES.get(capability)
    return cap.interface_class if cap else None

def validate_plugin_interface(plugin: FloatPlugin, expected_capability: str) -> bool:
    """Validate that a plugin implements the expected interface"""
    expected_interface = get_plugin_interface(expected_capability)
    if not expected_interface:
        return False
    
    return isinstance(plugin, expected_interface)