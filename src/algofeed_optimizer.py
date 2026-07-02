"""
ALGOFEED minimal humanitarian routing prototype.

This file demonstrates a simplified version of the project logic:
donations are matched to beneficiaries using urgency, expiry time,
capacity and distance.

The goal is not to replace a full routing engine yet, but to show
a transparent first version of the optimization logic.
"""

from dataclasses import dataclass
from math import radians, sin, cos, sqrt, atan2
from typing import List, Dict, Any


@dataclass
class Donor:
    id: str
    name: str
    latitude: float
    longitude: float
    food_type: str
    quantity_kg: float
    expiry_hours: float


@dataclass
class Beneficiary:
    id: str
    name: str
    latitude: float
    longitude: float
    needed_food_type: str
    needed_kg: float
    urgency: int  # 1 = low, 5 = critical


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two GPS points in kilometers."""
    earth_radius_km = 6371.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * c


def humanitarian_score(
    distance_km: float,
    urgency: int,
    expiry_hours: float,
    quantity_match_ratio: float,
) -> float:
    """
    Calculate a priority score for a possible delivery.

    Higher score = better match.

    The score rewards:
    - higher beneficiary urgency,
    - shorter expiry time,
    - better quantity match,
    - shorter distance.
    """
    urgency_component = urgency * 3.0
    expiry_component = max(1.0, 48.0 - expiry_hours) * 1.5
    quantity_component = quantity_match_ratio * 5.0
    distance_penalty = max(distance_km, 1.0)

    return (urgency_component + expiry_component + quantity_component) / distance_penalty


def create_delivery_plan(
    donors: List[Donor],
    beneficiaries: List[Beneficiary],
    vehicle_capacity_kg: float = 80.0,
) -> List[Dict[str, Any]]:
    """
    Create a simple ranked delivery plan.

    This prototype does greedy matching:
    it evaluates all donor-beneficiary pairs, ranks them by humanitarian score,
    then selects feasible deliveries while respecting available food quantity,
    beneficiary need and vehicle capacity.
    """
    candidate_routes = []

    for donor in donors:
        for beneficiary in beneficiaries:
            if donor.food_type.lower() != beneficiary.needed_food_type.lower():
                continue

            distance = haversine_km(
                donor.latitude,
                donor.longitude,
                beneficiary.latitude,
                beneficiary.longitude,
            )

            deliverable_kg = min(
                donor.quantity_kg,
                beneficiary.needed_kg,
                vehicle_capacity_kg,
            )

            if deliverable_kg <= 0:
                continue

            quantity_match_ratio = deliverable_kg / max(beneficiary.needed_kg, 1.0)

            score = humanitarian_score(
                distance_km=distance,
                urgency=beneficiary.urgency,
                expiry_hours=donor.expiry_hours,
                quantity_match_ratio=quantity_match_ratio,
            )

            candidate_routes.append(
                {
                    "donor_id": donor.id,
                    "donor_name": donor.name,
                    "beneficiary_id": beneficiary.id,
                    "beneficiary_name": beneficiary.name,
                    "food_type": donor.food_type,
                    "delivery_kg": round(deliverable_kg, 2),
                    "distance_km": round(distance, 2),
                    "expiry_hours": donor.expiry_hours,
                    "urgency": beneficiary.urgency,
                    "score": round(score, 3),
                }
            )

    candidate_routes.sort(key=lambda item: item["score"], reverse=True)
    return candidate_routes
