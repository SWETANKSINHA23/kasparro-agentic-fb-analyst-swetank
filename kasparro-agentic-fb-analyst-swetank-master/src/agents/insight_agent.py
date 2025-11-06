from typing import Dict, Any, List

class InsightAgent:
    def __init__(self, config: Dict):
        self.cfg = config

    def analyze(self, data_agent, recent_start, recent_end, prev_start, prev_end) -> Dict:
        recent = data_agent.get_window_aggregates(recent_start, recent_end)
        prev = data_agent.get_window_aggregates(prev_start, prev_end)
        
        if not recent or not prev:
            return {'error': "Insufficient data"}

        changes = data_agent.calculate_percent_changes(recent, prev)
        hypotheses = self._generate_hypotheses(changes, recent)
        
        return {
            'recent_window': recent,
            'previous_window': prev,
            'changes': changes,
            'hypotheses': hypotheses,
            'analysis': self._format_analysis(changes),
            'thinking': "Comparing recent vs previous period."
        }

    def _generate_hypotheses(self, changes: Dict, current_metrics: Dict) -> List[Dict]:
        hypotheses = []
        
        roas_chg = changes.get('roas_change', 0)
        if roas_chg < -0.10:
            hypotheses.append({
                'hypothesis': "ROAS dropped significantly.",
                'confidence': 0.85,
                'actionable': True,
                'supporting_evidence': [f"ROAS down {abs(roas_chg)*100:.1f}%"]
            })
            
        ctr_chg = changes.get('ctr_change', 0)
        if ctr_chg < -0.15:
            hypotheses.append({
                'hypothesis': "Creative fatigue likely.",
                'confidence': 0.75,
                'actionable': True,
                'supporting_evidence': [f"CTR down {abs(ctr_chg)*100:.1f}%"],
                'recommendation': "Refresh creatives."
            })
            
        cpm_chg = changes.get('cpm_change', 0)
        if cpm_chg > 0.20:
            hypotheses.append({
                'hypothesis': "High competition (CPM spike).",
                'confidence': 0.60,
                'actionable': False,
                'supporting_evidence': [f"CPM up {cpm_chg*100:.1f}%"]
            })
            
        return hypotheses

    def _format_analysis(self, changes: Dict) -> str:
        lines = []
        for k, v in changes.items():
            metric = k.replace('_change', '').upper()
            direction = "increased" if v > 0 else "decreased"
            lines.append(f"- {metric} {direction} by {abs(v)*100:.1f}%")
        return "\n".join(lines)

# note: important

# note: important

# note: important

# TODO: check this

# refactor later
