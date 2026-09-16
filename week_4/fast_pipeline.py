"""
fast_pipeline.py
Direct function calls - no CrewAI overhead
"""

from agents.researcher import build_researcher
from agents.analyst import build_analyst
from agents.writer import build_writer
from agents.publisher import build_publisher

def run_fast_pipeline(topic: str):
    """Run pipeline without CrewAI overhead"""
    
    # Step 1: Research
    researcher = build_researcher()
    research_result = researcher.execute(f"Research: {topic}")
    
    # Step 2: Analysis
    analyst = build_analyst()
    analysis_result = analyst.execute(f"Analyze: {research_result}")
    
    # Step 3: Writer
    writer = build_writer()
    report = writer.execute(f"Write report on {topic}: {analysis_result}")
    
    # Step 4: Publisher
    publisher = build_publisher()
    published = publisher.execute(f"Publish: {report}")
    
    return {
        "research": research_result,
        "analysis": analysis_result,
        "report": report,
        "published": published,
    }