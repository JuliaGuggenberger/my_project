#***********************************************************************************************
# functions.py 
# 
# This file contains functions of to assist for several cases.
#***********************************************************************************************

#***********************************************************************************************
def timeout_sec(page=None):
    timeouts = {
        'market': 100,
        'choice': 100,
    }
    return timeouts.get(page, 100)

#***********************************************************************************************
def clean_zero(x):
    return 0.00 if round(x, 2) == -0.00 else round(x, 2)

#***********************************************************************************************
def extract_stops(trip, time_of_day):
        return [
            (trip.get(f'{time_of_day}_loc_stop{i}'), trip.get(f'{time_of_day}_stop{i}_reason'))
            for i in range(1, 5)
            if trip.get(f'{time_of_day}_loc_stop{i}') and str(trip.get(f'{time_of_day}_loc_stop{i}')).lower() != 'nan'
        ]

#***********************************************************************************************
def format_minutes_to_hm(total_minutes):
    """Format total minutes as 'X hours Y minutes' (skip empty parts)."""
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    parts = []
    if hours > 0:
        parts.append(f"{hours} h")
    if minutes > 0 or not parts:
        parts.append(f"{minutes} min")
    return ' '.join(parts)

#***********************************************************************************************
# Build trip preview/ overview data
def preview_overview_data(trips, weekly_choices=None):
    """Generate structured preview and optional weekly summary data for a list of trips."""
    preview_data = []
    
    total_base = 0
    total_token_used = 0

    for i, trip in enumerate(trips):
        base_token = int(trip.get('tour_total_token_base_mode', 0))

        total_base += base_token

        if weekly_choices:
            if i < len(weekly_choices):
                choice = weekly_choices[i].get('choice')
                token_used = 0 if choice == 'no_commute' else int(trip.get(f'tour_total_token_{choice}', 0))
            else:
                token_used = '-'

            if token_used != '-':
                total_token_used += token_used
        
        else:
            total_token_used = '-'
            token_used = '-'
        

        # Preview Data
        preview_data.append({
            'day': trip['day'],
            'mode': trip['mode'],
            'base_token': base_token,
            'morning_origin': trip.get('morning_origin'),
            'morning_stops': extract_stops(trip, 'morning'),
            'morning_destination': trip.get('morning_destination'),
            'evening_stops': extract_stops(trip, 'evening'),
            'token_used': token_used
        })

    return preview_data, total_base, total_token_used

#***********************************************************************************************
# Choice set
def choice_set(poss_modes, trip, vary = False, current_phase='I', week=0, day_in_week=0):
    modes = []
    for mode in poss_modes:
        rating = trip.get(f"rating_{mode}", 0)
        leaf_row = [True if i < rating else False for i in range(5)]

        if vary:
            modes.append({
                'mode': mode,
                'time': format_minutes_to_hm(trip.get(f'tour_total_duration_min_{mode}')),
                'cost': clean_zero(trip.get(f'tour_total_cost_{mode}_vary_{current_phase}_{week}_{day_in_week}')),
                'token': int(trip.get(f'tour_total_token_{mode}')),
                'rating': leaf_row
            })
        else:
            modes.append({
                'mode': mode,
                'time': format_minutes_to_hm(trip.get(f'tour_total_duration_min_{mode}')),
                'cost': clean_zero(trip.get(f'tour_total_cost_{mode}')),
                'token': int(trip.get(f'tour_total_token_{mode}')),
                'rating': leaf_row
            })

    return modes

#***********************************************************************************************
# Emissions equvialent benchmark
EMISSIONS_BENCHMARKS = [
    ("a large cappuccino", 0.235),
    ("a big dairy ice cream from a van", 0.5),
    ("a red rose grown in a heated greenhouse in the Netherlands", 2.1),
    ("1 kg of boiled potatoes (with lid off)", 1.17),
    ("a raw 4-ounce beefsteak", 2.0),
    ("a pair of average shoes", 11.5),
    ("a flight from London to Glasgow and back", 500),
    ("taking a hot bath (generously filled, electric heated)", 2.6),
]

def get_emissions_equivalent(saved_emissions):
    if saved_emissions < 0:
        excess = abs(saved_emissions)
        return (
            f"You produced <strong>{excess} kg CO₂eq</strong> more than originally."
            "Try more eco-friendly choices next week!"
        )

    if saved_emissions == 0:
        return "No emissions saved in total yet. Try again next week!"

    # Sort benchmarks descending by CO₂ value
    benchmarks = sorted(EMISSIONS_BENCHMARKS, key=lambda x: x[1], reverse=True)

    for desc, val in benchmarks:
        if saved_emissions >= val:
            count = saved_emissions / val
            rounded = int(count)
            if rounded >= 2:
                return (
                    f"You saved enough CO₂eq emissions to equal <strong>{rounded}×</strong>. {desc}"
                    f"<span style='color:gray'> ({val} kg CO₂eq each)</span>"
                )
            else:
                return (
                    f"You saved roughly the CO₂eq emissions needed for {desc}."
                    f"<span style='color:gray'> ({val} kg CO₂eq)</span>"
                )

    # If no match, fallback to smallest
    desc, val = benchmarks[-1]
    return (
        f"You're approaching the CO₂eq emissions impact of {desc}."
        f"<span style='color:gray'> ({val} kg CO₂eq)</span>"
    )