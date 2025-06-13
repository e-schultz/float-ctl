"""
Simple daemon tests that work with the current codebase
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

class TestDaemonSimple:
    """Simplified daemon tests that focus on testable functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.dropzone_path = self.temp_dir / "dropzone"
        self.vault_path = self.temp_dir / "vault"
        self.chroma_path = self.temp_dir / "chroma"
        
        # Create directories
        self.dropzone_path.mkdir(exist_ok=True)
        self.vault_path.mkdir(exist_ok=True)
        self.chroma_path.mkdir(exist_ok=True)
        
        # Create test config
        self.test_config = {
            "vault_path": str(self.vault_path),
            "chroma_data_path": str(self.chroma_path),
            "dropzone_path": str(self.dropzone_path),
            "enable_ollama": False,
            "enable_enhanced_integration": False,
            "auto_update_daily_context": False,
            "max_file_size_mb": 10,
            "log_level": "ERROR"
        }
        
        self.config_file = self.temp_dir / "test_config.json"
        with open(self.config_file, 'w') as f:
            json.dump(self.test_config, f)
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @pytest.mark.unit
    @patch('enhanced_integration.EnhancedSystemIntegration')
    @patch('health_monitor.HealthMonitor')
    @patch('performance_monitor.PerformanceMonitor')
    @patch('error_recovery.FileProcessingRecovery')
    @patch('logging_config.setup_logging')
    def test_daemon_can_be_imported(self, mock_logging, mock_recovery, mock_perf, mock_health, mock_integration):
        """Test that the daemon can be imported and instantiated"""
        mock_logging.return_value = Mock()
        
        # This should not raise an exception
        from streamlined_float_daemon import StreamlinedFloatDaemon
        
        daemon = StreamlinedFloatDaemon(
            dropzone_path=str(self.dropzone_path),
            config_path=str(self.config_file)
        )
        
        # Basic checks
        assert daemon is not None
        assert hasattr(daemon, 'config')
        
    @pytest.mark.unit
    def test_config_loading_works(self):
        """Test that config loading works independently"""
        from config import FloatConfig
        
        config = FloatConfig(str(self.config_file))
        
        assert config is not None
        assert config.get('vault_path') == str(self.vault_path)
        assert config.get('dropzone_path') == str(self.dropzone_path)
        
    @pytest.mark.unit
    def test_daemon_manager_import(self):
        """Test that the daemon manager can be imported"""
        from streamlined_float_daemon import FloatDaemonManager
        
        # Should be able to import without error
        assert FloatDaemonManager is not None