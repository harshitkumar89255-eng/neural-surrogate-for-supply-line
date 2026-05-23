import copy
import numpy as np 

def generate_normal_config(base_config,scenario_ranges):
    config = copy.deepcopy(base_config)
    ranges = copy.deepcopy(scenario_ranges['normal'])

    for key, values in config.items():

        if key == 'retailers':
            for id, data in values.items():
                sampled_capac = round(np.random.normal(data['capacity'],data['capacity'] * ranges['capacity_std_frac']))
            
                data['capacity'] = max(1,sampled_capac)
                data['inventory'] = round(data['capacity']/2)

                sampled_mean = round(np.random.normal(data['demand_mean'],data['demand_mean'] * ranges['demand_std_frac']))
                sampled_std = round(np.random.normal(data['demand_std'],data['demand_std']*ranges['demand_std_frac']))
            
                data['demand_mean'] = max(1,sampled_mean)
                data['demand_std'] = max(1,sampled_std)

                sampled_point = round(np.random.normal(data['reorder_point'],data['reorder_point'] * ranges['reorder_std_frac']))
                qty = round(np.random.normal(data['reorder_quantity'],data['reorder_quantity']*ranges['reorder_std_frac']))
    
                data['reorder_point'] = max(1,sampled_point)           
                data['reorder_quantity'] = max(1,qty)

        if key == 'warehouses':
            for id, data in values.items():
                sampled_mean = round(np.random.normal(data['reorder_point'],data['reorder_point'] * ranges['reorder_std_frac']))
                qty = round(np.random.normal(data['reorder_quantity'],data['reorder_quantity']*ranges['reorder_std_frac']))
    
                data['reorder_point'] = max(1,sampled_mean)           
                data['reorder_quantity'] = max(1,qty)

                sampled_capac = round(np.random.normal(data['capacity'],data['capacity'] * ranges['capacity_std_frac']))
            
                data['capacity'] = max(1,sampled_capac)
                data['inventory'] = round(data['capacity']/2)
                data['processing_rate'] = max(1,round(np.random.normal(data['processing_rate'],data['processing_rate']*ranges['processing_rate_std_frac'])))
        if key =='routes':
            for route in values:
                route['delay_probability'] = np.random.normal(route['delay_probability'],ranges['delay_probability_std'])
                route['delay_probability'] = max(0,route['delay_probability'])
                route['delay_probability'] = min(route['delay_probability'],1)
                route['travel_time'] = int(max(1,route['travel_time'] + np.random.choice([2,1,0,-1,-2])))
                route['capacity'] = max(1,round(np.random.normal(route['capacity'],route['capacity']*ranges['capacity_std_frac'])))

        if key == 'suppliers':
            for id, data in values.items():
            
                sampled_capac = round(np.random.normal(data['capacity'],data['capacity'] * ranges['capacity_std_frac']))
                data['capacity'] = max(1,sampled_capac)
                data['inventory'] = data['capacity']
            
                data['reliability'] = np.random.normal(data['reliability'],data['reliability'] * ranges['reliability_std_frac'])
                data['reliability'] = min(data['reliability'],1)
                data['reliability'] = max(0,data['reliability'])
                data['production_rate'] = max(1,round(np.random.normal(data['production_rate'],data['production_rate'] * ranges['production_rate_std_frac'])))
        
    return config