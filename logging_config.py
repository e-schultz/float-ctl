"""
Comprehensive logging configuration for FLOAT daemon
Supports console, file, and structured logging with performance metrics
"""

import logging
import logging.handlers
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any

class FloatFormatter(logging.Formatter):
    """Custom formatter for FLOAT logging with emoji indicators"""
    
    LEVEL_EMOJIS = {
        'DEBUG': '🔍',
        'INFO': '📝', 
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🚨'
    }
    
    def format(self, record):
        # Add emoji for level
        emoji = self.LEVEL_EMOJIS.get(record.levelname, '📝')
        
        # Create base message
        if hasattr(record, 'float_id'):
            prefix = f"{emoji} [{record.float_id}]"
        else:
            prefix = f"{emoji}"
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
        
        # Build formatted message
        formatted_msg = f"{timestamp} | {prefix} | {record.getMessage()}"
        
        # Add extra context if present
        if hasattr(record, 'file_name'):
            formatted_msg += f" | File: {record.file_name}"
        if hasattr(record, 'processing_time'):
            formatted_msg += f" | Time: {record.processing_time:.2f}s"
        if hasattr(record, 'file_size'):
            formatted_msg += f" | Size: {record.file_size:,} bytes"
        
        return formatted_msg

class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add FLOAT-specific fields
        float_fields = ['float_id', 'file_name', 'processing_time', 'file_size', 
                       'error_type', 'retry_count', 'memory_usage', 'chunk_count']
        
        for field in float_fields:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': self.formatException(record.exc_info)
            }
        
        return json.dumps(log_data)

class PerformanceLogAdapter(logging.LoggerAdapter):
    """Adapter for adding performance metrics to log records"""
    
    def process(self, msg, kwargs):
        # Add extra fields from adapter context
        extra = kwargs.get('extra', {})
        extra.update(self.extra)
        kwargs['extra'] = extra
        return msg, kwargs

