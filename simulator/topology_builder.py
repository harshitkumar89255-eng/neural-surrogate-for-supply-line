import networkx as nx

def build_supply_chain_graph(config):
    G = nx.DiGraph()
    for supplier_id,supplier_data in config['suppliers'].items():
        G.add_node(supplier_id, **supplier_data, node_type='supplier')
        
    for warehouse_id,warehouse_data in config['warehouses'].items():
        G.add_node(warehouse_id, **warehouse_data, node_type='warehouse')
        
    for retailer_id,retailer_data in config['retailers'].items():
        G.add_node(retailer_id, **retailer_data, node_type='retailer')
        
    route_lookup = {}
    
    for route_index,route_data in enumerate(config['routes']):
        route_id = f"route_{route_index+1}"
        route_lookup[route_id] = route_data
        
        G.add_edge(route_data['source'],route_data['target'],route_id=route_id,
                   travel_time=route_data['travel_time'],
                   capacity=route_data['capacity'],
                   delay_probability=route_data['delay_probability'],
                   transport_cost=route_data['transport_cost'],
                   congestion_threshold=route_data['congestion_threshold'],
                   congestion_delay_multiplier=route_data['congestion_delay_multiplier'],
                   is_primary=route_data['is_primary'])
        
    return G, route_lookup