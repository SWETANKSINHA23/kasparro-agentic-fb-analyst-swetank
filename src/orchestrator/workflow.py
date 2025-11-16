import argparse
import json
import os
import sys
import traceback
import yaml
from datetime import datetime, timedelta
import pandas as pd

# Add root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.agents.data_agent import DataAgent
from src.agents.planner import PlannerAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.creative_generator import CreativeGenerator

from src.utils.helpers import (
    NumpyEncoder, 
    format_markdown_report, 
    should_generate_creatives
)
from src.utils.loader import ensure_reports_directory

def load_config(path):
    if not os.path.isabs(path):
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(base, path)
        
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(description='Facebook Ads Analysis System')
    parser.add_argument('query', type=str, help='Analysis query')
    parser.add_argument('--config', type=str, default='config/config.yaml', help='Config file path')
    parser.add_argument('--days-back', type=int, default=7, help='Lookback days')
    parser.add_argument('--no-creatives', action='store_true', help='Skip creatives')
    
    args = parser.parse_args()
    
    try:
        # Setup
        ensure_reports_directory()
        cfg = load_config(args.config)
        
        # Initialize Agents
        print("\nInitializing Agents...")
        planner = PlannerAgent(cfg)
        data_agent = DataAgent(cfg)
        insight_agent = InsightAgent(cfg)
        evaluator = EvaluatorAgent(data_agent, cfg)
        creative_gen = CreativeGenerator(data_agent, cfg)
        
        # 1. Plan
        print(f"\nPlanning analysis for: '{args.query}'")
        plan = planner.create_plan(args.query)
        print(f"   Reasoning: {plan['reasoning']}")
        
        # 2. Data
        print("\nLoading and aggregating data...")
        data_info = data_agent.get_data_info()
        end_date = pd.to_datetime(data_info['date_range']['end'])
        start_date = end_date - timedelta(days=args.days_back)
        prev_start = start_date - timedelta(days=args.days_back)
        
        print(f"   Analysis Window: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # 3. Insights
        print("\nGenerating insights...")
        insights = insight_agent.analyze(
            data_agent,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            prev_start.strftime('%Y-%m-%d'),
            start_date.strftime('%Y-%m-%d')
        )
        
        # 4. Evaluation
        print("\nValidating hypotheses...")
        validated_hypotheses = []
        for h in insights.get('hypotheses', []):
            eval_result = evaluator.evaluate_hypothesis(
                h['hypothesis'],
                insights['recent_window'],
                insights['previous_window']
            )
            if eval_result['validated']:
                validated_hypotheses.append(eval_result)
                print(f"   - Confirmed: {h['hypothesis']} (Conf: {eval_result['confidence']:.2f})")
            else:
                print(f"   - Rejected: {h['hypothesis']} (Conf: {eval_result['confidence']:.2f})")
        
        # 5. Creatives
        creative_recs = []
        if not args.no_creatives and should_generate_creatives(validated_hypotheses):
            print("\nGenerating creative recommendations...")
            creative_recs = creative_gen.generate_creatives(
                insights['recent_window'],
                validated_hypotheses
            )
            print(f"   Generated {len(creative_recs)} recommendations")
            
        # 6. Report
        print("\nCompiling final report...")
        
        # Save JSONs
        with open('reports/insights.json', 'w') as f:
            json.dump(validated_hypotheses, f, indent=2, cls=NumpyEncoder)
            
        with open('reports/creatives.json', 'w') as f:
            json.dump(creative_recs, f, indent=2, cls=NumpyEncoder)
            
        # Generate Markdown
        report_content = format_markdown_report(
            args.query,
            plan,
            data_info,
            insights,
            validated_hypotheses,
            creative_recs,
            cfg
        )
        
        with open('reports/report.md', 'w') as f:
            f.write(report_content)
            
        print(f"\nAnalysis Complete! Reports saved to reports/")
        
    except Exception as e:
        print(f"\nError during execution: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

# TODO: check this

# note: important

# temporary fix

# optimized

# temporary fix

# refactor later
