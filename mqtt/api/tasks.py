#!/usr/bin/env python3
"""
Jellyfin API - Tasks Group
Endpoints: 5
- Scheduled tasks management
"""

from typing import Optional, Dict, List
from .base import JellyfinAPIBase


class TasksAPI(JellyfinAPIBase):
    """Scheduled Tasks API endpoints"""
    
    GROUP_NAME = 'tasks'
    
    # =========================================================================
    # SCHEDULED TASKS (5 endpoints)
    # =========================================================================
    
    def get_scheduled_tasks(self, is_hidden: bool = None, is_enabled: bool = None) -> Optional[List]:
        """GET /ScheduledTasks - Get scheduled tasks"""
        params = {k: v for k, v in {'isHidden': is_hidden, 'isEnabled': is_enabled}.items() if v is not None}
        return self._get('/ScheduledTasks', params)
    
    def get_scheduled_task(self, task_id: str) -> Optional[Dict]:
        """GET /ScheduledTasks/{taskId} - Get scheduled task"""
        return self._get(f'/ScheduledTasks/{task_id}')
    
    def start_scheduled_task(self, task_id: str) -> bool:
        """POST /ScheduledTasks/Running/{taskId} - Start scheduled task"""
        return self._post(f'/ScheduledTasks/Running/{task_id}') is not None
    
    def stop_scheduled_task(self, task_id: str) -> bool:
        """DELETE /ScheduledTasks/Running/{taskId} - Stop scheduled task"""
        return self._delete(f'/ScheduledTasks/Running/{task_id}') is not None
    
    def update_task_triggers(self, task_id: str, triggers: List[Dict]) -> bool:
        """POST /ScheduledTasks/{taskId}/Triggers - Update task triggers"""
        return self._post(f'/ScheduledTasks/{task_id}/Triggers', json_data=triggers) is not None
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def get_running_tasks(self) -> List[Dict]:
        """Get only running tasks"""
        tasks = self.get_scheduled_tasks()
        if tasks:
            return [t for t in tasks if t.get('State') == 'Running']
        return []
    
    def get_task_by_name(self, name: str) -> Optional[Dict]:
        """Find task by name"""
        tasks = self.get_scheduled_tasks()
        if tasks:
            for task in tasks:
                if task.get('Name') == name or task.get('Key') == name:
                    return task
        return None
    
    def start_task_by_name(self, name: str) -> bool:
        """Start task by name"""
        task = self.get_task_by_name(name)
        if task:
            return self.start_scheduled_task(task.get('Id'))
        return False
