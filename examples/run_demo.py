import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from algofeed_optimizer import Donor, Beneficiary, create_delivery_plan


def load_donors(path: Path):
    df = pd.read_csv(path)
    return [
        Donor(
            id=row["id"],
            name=row["name"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            food_type=row["food_type"],
            quantity_kg=float(row["quantity_kg"]),
            expiry_hours=float(row["expiry_hours"]),
        )
        for _, row in df.iterrows()
    ]


def load_beneficiaries(path: Path):
    df = pd.read_csv(path)
    return [
        Beneficiary(
            id=row["id"],
            name=row["name"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            needed_food_type=row["needed_food_type"],
            needed_kg=float(row["needed_kg"]),
            urgency=int(row["urgency"]),
        )
        for _, row in df.iterrows()
    ]


if __name__ == "__main__":
    donors = load_donors(ROOT / "data" / "sample_donors.csv")
    beneficiaries = load_beneficiaries(ROOT / "data" / "sample_beneficiaries.csv")

    plan = create_delivery_plan(
        donors=donors,
        beneficiaries=beneficiaries,
        vehicle_capacity_kg=80.0,
    )

    print("\nALGOFEED – Suggested humanitarian delivery plan\n")
    for index, route in enumerate(plan[:10], start=1):
        print(
            f"{index}. {route['donor_name']} -> {route['beneficiary_name']} | "
            f"{route['delivery_kg']} kg {route['food_type']} | "
            f"{route['distance_km']} km | "
            f"urgency: {route['urgency']} | "
            f"expiry: {route['expiry_hours']}h | "
            f"score: {route['score']}"
        )
