def calculate_score(row):
    route_length = 450
    score = 0
    dist_without_stop = row['engine_capacity'] / row['fuel_consumption'] * 100
    pit_stops_needed = route_length // dist_without_stop
    if pit_stops_needed == 1:
        score += 1
    elif pit_stops_needed == 0:
        score += 2

    fuel_burned_on_trip = route_length / 100 * row['fuel_consumption']
    if fuel_burned_on_trip <= 230:
        score += 2
    else:
        score += 1

    if row['maximum_load'] >= 20:
        score += 2

    return score
