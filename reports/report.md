# Facebook Ads Agentic Analysis Report

Generated: 2025-11-30 06:04 UTC

## Quick summary

Top validated insights:

- ROAS dropped significantly. - Confirmed ROAS drop of 13.5% (confidence: 0.800)


## Validated Insights (full)

### ROAS dropped significantly.

- Evidence: Confirmed ROAS drop of 13.5%; Revenue also declined.

- Confidence: 0.800

- Validated: True



## Creative Recommendations


Rationale:

Derived headlines from creative message keywords. Focused on benefit. CTR observed used to decide CTA urgency.


## Config snapshot

```json
{
  "project": {
    "name": "Kasparro Agentic FB Analyst",
    "version": "1.0.0"
  },
  "data": {
    "csv_path": "data/synthetic_fb_ads_undergarments.csv",
    "sample_mode": true
  },
  "thresholds": {
    "confidence_min": 0.6,
    "min_confidence": 0.65,
    "min_support": 0.12,
    "roas_drop_pct": 10.0,
    "ctr_drop_pct": 10.0,
    "cpm_rise_pct": 10.0,
    "spend_change_pct": 15.0
  },
  "analysis": {
    "default_days_back": 7,
    "min_data_points": 5
  },
  "outputs": {
    "reports_dir": "reports",
    "save_json": true,
    "save_markdown": true
  },
  "runtime": {
    "log_level": "INFO",
    "random_seed": 42,
    "python": "3.10"
  },
  "agents": {
    "max_iterations": 8,
    "timeout_seconds": 240
  }
}
```

<!-- updated -->

<!-- updated -->

<!-- updated -->

<!-- updated -->

<!-- updated -->

<!-- updated -->

<!-- updated -->
