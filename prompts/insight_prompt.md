# Insight Analysis Specification

## Objective
Analyze Facebook Ads performance data to identify the root causes of metric fluctuations. The system compares two time windows (Recent vs. Previous) to generate diagnostic insights explaining *why* performance changed.

## Analysis Logic

### Input Data
- **Performance Data**: Aggregated metrics for the analysis window.
- **Trends**: Percentage changes for key metrics (CTR, CPC, ROAS).
- **Context**: Product category and creative themes.

### Output Schema
The agent produces a list of insight objects. Each object contains:

| Field | Type | Description |
|:---|:---|:---|
| `hypothesis` | string | The main diagnostic claim (e.g., "Creative fatigue detected"). |
| `confidence` | float | Certainty score (0.0 - 1.0) based on metric magnitude. |
| `actionable` | boolean | Whether this insight requires user intervention. |
| `supporting_evidence` | list | Strings citing specific data points (e.g., "CTR down 15%"). |
| `recommendation` | string | (Optional) Suggested next step. |

### Generation Rules
1. **Conciseness**: Insights must be 2-3 sentences max.
2. **Evidence-Based**: Every claim must cite a numeric change.
3. **Diagnostic Focus**: Explain the *cause* (e.g., "High competition"), not just the *symptom* (e.g., "CPM increased").

## Example Output (JSON)
```json
{
  "hypotheses": [
    {
      "hypothesis": "Creative fatigue likely.",
      "confidence": 0.75,
      "actionable": true,
      "supporting_evidence": [
        "CTR down 15.1%"
      ],
      "recommendation": "Refresh creatives."
    }
  ]
}
```



