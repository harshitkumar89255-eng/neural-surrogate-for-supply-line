import random
import numpy as np


def retailer_demand(retailer_config):
    demand = np.random.normal(retailer_config['demand_mean'], retailer_config['demand_std'])
    return max(0, round(demand))

def demand_spike_disruption(base_demand,disruption_config):
    multiplier = random.uniform(disruption_config['multiplier_min'], disruption_config['multiplier_max'])
    return round(base_demand * multiplier)

def generate_retailer_demand(config,active_demand_spikes):
    retailer_demands = {}
    disruptions_enabled = config['disruptions']['enabled']
    spike_config = config['disruptions']['demand_spike']
    for retailer_id,retailer_data in config['retailers'].items():
        demand = retailer_demand(retailer_data)
        if retailer_id in active_demand_spikes:
            demand = demand_spike_disruption(demand, spike_config)
            active_demand_spikes[retailer_id] -= 1
            if active_demand_spikes[retailer_id] <= 0:
                del active_demand_spikes[retailer_id]
                
        elif disruptions_enabled:
            if random.random() < spike_config['probability']:
                demand = demand_spike_disruption(demand, spike_config)
                active_demand_spikes[retailer_id] = spike_config['duration']-1
        retailer_demands[retailer_id] = demand
                
    return retailer_demands


def apply_demand(retailer_demands, states, config):
    backlog_enabled = config['simulation']['backlog_enabled']
    lost_sales_enabled = config['simulation']['lost_sales_enabled']
    lost_sales = []

    for retailer_id, demand in retailer_demands.items():
        r_state = states[retailer_id]
        if backlog_enabled and r_state.backlog > 0:
            backlog_fill = min(r_state.backlog, r_state.inventory)
            r_state.inventory -= backlog_fill
            r_state.backlog -= backlog_fill
            
        available = r_state.inventory
        if demand <= available:
            r_state.inventory -= demand
        else:
            shortfall = demand - available
            r_state.inventory = 0
            r_state.stockout += 1
            if backlog_enabled:
                r_state.backlog += shortfall
            elif lost_sales_enabled:
                lost = {'retailer_id': retailer_id, 'lost_quantity': shortfall}
                lost_sales.append(lost)
                
    return lost_sales
               