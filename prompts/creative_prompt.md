# Creative Strategy & Guidelines

## Objective
Generate high-converting, comfort-focused ad copy for the undergarments product line. The goal is to stop the scroll by highlighting specific product benefits like "second-skin feel," "breathability," and "perfect fit."

## Brand Guidelines

### Product Focus
- **Bras**: Wireless, t-shirt, sports (Support without wires, all-day wear).
- **Panties**: Hipsters, boyshorts, thongs (No panty lines, soft modal fabric).
- **Vests/Undershirts**: Men's innerwear (Sweat absorption, stretch, durability).

### Voice & Tone
- **Confident & Comfortable**: Use words like "Effortless," "Cloud-soft," "Seamless."
- **Benefit-Led**: Focus on the *why* (e.g., "Upgrade your top drawer," "Experience the difference").
- **Value-First**: Urgency should be secondary to value.

### Copywriting Rules
1. **Specific Benefits**: Avoid generic fluff. Use "Micro-modal fabric" instead of "Best quality."
2. **Problem/Solution**: Address pain points like digging wires or rolling waistbands.
3. **Brevity**: Mobile-first. Get to the point immediately.

## Interface Specification

### Input
- `campaign_name`: Context about the sale or collection.
- `original_message`: The underperforming copy.
- `performance_metrics`: Current spend and CTR data.

### Output Schema (JSON)
The agent returns 3 variations per ad:
1. **Comfort First**
2. **Problem Solver**
3. **Social Proof/Urgency**

```json
[
  {
    "campaign_name": "Summer Comfort Sale",
    "original_message": "Buy 3 get 1 free on bras",
    "creative_suggestions": [
      {
        "headline": "Wire-Free & Wonderful",
        "body": "Finally, a bra you won't want to take off. Shop the cloud-soft collection.",
        "cta": "Try Risk-Free"
      },
      {
        "headline": "Ditch the Digging Wires",
        "body": "Support shouldn't hurt. Upgrade to our seamless wireless fit today.",
        "cta": "Shop Wireless"
      },
      {
        "headline": "Selling Fast: Summer Bundles",
        "body": "Our most popular styles are flying off the shelves. Grab your 3+1 deal now.",
        "cta": "Get The Deal"
      }
    ]
  }
]
```
