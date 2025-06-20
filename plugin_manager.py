"""
Memory-Safe Plugin Manager for FLOAT

This module provides safe plugin discovery and loading using entry points
instead of the problematic importlib.util.exec_module() approach that
caused segfaults in the previous implementation.

Key safety features:
1. Entry points-based discovery (no dynamic imports)
2. Defensive loading with proper error handling
3. Plugin validation and lifecycle management
4. Graceful fallbacks when plugins fail
5. Memory management and cleanup

Issue #14: Memory-safe plugin architecture
"""

import logging
import gc
import time
from typing import Dict, List, Optional, Any, Type, Union
from pathlib import Path
from collections import defaultdict

try:
    # Try modern importlib.metadata first (Python 3.8+)
    from importlib.metadata import entry_points
except ImportError:
    # Fallback to pkg_resources for older Python versions
    try:
        import pkg_resources
        def entry_points(group=None):
            """
            Provides a compatibility shim for retrieving entry points using pkg_resources.
            
            Parameters:
                group (str, optional): The entry point group to retrieve. If None, returns all entry points grouped by their group name.
            
            Returns:
                If group is specified, returns an iterator over entry points in the given group.
                If group is None, returns a dictionary mapping group names to lists of entry points.
            """
            if group:
                return pkg_resources.iter_entry_points(group)
            else:
                # Return all entry points grouped
                all_eps = defaultdict(list)
                for ep in pkg_resources.iter_entry_points():
                    all_eps[ep.group].append(ep)
                return all_eps
    except ImportError:
        # No entry point support available
        def entry_points(group=None):
            """
            Return an empty list if a group is specified, or an empty dictionary if not.
            
            This function serves as a compatibility shim for entry point discovery when no entry point mechanism is available.
            """
            return [] if group else {}

from plugin_base import (
    FloatPlugin, PatternDetectorPlugin, ContentAnalyzerPlugin,
    StorageBackendPlugin, SummarizerPlugin, PluginError, 
    PluginLoadError, PluginValidationError, FLOAT_CAPABILITIES
)

