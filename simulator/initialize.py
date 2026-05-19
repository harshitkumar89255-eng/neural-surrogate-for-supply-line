from simulator.entities import State, RouteState

def init_states(graph):
    states = {}
    for nid, nd in graph.nodes(data=True):
        states[nid] = State(
            node_id=nid,
            node_type=nd['node_type'],
            inventory=nd.get('inventory', 0),
            capacity=nd.get('capacity', float('inf'))
        )
    return states

def init_route_states(route_lookup):
    route_states = {}
    for rid in route_lookup:
        route_states[rid] = RouteState(route_id=rid)
        
    return route_states