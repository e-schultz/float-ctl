#!/usr/bin/env python3
"""
Test suite for FLOAT configuration management
Tests configuration loading, validation, and environment variable handling
"""

import pytest
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from config import FloatConfig, create_config_template


class TestFloatConfig:
    """Test suite for FloatConfig class"""
    
    def test_default_config_loading(self):
        """Test that default configuration loads correctly"""
        config = FloatConfig()
        
        # Test required default values
        assert config.get('enable_ollama') is True
        assert config.get('auto_update_daily_context') is True
        assert config.get('max_file_size_mb') == 50
        assert config.get('chunk_size') == 2000
        assert config.get('retry_attempts') == 3
        
        # Test path defaults
        assert 'vault_path' in config.config
        assert 'chroma_data_path' in config.config
        assert 'dropzone_path' in config.config
    
    def test_config_file_loading(self):
        """Test loading configuration from file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_config = {
                "vault_path": "/tmp/test-vault",
                "enable_ollama": False,
                "max_file_size_mb": 100,
                "custom_setting": "test_value"
            }
            json.dump(test_config, f)
            config_path = f.name
        
        try:
            config = FloatConfig(config_path)
            
            # Test file values override defaults
            assert config.get('vault_path') == "/tmp/test-vault"
            assert config.get('enable_ollama') is False
            assert config.get('max_file_size_mb') == 100
            assert config.get('custom_setting') == "test_value"
            
            # Test defaults still present for unspecified values
            assert config.get('chunk_size') == 2000
            
        finally:
            os.unlink(config_path)
    
    def test_environment_variable_overrides(self):
        """Test that environment variables override config values"""
        with patch.dict(os.environ, {
            'FLOAT_VAULT_PATH': '/env/vault',
            'FLOAT_ENABLE_OLLAMA': 'false',
            'OLLAMA_URL': 'http://custom:11434'
        }):
            config = FloatConfig()
            
            assert config.get('vault_path') == '/env/vault'
            assert config.get('enable_ollama') is False
            assert config.get('ollama_url') == 'http://custom:11434'
    
    def test_boolean_environment_variables(self):
        """Test proper boolean parsing of environment variables"""
        # Test true values
        with patch.dict(os.environ, {'FLOAT_ENABLE_OLLAMA': 'true'}):
            config = FloatConfig()
            assert config.get('enable_ollama') is True
        
        # Test false values
        with patch.dict(os.environ, {'FLOAT_ENABLE_OLLAMA': 'false'}):
            config = FloatConfig()
            assert config.get('enable_ollama') is False
        
        # Test case insensitivity
        with patch.dict(os.environ, {'FLOAT_ENABLE_OLLAMA': 'TRUE'}):
            config = FloatConfig()
            assert config.get('enable_ollama') is True
    
    def test_path_expansion(self):
        """Test that paths are properly expanded"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_config = {
                "vault_path": "~/test-vault",
                "dropzone_path": "~/test-dropzone"
            }
            json.dump(test_config, f)
            config_path = f.name
        
        try:
            config = FloatConfig(config_path)
            
            # Paths should be expanded
            assert not config.get('vault_path').startswith('~')
            assert not config.get('dropzone_path').startswith('~')
            assert config.get('vault_path').startswith(str(Path.home()))
            
        finally:
            os.unlink(config_path)
    
    def test_conversation_dis_path_generation(self):
        """Test automatic conversation_dis_path generation"""
        config = FloatConfig()
        
        # Should automatically generate conversation_dis_path
        conversation_path = config.get('conversation_dis_path')
        vault_path = config.get('vault_path')
        
        assert conversation_path is not None
        assert 'FLOAT.conversations' in conversation_path
        assert vault_path in conversation_path
    
    def test_config_validation(self):
        """Test configuration validation"""
        config = FloatConfig()
        validations = config.validate()
        
        # Check validation structure
        assert isinstance(validations, dict)
        assert 'max_file_size_valid' in validations
        assert 'retry_attempts_valid' in validations
        assert 'chunk_size_valid' in validations
        
        # Test numeric validation
        assert validations['max_file_size_valid'] is True
        assert validations['retry_attempts_valid'] is True
        assert validations['chunk_size_valid'] is True
    
    def test_config_set_and_update(self):
        """Test setting and updating configuration values"""
        config = FloatConfig()
        
        # Test single value setting
        config.set('test_key', 'test_value')
        assert config.get('test_key') == 'test_value'
        
        # Test bulk update
        updates = {
            'batch_key1': 'batch_value1',
            'batch_key2': 'batch_value2'
        }
        config.update(updates)
        assert config.get('batch_key1') == 'batch_value1'
        assert config.get('batch_key2') == 'batch_value2'
    
    def test_config_save_to_file(self):
        """Test saving configuration to file"""
        config = FloatConfig()
        config.set('test_save_key', 'test_save_value')
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            save_path = f.name
        
        try:
            config.save_to_file(save_path)
            
            # Verify file was created and contains our data
            assert Path(save_path).exists()
            
            with open(save_path, 'r') as f:
                saved_config = json.load(f)
            
            assert saved_config['test_save_key'] == 'test_save_value'
            
        finally:
            if Path(save_path).exists():
                os.unlink(save_path)
    
    def test_invalid_config_file_handling(self):
        """Test handling of invalid configuration files"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content {")
            invalid_config_path = f.name
        
        try:
            # Should not crash, should use defaults
            config = FloatConfig(invalid_config_path)
            assert config.get('enable_ollama') is True  # Default value
            
        finally:
            os.unlink(invalid_config_path)
    
    def test_nonexistent_config_file(self):
        """Test handling of nonexistent configuration file"""
        config = FloatConfig('/nonexistent/config.json')
        
        # Should use defaults when file doesn't exist
        assert config.get('enable_ollama') is True
        assert config.get('max_file_size_mb') == 50


class TestConfigTemplate:
    """Test configuration template creation"""
    
    def test_config_template_creation(self):
        """Test creating configuration template"""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            template_path = f.name
        
        try:
            create_config_template(template_path)
            
            # Verify template was created
            assert Path(template_path).exists()
            
            # Verify template content
            with open(template_path, 'r') as f:
                template_config = json.load(f)
            
            # Check for required template fields
            assert 'vault_path' in template_config
            assert 'enable_ollama' in template_config
            assert 'max_file_size_mb' in template_config
            assert template_config['enable_ollama'] is True
            
        finally:
            if Path(template_path).exists():
                os.unlink(template_path)


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_empty_environment_variable(self):
        """Test handling of empty environment variables"""
        with patch.dict(os.environ, {'FLOAT_VAULT_PATH': ''}):
            config = FloatConfig()
            # Empty string should not override default
            assert config.get('vault_path') != ''
    
    def test_config_string_representation(self):
        """Test string representation of config"""
        config = FloatConfig()
        config_str = str(config)
        
        # Should be valid JSON
        parsed = json.loads(config_str)
        assert isinstance(parsed, dict)
        assert 'vault_path' in parsed
    
    def test_config_repr(self):
        """Test repr representation of config"""
        config = FloatConfig()
        repr_str = repr(config)
        
        assert 'FloatConfig' in repr_str
        assert 'settings' in repr_str


if __name__ == '__main__':
    pytest.main([__file__, '-v'])