"""
Pattern Plugin Interface for FLOAT System - Issue #5
Minimal plugin architecture following "shacks not cathedrals" philosophy
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path
import importlib
import inspect
import re


class PatternPlugin(ABC):
    """
    Base class for FLOAT pattern detection plugins.
    
    Philosophy: Simple, focused interface that's easy to implement and extend.
    Each plugin should do one thing well - detect specific patterns.
    """
    
    @property
    @abstractmethod
    def plugin_name(self) -> str:
        """Unique name for this plugin"""
        pass
    
    @property
    @abstractmethod  
    def plugin_version(self) -> str:
        """Version of this plugin"""
        pass
    
    @property
    @abstractmethod
    def pattern_types(self) -> List[str]:
        """List of pattern types this plugin detects"""
        pass
    
    @abstractmethod
    def detect_patterns(self, content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Detect patterns in content and return structured results.
        
        Args:
            content: Text content to analyze
            metadata: Optional file metadata (filename, size, etc.)
        
        Returns:
            Dict with pattern detection results in format:
            {
                'pattern_type': {
                    'count': int,
                    'matches': List[str],
                    'has_pattern': bool,
                    'confidence': float  # 0.0-1.0, optional
                }
            }
        """
        pass
    
    def is_compatible(self, file_type: str) -> bool:
        """
        Check if this plugin should process the given file type.
        Default: process all file types.
        """
        return True
    
    def get_plugin_info(self) -> Dict[str, str]:
        """Get basic plugin information"""
        return {
            'name': self.plugin_name,
            'version': self.plugin_version,
            'pattern_types': self.pattern_types,
            'class': self.__class__.__name__
        }


class PatternPluginManager:
    """
    Simple plugin manager for FLOAT pattern detection.
    
    Philosophy: Load plugins dynamically, fail gracefully, easy to extend.
    """
    
    def __init__(self, logger=None):
        self.logger = logger
        self.plugins: Dict[str, PatternPlugin] = {}
        self.plugin_dirs: List[Path] = []
        
        # Built-in plugin locations
        self.plugin_dirs.append(Path(__file__).parent / "plugins")
        
    def add_plugin_directory(self, path: Path):
        """Add a directory to search for plugins"""
        if path.exists() and path.is_dir():
            self.plugin_dirs.append(path)
            if self.logger:
                self.logger.info(f"Added plugin directory: {path}")
    
    def register_plugin(self, plugin: PatternPlugin):
        """Manually register a plugin instance"""
        self.plugins[plugin.plugin_name] = plugin
        if self.logger:
            self.logger.info(f"Registered plugin: {plugin.plugin_name}")
    
    def load_plugins_from_directory(self, plugin_dir: Path):
        """Load all plugins from a directory"""
        if not plugin_dir.exists():
            return
        
        for file_path in plugin_dir.glob("*.py"):
            if file_path.name.startswith("_"):
                continue  # Skip private files
            
            try:
                self._load_plugin_from_file(file_path)
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to load plugin {file_path.name}: {e}")
    
    def _load_plugin_from_file(self, file_path: Path):
        """Load a plugin from a Python file"""
        module_name = file_path.stem
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find PatternPlugin subclasses in the module
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, PatternPlugin) and 
                obj != PatternPlugin):
                
                plugin_instance = obj()
                self.register_plugin(plugin_instance)
                if self.logger:
                    self.logger.info(f"Loaded plugin: {plugin_instance.plugin_name} from {file_path.name}")
    
    def load_all_plugins(self):
        """Load all plugins from all plugin directories"""
        for plugin_dir in self.plugin_dirs:
            self.load_plugins_from_directory(plugin_dir)
    
    def detect_patterns(self, content: str, metadata: Optional[Dict] = None, 
                       file_type: str = "unknown") -> Dict[str, Any]:
        """
        Run pattern detection using all compatible plugins.
        
        Returns consolidated results from all plugins.
        """
        results = {}
        
        for plugin_name, plugin in self.plugins.items():
            try:
                if plugin.is_compatible(file_type):
                    plugin_results = plugin.detect_patterns(content, metadata)
                    
                    # Merge results, prefixing with plugin name if conflicts
                    for pattern_type, pattern_data in plugin_results.items():
                        result_key = pattern_type
                        
                        # Handle conflicts by prefixing with plugin name
                        if result_key in results:
                            result_key = f"{plugin_name}_{pattern_type}"
                        
                        results[result_key] = pattern_data
                        
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Plugin {plugin_name} failed: {e}")
        
        return results
    
    def get_plugin_info(self) -> Dict[str, Dict]:
        """Get information about all loaded plugins"""
        return {name: plugin.get_plugin_info() for name, plugin in self.plugins.items()}
    
    def get_pattern_types(self) -> List[str]:
        """Get all pattern types supported by loaded plugins"""
        pattern_types = []
        for plugin in self.plugins.values():
            pattern_types.extend(plugin.pattern_types)
        return list(set(pattern_types))  # Deduplicate


