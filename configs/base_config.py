BASE_CONFIG = {

    # ─────────────────────────────────────────
    # SIMULATION CONTROL
    # ─────────────────────────────────────────
    "simulation": {
        "ticks": 100,
        "random_seed": 5,
        "backlog_enabled": False,
        "lost_sales_enabled": True,  #if both true Backlog takes priority
        "warmup_ticks": 10,
    },

    # ─────────────────────────────────────────
    # DISRUPTION PARAMETERS
    # ─────────────────────────────────────────
    "disruptions": {
        "enabled": True,

        "supplier_failure": {
            "probability": 0.05,
            "duration_min": 2,
            "duration_max": 5
        },

        "demand_spike": {
            "probability": 0.05,
            "multiplier_min": 2.0,
            "multiplier_max": 4.0,
            "duration": 3
        },

        "transport_disruption": {
            "probability": 0.05,
            "delay_multiplier": 3.0,
            "duration_min": 1,
            "duration_max": 4
        },

        "warehouse_overload": {
            "threshold": 0.95,
            "slowdown_factor": 0.5
        }
    },

    # ─────────────────────────────────────────
    # SUPPLIERS
    # ─────────────────────────────────────────
    "suppliers": {
        "S1": {
            "inventory": 1000,
            "capacity": 1000,
            "reliability": 0.95,
            "production_rate": 150,
            "holding_cost_per_unit": 0.2
        },
        "S2": {
            "inventory": 1000,
            "capacity": 1000,
            "reliability": 0.90,
            "production_rate": 120,
            "holding_cost_per_unit": 0.2
        }
    },

    # ─────────────────────────────────────────
    # WAREHOUSES
    # ─────────────────────────────────────────
    "warehouses": {
        "W1": {
            "inventory": 300,
            "capacity": 600,
            "reorder_point": 100,
            "reorder_quantity": 300,
            "holding_cost_per_unit": 0.5,
            "processing_rate": 300
        },
        "W2": {
            "inventory": 300,
            "capacity": 600,
            "reorder_point": 100,
            "reorder_quantity": 300,
            "holding_cost_per_unit": 0.5,
            "processing_rate": 300
        }
    },

    # ─────────────────────────────────────────
    # RETAILERS
    # ─────────────────────────────────────────
    "retailers": {
        "R1": {
            "inventory": 200,
            "capacity": 400,
            "demand_mean": 25,
            "demand_std": 5,
            "reorder_point": 50,
            "reorder_quantity": 160,
            "holding_cost_per_unit": 1.0,
            "stockout_penalty_per_unit": 5.0
        },
        "R2": {
            "inventory": 200,
            "capacity": 400,
            "demand_mean": 20,
            "demand_std": 4,
            "reorder_point": 40,
            "reorder_quantity": 150,
            "holding_cost_per_unit": 1.0,
            "stockout_penalty_per_unit": 5.0
        },
        "R3": {
            "inventory": 200,
            "capacity": 400,
            "demand_mean": 30,
            "demand_std": 6,
            "reorder_point": 60,
            "reorder_quantity": 170,
            "holding_cost_per_unit": 1.0,
            "stockout_penalty_per_unit": 5.0
        }
    },

    # ─────────────────────────────────────────
    # ROUTES
    # ─────────────────────────────────────────
    "routes": [

        # primary supplier → warehouse
        {
            "source": "S1", "target": "W1",
            "travel_time": 2,
            "capacity": 400,
            "delay_probability": 0.10,
            "transport_cost": 5,
            "congestion_threshold": 0.75,
            "congestion_delay_multiplier": 2.0,
            "is_primary": True
        },
        {
            "source": "S2", "target": "W2",
            "travel_time": 2,
            "capacity": 400,
            "delay_probability": 0.15,
            "transport_cost": 5,
            "congestion_threshold": 0.75,
            "congestion_delay_multiplier": 2.0,
            "is_primary": True
        },

        # cross routes
        {
            "source": "S1", "target": "W2",
            "travel_time": 3,
            "capacity": 300,
            "delay_probability": 0.12,
            "transport_cost": 8,
            "congestion_threshold": 0.75,
            "congestion_delay_multiplier": 2.0,
            "is_primary": False
        },
        {
            "source": "S2", "target": "W1",
            "travel_time": 3,
            "capacity": 300,
            "delay_probability": 0.12,
            "transport_cost": 8,
            "congestion_threshold": 0.75,
            "congestion_delay_multiplier": 2.0,
            "is_primary": False
        },

        # last mile — warehouse → retailer
        {
            "source": "W1", "target": "R1",
            "travel_time": 1,
            "capacity": 200,
            "delay_probability": 0.05,
            "transport_cost": 2,
            "congestion_threshold": 0.80,
            "congestion_delay_multiplier": 1.5,
            "is_primary": True
        },
        {
            "source": "W1", "target": "R2",
            "travel_time": 1,
            "capacity": 200,
            "delay_probability": 0.05,
            "transport_cost": 2,
            "congestion_threshold": 0.80,
            "congestion_delay_multiplier": 1.5,
            "is_primary": True
        },
        {
            "source": "W2", "target": "R2",
            "travel_time": 1,
            "capacity": 200,
            "delay_probability": 0.08,
            "transport_cost": 3,
            "congestion_threshold": 0.80,
            "congestion_delay_multiplier": 1.5,
            "is_primary": False
        },
        {
            "source": "W2", "target": "R3",
            "travel_time": 1,
            "capacity": 80,
            "delay_probability": 0.08,
            "transport_cost": 2,
            "congestion_threshold": 0.80,
            "congestion_delay_multiplier": 1.5,
            "is_primary": True
        },
        {
            "source": "W1", "target": "R3",
            "travel_time": 2,
            "capacity": 80,
            "delay_probability": 0.10,
            "transport_cost": 4,
            "congestion_threshold": 0.80,
            "congestion_delay_multiplier": 1.5,
            "is_primary": False
        }
    ],

    # ─────────────────────────────────────────
    # METRICS CONFIG
    # ─────────────────────────────────────────
    "metrics": {
        "record_per_tick": True,
        "record_per_run": True,
        "cost_weights": {
            "alpha": 1.0,
            "beta": 1.0,
            "gamma": 2.0
        }
    }
}