from dataset.config_generator import generate_normal_config
import time
from simulator.metrics import final_metrics
import json
import numpy as np
from pathlib import Path
from simulator.engine import Simulator

def generate_dataset(base_config,scenario_ranges,amount):
    X_data = []
    Y_data = []
    time_taken = {}
    base_seed = base_config.get('simulation', {}).get('random_seed')
    config_rng = np.random.default_rng(base_seed)
    for i in range(amount):
        config = generate_normal_config(base_config,scenario_ranges,rng=config_rng)
        if base_seed is not None:
            config['simulation']['random_seed'] = base_seed + i
        X = {}
        for keys,values in config.items():
            if keys == 'simulation':
                X['ticks'] = values['ticks']
                X['backlog_enabled'] = 1 if values['backlog_enabled'] else 0
                X['lost_sales_enabled'] = 1 if values['lost_sales_enabled'] else 0 

            if keys in ['suppliers','warehouses','retailers']:
                for id,data in values.items():
                    for key,value in data.items():
                        if key in ['inventory','capacity','reliability','production_rate','reorder_point','reorder_quantity','processing_rate','demand_mean','demand_std']:
                            X[f'{id}_{key}'] = value
            
            if keys == 'routes':
                for id,data in enumerate(values):
                    for key,value in data.items():
                        if key in ['travel_time','delay_probability','capacity','transport_cost']:
                            X[f'R_{id}_{key}'] = value
        
        sim = Simulator(config)
        start_time = time.perf_counter()
        results = sim.run()
        end_time = time.perf_counter()

        time_taken[i] = end_time - start_time
        Y = final_metrics(results,sim.config,sim.route_lookup)


        Y_data.append(Y)
        X_data.append(X)
    
    dataset = {'X_data':X_data,
            'Y_data':Y_data}
    
    dir = Path(__file__).resolve().parent
    data_folder = dir.parent / "data"
    data_folder.mkdir(exist_ok=True)
    save_path = data_folder / "normal_dataset.json"
    with open(save_path,mode='w') as f:
        json.dump(dataset,f,indent=4)
    return time_taken



    

    
