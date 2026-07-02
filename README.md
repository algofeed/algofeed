# ALGOFEED – Minimal Humanitarian Routing Prototype

ALGOFEED is an early-stage, open-source humanitarian logistics project for food aid redistribution.

This repository currently contains a minimal proof-of-concept demonstrating the core idea:

- match surplus food donations with beneficiary locations,
- prioritize urgent needs,
- consider food expiry time,
- respect volunteer vehicle capacity,
- reduce unnecessary travel distance.

This is not yet a full production system. It is a transparent prototype showing the first version of the optimization logic.

## Demo

```bash
pip install -r requirements.txt
python examples/run_demo.py
```

## What the prototype does

The demo loads sample donors and beneficiaries, calculates a humanitarian priority score for possible deliveries, and suggests an initial delivery plan.

The score considers:

- distance between donor and beneficiary,
- urgency of beneficiary need,
- expiry time of the food,
- available quantity,
- vehicle capacity.

## Project direction

Next development steps:

1. Multi-stop route optimization
2. Real-time volunteer availability
3. Food category matching
4. Time-window constraints
5. API endpoint for NGOs and municipalities
6. GDPR-compliant data handling
7. Web dashboard for dispatchers

## License

AGPL-3.0
