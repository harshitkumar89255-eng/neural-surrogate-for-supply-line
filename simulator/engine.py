import random
import numpy as np
from simulator.initialize import init_states,init_route_states
from simulator.topology_builder import build_supply_chain_graph
from dataclasses import asdict
from simulator.demand import apply_demand, generate_retailer_demand
from simulator.disruptions import supplier_failure_disruption, transport_disruption
from simulator.production import replenish_supply
from simulator.reorder import check_reorders
from simulator.shipment import advance_shipments, process, update_congestion


class Simulator:
    def __init__(self,config):
        self.config = config
        
        seed = config['simulation'].get('random_seed')
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
            
        self.graph,self.route_lookup = build_supply_chain_graph(self.config)
        self.states = init_states(self.graph)
        self.route_states = init_route_states(self.route_lookup)
        
        self.active_shipments = []
        self.active_demand_spikes = {}
        self.shipment_id = 1
        self.state_history = {}
        self.lost_sales_history = {}
        self.lost_shipments_history = {}

    def reset_tick(self):
        for state in self.states.values():
            state.incoming = 0
            state.outgoing = 0
        
        
    def logs(self,tick):
        self.state_history[tick] = {
            'nodes': {node_id: asdict(state) for node_id,state in self.states.items()},
            'routes': {route_id: asdict(route) for route_id,route in self.route_states.items()},
            'active_shipments':[asdict(shipment) for shipment in self.active_shipments]
        }
        
    def step(self,tick):
        self.reset_tick()
        
        retailer_demand = generate_retailer_demand(self.config,self.active_demand_spikes)
        lost_sales = apply_demand(retailer_demand,self.states,self.config)  #in my code lost sales return a lost dict for lost sales i.e if retailer doesnt have enough items to meet the demand the shortfall will be lost if backlog is not enabled 
        self.shipment_id = check_reorders(self.config,self.states,self.route_lookup,self.route_states,self.active_shipments,self.shipment_id)
        delivered = advance_shipments(self.active_shipments,self.route_lookup)
        lost_shipments = process(delivered,self.states) #process returns lost shipment if in any case more quantity is supplied than the available space
        update_congestion(self.active_shipments,self.route_states,self.route_lookup)
        supplier_failure_disruption(self.config,self.states)
        transport_disruption(self.config,self.route_states,self.route_lookup)
        replenish_supply(self.config,self.states)
        self.lost_sales_history[tick]=lost_sales
        self.lost_shipments_history[tick] = lost_shipments
        self.logs(tick)
        
    def run(self):
        ticks = self.config['simulation']['ticks']
        for tick in range(ticks):
            self.step(tick)
        return {
            'state_history': self.state_history,
            'lost_sales_history': self.lost_sales_history,
            'lost_shipments_history': self.lost_shipments_history
        }