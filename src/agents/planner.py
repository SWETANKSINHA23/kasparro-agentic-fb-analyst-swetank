from typing import Dict, Any, List, Optional

class PlannerAgent:
    def __init__(self, config: Dict):
        self.cfg = config

    def create_plan(self, q: str, context: Optional[Dict] = None) -> Dict:
        # basic plan structure
        plan = {
            'original_query': q,
            'reasoning': "Standard analysis flow.",
            'tasks': []
        }
        
        q_lower = q.lower()
        
        # always start with data aggregation
        plan['tasks'].append({
            'step': 1,
            'description': "Aggregate data",
            'tool': "DataAgent.get_window_aggregates"
        })
        
        # figure out what metrics to look at
        metrics = ['spend', 'roas', 'cpa', 'ctr']
        relevant = [m for m in metrics if m in q_lower] or ['roas', 'spend']
            
        plan['tasks'].append({
            'step': 2,
            'description': f"Analyze trends for: {', '.join(relevant)}",
            'required_metrics': relevant
        })
        
        # if they ask why, we need deep dive
        if 'why' in q_lower or 'reason' in q_lower:
            plan['tasks'].append({
                'step': 3,
                'description': "Generate hypotheses",
                'tool': "InsightAgent.analyze"
            })
            
        return plan
