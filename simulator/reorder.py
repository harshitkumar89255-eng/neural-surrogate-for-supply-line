from simulator.shipment import dispatch_shipment
from simulator.disruptions import effective_process_rate


def build_st_lookup(route_lookup):
    st_lookup = {}
    for rid, rd in route_lookup.items():
        key = (rd['source'], rd['target'])
        st_lookup.setdefault(key, []).append(rid)
    return st_lookup


def in_transit_quantity(node_id, active_shipments):
    return sum(s.quantity for s in active_shipments if s.target == node_id)


def check_reorders(config, states, route_lookup, route_states, active_shipments, shipment_id):
    st_lookup = build_st_lookup(route_lookup)

    for wid, wd in config['warehouses'].items():
        w_state = states[wid]
        in_transit = in_transit_quantity(wid, active_shipments)
        effective_stock = w_state.inventory + in_transit
        if effective_stock >= wd['reorder_point']:
            continue
        upstream_nodes = [sid for sid in config['suppliers'] if (sid, wid) in st_lookup]
        if not upstream_nodes:
            continue
        shipment_id = dispatch_shipment(
            shipment_id, target=wid, quantity=wd['reorder_quantity'],
            route_lookup=route_lookup, route_states=route_states,
            active_shipments=active_shipments, config=config, states=states)

    for rid, rd in config['retailers'].items():
        r_state = states[rid]
        in_transit = in_transit_quantity(rid, active_shipments)
        effective_stock = r_state.inventory + in_transit

        if effective_stock >= rd['reorder_point']:
            continue
        upstream_nodes = [wid for wid in config['warehouses'] if (wid, rid) in st_lookup]
        if not upstream_nodes:
            continue
        available_warehouses = [wid for wid in upstream_nodes if not states[wid].disrupted and states[wid].inventory > 0]
        if not available_warehouses:
            continue
        best_wid = max(available_warehouses, key=lambda wid: states[wid].inventory)
        process_rate = effective_process_rate(best_wid, states[best_wid], config)
        shipment_quantity = min(rd['reorder_quantity'], process_rate)
        shipment_id = dispatch_shipment(
            shipment_id,
            target=rid,
            quantity=shipment_quantity,
            route_lookup=route_lookup,
            route_states=route_states,
            active_shipments=active_shipments,
            config=config,
            states=states,
            source=best_wid)

    return shipment_id