import re
import pandas as pd
from typing import Dict, Any, List

class CreativeGenerator:
    def __init__(self, data_agent, config: Dict):
        self.data_agent = data_agent
        self.cfg = config
        
        self.templates = [
            {"prefix": "", "suffix": " - Limited Time!"},
            {"prefix": "New: ", "suffix": ""},
            {"prefix": "Don't Miss: ", "suffix": " - Act Now"},
            {"prefix": "Hot Deal: ", "suffix": ""},
            {"prefix": "Exclusive Offer: ", "suffix": ""},
        ]
        
        self.action_words = ["Discover", "Unlock", "Get", "Grab", "Save", "Shop", "Upgrade", "Try"]
        self.power_words = ["Amazing", "Incredible", "Exclusive", "Premium", "Limited", "Special"]

    def generate_creatives(self, min_spend=500.0, max_ctr=0.015, min_samples=5) -> List[Dict]:
        df = self.data_agent.get_data()
        
        if df is None or df.empty:
            return []
        
        bad_ads = self._find_underperformers(df, min_spend, max_ctr, min_samples)
        
        if bad_ads.empty:
            print("No ads found to optimize.")
            return []
        
        recs = []
        for _, row in bad_ads.iterrows():
            msg = row.get('creative_message', '')
            campaign = row.get('campaign_name', 'Unknown')
            
            if not msg: continue
            
            variations = self._make_variations(msg)
            
            recs.append({
                'campaign_name': campaign,
                'adset_name': row.get('adset_name', ''),
                'original_message': msg,
                'recommended_messages': variations,
                'performance_metrics': {
                    'total_spend': row.get('total_spend', 0),
                    'average_ctr': row.get('average_ctr', 0),
                    'total_impressions': row.get('total_impressions', 0)
                }
            })
        
        return recs

    def _find_underperformers(self, df, min_spend, max_ctr, min_samples):
        if 'creative_message' not in df.columns:
            return pd.DataFrame()
        
        stats = df.groupby(['campaign_name', 'creative_message']).agg({
            'spend': 'sum',
            'impressions': 'sum',
            'clicks': 'sum',
            'ctr': 'mean'
        }).reset_index()
        
        stats.columns = ['campaign_name', 'creative_message', 'total_spend', 
                        'total_impressions', 'total_clicks', 'average_ctr']
        
        stats['sample_count'] = df.groupby(['campaign_name', 'creative_message']).size().values
        
        mask = (stats['total_spend'] >= min_spend) & \
               (stats['average_ctr'] <= max_ctr) & \
               (stats['sample_count'] >= min_samples)
               
        return stats[mask].sort_values('total_spend', ascending=False).head(10)

    def _make_variations(self, msg):
        variations = []
        keywords = self._get_keywords(msg)
        
        t = self.templates[0]
        variations.append(f"{t['prefix']}{msg.strip()}{t['suffix']}")
        
        pw = self.power_words[len(msg) % len(self.power_words)]
        if keywords:
            variations.append(f"{pw} {keywords[0].capitalize()} - {msg}")
        else:
            variations.append(f"{pw} Deal: {msg}")
            
        aw = self.action_words[len(msg) % len(self.action_words)]
        if keywords:
            variations.append(f"{aw} {keywords[0].capitalize()} Today! {msg.split('.')[0]}.")
        else:
            variations.append(f"{aw} This Offer - {msg}")
            
        return variations

    def _get_keywords(self, msg):
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'are'}
        tokens = re.findall(r'\b[a-zA-Z]+\b', msg.lower())
        return [w for w in tokens if len(w) > 3 and w not in stopwords][:5]

# note: important

# temporary fix

# note: important