def setup_logging(config: Dict) -> logging.Logger:
    """Setup comprehensive logging for FLOAT daemon"""
    
    log_level = config.get('log_level', 'INFO').upper()
    log_file = config.get('log_file')
    dropzone_path = Path(config.get('dropzone_path', '.'))
    
    # Default log file location
    if not log_file:
        log_dir = dropzone_path / '.logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'float_daemon.log'
    
    # Create root logger
    logger = logging.getLogger('float_daemon')
    logger.setLevel(getattr(logging, log_level))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with emoji formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = FloatFormatter()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with detailed formatting
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, log_level))
        
        # Use JSON formatting for file logs
        file_formatter = JsonFormatter()
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Error-only handler for critical issues
    error_log = log_path.parent / 'float_errors.log' if log_file else None
    if error_log:
        error_handler = logging.handlers.RotatingFileHandler(
            error_log,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JsonFormatter())
        logger.addHandler(error_handler)
    
    # Performance metrics handler
    metrics_log = log_path.parent / 'float_metrics.log' if log_file else None
    if metrics_log and config.get('enable_performance_logging', True):
        metrics_handler = logging.handlers.RotatingFileHandler(
            metrics_log,
            maxBytes=20*1024*1024,  # 20MB for metrics
            backupCount=3,
            encoding='utf-8'
        )
        metrics_handler.setLevel(logging.INFO)
        metrics_handler.setFormatter(JsonFormatter())
        
        # Create metrics logger
        metrics_logger = logging.getLogger('float_daemon.metrics')
        metrics_logger.addHandler(metrics_handler)
        metrics_logger.setLevel(logging.INFO)
        metrics_logger.propagate = False  # Don't propagate to root logger
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance for a specific module"""
    if name:
        return logging.getLogger(f'float_daemon.{name}')
    return logging.getLogger('float_daemon')

def get_performance_adapter(logger: logging.Logger, float_id: str = None, **context) -> PerformanceLogAdapter:
    """Get a performance logging adapter with context"""
    extra = {'float_id': float_id} if float_id else {}
    extra.update(context)
    return PerformanceLogAdapter(logger, extra)

def log_file_processing_start(logger: logging.Logger, file_path: Path, float_id: str, file_size: int):
    """Log the start of file processing"""
    logger.info(
        "Starting file processing",
        extra={
            'float_id': float_id,
            'file_name': file_path.name,
            'file_size': file_size,
            'event': 'processing_start'
        }
    )

def log_file_processing_complete(logger: logging.Logger, float_id: str, file_name: str, 
                                processing_time: float, chunk_count: int, success: bool = True):
    """Log the completion of file processing"""
    level = logging.INFO if success else logging.ERROR
    logger.log(
        level,
        f"File processing {'completed' if success else 'failed'}",
        extra={
            'float_id': float_id,
            'file_name': file_name,
            'processing_time': processing_time,
            'chunk_count': chunk_count,
            'success': success,
            'event': 'processing_complete'
        }
    )

def log_error_with_context(logger: logging.Logger, error: Exception, context: Dict[str, Any]):
    """Log an error with comprehensive context"""
    logger.error(
        f"Error: {str(error)}",
        exc_info=True,
        extra={
            'error_type': type(error).__name__,
            'error_message': str(error),
            'event': 'error',
            **context
        }
    )

def log_performance_metrics(logger: logging.Logger, metrics: Dict[str, Any]):
    """Log performance metrics"""
    metrics_logger = logging.getLogger('float_daemon.metrics')
    metrics_logger.info(
        "Performance metrics",
        extra={
            'event': 'performance_metrics',
            **metrics
        }
    )

def log_system_health(logger: logging.Logger, health_data: Dict[str, Any]):
    """Log system health information"""
    logger.info(
        f"System health check: {health_data.get('status', 'unknown')}",
        extra={
            'event': 'health_check',
            **health_data
        }
    )

def log_ollama_summary(logger: logging.Logger, float_id: str, file_name: str, 
                      summary_time: float, token_count: int = None):
    """Log Ollama summarization metrics"""
    logger.info(
        "Ollama summary generated",
        extra={
            'float_id': float_id,
            'file_name': file_name,
            'summary_time': summary_time,
            'token_count': token_count,
            'event': 'ollama_summary'
        }
    )

def log_chroma_storage(logger: logging.Logger, float_id: str, file_name: str,
                      collection_name: str, chunk_count: int, storage_time: float):
    """Log Chroma database storage"""
    logger.info(
        f"Stored in Chroma collection: {collection_name}",
        extra={
            'float_id': float_id,
            'file_name': file_name,
            'collection_name': collection_name,
            'chunk_count': chunk_count,
            'storage_time': storage_time,
            'event': 'chroma_storage'
        }
    )

def log_dis_file_generation(logger: logging.Logger, float_id: str, file_name: str,
                           dis_file_path: Path, generation_time: float):
    """Log .dis file generation"""
    logger.info(
        f"Generated .dis file: {dis_file_path.name}",
        extra={
            'float_id': float_id,
            'file_name': file_name,
            'dis_file_name': dis_file_path.name,
            'generation_time': generation_time,
            'event': 'dis_file_generation'
        }
    )

class LogContext:
    """Context manager for adding context to all log messages"""
    
    def __init__(self, logger: logging.Logger, **context):
        self.logger = logger
        self.context = context
        self.adapter = PerformanceLogAdapter(logger, context)
    
    def __enter__(self):
        return self.adapter
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            log_error_with_context(self.logger, exc_val, self.context)

# Convenience function for creating log context
def log_context(logger: logging.Logger, **context):
    """Create a logging context manager"""
    return LogContext(logger, **context)

if __name__ == "__main__":
    # Test logging configuration
    test_config = {
        'log_level': 'DEBUG',
        'dropzone_path': '.',
        'enable_performance_logging': True
    }
    
    logger = setup_logging(test_config)
    
    # Test different log levels
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    # Test structured logging
    log_file_processing_start(logger, Path("test.txt"), "float_123", 1024)
    log_file_processing_complete(logger, "float_123", "test.txt", 2.5, 3, True)
    
    # Test context logging
    with log_context(logger, float_id="float_456", file_name="test2.txt") as ctx_logger:
        ctx_logger.info("Processing with context")
    
    print("Logging test complete")