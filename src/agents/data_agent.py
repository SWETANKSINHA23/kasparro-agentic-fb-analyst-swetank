import pandas as pd
import os
from typing import Dict, Any

from src.utils.retry import retry
from src.utils.schema import validate_schema

class DataAgent:
    def __init__(self, config: Dict):
        self.cfg = config
        self.df = None
        self._load_data()

    def _load_data(self):
        # default to sample data if not specified
        path = self.cfg.get('data', {}).get('csv_path', 'data/synthetic_fb_ads_undergarments.csv')
        
        if not os.path.isabs(path):
            base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            path = os.path.join(base, path)

        print(f"Loading data from {path}")
        try:
            self.df = retry(pd.read_csv, args=(path,), retries=3)
            print(f"Loaded {len(self.df)} rows")
            
            validate_schema(self.df.columns)
            
            if 'date' in self.df.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                
            # handle sampling for dev/test
            mode = self.cfg.get('data', {}).get('sample_mode')
            
            if mode is True or mode == 'head_1000':
                self.df = self.df.head(1000)
            elif mode == 'random_1000':
                self.df = self.df.sample(n=1000, random_state=42)
                
        except Exception as e:
            # fallback to empty df on error
            print(f"Error reading CSV: {e}")
            self.df = pd.DataFrame()

    def get_data(self) -> pd.DataFrame:
        return self.df

    def filter_by_date_range(self, start, end):
        if self.df is None or self.df.empty:
            return pd.DataFrame()
        mask = (self.df['date'] >= start) & (self.df['date'] <= end)
        return self.df.loc[mask]

    def get_window_aggregates(self, start, end) -> Dict[str, float]:
        sub = self.filter_by_date_range(start, end)
        
        if sub.empty: return {}

        # sum up the basics
        aggs = {
            'spend': float(sub['spend'].sum()),
            'impressions': int(sub['impressions'].sum()),
            'clicks': int(sub['clicks'].sum()),
            'purchases': int(sub['purchases'].sum()),
            'revenue': float(sub['revenue'].sum())
        }
        
        # derived metrics
        aggs['ctr'] = aggs['clicks'] / aggs['impressions'] if aggs['impressions'] > 0 else 0.0
        aggs['cpc'] = aggs['spend'] / aggs['clicks'] if aggs['clicks'] > 0 else 0.0
        aggs['roas'] = aggs['revenue'] / aggs['spend'] if aggs['spend'] > 0 else 0.0
        aggs['cpa'] = aggs['spend'] / aggs['purchases'] if aggs['purchases'] > 0 else 0.0
        
        return aggs

    def calculate_percent_changes(self, curr: Dict, prev: Dict) -> Dict[str, float]:
        changes = {}
        for k, v1 in curr.items():
            if k in prev:
                v0 = prev[k]
                if v0 == 0:
                    changes[f'{k}_change'] = 0.0 if v1 == 0 else 1.0
                else:
                    changes[f'{k}_change'] = (v1 - v0) / v0
        return changes

    def get_data_info(self):
        if self.df is None or self.df.empty:
            return {'rows': 0, 'date_range': {'start': None, 'end': None}, 'unique_campaigns': 0}
            
        return {
            'rows': len(self.df),
            'date_range': {
                'start': self.df['date'].min().strftime('%Y-%m-%d'),
                'end': self.df['date'].max().strftime('%Y-%m-%d')
            },
            'unique_campaigns': self.df['campaign_name'].nunique()
        }

    def get_summary_stats(self) -> Dict:
        if self.df is None or self.df.empty: return {}
        
        spend = self.df['spend'].sum()
        rev = self.df['revenue'].sum()
        
        return {
            'total_spend': float(spend),
            'total_revenue': float(rev),
            'total_roas': float(rev / spend) if spend > 0 else 0,
            'total_impressions': int(self.df['impressions'].sum()),
            'total_clicks': int(self.df['clicks'].sum()),
            'total_purchases': int(self.df['purchases'].sum()),
            'average_ctr': float(self.df['ctr'].mean())
        }