class PluginManager:
    """
    Memory-safe plugin manager using entry points for discovery.
    
    Provides safe loading, validation, and lifecycle management of plugins.
    Includes comprehensive error handling and fallback mechanisms.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the PluginManager with logging, configuration, and internal data structures for plugin management.
        
        Parameters:
            logger (Optional[logging.Logger]): Logger instance to use for plugin manager messages. If not provided, a default logger is created.
        """
        self.logger = logger or logging.getLogger("float.plugin_manager")
        
        # Plugin storage by capability
        self.plugins_by_capability: Dict[str, List[FloatPlugin]] = defaultdict(list)
        self.plugin_metadata: Dict[str, Dict[str, Any]] = {}
        self.failed_plugins: Dict[str, str] = {}  # plugin_name -> error_message
        
        # Configuration
        self.enable_plugins = True
        self.plugin_timeout = 30.0  # seconds
        self.max_plugins_per_capability = 5
        
        # Safety tracking
        self.load_attempts = 0
        self.successful_loads = 0
        
        self.logger.info("Plugin manager initialized with entry points-based loading")
    
    def discover_plugins(self) -> Dict[str, List[str]]:
        """
        Discovers available plugins for each FLOAT capability using entry points.
        
        Returns:
            Dict[str, List[str]]: A dictionary mapping each capability name to a list of discovered plugin names.
        """
        discovered = defaultdict(list)
        
        if not self.enable_plugins:
            self.logger.info("Plugin discovery skipped - plugins disabled")
            return dict(discovered)
        
        try:
            # Discover plugins for each FLOAT capability
            for capability_name in FLOAT_CAPABILITIES.keys():
                entry_point_group = f"float.{capability_name}"
                
                try:
                    eps = entry_points(group=entry_point_group)
                    for ep in eps:
                        discovered[capability_name].append(ep.name)
                        self.logger.debug(f"Discovered plugin: {ep.name} for {capability_name}")
                        
                except Exception as e:
                    self.logger.warning(f"Failed to discover plugins for {capability_name}: {e}")
            
            total_discovered = sum(len(plugins) for plugins in discovered.values())
            self.logger.info(f"Plugin discovery complete: {total_discovered} plugins found across {len(discovered)} capabilities")
            
        except Exception as e:
            self.logger.error(f"Plugin discovery failed: {e}")
            
        return dict(discovered)
    
    def load_plugins(self, capability_filter: Optional[List[str]] = None) -> bool:
        """
        Loads plugins for the specified capabilities or all available capabilities if none are specified.
        
        Parameters:
            capability_filter (Optional[List[str]]): List of capability names to load plugins for, or None to load all capabilities.
        
        Returns:
            bool: True if at least one plugin was loaded successfully; False otherwise.
        """
        if not self.enable_plugins:
            self.logger.info("Plugin loading skipped - plugins disabled")
            return False
        
        start_time = time.time()
        self.logger.info("Starting plugin loading...")
        
        # Clear previous state
        self.plugins_by_capability.clear()
        self.plugin_metadata.clear()
        self.failed_plugins.clear()
        
        # Force garbage collection before loading
        gc.collect()
        time.sleep(0.1)  # Brief pause for memory stabilization
        
        capabilities_to_load = capability_filter or list(FLOAT_CAPABILITIES.keys())
        
        for capability_name in capabilities_to_load:
            self._load_plugins_for_capability(capability_name)
        
        elapsed = time.time() - start_time
        total_loaded = sum(len(plugins) for plugins in self.plugins_by_capability.values())
        
        self.logger.info(f"Plugin loading complete: {total_loaded} plugins loaded in {elapsed:.2f}s")
        self.logger.info(f"Success rate: {self.successful_loads}/{self.load_attempts} ({self.successful_loads/max(self.load_attempts, 1)*100:.1f}%)")
        
        if self.failed_plugins:
            self.logger.warning(f"Failed to load {len(self.failed_plugins)} plugins: {list(self.failed_plugins.keys())}")
        
        return total_loaded > 0
    
    def _load_plugins_for_capability(self, capability_name: str) -> None:
        """
        Loads all plugins for a given capability using entry points, up to the configured maximum per capability.
        
        Attempts to load and initialize each discovered plugin for the specified capability, validating against the expected interface. Successfully loaded plugins are added to the manager's registry. Logs warnings if the maximum number of plugins is reached and errors if loading fails.
        """
        entry_point_group = f"float.{capability_name}"
        expected_interface = FLOAT_CAPABILITIES[capability_name].interface_class
        
        try:
            eps = entry_points(group=entry_point_group)
            loaded_count = 0
            
            for ep in eps:
                if loaded_count >= self.max_plugins_per_capability:
                    self.logger.warning(f"Reached maximum plugins for {capability_name}, skipping {ep.name}")
                    break
                
                plugin = self._load_single_plugin(ep, expected_interface, capability_name)
                if plugin:
                    self.plugins_by_capability[capability_name].append(plugin)
                    loaded_count += 1
            
            self.logger.info(f"Loaded {loaded_count} plugins for {capability_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load plugins for {capability_name}: {e}")
    
    def _load_single_plugin(self, entry_point, expected_interface: Type, capability_name: str) -> Optional[FloatPlugin]:
        """
        Attempts to load, validate, and initialize a single plugin for a given capability using the provided entry point.
        
        If the plugin class does not implement the expected interface, fails validation, or fails to initialize, the error is logged, the failure is recorded, and None is returned. On success, the plugin instance is returned and its metadata is stored.
         
        Parameters:
            entry_point: The entry point object representing the plugin to load.
            expected_interface (Type): The required interface or base class the plugin must implement.
            capability_name (str): The capability under which the plugin is being loaded.
        
        Returns:
            Optional[FloatPlugin]: The loaded and initialized plugin instance, or None if loading failed.
        """
        plugin_name = entry_point.name
        self.load_attempts += 1
        
        try:
            self.logger.debug(f"Loading plugin: {plugin_name}")
            
            # Load the plugin class (this is the safe part - no exec_module!)
            plugin_class = entry_point.load()
            
            # Validate the plugin class
            if not issubclass(plugin_class, expected_interface):
                raise PluginValidationError(f"Plugin {plugin_name} does not implement {expected_interface.__name__}")
            
            # Instantiate the plugin
            plugin_instance = plugin_class()
            
            # Validate the plugin instance
            if not plugin_instance.validate():
                raise PluginValidationError(f"Plugin {plugin_name} failed validation")
            
            # Initialize the plugin
            if not plugin_instance.initialize(logger=self.logger.getChild(plugin_name)):
                raise PluginLoadError(f"Plugin {plugin_name} failed initialization")
            
            # Store metadata
            self.plugin_metadata[plugin_name] = plugin_instance.metadata
            
            self.successful_loads += 1
            self.logger.info(f"✅ Loaded plugin: {plugin_name} v{plugin_instance.version}")
            
            return plugin_instance
            
        except Exception as e:
            error_msg = f"Failed to load plugin {plugin_name}: {e}"
            self.logger.warning(error_msg)
            self.failed_plugins[plugin_name] = str(e)
            
            # Force cleanup after failed load
            gc.collect()
            
            return None
    
    def get_plugins(self, capability: str) -> List[FloatPlugin]:
        """
        Return all loaded plugins that provide the specified capability.
        
        Parameters:
            capability (str): The capability name to query.
        
        Returns:
            List[FloatPlugin]: List of plugin instances loaded for the given capability, or an empty list if none are loaded.
        """
        return self.plugins_by_capability.get(capability, [])
    
    def get_plugin(self, capability: str, plugin_name: Optional[str] = None) -> Optional[FloatPlugin]:
        """
        Return a plugin instance for a given capability, optionally matching a specific plugin name.
        
        Parameters:
        	capability (str): The capability for which to retrieve a plugin.
        	plugin_name (Optional[str]): The name of the specific plugin to retrieve. If None, returns the first available plugin for the capability.
        
        Returns:
        	Optional[FloatPlugin]: The matching plugin instance, or None if not found.
        """
        plugins = self.get_plugins(capability)
        
        if not plugins:
            return None
        
        if plugin_name is None:
            return plugins[0]  # Return first available
        
        # Find specific plugin by name
        for plugin in plugins:
            if plugin.name == plugin_name:
                return plugin
        
        return None
    
    def has_capability(self, capability: str) -> bool:
        """
        Return True if any plugins are loaded for the specified capability.
        
        Parameters:
            capability (str): The capability name to check.
        
        Returns:
            bool: True if at least one plugin is loaded for the capability, False otherwise.
        """
        return len(self.get_plugins(capability)) > 0
    
    def get_plugin_status(self) -> Dict[str, Any]:
        """
        Return a detailed status report of the plugin system, including enablement, load statistics, per-capability plugin details, and failure information.
        
        Returns:
            status (dict): Dictionary containing plugin system status, including whether plugins are enabled, load attempts, successful loads, success rate, loaded plugin details per capability, failed plugins, and total plugins loaded.
        """
        status = {
            'enabled': self.enable_plugins,
            'load_attempts': self.load_attempts,
            'successful_loads': self.successful_loads,
            'success_rate': self.successful_loads / max(self.load_attempts, 1),
            'capabilities': {},
            'failed_plugins': dict(self.failed_plugins),
            'total_plugins_loaded': sum(len(plugins) for plugins in self.plugins_by_capability.values())
        }
        
        # Add capability details
        for capability, plugins in self.plugins_by_capability.items():
            status['capabilities'][capability] = {
                'count': len(plugins),
                'plugins': [{'name': p.name, 'version': p.version} for p in plugins]
            }
        
        return status
    
    def cleanup(self) -> None:
        """
        Cleans up all loaded plugins, releases resources, and clears plugin state.
        
        Calls the `cleanup()` method on each loaded plugin, handles any exceptions, clears all plugin references and metadata, and triggers garbage collection to free memory.
        """
        self.logger.info("Cleaning up plugin manager...")
        
        cleanup_count = 0
        for capability, plugins in self.plugins_by_capability.items():
            for plugin in plugins:
                try:
                    if plugin.cleanup():
                        cleanup_count += 1
                except Exception as e:
                    self.logger.warning(f"Plugin {plugin.name} cleanup failed: {e}")
        
        # Clear all plugin references
        self.plugins_by_capability.clear()
        self.plugin_metadata.clear()
        
        # Force garbage collection
        gc.collect()
        
        self.logger.info(f"Plugin cleanup complete: {cleanup_count} plugins cleaned up")
    
    def reload_plugins(self, capability_filter: Optional[List[str]] = None) -> bool:
        """
        Reloads plugins by performing cleanup and then loading plugins for specified capabilities.
        
        Parameters:
            capability_filter (Optional[List[str]]): List of capabilities to reload, or None to reload all.
        
        Returns:
            bool: True if at least one plugin was successfully reloaded, False otherwise.
        """
        self.logger.info("Reloading plugins...")
        
        # Cleanup existing plugins
        self.cleanup()
        
        # Brief pause for memory stabilization
        time.sleep(0.2)
        
        # Reload plugins
        return self.load_plugins(capability_filter)
    
    def disable_plugins(self) -> None:
        """
        Disables the plugin system and cleans up all loaded plugins.
        """
        self.logger.info("Disabling plugin system...")
        self.enable_plugins = False
        self.cleanup()
        
    def enable_plugins(self) -> None:
        """
        Enables the plugin system, allowing plugins to be discovered and loaded.
        """
        self.logger.info("Enabling plugin system...")
        self.enable_plugins = True

# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None

def get_plugin_manager() -> PluginManager:
    """
    Returns the global singleton instance of the plugin manager, creating it if it does not already exist.
    """
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager

def initialize_plugin_system(logger: Optional[logging.Logger] = None) -> bool:
    """
    Initializes the global plugin manager and loads all available plugins.
    
    Parameters:
        logger (Optional[logging.Logger]): Optional logger to use for plugin system messages.
    
    Returns:
        bool: True if the plugin system was initialized and at least one plugin loaded successfully; False otherwise.
    """
    global _plugin_manager
    try:
        _plugin_manager = PluginManager(logger=logger)
        return _plugin_manager.load_plugins()
    except Exception as e:
        if logger:
            logger.error(f"Plugin system initialization failed: {e}")
        return False

def shutdown_plugin_system() -> None:
    """
    Shuts down the global plugin system and releases all associated resources.
    """
    global _plugin_manager
    if _plugin_manager:
        _plugin_manager.cleanup()
        _plugin_manager = None