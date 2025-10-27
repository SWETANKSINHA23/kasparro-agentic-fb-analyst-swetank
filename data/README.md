# Facebook Ads Data

## Dataset Information

**File:** `synthetic_fb_ads_undergarments.csv`  
**Size:** ~811 KB  
**Rows:** ~5,000 records  
**Date Range:** 2024 data

## Data Schema

| Column | Type | Description |
|--------|------|-------------|
| date | Date | Campaign run date |
| campaign_name | String | Name of the Facebook Ads campaign |
| adset_name | String | Adset identifier |
| creative_message | String | Ad copy text |
| spend | Float | Amount spent ($) |
| impressions | Integer | Number of ad impressions |
| clicks | Integer | Number of clicks |
| purchases | Integer | Number of conversions/purchases |
| revenue | Float | Revenue generated ($) |
| ctr | Float | Click-through rate (clicks/impressions) |

## Derived Metrics (Calculated by DataAgent)

- **ROAS** (Return on Ad Spend): revenue / spend
- **CPM** (Cost Per Mille): (spend / impressions) * 1000
- **CPC** (Cost Per Click): spend / clicks
- **CPA** (Cost Per Acquisition): spend / purchases

## Data Source

This is **synthetic data** generated for the Kasparro assignment. It simulates a Facebook Ads campaign for an undergarments e-commerce business.

## Usage

The data is automatically loaded by the DataAgent when you run:

```bash
python src/run.py "Your analysis query"
```

No manual data loading required!

## Data Quality

- ✅ No missing values in core metrics
- ✅ Consistent date formatting (YYYY-MM-DD)
- ✅ Realistic metric distributions
- ✅ Campaign names categorized by product type
- ✅ Safe for reproducible testing (deterministic)

## Configuration

To use a different dataset, update `config/config.yaml`:

```yaml
data:
  csv_path: "data/your_data.csv"
```

## Sample Records

```csv
date,campaign_name,spend,revenue,roas
2024-01-15,Winter_Promo_Bras,125.50,385.20,3.07
2024-01-15,Comfort_Boxers_Sale,89.30,267.90,3.00
2024-01-16,Premium_Lingerie,210.75,420.15,1.99
```

## Privacy & Compliance

- No real customer data
- No PII (Personally Identifiable Information)
- Generated for educational purposes
- GDPR/CCPA compliant (synthetic)

<!-- updated -->

<!-- updated -->
