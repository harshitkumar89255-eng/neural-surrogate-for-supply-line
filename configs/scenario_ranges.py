SCENARIO_RANGES = {
    "normal": {
        "capacity_std_frac": 0.15,
        "demand_std_frac": 0.15,
        "reorder_std_frac": 0.15,
        "delay_probability_std": 0.03,
        "reliability_std_frac": 0.05,
        "production_rate_std_frac":0.1,
        "processing_rate_std_frac":0.1,
    },
    "stress": {
        "high_demand_multiplier": (1.5, 2.5),
        "low_capacity_multiplier": (0.5, 0.8),
        "low_reliability_range": (0.4, 0.8),
        "high_delay_probability": (0.2, 0.5),
    }
}