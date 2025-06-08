"""
Error recovery system for FLOAT file processing
Handles various error conditions with retry logic and quarantine management
"""

import shutil
import json
import traceback
from pathlib import Path
from typing import Dict, Optional, Callable, Any
import time
from datetime import datetime

class FileProcessingRecovery:
    """Error recovery system for file processing"""
    
    def __init__(self, dropzone_path: Path, max_retries: int = 3):
        self.dropzone_path = dropzone_path
        self.max_retries = max_retries
        
        # Create error handling directories
        self.error_folder = dropzone_path / ".errors"
        self.retry_folder = dropzone_path / ".retry" 
        self.quarantine_folder = dropzone_path / ".quarantine"
        self.processed_folder = dropzone_path / ".processed"
        
        for folder in [self.error_folder, self.retry_folder, self.quarantine_folder, self.processed_folder]:
            folder.mkdir(exist_ok=True)
        
        # Track retry history
        self.retry_history = {}
    
    def process_with_recovery(self, file_path: Path, processor_func: Callable, retry_count: int = 0) -> Dict:
        """Process file with comprehensive error recovery"""
        try:
            # Call the processor function
            result = processor_func(file_path)
            
            # If successful, clear retry history
            if str(file_path) in self.retry_history:
                del self.retry_history[str(file_path)]
            
            return result
            
        except MemoryError as e:
            return self._handle_memory_error(file_path, e, processor_func, retry_count)
            
        except PermissionError as e:
            return self._handle_permission_error(file_path, e, processor_func, retry_count)
            
        except FileNotFoundError as e:
            return self._handle_file_not_found(file_path, e)
            
        except Exception as e:
            return self._handle_general_error(file_path, e, processor_func, retry_count)
    
    def _handle_memory_error(self, file_path: Path, error: Exception, processor_func: Callable, retry_count: int) -> Dict:
        """Handle memory errors by moving large files"""
        print(f"💾 Memory error processing {file_path.name}, moving to quarantine")
        
        # Create error details
        error_details = {
            'error_type': 'memory_error',
            'error_message': str(error),
            'file_size': file_path.stat().st_size if file_path.exists() else 'unknown',
            'timestamp': datetime.now().isoformat()
        }
        
        quarantine_path = self._quarantine_file(file_path, f"Memory error: {error}", error_details)
        
        return {
            'success': False,
            'error': 'memory_error',
            'error_message': str(error),
            'quarantined': True,
            'quarantine_path': str(quarantine_path)
        }
    
    def _handle_permission_error(self, file_path: Path, error: Exception, processor_func: Callable, retry_count: int) -> Dict:
        """Handle permission errors with retry after delay"""
        print(f"🔒 Permission error processing {file_path.name}")
        
        if retry_count < self.max_retries:
            print(f"   Waiting 5 seconds before retry {retry_count + 1}/{self.max_retries}")
            time.sleep(5)
            
            # Try to fix permissions if possible
            try:
                import stat
                file_path.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
            except:
                pass
            
            return self.process_with_recovery(file_path, processor_func, retry_count + 1)
        else:
            error_details = {
                'error_type': 'permission_error',
                'error_message': str(error),
                'retry_count': retry_count,
                'timestamp': datetime.now().isoformat()
            }
            
            quarantine_path = self._quarantine_file(file_path, f"Permission error after {retry_count} retries: {error}", error_details)
            
            return {
                'success': False,
                'error': 'permission_error',
                'error_message': str(error),
                'quarantined': True,
                'quarantine_path': str(quarantine_path)
            }
    
    def _handle_file_not_found(self, file_path: Path, error: Exception) -> Dict:
        """Handle case where file disappeared"""
        print(f"❓ File not found: {file_path.name}")
        
        # Log the error but don't quarantine since file doesn't exist
        error_log_path = self.error_folder / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_path.name}.error.json"
        
        error_details = {
            'error_type': 'file_not_found',
            'error_message': str(error),
            'original_path': str(file_path),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(error_log_path, 'w') as f:
            json.dump(error_details, f, indent=2)
        
        return {
            'success': False,
            'error': 'file_not_found',
            'error_message': str(error),
            'quarantined': False,
            'error_log': str(error_log_path)
        }
    
    def _handle_general_error(self, file_path: Path, error: Exception, processor_func: Callable, retry_count: int) -> Dict:
        """Handle general errors with retry logic"""
        error_type = type(error).__name__
        print(f"⚠️ {error_type} processing {file_path.name}: {error}")
        
        # Track retry history
        file_key = str(file_path)
        if file_key not in self.retry_history:
            self.retry_history[file_key] = []
        
        self.retry_history[file_key].append({
            'attempt': retry_count + 1,
            'error_type': error_type,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat()
        })
        
        if retry_count < self.max_retries:
            print(f"🔄 Retry {retry_count + 1}/{self.max_retries} for {file_path.name}")
            
            # Exponential backoff
            wait_time = 2 ** retry_count
            print(f"   Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            
            # Move to retry folder temporarily
            retry_path = self.retry_folder / f"{retry_count}_{datetime.now().strftime('%H%M%S')}_{file_path.name}"
            shutil.copy2(str(file_path), str(retry_path))
            
            try:
                result = self.process_with_recovery(retry_path, processor_func, retry_count + 1)
                # If successful, remove the retry copy
                if result.get('success'):
                    retry_path.unlink()
                return result
            except Exception as e:
                # Clean up retry file on failure
                if retry_path.exists():
                    retry_path.unlink()
                raise
        else:
            print(f"❌ Max retries exceeded for {file_path.name}, quarantining")
            
            error_details = {
                'error_type': error_type,
                'error_message': str(error),
                'retry_history': self.retry_history.get(file_key, []),
                'traceback': traceback.format_exc(),
                'timestamp': datetime.now().isoformat()
            }
            
            quarantine_path = self._quarantine_file(file_path, f"Max retries exceeded: {error}", error_details)
            
            # Clear retry history
            if file_key in self.retry_history:
                del self.retry_history[file_key]
            
            return {
                'success': False,
                'error': 'max_retries_exceeded',
                'error_type': error_type,
                'error_message': str(error),
                'quarantined': True,
                'quarantine_path': str(quarantine_path),
                'retry_count': retry_count
            }
    
    def _quarantine_file(self, file_path: Path, reason: str, error_details: Dict) -> Path:
        """Move file to quarantine with error details"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        quarantine_name = f"{timestamp}_{file_path.name}"
        quarantine_path = self.quarantine_folder / quarantine_name
        
        # Move or copy file (copy if move fails)
        try:
            shutil.move(str(file_path), str(quarantine_path))
        except Exception as e:
            print(f"   Failed to move file, copying instead: {e}")
            shutil.copy2(str(file_path), str(quarantine_path))
        
        # Create detailed error log
        error_log = quarantine_path.with_suffix(quarantine_path.suffix + '.error.json')
        error_info = {
            'file': file_path.name,
            'original_path': str(file_path),
            'quarantined': timestamp,
            'reason': reason,
            'details': error_details
        }
        
        with open(error_log, 'w') as f:
            json.dump(error_info, f, indent=2)
        
        # Create human-readable error summary
        error_summary = quarantine_path.with_suffix(quarantine_path.suffix + '.error.txt')
        with open(error_summary, 'w') as f:
            f.write(f"FLOAT Processing Error Report\n")
            f.write(f"{'=' * 50}\n\n")
            f.write(f"File: {file_path.name}\n")
            f.write(f"Quarantined: {timestamp}\n")
            f.write(f"Reason: {reason}\n")
            f.write(f"\nError Type: {error_details.get('error_type', 'Unknown')}\n")
            f.write(f"Error Message: {error_details.get('error_message', 'No message')}\n")
            
            if 'retry_history' in error_details:
                f.write(f"\nRetry History:\n")
                for attempt in error_details['retry_history']:
                    f.write(f"  - Attempt {attempt['attempt']}: {attempt['error_type']} at {attempt['timestamp']}\n")
            
            if 'traceback' in error_details:
                f.write(f"\nFull Traceback:\n{error_details['traceback']}\n")
        
        return quarantine_path
    
    def move_to_processed(self, file_path: Path) -> Path:
        """Move successfully processed file to processed folder"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        processed_name = f"{timestamp}_{file_path.name}"
        processed_path = self.processed_folder / processed_name
        
        try:
            shutil.move(str(file_path), str(processed_path))
            return processed_path
        except Exception as e:
            print(f"⚠️ Failed to move to processed folder: {e}")
            return file_path
    
    def get_quarantine_summary(self) -> Dict:
        """Get summary of quarantined files"""
        quarantined_files = list(self.quarantine_folder.glob('*'))
        error_logs = list(self.quarantine_folder.glob('*.error.json'))
        
        summary = {
            'total_quarantined': len([f for f in quarantined_files if not f.name.endswith('.error.json') and not f.name.endswith('.error.txt')]),
            'by_error_type': {},
            'recent_errors': []
        }
        
        # Analyze error logs
        for error_log in error_logs:
            try:
                with open(error_log, 'r') as f:
                    error_info = json.load(f)
                    error_type = error_info.get('details', {}).get('error_type', 'unknown')
                    
                    if error_type not in summary['by_error_type']:
                        summary['by_error_type'][error_type] = 0
                    summary['by_error_type'][error_type] += 1
                    
                    # Add to recent errors
                    summary['recent_errors'].append({
                        'file': error_info.get('file', 'unknown'),
                        'error_type': error_type,
                        'timestamp': error_info.get('quarantined', 'unknown'),
                        'reason': error_info.get('reason', 'unknown')
                    })
            except Exception as e:
                print(f"⚠️ Failed to read error log {error_log}: {e}")
        
        # Sort recent errors by timestamp
        summary['recent_errors'].sort(key=lambda x: x['timestamp'], reverse=True)
        summary['recent_errors'] = summary['recent_errors'][:10]  # Keep only 10 most recent
        
        return summary
    
    def cleanup_old_files(self, days_to_keep: int = 7):
        """Clean up old files from error handling folders"""
        import time
        current_time = time.time()
        cutoff_time = current_time - (days_to_keep * 24 * 60 * 60)
        
        folders_to_clean = [self.error_folder, self.retry_folder, self.processed_folder]
        total_cleaned = 0
        
        for folder in folders_to_clean:
            for file_path in folder.iterdir():
                if file_path.stat().st_mtime < cutoff_time:
                    try:
                        if file_path.is_file():
                            file_path.unlink()
                        elif file_path.is_dir():
                            shutil.rmtree(file_path)
                        total_cleaned += 1
                    except Exception as e:
                        print(f"⚠️ Failed to clean up {file_path}: {e}")
        
        if total_cleaned > 0:
            print(f"🧹 Cleaned up {total_cleaned} old files")
        
        return total_cleaned


class RecoveryContext:
    """Context manager for error recovery"""
    
    def __init__(self, recovery: FileProcessingRecovery, file_path: Path, processor_func: Callable):
        self.recovery = recovery
        self.file_path = file_path
        self.processor_func = processor_func
        self.result = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # An error occurred, use recovery
            self.result = self.recovery.process_with_recovery(
                self.file_path, 
                self.processor_func,
                retry_count=0
            )
            return True  # Suppress the exception
        return False
    
    def process(self):
        """Process the file with recovery"""
        self.result = self.recovery.process_with_recovery(
            self.file_path,
            self.processor_func
        )
        return self.result