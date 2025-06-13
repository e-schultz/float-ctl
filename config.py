"""
Configuration management for FLOAT ecosystem
Handles configuration from file, environment variables, and defaults
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional

class FloatConfig:
    """Configuration management for FLOAT ecosystem"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file, environment, or defaults"""
        config = self._get_defaults()
        
        # Override with config file if provided
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
                print(f"✅ Loaded config from: {config_path}")
            except Exception as e:
                print(f"⚠️ Failed to load config file {config_path}: {e}")
        
        # Override with environment variables
        env_overrides = {
            'vault_path': os.getenv('FLOAT_VAULT_PATH'),
            'chroma_data_path': os.getenv('FLOAT_CHROMA_PATH'),
            'dropzone_path': os.getenv('FLOAT_DROPZONE_PATH'),
            'log_dir': os.getenv('FLOAT_LOG_DIR'),
            'ollama_url': os.getenv('OLLAMA_URL')
        }
        
        # Special handling for boolean environment variables
        float_enable_ollama = os.getenv('FLOAT_ENABLE_OLLAMA')
        if float_enable_ollama is not None:
            env_overrides['enable_ollama'] = float_enable_ollama.lower() == 'true'
        
        for key, value in env_overrides.items():
            if value is not None and value != '':
                config[key] = value
        
        # Ensure paths are expanded
        for key in ['vault_path', 'chroma_data_path', 'dropzone_path', 'conversation_dis_path', 'log_dir']:
            if key in config and config[key]:
                config[key] = str(Path(config[key]).expanduser())
        
        # Set conversation_dis_path if not specified
        if not config.get('conversation_dis_path'):
            config['conversation_dis_path'] = str(Path(config['vault_path']) / 'FLOAT.conversations')
        
        return config
    
    def _get_defaults(self) -> Dict:
        """Default configuration values"""
        return {
            'vault_path': '/Users/evan/vault',
            'chroma_data_path': '/Users/evan/github/chroma-data',
            'dropzone_path': '/Users/evan/float-dropzone',
            'conversation_dis_path': None,  # Will use vault_path/FLOAT.conversations
            'enable_ollama': True,
            'auto_update_daily_context': True,
            'max_file_size_mb': 50,
            'retry_attempts': 3,
            'collection_name': 'float_dropzone_comprehensive',
            'ollama_url': 'http://localhost:11434',
            'ollama_model': 'llama3.1:8b',
            'chunk_size': 2000,
            'chunk_overlap': 200,
            'log_level': 'INFO',
            'log_dir': None,   # Will default to dropzone/.logs/
            'log_file': None,  # Will default to log_dir/float_daemon.log
            'enable_performance_monitoring': True,
            'enable_health_checks': True,
            'health_check_interval': 60,  # seconds
            'process_hidden_files': False,
            'supported_extensions': [
                '.txt', '.md', '.json', '.csv', '.log', '.html',
                '.pdf', '.docx', '.doc', '.py', '.js', '.yaml', '.yml'
            ],
            'quarantine_on_error': True,
            'delete_after_processing': False,
            'enable_tripartite_routing': True,
            'enable_enhanced_integration': True,
            'tripartite_collections': {
                'concept': 'float_tripartite_v2_concept',
                'framework': 'float_tripartite_v2_framework',
                'metaphor': 'float_tripartite_v2_metaphor'
            },
            'special_pattern_collections': {
                'dispatch': 'float_dispatch_bay',
                'rfc': 'float_rfc',
                'echo_copy': 'float_echoCopy'
            },
            'enable_temporal_queries': True
        }
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set configuration value"""
        self.config[key] = value
    
    def update(self, updates: Dict):
        """Update multiple configuration values"""
        self.config.update(updates)
    
    def save_to_file(self, path: str):
        """Save current configuration to file"""
        try:
            with open(path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"✅ Configuration saved to: {path}")
        except Exception as e:
            print(f"❌ Failed to save configuration: {e}")
    
    def validate(self) -> Dict[str, bool]:
        """Validate configuration settings"""
        validations = {}
        
        # Check required paths exist
        path_keys = ['vault_path', 'chroma_data_path']
        for key in path_keys:
            path = self.config.get(key)
            if path:
                path_obj = Path(path)
                validations[f'{key}_exists'] = path_obj.exists()
                validations[f'{key}_readable'] = path_obj.exists() and os.access(path, os.R_OK)
            else:
                validations[f'{key}_exists'] = False
                validations[f'{key}_readable'] = False
        
        # Check dropzone path (will be created if doesn't exist)
        dropzone = Path(self.config.get('dropzone_path', ''))
        if dropzone:
            if not dropzone.exists():
                try:
                    dropzone.mkdir(parents=True, exist_ok=True)
                    validations['dropzone_path_exists'] = True
                    validations['dropzone_path_writable'] = True
                except Exception:
                    validations['dropzone_path_exists'] = False
                    validations['dropzone_path_writable'] = False
            else:
                validations['dropzone_path_exists'] = True
                validations['dropzone_path_writable'] = os.access(dropzone, os.W_OK)
        
        # Check numeric values are in valid ranges
        validations['max_file_size_valid'] = 0 < self.config.get('max_file_size_mb', 50) <= 1000
        validations['retry_attempts_valid'] = 0 <= self.config.get('retry_attempts', 3) <= 10
        validations['chunk_size_valid'] = 100 <= self.config.get('chunk_size', 2000) <= 10000
        
        return validations
    
    def __str__(self) -> str:
        """String representation of configuration"""
        safe_config = self.config.copy()
        # Mask sensitive values if any
        if 'api_key' in safe_config:
            safe_config['api_key'] = '***' + safe_config['api_key'][-4:]
        return json.dumps(safe_config, indent=2)
    
    def __repr__(self) -> str:
        return f"FloatConfig({len(self.config)} settings)"


# Example configuration file template
CONFIG_TEMPLATE = {
    "_comment": "FLOAT Ecosystem Configuration File",
    "vault_path": "~/vault",
    "chroma_data_path": "~/github/chroma-data",
    "dropzone_path": "~/float-dropzone",
    "enable_ollama": True,
    "ollama_model": "llama3.1:8b",
    "max_file_size_mb": 50,
    "chunk_size": 2000,
    "auto_update_daily_context": True,
    "log_level": "INFO",
    "retry_attempts": 3,
    "enable_tripartite_routing": True
}

def create_config_template(path: str):
    """Create a configuration file template"""
    with open(path, 'w') as f:
        json.dump(CONFIG_TEMPLATE, f, indent=2)
    print(f"✅ Configuration template created at: {path}")

if __name__ == "__main__":
    # Test configuration loading
    config = FloatConfig()
    print("Default configuration:")
    print(config)
    
    print("\nValidation results:")
    validations = config.validate()
    for key, valid in validations.items():
        status = "✅" if valid else "❌"
        print(f"{status} {key}: {valid}")