"""
crew_local.py
-------------
Stable sequential pipeline (parallel disabled for reliability)
"""

import os
from crewai import Crew, Process
from tasks import build_tasks
from utils import retry_on_failure

def run_sequential_pipeline(topic, step_callback=None):
    """Run pipeline in sequential mode (most stable)"""
    print("🔄 Running in sequential mode...")
    tasks = build_tasks()
    agents = [t.agent for t in tasks]
    
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )
    
    if step_callback:
        step_callback("research_started")
    
    try:
        result = crew.kickoff(inputs={"topic": topic})
        
        # ✅ FIX: Safer output extraction with error handling
        outputs = {
            "research": "",
            "analysis": "",
            "report": "",
            "published": "",
            "final": "",
        }
        
        # Safely extract each task output
        for i, task in enumerate(tasks):
            try:
                if task.output and hasattr(task.output, 'raw'):
                    if i == 0:
                        outputs["research"] = task.output.raw or ""
                    elif i == 1:
                        outputs["analysis"] = task.output.raw or ""
                    elif i == 2:
                        outputs["report"] = task.output.raw or ""
                    elif i == 3:
                        outputs["published"] = task.output.raw or ""
            except Exception as e:
                print(f"⚠️ Could not extract output from task {i}: {e}")
        
        # Final output
        if result and hasattr(result, 'raw'):
            outputs["final"] = result.raw or ""
        
        print(f"✅ Research: {len(outputs['research'])} chars")
        print(f"✅ Analysis: {len(outputs['analysis'])} chars")
        print(f"✅ Report: {len(outputs['report'])} chars")
        print(f"✅ Published: {len(outputs['published'])} chars")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        outputs = {
            "research": "",
            "analysis": "",
            "report": "",
            "published": "",
            "final": "",
        }
    
    if step_callback:
        step_callback("pipeline_complete")
    
    return outputs

@retry_on_failure(max_attempts=2, delay_seconds=3)
def run_pipeline(topic: str, step_callback=None):
    """Run pipeline with sequential execution (stable)"""
    os.makedirs("output", exist_ok=True)
    
    if step_callback:
        step_callback("research_started")
    
    outputs = run_sequential_pipeline(topic, step_callback)
    
    return outputs