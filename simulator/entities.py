from dataclasses import dataclass, field

@dataclass
class State:
    node_id: str
    node_type: str
    inventory:float
    capacity:float
    backlog:float=0
    incoming:float=0
    outgoing:float=0
    received:float=0
    sent:float=0
    stockout:int=0
    disruption_count:int = 0
    disrupted: bool = False
    disruption_remaining: int = 0
    
@dataclass
class Shipment:
    shipment_id: str
    source:str
    target:str
    quantity:float
    route_id:str
    remaining_time:int
    base_time:float
    dispatch_tick:float
    expected_tick:float
    final_tick:float | None = None
    transport_cost:float=0
    delayed:bool=False
    delivered:bool=False
    
    
@dataclass
class RouteState:
    route_id:str
    current_flow:float=0
    congestion_level:float=0
    disruption_count:int= 0
    disrupted: bool = False
    disruption_remaining: int = 0 
    