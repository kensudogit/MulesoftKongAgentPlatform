# Cost / chargeback model (configurable placeholders)

## Billable event fields
timestamp, API, agent, owner department, request count, latency, response status, gateway/integration tier, optional model token counts.

## Formula
```
request_cost =
  kong_unit_cost
  + mulesoft_unit_cost
  + backend_unit_cost
  + model_input_tokens * input_token_rate
  + model_output_tokens * output_token_rate
```
Include only applicable components. Separate fixed licensing from variable usage to avoid double-counting.

## Demo defaults (illustrative only)
| Component | Placeholder USD |
|-----------|-----------------|
| kong_unit_cost | 0.0001 |
| mulesoft_unit_cost | 0.0005 |
| backend_unit_cost | 0.001 (sample POST default) |
| token rates | unset until LLM APIs are in inventory |

## Forecast
```
forecast_month = observed_daily_cost * remaining_days + month_to_date_actual + allocated_fixed_cost
```
Label low-confidence when sparse; use 7/30-day scenarios. Currency: USD placeholder; tax/FX TBD.

## Controls
- Per-agent daily quota
- Department budget soft alert / hard stop (exclude critical APIs unless approved)
- Anomaly alerts vs trailing baseline
- Monthly reconciliation against vendor invoices
