# Planner Specification

## Objective
Convert user analysis queries into a structured execution plan. The planner interprets the query and breaks it down into sequential tasks that other agents can execute.

## Planning Logic

### Input
- **Query**: User's analysis request (e.g., "Analyze ROAS drop").
- **Context**: Optional metadata about the analysis scope.

### Output Schema
The planner returns a JSON object with:

| Field | Type | Description |
|:---|:---|:---|
| `original_query` | string | The input query verbatim. |
| `reasoning` | string | Brief strategy explanation. |
| `tasks` | list | Ordered list of execution steps. |

### Task Generation Rules
1. **Always start with data aggregation** using `DataAgent.get_window_aggregates`.
2. **Identify relevant metrics** from the query (default: ROAS, Spend).
3. **Add deep dive step** if the query includes "why" or "reason" (triggers `InsightAgent.analyze`).

## Example Output (JSON)
```json
{
  "original_query": "Analyze ROAS drop",
  "reasoning": "Standard analysis flow.",
  "tasks": [
    {
      "step": 1,
      "description": "Aggregate data",
      "tool": "DataAgent.get_window_aggregates"
    },
    {
      "step": 2,
      "description": "Analyze trends for: roas, spend",
      "required_metrics": ["roas", "spend"]
    },
    {
      "step": 3,
      "description": "Generate hypotheses",
      "tool": "InsightAgent.analyze"
    }
  ]
}
```
