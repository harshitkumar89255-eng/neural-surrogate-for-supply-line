import random 
from simulator.entities import Shipment

def select_route(target, route_lookup, r_states, states, source=None):
    candidates = []
    for rid, rd in route_lookup.items():
        r_state = r_states[rid]
        route_source = rd['source']
        source_state = states[route_source]
        if rd['target'] != target:
            continue
        if source is not None and route_source != source:
            continue
        if r_state.disrupted:
            continue
        if source_state.disrupted:
            continue
        if source_state.inventory <= 0:
            continue
        candidates.append((rid, rd))
    if not candidates:
        return None, None
    scored = [score_route(rid, rd, r_states) for rid, rd in candidates]
    return candidates[scored.index(min(scored))]

def create_shipment(shipment_id,route_id,route_data,quantity,route_states,tick):
    time = effective_travel_time(route_id,route_data,route_states)
    return Shipment(
        shipment_id=shipment_id,
        source=route_data['source'],
        target=route_data['target'],
        route_id=route_id,
        base_time = route_data['travel_time'],
        dispatch_tick=tick,
        expected_tick=tick+route_data['travel_time'],
        quantity=quantity,
        remaining_time=time,
        transport_cost=route_data['transport_cost'] * quantity)
    
def dispatch_shipment(shipment_id, target, quantity, route_lookup, route_states, active_shipments, config, states, tick,source=None):
    rid, rd = select_route(target, route_lookup, route_states, states, source)
    if rid is None:
        return shipment_id
    sid = rd['source']
    dispatch_quantity = min(quantity, states[sid].inventory)
    dispatch_quantity = min(dispatch_quantity, rd['capacity'])
    if sid in config['suppliers']:
        if random.random() > config['suppliers'][sid]['reliability']:
            dispatch_quantity = round(dispatch_quantity * random.uniform(0.5, 0.9))
    if dispatch_quantity <= 0:
        return shipment_id
    states[sid].inventory -= dispatch_quantity
    states[sid].outgoing += dispatch_quantity
    states[sid].sent += dispatch_quantity
    shipment = create_shipment(shipment_id, rid, rd, dispatch_quantity, route_states,tick)
    active_shipments.append(shipment)
    return shipment_id + 1

def apply_delay(shipment,route_data):
    if random.random() < route_data['delay_probability']:
        shipment.delayed = True
        shipment.remaining_time += 1
        
def advance_shipments(active_shipments,route_lookup,tick):
    delivered_shipments = []
    for shipment in active_shipments:
        route_data = route_lookup[shipment.route_id]
        if not shipment.delayed:
            apply_delay(shipment,route_data)
        shipment.remaining_time -= 1
        if shipment.remaining_time <= 0:
            shipment.delivered = True
            shipment.final_tick = tick
            delivered_shipments.append(shipment)
    for ds in delivered_shipments:
        active_shipments.remove(ds)
    return delivered_shipments

def process(delivered_shipments, states):
    lost_shipments = []
    for shipment in delivered_shipments:
        target_state = states[shipment.target]
        space_available = max(0, target_state.capacity - target_state.inventory)
        accepted = min(space_available, shipment.quantity)
        target_state.inventory += accepted
        target_state.incoming += accepted
        target_state.received += accepted
        if accepted < shipment.quantity:
            lost_shipments.append({
                'shipment_id': shipment.shipment_id,
                'lost_quantity': shipment.quantity - accepted,
                'target': shipment.target
            })
    return lost_shipments

            

def update_congestion(active_shipments,route_states,route_lookup):
    for route_state in route_states.values():
        route_state.current_flow = 0
        route_state.congestion_level = 0
    for shipment in active_shipments:
        route_states[shipment.route_id].current_flow += shipment.quantity
    for route_id,route_state in route_states.items():
        route_capactity = route_lookup[route_id]['capacity']
        congestion = route_state.current_flow / route_capactity 
        route_state.congestion_level = congestion
    
def effective_travel_time(rid,rd,r_states):
    r_state = r_states[rid]
    if r_state.congestion_level > rd['congestion_threshold']:
        return round(rd['travel_time'] * rd['congestion_delay_multiplier'])
    return round(rd['travel_time'])

def score_route(rid,rd,r_states):
    r_state = r_states[rid]
    congestion = r_state.congestion_level
    base = rd['transport_cost']
    ct = rd['congestion_threshold']
    cm = rd['congestion_delay_multiplier']
    prim = 0 if rd['is_primary'] else 5
    if congestion >= ct:
        congestion_penalty = congestion * cm * 10
    else:
        congestion_penalty = congestion * 5

    return base + congestion_penalty + prim