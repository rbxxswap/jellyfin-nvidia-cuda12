#!/usr/bin/env python3
"""
Container Stats Monitor
Collects container resource usage metrics
"""

import os
import logging

logger = logging.getLogger(__name__)


class ContainerStats:
    """Container resource monitoring"""
    
    def __init__(self):
        self.cgroup_v2 = os.path.exists('/sys/fs/cgroup/cgroup.controllers')
        self.cgroup_path = self._find_cgroup_path()
    
    def _find_cgroup_path(self):
        """Find the cgroup path for this container"""
        if self.cgroup_v2:
            return '/sys/fs/cgroup'
        else:
            # cgroup v1
            return '/sys/fs/cgroup/memory'
    
    def _read_file(self, path):
        """Read a file and return content"""
        try:
            with open(path, 'r') as f:
                return f.read().strip()
        except (FileNotFoundError, PermissionError):
            return None
    
    def get_memory_stats(self):
        """Get container memory usage"""
        try:
            if self.cgroup_v2:
                # cgroup v2
                current = self._read_file('/sys/fs/cgroup/memory.current')
                max_mem = self._read_file('/sys/fs/cgroup/memory.max')
                
                if current and max_mem and max_mem != 'max':
                    used = int(current)
                    limit = int(max_mem)
                    percent = int((used / limit * 100)) if limit > 0 else 0
                    return {
                        'used_bytes': used,
                        'used_mb': used // (1024 * 1024),
                        'limit_bytes': limit,
                        'limit_mb': limit // (1024 * 1024),
                        'percent': percent
                    }
            else:
                # cgroup v1
                usage = self._read_file('/sys/fs/cgroup/memory/memory.usage_in_bytes')
                limit = self._read_file('/sys/fs/cgroup/memory/memory.limit_in_bytes')
                
                if usage and limit:
                    used = int(usage)
                    lim = int(limit)
                    # Check for "unlimited" (very large number)
                    if lim > 10**15:
                        lim = self._get_host_memory()
                    percent = int((used / lim * 100)) if lim > 0 else 0
                    return {
                        'used_bytes': used,
                        'used_mb': used // (1024 * 1024),
                        'limit_bytes': lim,
                        'limit_mb': lim // (1024 * 1024),
                        'percent': percent
                    }
        except Exception as e:
            logger.debug("Memory stats error: %s", str(e))
        
        return None
    
    def _get_host_memory(self):
        """Get total host memory from /proc/meminfo"""
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        # Value is in kB
                        kb = int(line.split()[1])
                        return kb * 1024
        except:
            pass
        return 0
    
    def get_cpu_stats(self):
        """
        Get container CPU usage
        Note: This is a point-in-time snapshot, not a percentage
        For accurate CPU %, need to calculate delta between two readings
        """
        try:
            if self.cgroup_v2:
                stat = self._read_file('/sys/fs/cgroup/cpu.stat')
                if stat:
                    for line in stat.split('\n'):
                        if line.startswith('usage_usec'):
                            return {'usage_usec': int(line.split()[1])}
            else:
                usage = self._read_file('/sys/fs/cgroup/cpu/cpuacct.usage')
                if usage:
                    return {'usage_ns': int(usage)}
        except Exception as e:
            logger.debug("CPU stats error: %s", str(e))
        
        return None
    
    def get_network_stats(self):
        """Get container network stats from /proc/net/dev"""
        try:
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()
            
            rx_bytes = 0
            tx_bytes = 0
            
            for line in lines[2:]:  # Skip header lines
                parts = line.split()
                if len(parts) >= 10:
                    iface = parts[0].rstrip(':')
                    # Skip loopback
                    if iface != 'lo':
                        rx_bytes += int(parts[1])
                        tx_bytes += int(parts[9])
            
            return {
                'rx_bytes': rx_bytes,
                'rx_mb': rx_bytes // (1024 * 1024),
                'tx_bytes': tx_bytes,
                'tx_mb': tx_bytes // (1024 * 1024)
            }
        except Exception as e:
            logger.debug("Network stats error: %s", str(e))
        
        return None
    
    def get_all_stats(self):
        """Get all available container stats"""
        return {
            'memory': self.get_memory_stats(),
            'cpu': self.get_cpu_stats(),
            'network': self.get_network_stats()
        }


# Singleton instance
_stats = None

def get_container_stats():
    """Get container stats singleton"""
    global _stats
    if _stats is None:
        _stats = ContainerStats()
    return _stats
