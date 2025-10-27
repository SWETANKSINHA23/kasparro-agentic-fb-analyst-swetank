import json
from datetime import datetime
from typing import Dict, Any, List
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def should_generate_creatives(hypotheses: List[Dict]) -> bool:
    keywords = [
        'creative', 'ad copy', 'message', 'headline', 
        'ad fatigue', 'underperforming', 'low ctr', 'ctr'
    ]
    
    for h in hypotheses:
        text = h.get('hypothesis', '').lower()
        if any(k in text for k in keywords):
            return True
    return False

def format_markdown_report(
    user_query: str,
    plan: Dict,
    data_summary: Dict,
    insights: Dict,
    validated_hypotheses: List[Dict],
    creatives: List[Dict],
    config: Dict = None
) -> str:
    
    md = f"""# Facebook Ads Agentic Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

## Quick summary

Top validated insights:

"""
    
    for v in validated_hypotheses:
        if v.get('validated'):
            md += f"- {v.get('hypothesis')} - {v.get('evidence').split(chr(10))[0]} (confidence: {v.get('confidence'):.3f})\n\n"
            
    md += """
## Validated Insights (full)

"""
    
    for v in validated_hypotheses:
        md += f"""### {v.get('hypothesis')}

- Evidence: {v.get('evidence').replace(chr(10), '; ')}

- Confidence: {v.get('confidence'):.3f}

- Validated: {v.get('validated')}


"""

    md += """
## Creative Recommendations

"""
    
    count = 1
    for c in creatives:
        for msg in c.get('recommended_messages', []):
            md += f"{count}. {msg}\n\n"
            count += 1
            
    md += """
Rationale:

Derived headlines from creative message keywords. Focused on benefit. CTR observed used to decide CTA urgency.


## Config snapshot

```json
"""
    if config:
        md += json.dumps(config, indent=2)
    else:
        md += "{}"
        
    md += "\n```\n"
    
    return md

# TODO: check this
