import random

def supplier_failure_disruption(config,states):
    if config['disruptions']['enabled']:
        disruptions_config = config['disruptions']['supplier_failure']
        for sid in config['suppliers'].keys():
            s_state = states[sid]
            if s_state.disrupted:
                s_state.disruption_remaining -= 1
                if s_state.disruption_remaining <= 0:
                    s_state.disrupted = False
                    s_state.disruption_remaining = 0
            else:
                if random.random() < disruptions_config['probability']:
                    s_state.disrupted = True
                    s_state.disruption_count += 1
                    s_state.disruption_remaining     = random.randint(disruptions_config['duration_min'], disruptions_config['duration_max'])
                
            
def transport_disruption(config,routestates,route_lookup):
    if config['disruptions']['enabled']:
        disruptions_config = config['disruptions']['transport_disruption']
        for route_id in route_lookup.keys():
            route_state = routestates[route_id]
            if route_state.disrupted:
                route_state.disruption_remaining -= 1
                if route_state.disruption_remaining <= 0:
                    route_state.disrupted = False
                    route_state.disruption_remaining = 0
            else:
                if random.random() < disruptions_config['probability']:
                    route_state.disrupted = True
                    route_state.disruption_count += 1
                    route_state.disruption_remaining = random.randint(disruptions_config['duration_min'], disruptions_config['duration_max'])
                
                
def supplier_fail_check(supplier_id,states):
    return states[supplier_id].disrupted

def transport_disrupt_check(route_id,routestates):
    return routestates[route_id].disrupted  

def check_warehouse_overload(w_state, config):
    threshold = config['disruptions']['warehouse_overload']['threshold']
    utilisation = w_state.inventory / w_state.capacity
    return utilisation >= threshold

def effective_process_rate(warehouse_id,w_state,config):
    w_config = config['warehouses'][warehouse_id]
    processing_rate = w_config['processing_rate']
    if check_warehouse_overload(w_state, config):
        overload_config = config['disruptions']['warehouse_overload']
        processing_rate *= overload_config['slowdown_factor']
    return processing_rate