# Example: Core FLOAT patterns as a plugin
class CoreFloatPatternPlugin(PatternPlugin):
    """
    Core FLOAT patterns: ctx::, highlight::, signal::
    These are the essential patterns for the FLOAT system.
    """
    
    @property
    def plugin_name(self) -> str:
        return "core_float_patterns"
    
    @property
    def plugin_version(self) -> str:
        return "1.0"
    
    @property
    def pattern_types(self) -> List[str]:
        return ["ctx_markers", "highlight_markers", "signal_markers"]
    
    def detect_patterns(self, content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        results = {}
        
        # Core FLOAT patterns
        patterns = {
            'ctx_markers': re.compile(r'ctx::\s*([^\n]+)', re.IGNORECASE),
            'highlight_markers': re.compile(r'highlight::\s*([^\n]+)', re.IGNORECASE),
            'signal_markers': re.compile(r'signal::\s*([^\n]+)', re.IGNORECASE)
        }
        
        for pattern_name, pattern_regex in patterns.items():
            matches = pattern_regex.findall(content)
            results[pattern_name] = {
                'count': len(matches),
                'matches': matches[:5],  # First 5 matches
                'has_pattern': len(matches) > 0,
                'confidence': 1.0 if matches else 0.0
            }
        
        return results


# Example: Enhanced patterns from Issue #3 as a plugin  
class EnhancedFloatPatternPlugin(PatternPlugin):
    """
    Enhanced FLOAT patterns from Issue #3: inline and line-level patterns
    """
    
    @property
    def plugin_name(self) -> str:
        return "enhanced_float_patterns"
    
    @property
    def plugin_version(self) -> str:
        return "1.0"
    
    @property
    def pattern_types(self) -> List[str]:
        return [
            "inline_expand_on", "inline_relates_to", "inline_connect_to",
            "line_mood", "line_boundary", "line_progress", "line_issue"
        ]
    
    def detect_patterns(self, content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        results = {}
        
        # Enhanced patterns from Issue #3
        patterns = {
            # Inline patterns (bracketed format)
            'inline_expand_on': re.compile(r'\[expandOn::\s*([^\]]+)\]', re.IGNORECASE),
            'inline_relates_to': re.compile(r'\[relatesTo::\s*([^\]]+)\]', re.IGNORECASE),
            'inline_connect_to': re.compile(r'\[connectTo::\s*([^\]]+)\]', re.IGNORECASE),
            
            # Line-level :: patterns (allow indentation and bullet points)
            'line_mood': re.compile(r'^\s*[-*]?\s*mood::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            'line_boundary': re.compile(r'^\s*[-*]?\s*boundary::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            'line_progress': re.compile(r'^\s*[-*]?\s*progress::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
            'line_issue': re.compile(r'^\s*[-*]?\s*issue::\s*(.+)$', re.MULTILINE | re.IGNORECASE),
        }
        
        for pattern_name, pattern_regex in patterns.items():
            matches = pattern_regex.findall(content)
            results[pattern_name] = {
                'count': len(matches),
                'matches': matches[:3],  # First 3 matches for enhanced patterns
                'has_pattern': len(matches) > 0,
                'confidence': 0.9 if matches else 0.0  # Slightly lower confidence than core
            }
        
        return results


# Example: Personal patterns that are evan-specific
class PersonalPatternPlugin(PatternPlugin):
    """
    Personal/experimental patterns specific to evan's workflow.
    These are separated to distinguish transferable vs personal patterns.
    """
    
    @property
    def plugin_name(self) -> str:
        return "personal_patterns"
    
    @property
    def plugin_version(self) -> str:
        return "0.1"
    
    @property
    def pattern_types(self) -> List[str]:
        return ["qtb_notes", "karen_notes", "sysop_notes", "little_fucker_notes"]
    
    def detect_patterns(self, content: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        results = {}
        
        # Personal persona patterns (evan's weird implementation)
        patterns = {
            'qtb_notes': re.compile(r'\[qtb::[^\]]+\]', re.IGNORECASE),
            'karen_notes': re.compile(r'\[karen::[^\]]+\]', re.IGNORECASE),
            'sysop_notes': re.compile(r'\[sysop::[^\]]+\]', re.IGNORECASE),
            'little_fucker_notes': re.compile(r'\[little-fucker::[^\]]+\]', re.IGNORECASE),
        }
        
        for pattern_name, pattern_regex in patterns.items():
            matches = pattern_regex.findall(content)
            results[pattern_name] = {
                'count': len(matches),
                'matches': matches,
                'has_pattern': len(matches) > 0,
                'confidence': 0.8,  # Personal patterns have lower confidence for transferability
                'transferable': False  # Mark as non-transferable
            }
        
        return results


if __name__ == "__main__":
    # Test the plugin system
    print("Testing FLOAT Pattern Plugin System - Issue #5")
    print("=" * 60)
    
    # Initialize plugin manager
    manager = PatternPluginManager()
    
    # Register built-in plugins
    manager.register_plugin(CoreFloatPatternPlugin())
    manager.register_plugin(EnhancedFloatPatternPlugin())
    manager.register_plugin(PersonalPatternPlugin())
    
    # Test content with various patterns
    test_content = """
    ctx:: 2025-06-20 - testing plugin system
    highlight:: this is an important insight
    
    [expandOn:: plugin architecture patterns]
    [relatesTo:: FLOAT methodology]
    
    mood:: focused and productive
    boundary:: keep plugins simple
    progress:: 70% complete
    
    [qtb:: some creative notation]
    [sysop:: system level thinking]
    """
    
    # Detect patterns
    results = manager.detect_patterns(test_content)
    
    print("🔍 PATTERN DETECTION RESULTS:")
    for pattern_type, data in results.items():
        if data['has_pattern']:
            transferable = data.get('transferable', True)
            transfer_note = " (non-transferable)" if not transferable else ""
            print(f"  ✅ {pattern_type}: {data['count']} matches{transfer_note}")
            for match in data['matches']:
                print(f"     - {match}")
    
    print(f"\n📊 PLUGIN INFO:")
    plugin_info = manager.get_plugin_info()
    for plugin_name, info in plugin_info.items():
        print(f"  🔌 {plugin_name} v{info['version']}")
        print(f"     Patterns: {', '.join(info['pattern_types'])}")
    
    print(f"\n🎯 SUCCESS: Plugin system working with {len(manager.plugins)} plugins")
    print("Philosophy: Simple extension points, let usage guide evolution")