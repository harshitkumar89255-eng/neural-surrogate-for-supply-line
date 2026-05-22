import pandas as pd


def final_metrics(results,config,route_lookup):
    
    df = results['state_history'][len(results['state_history'])-1]['nodes']
    fdf = pd.DataFrame(df).T
    

    throughput = fdf[fdf['node_type']=='retailer']['sent'].sum() #total delivered to the consumers

    stockout_rate = fdf['stockout'].sum()/(len(results['state_history']) * fdf[fdf['node_type']=='retailer']['stockout'].count()) #stockout per retailer per tick
    
    lost_sales = 0
    for tick, items in results['lost_sales_history'].items():
        if items :
            for item in items:
                lost_sales+=item['lost_quantity']
    
     #will be 0 if lost sales is not enabled
    
    shipments = results['completed_shipment_history']
    total_delay = 0
    total_shipments = 0
    for tick,shipment in shipments.items():
        if shipment:
            for ship in shipment:
                total_shipments +=1
                delay = ship.final_tick - ship.expected_tick
                total_delay += delay
    if total_shipments != 0:
        average_delivery_delay = total_delay/total_shipments
    else:
        average_delivery_delay = 0

    inventory_holding_cost = 0

    for tick_data in results["state_history"].values():
        for node_id, node in tick_data["nodes"].items():
            if node["node_type"] == "supplier":
                cost = config["suppliers"][node_id]["holding_cost_per_unit"]
            elif node["node_type"] == "warehouse":
                cost = config["warehouses"][node_id]["holding_cost_per_unit"]
            elif node["node_type"] == "retailer":
                cost = config["retailers"][node_id]["holding_cost_per_unit"]

            inventory_holding_cost += node["inventory"] * cost

    utilisation = []
    for tickd in results['state_history'].values():
        for node in tickd['nodes'].values():
            if node['capacity'] > 0:
                utilisation.append(node['inventory']/node['capacity'])

    average_utilisation = sum(utilisation)/len(utilisation)
    max_utilisation = max(utilisation)

    congestions = []
    for tick_data in results["state_history"].values():
        for route in tick_data["routes"].values():
            congestions.append(route["congestion_level"])

    average_congestion = sum(congestions) / len(congestions)
    max_congestion = max(congestions)

    severity_values = []

    for tick_data in results["state_history"].values():
        for route_id, route in tick_data["routes"].items():
            threshold = route_lookup[route_id]["congestion_threshold"]
            excess = max(0, route["congestion_level"] - threshold)
            severity_values.append(excess)

    congestion_severity = sum(severity_values) / len(severity_values)

    backlog_count = fdf[fdf['node_type']=='retailer']['backlog'].sum()

    total_transport_cost = 0

    for shipments in results["completed_shipment_history"].values():
        for shipment in shipments:
            total_transport_cost += shipment.transport_cost
            
    total_inventory = sum(node['inventory'] for node in df.values())

    total_received = sum(node["received"] for node in df.values())
    
    total_sent = sum(node["sent"] for node in df.values())
    
    total_demand = 0
    for tick_demands in results["demand_history"].values():
        total_demand += sum(tick_demands.values())
    
    service_level = throughput / total_demand if total_demand > 0 else 0
    return ({
        "throughput": throughput,
        "stockout_rate": float(stockout_rate),
        "total_lost_sales": lost_sales,
        "average_delivery_delay": average_delivery_delay,
        "inventory_holding_cost": inventory_holding_cost,
        "average_node_utilisation": average_utilisation,
        "max_node_utilisation": max_utilisation,
        "average_congestion": average_congestion,
        "max_congestion": max_congestion,
        "congestion_severity": congestion_severity,
        "backorder_count": backlog_count,
        "total_transport_cost": total_transport_cost,
        "total_inventory": total_inventory,
        "total_received": total_received,
        "total_sent": total_sent,
        "service_level": service_level
        })
