#!/usr/bin/env python3
"""
Discovery - Tasks Group - ALLE ENTITIES
"""

from .base import DiscoveryBase


class TasksDiscovery(DiscoveryBase):
    """Tasks group - ALLE Entities"""
    
    GROUP_NAME = 'tasks'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registered_tasks = set()
    
    def register_all(self):
        """Register ALLE task entities"""
        
        # =====================================================================
        # GET /ScheduledTasks - Task List
        # =====================================================================
        self.sensor("tasks_count", "Scheduled Tasks Count", "tasks/count", "mdi:calendar-check")
        self.sensor("tasks_running_count", "Running Tasks Count", "tasks/running_count", "mdi:run")
        self.sensor("tasks_idle_count", "Idle Tasks Count", "tasks/idle_count", "mdi:sleep")
        self.sensor("tasks_list", "Tasks List", "tasks/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # GET /ScheduledTasks/Running - Running Tasks
        # =====================================================================
        self.sensor("running_tasks_list", "Running Tasks List", "tasks/running/list", "mdi:format-list-bulleted")
        
        # =====================================================================
        # Common Task Buttons (by key)
        # =====================================================================
        self.button("task_refresh_library", "Task: Refresh Library", "tasks/command/key", "RefreshLibrary", "mdi:magnify-scan")
        self.button("task_refresh_chapter_images", "Task: Refresh Chapter Images", "tasks/command/key", "RefreshChapterImages", "mdi:image-multiple")
        self.button("task_refresh_people", "Task: Refresh People", "tasks/command/key", "RefreshPeople", "mdi:account-sync")
        self.button("task_clean_cache", "Task: Clean Cache", "tasks/command/key", "DeleteCache", "mdi:broom")
        self.button("task_clean_transcode", "Task: Clean Transcode", "tasks/command/key", "DeleteTranscode", "mdi:folder-remove")
        self.button("task_optimize_database", "Task: Optimize Database", "tasks/command/key", "OptimizeDatabase", "mdi:database-cog")
        self.button("task_update_plugins", "Task: Update Plugins", "tasks/command/key", "PluginsUpdate", "mdi:puzzle")
        self.button("task_refresh_guide", "Task: Refresh Guide", "tasks/command/key", "RefreshGuide", "mdi:television-guide")
        self.button("task_refresh_channels", "Task: Refresh Channels", "tasks/command/key", "RefreshChannels", "mdi:television")
        self.button("task_cleanup_collections", "Task: Cleanup Collections", "tasks/command/key", "RefreshBoxSets", "mdi:folder-star")
        
        return self.entity_count
    
    def register_task(self, task_id, task_name, task_key, task_description=None, category=None):
        """Register ALLE Entities für einen spezifischen Task"""
        if task_id in self.registered_tasks:
            return 0
        
        safe_name = task_name.replace(" ", "_").replace("/", "_").replace(":", "").lower()[:30]
        prefix = f"task_{safe_name}"
        base_topic = f"tasks/{task_id}"
        
        # =====================================================================
        # Task Basic Info
        # =====================================================================
        self.sensor(f"{prefix}_name", f"Task: {task_name}", f"{base_topic}/Name", "mdi:cog")
        self.sensor(f"{prefix}_id", f"{task_name} ID", f"{base_topic}/Id", "mdi:identifier")
        self.sensor(f"{prefix}_key", f"{task_name} Key", f"{base_topic}/Key", "mdi:key")
        self.sensor(f"{prefix}_description", f"{task_name} Description", f"{base_topic}/Description", "mdi:text")
        self.sensor(f"{prefix}_category", f"{task_name} Category", f"{base_topic}/Category", "mdi:tag")
        
        # =====================================================================
        # Task State
        # =====================================================================
        self.sensor(f"{prefix}_state", f"{task_name} State", f"{base_topic}/State", "mdi:progress-check")
        self.binary_sensor(f"{prefix}_is_running", f"{task_name} Is Running", f"{base_topic}/is_running", "mdi:run")
        self.binary_sensor(f"{prefix}_is_hidden", f"{task_name} Is Hidden", f"{base_topic}/IsHidden", "mdi:eye-off")
        self.sensor(f"{prefix}_current_progress", f"{task_name} Progress", f"{base_topic}/CurrentProgressPercentage", "mdi:percent", unit="%")
        
        # =====================================================================
        # Task Triggers
        # =====================================================================
        self.sensor(f"{prefix}_triggers_count", f"{task_name} Triggers Count", f"{base_topic}/Triggers/count", "mdi:timer")
        self.sensor(f"{prefix}_triggers", f"{task_name} Triggers", f"{base_topic}/Triggers", "mdi:timer")
        
        # Trigger 0 (first trigger)
        self.sensor(f"{prefix}_trigger_type", f"{task_name} Trigger Type", f"{base_topic}/Triggers/0/Type", "mdi:timer")
        self.sensor(f"{prefix}_trigger_interval", f"{task_name} Trigger Interval", f"{base_topic}/Triggers/0/IntervalTicks", "mdi:timer")
        self.sensor(f"{prefix}_trigger_time_of_day", f"{task_name} Trigger Time", f"{base_topic}/Triggers/0/TimeOfDayTicks", "mdi:clock")
        self.sensor(f"{prefix}_trigger_day_of_week", f"{task_name} Trigger Day", f"{base_topic}/Triggers/0/DayOfWeek", "mdi:calendar")
        self.sensor(f"{prefix}_trigger_max_runtime", f"{task_name} Max Runtime", f"{base_topic}/Triggers/0/MaxRuntimeTicks", "mdi:timer-outline")
        
        # =====================================================================
        # Last Execution Result
        # =====================================================================
        self.sensor(f"{prefix}_last_execution_status", f"{task_name} Last Status", f"{base_topic}/LastExecutionResult/Status", "mdi:check-circle")
        self.sensor(f"{prefix}_last_execution_start", f"{task_name} Last Start", f"{base_topic}/LastExecutionResult/StartTimeUtc", "mdi:clock-start")
        self.sensor(f"{prefix}_last_execution_end", f"{task_name} Last End", f"{base_topic}/LastExecutionResult/EndTimeUtc", "mdi:clock-end")
        self.sensor(f"{prefix}_last_execution_name", f"{task_name} Last Name", f"{base_topic}/LastExecutionResult/Name", "mdi:text")
        self.sensor(f"{prefix}_last_execution_key", f"{task_name} Last Key", f"{base_topic}/LastExecutionResult/Key", "mdi:key")
        self.sensor(f"{prefix}_last_execution_id", f"{task_name} Last ID", f"{base_topic}/LastExecutionResult/Id", "mdi:identifier")
        self.sensor(f"{prefix}_last_execution_error", f"{task_name} Last Error", f"{base_topic}/LastExecutionResult/ErrorMessage", "mdi:alert")
        self.sensor(f"{prefix}_last_execution_long_error", f"{task_name} Last Long Error", f"{base_topic}/LastExecutionResult/LongErrorMessage", "mdi:alert-circle")
        
        # =====================================================================
        # Task Control Buttons
        # =====================================================================
        self.button(f"{prefix}_start", f"Start: {task_name}", f"{base_topic}/command", "start", "mdi:play")
        self.button(f"{prefix}_stop", f"Stop: {task_name}", f"{base_topic}/command", "stop", "mdi:stop")
        
        self.registered_tasks.add(task_id)
        return self.entity_count
