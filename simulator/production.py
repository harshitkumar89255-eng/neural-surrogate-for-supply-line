def replenish_supply(config,states):
    for sid,sd in config['suppliers'].items():
        s_state = states[sid]
        production = sd['production_rate']
        if not s_state.disrupted:
            s_state.inventory = min(s_state.inventory + production, s_state.capacity)

