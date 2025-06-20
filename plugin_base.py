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
        """
        Returns the unique, filename-safe name of the plugin.
        """
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """
        Returns the version of the plugin, typically in semantic versioning format.
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """
        Returns a human-readable description of the plugin.
        """
        pass
    
    @property
    def author(self) -> str:
        """
        Returns the author of the plugin.
        
        Defaults to "Unknown" if not specified by the plugin implementation.
        """
        return "Unknown"
    
    @property
    def requires_float_version(self) -> str:
        """
        Returns the minimum required FLOAT version for the plugin.
        
        Returns:
            str: The minimum FLOAT version required to use this plugin. Defaults to "3.1.0".
        """
        return "3.1.0"
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Return a dictionary containing the plugin's metadata, including name, version, description, author, required FLOAT version, load timestamp, and plugin type.
        """
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
        Validates that the plugin's name and version are non-empty strings and that the name is filename-safe.
        
        Raises:
            PluginValidationError: If the name or version is invalid.
        
        Returns:
            bool: True if validation passes.
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
        Initializes the plugin with the provided configuration and logger.
        
        Override this method in subclasses to perform custom initialization logic.
        
        Returns:
            bool: True if initialization succeeds.
        """
        self._config = config or {}
        self._logger = logger or logging.getLogger(f"float.plugin.{self.name}")
        return True
    
    def cleanup(self) -> bool:
        """
        Release any resources held by the plugin.
        
        Override this method in subclasses to implement custom cleanup logic.
        
        Returns:
            bool: True if cleanup was successful.
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
        Detects and extracts patterns from the provided content, optionally considering the file path.
        
        Parameters:
            content (str): The text content to analyze for patterns.
            file_path (Optional[Path]): The path to the source file, if available.
        
        Returns:
            Dict[str, Any]: A dictionary containing the detection outcome, including:
                - 'success' (bool): Whether pattern detection completed successfully.
                - 'patterns_found' (int): The number of patterns detected.
                - 'analysis_results' (dict): Detailed information about the detected patterns.
        """
        pass
    
    @property
    def supported_patterns(self) -> List[str]:
        """
        Returns a list of pattern types that this plugin can detect.
        
        By default, returns an empty list. Subclasses should override to specify supported pattern types.
        """
        return []
    
    @property
    def pattern_confidence_threshold(self) -> float:
        """
        Returns the minimum confidence score required for pattern detection, as a float between 0.0 and 1.0.
        """
        return 0.5
    
    def get_pattern_summary(self, detection_results: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the number of patterns detected.
        
        Parameters:
            detection_results (dict): Dictionary containing detection results, including the 'patterns_found' key.
        
        Returns:
            str: Summary string indicating the number of patterns detected and the plugin's name and version.
        """
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
        Analyze the provided content and associated metadata, returning a dictionary of analysis results.
        
        Parameters:
            content (str): The text content to be analyzed.
            metadata (dict): Metadata and contextual information related to the content.
        
        Returns:
            dict: Analysis results produced by the plugin.
        """
        pass
    
    @property
    def analysis_type(self) -> str:
        """
        Returns the type of analysis performed by the plugin.
        
        Returns:
            str: A string describing the analysis type. Defaults to "general".
        """
        return "general"

class StorageBackendPlugin(FloatPlugin):
    """
    Base class for storage backend plugins.
    
    Storage backends handle persistence of processed content,
    metadata, and search capabilities.
    """
    
    @abstractmethod
    def store_content(self, content: str, metadata: Dict[str, Any], collection: str) -> bool:
        """
        Store the provided content and associated metadata in the specified collection.
        
        Parameters:
            content (str): The content to be stored.
            metadata (Dict[str, Any]): Metadata describing the content.
            collection (str): The name of the collection where the content will be stored.
        
        Returns:
            bool: True if the content was stored successfully, False otherwise.
        """
        pass
    
    @abstractmethod
    def search_content(self, query: str, collection: Optional[str] = None, 
                      limit: int = 10) -> List[Dict[str, Any]]:
        """
                      Searches stored content for entries matching the given query.
                      
                      Parameters:
                          query (str): The search query string.
                          collection (Optional[str]): The collection to search within, if applicable.
                          limit (int): The maximum number of results to return.
                      
                      Returns:
                          List[Dict[str, Any]]: A list of dictionaries representing the search results.
                      """
        pass
    
    @property
    def supports_collections(self) -> bool:
        """
        Indicates whether the storage backend supports multiple collections.
        
        Returns:
            bool: True if multiple collections are supported; otherwise, False.
        """
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
                         Generate a summary of the provided content using file metadata and optional processing hints.
                         
                         Parameters:
                             content (str): The text content to be summarized.
                             file_metadata (Dict[str, Any]): Metadata and contextual information about the file.
                             processing_hints (Optional[str]): Optional hints to influence the summarization process.
                         
                         Returns:
                             Dict[str, Any]: A dictionary containing the generated summary and related metadata.
                         """
        pass
    
    @property
    def max_content_length(self) -> int:
        """
        Returns the maximum content length supported by the summarizer.
        
        Returns:
            int: The maximum number of characters the summarizer can process.
        """
        return 50000
    
    @property
    def supports_streaming(self) -> bool:
        """
        Indicates whether the summarizer supports streaming or chunked content processing.
        
        Returns:
            bool: True if streaming is supported; otherwise, False.
        """
        return False

# Plugin capability definitions
class PluginCapability:
    """Defines a specific capability that plugins can provide"""
    
    def __init__(self, name: str, description: str, interface_class: type):
        """
        Initialize a PluginCapability instance with a name, description, and associated interface class.
        
        Parameters:
            name (str): The capability's unique name.
            description (str): A brief description of the capability.
            interface_class (type): The interface class that plugins must implement for this capability.
        """
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
    """
    Return the interface class associated with a given plugin capability.
    
    Parameters:
        capability (str): The capability name to look up.
    
    Returns:
        Optional[type]: The interface class for the capability, or None if not found.
    """
    cap = FLOAT_CAPABILITIES.get(capability)
    return cap.interface_class if cap else None

def validate_plugin_interface(plugin: FloatPlugin, expected_capability: str) -> bool:
    """
    Check whether a plugin instance implements the interface required for a specified capability.
    
    Parameters:
        plugin (FloatPlugin): The plugin instance to validate.
        expected_capability (str): The capability name to check against.
    
    Returns:
        bool: True if the plugin implements the expected interface, False otherwise.
    """
    expected_interface = get_plugin_interface(expected_capability)
    if not expected_interface:
        return False
    
    return isinstance(plugin, expected_interface)