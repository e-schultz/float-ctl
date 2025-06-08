"""
Performance monitoring for FLOAT daemon
Tracks processing metrics, memory usage, and system performance
"""

import time
import psutil
import json
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import threading
from collections import deque

@dataclass
class ProcessingMetrics:
    """Metrics for a single file processing operation"""
    file_name: str
    file_size_bytes: int
    processing_time_seconds: float
    memory_used_mb: float
    ollama_time_seconds: Optional[float]
    chroma_time_seconds: Optional[float]
    dis_generation_time_seconds: Optional[float]
    chunks_created: int
    success: bool
    error_type: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass
class SystemMetrics:
    """System-level performance metrics"""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    disk_free_gb: float
    process_count: int
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class PerformanceMonitor:
    """Monitor and log performance metrics for FLOAT daemon"""
    
    def __init__(self, dropzone_path: Path, max_history: int = 1000):
        self.dropzone_path = dropzone_path
        self.max_history = max_history
        
        # Metrics storage
        self.processing_history: deque = deque(maxlen=max_history)
        self.system_history: deque = deque(maxlen=100)  # Keep fewer system metrics
        
        # Performance tracking
        self.start_time = time.time()
        self.total_files_processed = 0
        self.total_bytes_processed = 0
        self.error_count = 0
        
        # System monitoring
        self.process = psutil.Process()
        self.system_monitor_active = False
        self.system_monitor_thread = None
        
        # Metrics file paths
        self.metrics_dir = dropzone_path / '.metrics'
        self.metrics_dir.mkdir(exist_ok=True)
        self.performance_log = self.metrics_dir / 'performance.jsonl'
        self.system_log = self.metrics_dir / 'system.jsonl'
        
    def start_system_monitoring(self, interval: int = 60):
        """Start background system monitoring"""
        if self.system_monitor_active:
            return
        
        self.system_monitor_active = True
        self.system_monitor_thread = threading.Thread(
            target=self._system_monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.system_monitor_thread.start()
    
    def stop_system_monitoring(self):
        """Stop background system monitoring"""
        self.system_monitor_active = False
        if self.system_monitor_thread:
            self.system_monitor_thread.join(timeout=5)
    
    def _system_monitor_loop(self, interval: int):
        """Background system monitoring loop"""
        while self.system_monitor_active:
            try:
                self._collect_system_metrics()
                time.sleep(interval)
            except Exception as e:
                print(f"⚠️ System monitoring error: {e}")
                time.sleep(interval)
    
    def _collect_system_metrics(self):
        """Collect current system performance metrics"""
        try:
            # CPU and memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Disk usage for dropzone
            disk_usage = psutil.disk_usage(str(self.dropzone_path))
            
            # Process count
            process_count = len(psutil.pids())
            
            metrics = SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / 1024 / 1024,
                memory_available_mb=memory.available / 1024 / 1024,
                disk_usage_percent=(disk_usage.used / disk_usage.total) * 100,
                disk_free_gb=disk_usage.free / 1024 / 1024 / 1024,
                process_count=process_count
            )
            
            self.system_history.append(metrics)
            self._log_system_metrics(metrics)
            
        except Exception as e:
            print(f"⚠️ Failed to collect system metrics: {e}")
    
    def track_processing(self, file_path: Path, file_size_bytes: int) -> 'ProcessingTracker':
        """Context manager for tracking file processing"""
        return ProcessingTracker(self, file_path, file_size_bytes)
    
    def add_processing_metrics(self, metrics: ProcessingMetrics):
        """Add processing metrics to history and update counters"""
        self.processing_history.append(metrics)
        self.total_files_processed += 1
        
        if metrics.success:
            self.total_bytes_processed += metrics.file_size_bytes
        else:
            self.error_count += 1
        
        # Log to file
        self._log_processing_metrics(metrics)
        
        # Print summary
        status = "✅" if metrics.success else "❌"
        print(f"📊 {status} {metrics.file_name}: {metrics.processing_time_seconds:.2f}s, "
              f"{metrics.memory_used_mb:.1f}MB, {metrics.chunks_created} chunks")
    
    def _log_processing_metrics(self, metrics: ProcessingMetrics):
        """Log processing metrics to file"""
        try:
            with open(self.performance_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(metrics)) + '\n')
        except Exception as e:
            print(f"⚠️ Failed to log processing metrics: {e}")
    
    def _log_system_metrics(self, metrics: SystemMetrics):
        """Log system metrics to file"""
        try:
            with open(self.system_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(metrics)) + '\n')
        except Exception as e:
            print(f"⚠️ Failed to log system metrics: {e}")
    
    def get_summary_stats(self) -> Dict:
        """Get comprehensive performance summary"""
        if not self.processing_history:
            return {
                'no_data': True,
                'uptime_seconds': time.time() - self.start_time
            }
        
        # Filter successful and failed operations
        successful = [m for m in self.processing_history if m.success]
        failed = [m for m in self.processing_history if not m.success]
        
        # Calculate averages for successful operations
        if successful:
            avg_processing_time = sum(m.processing_time_seconds for m in successful) / len(successful)
            avg_memory_usage = sum(m.memory_used_mb for m in successful) / len(successful)
            avg_file_size = sum(m.file_size_bytes for m in successful) / len(successful)
            avg_chunks = sum(m.chunks_created for m in successful) / len(successful)
            
            # Calculate processing rate
            total_time = sum(m.processing_time_seconds for m in successful)
            throughput_files_per_minute = (len(successful) / total_time) * 60 if total_time > 0 else 0
            throughput_mb_per_minute = (sum(m.file_size_bytes for m in successful) / 1024 / 1024 / total_time) * 60 if total_time > 0 else 0
        else:
            avg_processing_time = 0
            avg_memory_usage = 0
            avg_file_size = 0
            avg_chunks = 0
            throughput_files_per_minute = 0
            throughput_mb_per_minute = 0
        
        # Error analysis
        error_types = {}
        for m in failed:
            error_type = m.error_type or 'unknown'
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Recent performance (last 10 files)
        recent_files = list(self.processing_history)[-10:]
        recent_success_rate = sum(1 for m in recent_files if m.success) / len(recent_files) if recent_files else 0
        
        return {
            'uptime_seconds': time.time() - self.start_time,
            'total_files': self.total_files_processed,
            'successful_files': len(successful),
            'failed_files': len(failed),
            'success_rate': len(successful) / self.total_files_processed if self.total_files_processed > 0 else 0,
            'recent_success_rate': recent_success_rate,
            'total_bytes_processed': self.total_bytes_processed,
            'total_gb_processed': self.total_bytes_processed / 1024 / 1024 / 1024,
            'avg_processing_time_seconds': avg_processing_time,
            'avg_memory_usage_mb': avg_memory_usage,
            'avg_file_size_bytes': avg_file_size,
            'avg_chunks_per_file': avg_chunks,
            'throughput_files_per_minute': throughput_files_per_minute,
            'throughput_mb_per_minute': throughput_mb_per_minute,
            'error_types': error_types
        }
    
    def get_current_system_stats(self) -> Dict:
        """Get current system performance statistics"""
        try:
            # Process-specific stats
            process_memory = self.process.memory_info()
            process_cpu = self.process.cpu_percent()
            
            # System stats
            memory = psutil.virtual_memory()
            disk_usage = psutil.disk_usage(str(self.dropzone_path))
            
            return {
                'process_memory_mb': process_memory.rss / 1024 / 1024,
                'process_cpu_percent': process_cpu,
                'system_memory_percent': memory.percent,
                'system_memory_available_gb': memory.available / 1024 / 1024 / 1024,
                'disk_free_gb': disk_usage.free / 1024 / 1024 / 1024,
                'disk_usage_percent': (disk_usage.used / disk_usage.total) * 100
            }
        except Exception as e:
            return {'error': f"Failed to get system stats: {e}"}
    
    def get_performance_trends(self, hours: int = 24) -> Dict:
        """Analyze performance trends over specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter recent metrics
        recent_metrics = [
            m for m in self.processing_history
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        if not recent_metrics:
            return {'no_data': True, 'period_hours': hours}
        
        # Group by hour for trend analysis
        hourly_stats = {}
        for metric in recent_metrics:
            hour = datetime.fromisoformat(metric.timestamp).replace(minute=0, second=0, microsecond=0)
            hour_key = hour.isoformat()
            
            if hour_key not in hourly_stats:
                hourly_stats[hour_key] = {
                    'files_processed': 0,
                    'files_successful': 0,
                    'total_processing_time': 0,
                    'total_file_size': 0,
                    'errors': []
                }
            
            stats = hourly_stats[hour_key]
            stats['files_processed'] += 1
            stats['total_processing_time'] += metric.processing_time_seconds
            stats['total_file_size'] += metric.file_size_bytes
            
            if metric.success:
                stats['files_successful'] += 1
            else:
                stats['errors'].append(metric.error_type or 'unknown')
        
        # Calculate trends
        hours_data = []
        for hour_key, stats in sorted(hourly_stats.items()):
            hours_data.append({
                'hour': hour_key,
                'files_processed': stats['files_processed'],
                'success_rate': stats['files_successful'] / stats['files_processed'] if stats['files_processed'] > 0 else 0,
                'avg_processing_time': stats['total_processing_time'] / stats['files_processed'] if stats['files_processed'] > 0 else 0,
                'total_mb_processed': stats['total_file_size'] / 1024 / 1024,
                'error_count': len(stats['errors'])
            })
        
        return {
            'period_hours': hours,
            'total_files_in_period': len(recent_metrics),
            'hourly_breakdown': hours_data
        }
    
    def cleanup_old_metrics(self, days_to_keep: int = 30):
        """Clean up old metrics files"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days_to_keep)
            
            # Clean processing history in memory
            self.processing_history = deque([
                m for m in self.processing_history
                if datetime.fromisoformat(m.timestamp) > cutoff_time
            ], maxlen=self.max_history)
            
            # Archive old log files
            for log_file in [self.performance_log, self.system_log]:
                if log_file.exists():
                    archive_file = log_file.with_suffix(f'.{datetime.now().strftime("%Y%m%d")}.jsonl')
                    log_file.rename(archive_file)
                    print(f"📦 Archived metrics: {archive_file.name}")
            
        except Exception as e:
            print(f"⚠️ Failed to cleanup metrics: {e}")

