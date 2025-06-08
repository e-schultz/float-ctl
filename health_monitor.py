"""
Health monitoring system for FLOAT daemon
Monitors component health, connectivity, and provides status reporting
"""

import json
import os
import threading
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Any
import psutil

class HealthMonitor:
    """Monitor daemon health and provide comprehensive status information"""
    
    def __init__(self, config: Dict, performance_monitor=None):
        self.config = config
        self.performance_monitor = performance_monitor
        
        # Paths
        self.dropzone_path = Path(config.get('dropzone_path', '.'))
        self.vault_path = Path(config.get('vault_path', '.'))
        self.chroma_data_path = config.get('chroma_data_path', '.')
        
        # Health state
        self.last_processing_time = None
        self.component_health = {}
        self.error_count = 0
        self.processing_count = 0
        self.health_checks_enabled = config.get('enable_health_checks', True)
        
        # Health check interval
        self.check_interval = config.get('health_check_interval', 60)
        self.health_thread = None
        self.monitoring_active = False
        
        # Status file
        self.status_file = self.dropzone_path / '.daemon_status.json'
        
        # Health history
        self.health_history = []
        self.max_history = 100
        
        # Component checkers
        self._initialize_component_checkers()
    
    def _initialize_component_checkers(self):
        """Initialize component-specific health checkers"""
        self.component_checkers = {
            'dropzone': self._check_dropzone_health,
            'vault': self._check_vault_health,
            'chroma': self._check_chroma_health,
            'ollama': self._check_ollama_health,
            'disk_space': self._check_disk_space,
            'memory': self._check_memory_usage,
            'quarantine': self._check_quarantine_status
        }
    
    def start_monitoring(self):
        """Start continuous health monitoring"""
        if not self.health_checks_enabled or self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.health_thread = threading.Thread(
            target=self._health_check_loop,
            daemon=True
        )
        self.health_thread.start()
        print(f"🏥 Health monitoring started (interval: {self.check_interval}s)")
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring_active = False
        if self.health_thread:
            self.health_thread.join(timeout=5)
        print("🏥 Health monitoring stopped")
    
    def _health_check_loop(self):
        """Continuous health monitoring loop"""
        while self.monitoring_active:
            try:
                self.perform_health_check()
                self.write_status_file()
                time.sleep(self.check_interval)
            except Exception as e:
                print(f"⚠️ Health check error: {e}")
                time.sleep(min(self.check_interval, 30))  # Fallback interval
    
    def perform_health_check(self) -> Dict:
        """Perform comprehensive health check"""
        start_time = time.time()
        health_results = {}
        
        # Check all components
        for component, checker in self.component_checkers.items():
            try:
                health_results[component] = checker()
            except Exception as e:
                health_results[component] = {
                    'status': 'error',
                    'message': f"Health check failed: {e}",
                    'timestamp': datetime.now().isoformat()
                }
        
        # Overall health assessment
        overall_status = self._assess_overall_health(health_results)
        
        # Create complete health report
        health_report = {
            'overall_status': overall_status,
            'timestamp': datetime.now().isoformat(),
            'check_duration_seconds': time.time() - start_time,
            'components': health_results,
            'uptime_seconds': self._get_uptime(),
            'performance_summary': self._get_performance_summary()
        }
        
        # Store in history
        self.health_history.append(health_report)
        if len(self.health_history) > self.max_history:
            self.health_history.pop(0)
        
        self.component_health = health_results
        return health_report
    
    def _check_dropzone_health(self) -> Dict:
        """Check dropzone folder accessibility and state"""
        try:
            # Check existence and permissions
            if not self.dropzone_path.exists():
                return {
                    'status': 'critical',
                    'message': 'Dropzone path does not exist',
                    'path': str(self.dropzone_path)
                }
            
            if not os.access(self.dropzone_path, os.R_OK | os.W_OK):
                return {
                    'status': 'critical',
                    'message': 'Insufficient permissions on dropzone',
                    'path': str(self.dropzone_path)
                }
            
            # Count files in dropzone
            files = list(self.dropzone_path.glob('*'))
            regular_files = [f for f in files if f.is_file() and not f.name.startswith('.')]
            
            # Check for error folders
            error_folders = ['.errors', '.quarantine', '.retry']
            error_counts = {}
            for folder in error_folders:
                folder_path = self.dropzone_path / folder
                if folder_path.exists():
                    error_counts[folder] = len(list(folder_path.glob('*')))
            
            return {
                'status': 'healthy',
                'message': 'Dropzone accessible',
                'path': str(self.dropzone_path),
                'pending_files': len(regular_files),
                'error_counts': error_counts
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Dropzone check failed: {e}",
                'path': str(self.dropzone_path)
            }
    
    def _check_vault_health(self) -> Dict:
        """Check Obsidian vault accessibility"""
        try:
            if not self.vault_path.exists():
                return {
                    'status': 'warning',
                    'message': 'Vault path does not exist',
                    'path': str(self.vault_path)
                }
            
            if not os.access(self.vault_path, os.R_OK):
                return {
                    'status': 'warning',
                    'message': 'Cannot read vault path',
                    'path': str(self.vault_path)
                }
            
            # Check for key vault folders
            key_folders = ['FLOAT.conversations', 'FLOAT.logs', 'FLOAT.references']
            folder_status = {}
            for folder in key_folders:
                folder_path = self.vault_path / folder
                folder_status[folder] = {
                    'exists': folder_path.exists(),
                    'file_count': len(list(folder_path.glob('*'))) if folder_path.exists() else 0
                }
            
            return {
                'status': 'healthy',
                'message': 'Vault accessible',
                'path': str(self.vault_path),
                'folders': folder_status
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Vault check failed: {e}",
                'path': str(self.vault_path)
            }
    
    def _check_chroma_health(self) -> Dict:
        """Check ChromaDB connectivity and collections"""
        try:
            # Try to import and connect to ChromaDB
            import chromadb
            
            client = chromadb.PersistentClient(path=self.chroma_data_path)
            collections = client.list_collections()
            
            # Check for expected FLOAT collections
            collection_names = [c.name for c in collections]
            expected_collections = [
                'float_dropzone_comprehensive',
                'float_tripartite_v2_concept',
                'float_tripartite_v2_framework', 
                'float_tripartite_v2_metaphor'
            ]
            
            missing_collections = [c for c in expected_collections if c not in collection_names]
            
            # Get collection stats
            collection_stats = {}
            for collection in collections:
                try:
                    count = collection.count()
                    collection_stats[collection.name] = count
                except Exception as e:
                    collection_stats[collection.name] = f"Error: {e}"
            
            status = 'healthy' if not missing_collections else 'warning'
            message = 'ChromaDB healthy' if not missing_collections else f'Missing collections: {missing_collections}'
            
            return {
                'status': status,
                'message': message,
                'path': self.chroma_data_path,
                'total_collections': len(collections),
                'collection_stats': collection_stats,
                'missing_collections': missing_collections
            }
            
        except ImportError:
            return {
                'status': 'warning',
                'message': 'ChromaDB not available (import failed)',
                'path': self.chroma_data_path
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"ChromaDB check failed: {e}",
                'path': self.chroma_data_path
            }
    
    def _check_ollama_health(self) -> Dict:
        """Check Ollama service connectivity"""
        if not self.config.get('enable_ollama', True):
            return {
                'status': 'disabled',
                'message': 'Ollama disabled in configuration'
            }
        
        try:
            ollama_url = self.config.get('ollama_url', 'http://localhost:11434')
            
            # Try to connect to Ollama API
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m.get('name', 'unknown') for m in models]
                
                # Check if configured model is available
                configured_model = self.config.get('ollama_model', 'llama3.1:8b')
                model_available = any(configured_model in name for name in model_names)
                
                status = 'healthy' if model_available else 'warning'
                message = f'Ollama available, model {"found" if model_available else "not found"}'
                
                return {
                    'status': status,
                    'message': message,
                    'url': ollama_url,
                    'available_models': model_names,
                    'configured_model': configured_model,
                    'model_available': model_available
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Ollama API returned {response.status_code}',
                    'url': ollama_url
                }
                
        except requests.exceptions.ConnectionError:
            return {
                'status': 'error',
                'message': 'Cannot connect to Ollama service',
                'url': self.config.get('ollama_url', 'http://localhost:11434')
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Ollama check failed: {e}',
                'url': self.config.get('ollama_url', 'http://localhost:11434')
            }
    
    def _check_disk_space(self) -> Dict:
        """Check available disk space"""
        try:
            usage = psutil.disk_usage(str(self.dropzone_path))
            
            free_gb = usage.free / 1024 / 1024 / 1024
            used_percent = (usage.used / usage.total) * 100
            
            # Determine status based on available space
            if free_gb < 1:  # Less than 1GB
                status = 'critical'
                message = f'Very low disk space: {free_gb:.1f}GB free'
            elif free_gb < 5:  # Less than 5GB
                status = 'warning' 
                message = f'Low disk space: {free_gb:.1f}GB free'
            elif used_percent > 90:  # More than 90% used
                status = 'warning'
                message = f'Disk usage high: {used_percent:.1f}% used'
            else:
                status = 'healthy'
                message = f'Disk space adequate: {free_gb:.1f}GB free'
            
            return {
                'status': status,
                'message': message,
                'free_gb': round(free_gb, 2),
                'used_percent': round(used_percent, 1),
                'total_gb': round(usage.total / 1024 / 1024 / 1024, 2)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Disk space check failed: {e}'
            }
    
    def _check_memory_usage(self) -> Dict:
        """Check system and process memory usage"""
        try:
            # System memory
            system_memory = psutil.virtual_memory()
            
            # Process memory
            process = psutil.Process()
            process_memory = process.memory_info()
            
            system_used_percent = system_memory.percent
            process_used_mb = process_memory.rss / 1024 / 1024
            
            # Determine status
            if system_used_percent > 95:
                status = 'critical'
                message = f'Critical memory usage: {system_used_percent:.1f}%'
            elif system_used_percent > 85:
                status = 'warning'
                message = f'High memory usage: {system_used_percent:.1f}%'
            else:
                status = 'healthy'
                message = f'Memory usage normal: {system_used_percent:.1f}%'
            
            return {
                'status': status,
                'message': message,
                'system_used_percent': round(system_used_percent, 1),
                'system_available_gb': round(system_memory.available / 1024 / 1024 / 1024, 2),
                'process_used_mb': round(process_used_mb, 1)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Memory check failed: {e}'
            }
    
    def _check_quarantine_status(self) -> Dict:
        """Check quarantine folder for error accumulation"""
        try:
            quarantine_folder = self.dropzone_path / '.quarantine'
            if not quarantine_folder.exists():
                return {
                    'status': 'healthy',
                    'message': 'No quarantine folder',
                    'quarantined_files': 0
                }
            
            quarantined_files = list(quarantine_folder.glob('*'))
            # Filter out error logs
            actual_files = [f for f in quarantined_files if not f.name.endswith('.error.json') and not f.name.endswith('.error.txt')]
            
            count = len(actual_files)
            
            # Determine status based on quarantine accumulation
            if count > 50:
                status = 'critical'
                message = f'Too many quarantined files: {count}'
            elif count > 10:
                status = 'warning'
                message = f'Multiple quarantined files: {count}'
            elif count > 0:
                status = 'warning'
                message = f'Some quarantined files: {count}'
            else:
                status = 'healthy'
                message = 'No quarantined files'
            
            return {
                'status': status,
                'message': message,
                'quarantined_files': count,
                'quarantine_path': str(quarantine_folder)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Quarantine check failed: {e}'
            }
    
    def _assess_overall_health(self, component_results: Dict) -> str:
        """Assess overall system health based on component statuses"""
        statuses = [result.get('status', 'unknown') for result in component_results.values()]
        
        if 'critical' in statuses:
            return 'critical'
        elif 'error' in statuses:
            return 'error'
        elif 'warning' in statuses:
            return 'warning'
        elif all(status in ['healthy', 'disabled'] for status in statuses):
            return 'healthy'
        else:
            return 'unknown'
    
    def _get_uptime(self) -> float:
        """Get daemon uptime in seconds"""
        if self.performance_monitor:
            return time.time() - self.performance_monitor.start_time
        return 0
    
    def _get_performance_summary(self) -> Dict:
        """Get performance summary from performance monitor"""
        if self.performance_monitor:
            return self.performance_monitor.get_summary_stats()
        return {'no_performance_data': True}
    
    def record_processing(self, success: bool):
        """Record processing attempt"""
        self.last_processing_time = datetime.now()
        self.processing_count += 1
        if not success:
            self.error_count += 1
    
    def get_status(self) -> Dict:
        """Get comprehensive daemon status"""
        return {
            'overall_status': self._assess_overall_health(self.component_health),
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': self._get_uptime(),
            'last_processing': self.last_processing_time.isoformat() if self.last_processing_time else None,
            'processing_count': self.processing_count,
            'error_count': self.error_count,
            'error_rate': self.error_count / max(self.processing_count, 1),
            'components': self.component_health,
            'performance': self._get_performance_summary()
        }
    
    def write_status_file(self):
        """Write comprehensive status to file for external monitoring"""
        try:
            status = self.get_status()
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to write status file: {e}")
    
    def get_health_trends(self, hours: int = 24) -> Dict:
        """Analyze health trends over time"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_checks = [
            check for check in self.health_history
            if datetime.fromisoformat(check['timestamp']) > cutoff_time
        ]
        
        if not recent_checks:
            return {'no_data': True, 'period_hours': hours}
        
        # Analyze trends
        status_counts = {}
        avg_check_duration = 0
        component_failures = {}
        
        for check in recent_checks:
            status = check['overall_status']
            status_counts[status] = status_counts.get(status, 0) + 1
            avg_check_duration += check.get('check_duration_seconds', 0)
            
            # Track component failures
            for component, result in check['components'].items():
                if result.get('status') in ['error', 'critical']:
                    if component not in component_failures:
                        component_failures[component] = 0
                    component_failures[component] += 1
        
        avg_check_duration /= len(recent_checks)
        
        return {
            'period_hours': hours,
            'total_checks': len(recent_checks),
            'status_distribution': status_counts,
            'avg_check_duration_seconds': round(avg_check_duration, 3),
            'component_failures': component_failures,
            'latest_status': recent_checks[-1]['overall_status'] if recent_checks else 'unknown'
        }

if __name__ == "__main__":
    # Test health monitoring
    test_config = {
        'dropzone_path': '.',
        'vault_path': '/Users/evan/vault',
        'chroma_data_path': '/Users/evan/github/chroma-data',
        'enable_ollama': True,
        'ollama_url': 'http://localhost:11434',
        'health_check_interval': 10
    }
    
    monitor = HealthMonitor(test_config)
    
    print("Running health check...")
    health_report = monitor.perform_health_check()
    print(json.dumps(health_report, indent=2))
    
    print("\nWriting status file...")
    monitor.write_status_file()
    
    print("Health monitoring test complete")