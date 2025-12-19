#!/usr/bin/env python3
"""
GPU Monitor using nvidia-smi
Collects NVIDIA GPU metrics
"""

import subprocess
import logging

logger = logging.getLogger(__name__)


class GPUMonitor:
    """NVIDIA GPU monitoring via nvidia-smi"""
    
    def __init__(self):
        self.available = self._check_nvidia_smi()
        if not self.available:
            logger.warning("nvidia-smi not available, GPU metrics disabled")
    
    def _check_nvidia_smi(self):
        """Check if nvidia-smi is available"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--version'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_metrics(self):
        """
        Get GPU metrics from nvidia-smi
        Returns dict with metrics or None if unavailable
        """
        if not self.available:
            return None
        
        try:
            # Query comprehensive GPU stats
            result = subprocess.run(
                [
                    'nvidia-smi',
                    '--query-gpu=name,driver_version,temperature.gpu,utilization.gpu,'
                    'memory.total,memory.used,memory.free,utilization.encoder,'
                    'utilization.decoder,power.draw,fan.speed',
                    '--format=csv,noheader,nounits'
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                logger.error("nvidia-smi failed: %s", result.stderr)
                return None
            
            # Parse CSV output
            values = [v.strip() for v in result.stdout.strip().split(',')]
            
            if len(values) < 9:
                logger.error("Unexpected nvidia-smi output: %s", result.stdout)
                return None
            
            # Parse values (handle [N/A] values)
            def parse_int(val):
                try:
                    return int(val)
                except (ValueError, TypeError):
                    return 0
            
            def parse_float(val):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return 0.0
            
            memory_total = parse_int(values[4])
            memory_used = parse_int(values[5])
            memory_percent = int((memory_used / memory_total * 100)) if memory_total > 0 else 0
            
            metrics = {
                'name': values[0],
                'driver_version': values[1],
                'temperature': parse_int(values[2]),
                'utilization': parse_int(values[3]),
                'memory_total': memory_total,
                'memory_used': memory_used,
                'memory_free': parse_int(values[6]),
                'memory_percent': memory_percent,
                'encoder': parse_int(values[7]) if len(values) > 7 else 0,
                'decoder': parse_int(values[8]) if len(values) > 8 else 0,
                'power': parse_float(values[9]) if len(values) > 9 else 0.0,
                'fan_speed': parse_int(values[10]) if len(values) > 10 else 0,
            }
            
            return metrics
            
        except subprocess.TimeoutExpired:
            logger.error("nvidia-smi timeout")
            return None
        except Exception as e:
            logger.error("GPU metrics error: %s", str(e))
            return None
    
    def get_ffmpeg_processes(self):
        """Count active FFmpeg transcoding processes"""
        try:
            result = subprocess.run(
                ['pgrep', '-c', '-f', 'ffmpeg.*jellyfin'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return int(result.stdout.strip()) if result.returncode == 0 else 0
        except:
            return 0


# Singleton instance
_monitor = None

def get_gpu_monitor():
    """Get GPU monitor singleton"""
    global _monitor
    if _monitor is None:
        _monitor = GPUMonitor()
    return _monitor
