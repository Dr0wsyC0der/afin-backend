import simpy
from typing import Dict, Any
import time

def run_simulation(model_data: Dict[str, Any]) -> Dict[str, Any]:
    env = simpy.Environment()
    start_time = time.time()

    # Пример: симуляция по элементам BPMN
    elements = model_data.get("elements", [])
    tasks = [e for e in elements if e["type"] == "task"]

    def task_process(env, task):
        duration = float(task.get("duration", 1))  # можно из атрибутов
        yield env.timeout(duration)

    for task in tasks:
        env.process(task_process(env, task))

    env.run()
    total_time = time.time() - start_time

    return {
        "completed_tasks": len(tasks),
        "total_simulation_time": total_time,
        "status": "completed"
    }