class ProcessingTracker:
    """Context manager for tracking individual file processing"""
    
    def __init__(self, monitor: PerformanceMonitor, file_path: Path, file_size_bytes: int):
        self.monitor = monitor
        self.file_path = file_path
        self.file_size_bytes = file_size_bytes
        
        # Timing
        self.start_time = None
        self.start_memory = None
        
        # Component timings
        self.ollama_start = None
        self.ollama_time = None
        self.chroma_start = None
        self.chroma_time = None
        self.dis_start = None
        self.dis_time = None
        
        # Results
        self.chunks_created = 0
        self.success = False
        self.error_type = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.start_memory = self.monitor.process.memory_info().rss / 1024 / 1024
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        end_memory = self.monitor.process.memory_info().rss / 1024 / 1024
        
        self.success = exc_type is None
        if exc_type:
            self.error_type = exc_type.__name__
        
        metrics = ProcessingMetrics(
            file_name=self.file_path.name,
            file_size_bytes=self.file_size_bytes,
            processing_time_seconds=end_time - self.start_time,
            memory_used_mb=end_memory - self.start_memory,
            ollama_time_seconds=self.ollama_time,
            chroma_time_seconds=self.chroma_time,
            dis_generation_time_seconds=self.dis_time,
            chunks_created=self.chunks_created,
            success=self.success,
            error_type=self.error_type
        )
        
        self.monitor.add_processing_metrics(metrics)
    
    def start_ollama_timer(self):
        """Start timing Ollama summarization"""
        self.ollama_start = time.time()
    
    def end_ollama_timer(self):
        """End timing Ollama summarization"""
        if self.ollama_start:
            self.ollama_time = time.time() - self.ollama_start
    
    def start_chroma_timer(self):
        """Start timing Chroma storage"""
        self.chroma_start = time.time()
    
    def end_chroma_timer(self):
        """End timing Chroma storage"""
        if self.chroma_start:
            self.chroma_time = time.time() - self.chroma_start
    
    def start_dis_timer(self):
        """Start timing .dis file generation"""
        self.dis_start = time.time()
    
    def end_dis_timer(self):
        """End timing .dis file generation"""
        if self.dis_start:
            self.dis_time = time.time() - self.dis_start
    
    def set_chunks_created(self, count: int):
        """Set the number of chunks created"""
        self.chunks_created = count

if __name__ == "__main__":
    # Test performance monitoring
    from pathlib import Path
    
    monitor = PerformanceMonitor(Path("."))
    monitor.start_system_monitoring(interval=5)
    
    # Simulate some file processing
    with monitor.track_processing(Path("test1.txt"), 1024) as tracker:
        time.sleep(0.1)  # Simulate processing
        tracker.set_chunks_created(3)
    
    with monitor.track_processing(Path("test2.txt"), 2048) as tracker:
        time.sleep(0.2)  # Simulate processing
        tracker.set_chunks_created(5)
        
    # Show stats
    print("Summary stats:")
    print(json.dumps(monitor.get_summary_stats(), indent=2))
    
    print("\nCurrent system stats:")
    print(json.dumps(monitor.get_current_system_stats(), indent=2))
    
    monitor.stop_system_monitoring()
    print("Performance monitoring test complete")