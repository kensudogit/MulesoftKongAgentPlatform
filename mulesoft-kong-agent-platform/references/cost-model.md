# Chargeback and forecast

Record each billable request with timestamp, API, agent, owner department, request count, latency, response status, gateway/integration tier and any measured model token counts.

Cost model (configurable):
`request_cost = kong_unit_cost + mulesoft_unit_cost + backend_unit_cost + model_input_tokens * input_token_rate + model_output_tokens * output_token_rate`.
Only include costs applicable to the call. Rates are illustrative placeholders until vendor agreements and actual usage meters are mapped. Separate fixed licensing, capacity charges, and variable API costs to avoid double-counting.

Forecast per department/API/agent:
`forecast_month = observed_daily_cost * remaining_days + month_to_date_actual + allocated_fixed_cost`.
For sparse data, label forecast low-confidence; use trailing 7/30-day scenarios, seasonality and peak multipliers. Record currency, tax treatment and exchange-rate assumption.

Controls: budgets, daily limits, per-agent quotas, anomaly alerts, soft/hard stops (hard stop must exclude critical APIs unless explicitly approved), reconciliation with vendor invoices.
