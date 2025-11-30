from typing import Dict, Any, List

class EvaluatorAgent:
    def __init__(self, data_agent, config: Dict):
        self.data_agent = data_agent
        self.cfg = config

    def evaluate_hypothesis(self, hypothesis: str, recent_aggs: Dict, previous_aggs: Dict) -> Dict:
        score = 0.0
        evidence = []
        h_lower = hypothesis.lower()
        
        # check roas
        if 'roas' in h_lower:
            change = self._score_change('roas', recent_aggs, previous_aggs)
            if 'decrease' in h_lower or 'drop' in h_lower:
                if change < 0:
                    score += 0.5
                    evidence.append(f"Confirmed ROAS drop of {abs(change)*100:.1f}%")
                    
                    rev_change = self._score_change('revenue', recent_aggs, previous_aggs)
                    spend_change = self._score_change('spend', recent_aggs, previous_aggs)
                    
                    if rev_change < 0:
                        score += 0.3
                        evidence.append("Revenue also declined.")
                    if spend_change > 0:
                        score += 0.2
                        evidence.append("Spend increased despite lower returns.")
                else:
                    evidence.append("ROAS actually increased or stayed flat.")
            elif 'increase' in h_lower or 'improve' in h_lower:
                if change > 0:
                    score += 0.8
                    evidence.append(f"Confirmed ROAS improvement of {change*100:.1f}%")
                else:
                    evidence.append("ROAS actually decreased.")
            else:
                if abs(change) > 0.05:
                    score += 0.5
                    evidence.append(f"ROAS changed by {change*100:.1f}%")
                else:
                    evidence.append("ROAS remained stable.")
        
        # check ctr/fatigue
        elif 'ctr' in h_lower or 'creative' in h_lower or 'fatigue' in h_lower:
            change = self._score_change('ctr', recent_aggs, previous_aggs)
            if change < -0.05:
                score += 0.8
                evidence.append(f"CTR dropped by {abs(change)*100:.1f}%")
            else:
                evidence.append(f"CTR change was minor ({change*100:.1f}%)")

        else:
            score = 0.5
            evidence.append("Generic validation applied.")

        return {
            'hypothesis': hypothesis,
            'confidence': min(score, 1.0),
            'validated': score > 0.6,
            'evidence': "\n".join(evidence)
        }

    def _score_change(self, metric, current, previous):
        v1 = current.get(metric, 0)
        v0 = previous.get(metric, 0)
        if v0 == 0: return 0.0
        return (v1 - v0) / v0
