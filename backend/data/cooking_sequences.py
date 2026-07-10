"""Cooking sequence definitions mapped from the industrial control script."""

from config import timing_config as t

# Each step: action name, duration (seconds), UI title, UI description
# Actions are executed by CookingService._execute_action()

COOK_RICE_SEQUENCE = [
    {
        "action": "rice_bowl_down",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "Preparing ingredients",
        "description": "Lowering rice bowl into cooking position",
    },
    {
        "action": "stop_rice_bowl",
        "duration": 0,
        "title": "Heating",
        "description": "Stabilizing bowl position for heating",
    },
    {
        "action": "electronic_valve_open",
        "duration": t.VALVE_OPEN_TIME,
        "title": "Adding ingredients",
        "description": "Dispensing water and seasonings via valve",
    },
    {
        "action": "electronic_valve_close_wait",
        "duration": t.VALVE_CLOSE_WAIT,
        "title": "Mixing",
        "description": "Closing valve and distributing ingredients",
    },
    {
        "action": "stop_valve",
        "duration": 0,
        "title": "Cooking",
        "description": "Simmering rice to perfection",
    },
    {
        "action": "wait",
        "duration": 30,
        "title": "Cooking",
        "description": "Rice cooking in progress",
    },
    {
        "action": "rice_bowl_up",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "Finalizing",
        "description": "Raising rice bowl after cooking",
    },
    {
        "action": "stop_rice_bowl",
        "duration": 0,
        "title": "Ready to Serve",
        "description": "Rice is perfectly cooked!",
    },
]

CURRY_SEQUENCE = [
    {
        "action": "mixer_down",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "Preparing ingredients",
        "description": "Lowering mixer bowl for ingredient prep",
    },
    {
        "action": "stop_mixer_hydraulic",
        "duration": 0,
        "title": "Heating",
        "description": "Preheating cooking vessel",
    },
    {
        "action": "mixer_motor_on",
        "duration": t.MIXER_ROTATE_LONG,
        "title": "Adding ingredients",
        "description": "Sautéing onions, ginger, and spices",
    },
    {
        "action": "mixer_motor_off",
        "duration": 0,
        "title": "Mixing",
        "description": "Blending curry base evenly",
    },
    {
        "action": "electronic_valve_open",
        "duration": t.VALVE_OPEN_TIME,
        "title": "Cooking",
        "description": "Adding liquids via electronic valve",
    },
    {
        "action": "electronic_valve_close_wait",
        "duration": t.VALVE_CLOSE_WAIT,
        "title": "Cooking",
        "description": "Simmering curry to develop flavors",
    },
    {
        "action": "stop_valve",
        "duration": 0,
        "title": "Finalizing",
        "description": "Adjusting consistency and seasoning",
    },
    {
        "action": "wait",
        "duration": 20,
        "title": "Finalizing",
        "description": "Resting curry for aroma infusion",
    },
    {
        "action": "mixer_up",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "Ready to Serve",
        "description": "Curry is rich and ready!",
    },
    {
        "action": "stop_mixer_hydraulic",
        "duration": 0,
        "title": "Ready to Serve",
        "description": "Curry is rich and ready!",
    },
]

# Full 14-step biryani mode from the original control script
CHICKEN_BIRYANI_SEQUENCE = [
    {
        "action": "rice_bowl_down_mixer_down",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "Preparing ingredients",
        "description": "Lowering rice bowl and mixer into downposition",
    },
    {
        "action": "stop_bowls",
        "duration": 0,
        "title": "Preparing ingredients",
        "description": "Bowls positioned down",
    },
    {
        "action": "mixer_motor_on",
        "duration": t.MIXER_ROTATE_LONG,
        "title": "Mixing",
        "description": "Mixing spices(1 minute) and rice started cooking",
    },
    {
        "action": "mixer_motor_off",
        "duration": 0,
        "title": "Heating",
        "description": "Stopping mixer motor",
    },
    {
        "action": "stop_everything",
        "duration": t.COOK_WAIT,
        "title": "Cooking",
        "description": "rice cooking — resting for 2 minutes",
    },
    {
        "action": "electronic_valve_open",
        "duration": t.VALVE_OPEN_TIME,
        "title": "To remove water",
        "description": "Opening electronic valve",
    },
    {
        "action": "electronic_valve_close_wait",
        "duration": t.VALVE_CLOSE_WAIT,
        "title": "After removing water",
        "description": "Closing valve after dispensing",
    },
    {
        "action": "stop_valve",
        "duration": 0,
        "title": "water removed",
        "description": "Valve secured",
    },
    {
        "action": "rice_bowl_up_mixer_up",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "After rice Cooked for 70%",
        "description": "Raising rice bowl and mixer",
    },
    {
        "action": "stop_bowls",
        "duration": 0,
        "title": "To change positions",
        "description": "Bowls raised to cooking height",
    },
    {
        "action": "position_motor_forward",
        "duration": 0,
        "title": "To change positions",
        "description": "Rotating position motor 180°",
    },
    {
        "action": "rice_bowl_down_valve_open",
        "duration": t.VALVE_DISPENSE_TIME,
        "title": "Rice into chicken bowl",
        "description": "Lowering ricebowl and opening valve",
    },
    {
        "action": "electronic_valve_close_wait",
        "duration": t.VALVE_CLOSE_WAIT,
        "title": "Rice into chicken bowl",
        "description": "Closing valve after rice into chicken bowl",
    },
    {
        "action": "stop_rice_bowl_valve",
        "duration": 0,
        "title": "Rice into chicken bowl",
        "description": "Securing bowl and valve",
    },
    {
        "action": "rice_bowl_up",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "Rice into chicken bowl",
        "description": "Raising rice bowl to serve position",
    },
    {
        "action": "stop_rice_bowl",
        "duration": 0,
        "title": "Rice into chicken bowl",
        "description": "Bowl in serve position",
    },
    {
        "action": "position_motor_backward",
        "duration": 0,
        "title": "To change positions",
        "description": "Reverting position motor",
    },
    {
        "action": "mixer_down",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "To mix rice",
        "description": "Lowering mixer for final blend",
    },
    {
        "action": "stop_mixer_hydraulic",
        "duration": 0,
        "title": "Mixing",
        "description": "Mixer positioned",
    },
    {
        "action": "mixer_motor_on",
        "duration": t.MIXER_ROTATE_SHORT,
        "title": "Mixing",
        "description": "Final mixing (30 seconds)",
    },
    {
        "action": "mixer_motor_off",
        "duration": 0,
        "title": "Mixing",
        "description": "Mixing complete",
    },
    {
        "action": "mixer_up",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "To change the position",
        "description": "Raising mixer to up position",
    },
    {
        "action": "stop_mixer_hydraulic",
        "duration": 0,
        "title": "to change the position",
        "description": "Mixer secured",
    },
    {
        "action": "position_motor_forward",
        "duration": 0,
        "title": "For Dum",
        "description": "To close the Biryani bowl",
    },
    {
        "action": "rice_bowl_down",
        "duration": t.HYDRAULIC_MOVE_TIME,
        "title": "To close the Biryani bowl",
        "description": "Lowering rice bowl to close the Biryani bowl for dum",
    },
    {
        "action": "stop_rice_bowl",
        "duration": 0,
        "title": "Ready to Serve",
        "description": "Your Chicken Biryani is ready!",
    },
]

AUTO_SEQUENCE = [
    {
        "action": "stop_main_devices",
        "duration": 0,
        "title": "Auto Cycle",
        "description": "Resetting devices",
    },
    {
        "action": "rice_bowl_down",
        "duration": t.AUTO_RICE_BOWL_TIME,
        "title": "Auto Cycle",
        "description": "Rice bowl down",
    },
    {
        "action": "stop_rice_bowl",
        "duration": 0,
        "title": "Auto Cycle",
        "description": "Rice bowl stopped",
    },
    {
        "action": "mixer_down",
        "duration": t.AUTO_MIXER_TIME,
        "title": "Auto Cycle",
        "description": "Mixer down",
    },
    {
        "action": "stop_mixer_hydraulic",
        "duration": 0,
        "title": "Auto Cycle",
        "description": "Mixer stopped",
    },
    {
        "action": "electronic_valve_open",
        "duration": t.AUTO_VALVE_OPEN_TIME,
        "title": "Auto Cycle",
        "description": "Valve open",
    },
    {
        "action": "electronic_valve_close_wait",
        "duration": t.AUTO_VALVE_CLOSE_WAIT,
        "title": "Auto Cycle",
        "description": "Valve closing",
    },
    {
        "action": "stop_valve",
        "duration": 0,
        "title": "Auto Cycle",
        "description": "Auto cycle step complete",
    },
]

RECIPE_SEQUENCES = {
    "cook_rice": COOK_RICE_SEQUENCE,
    "curry": CURRY_SEQUENCE,
    "chicken_biryani": CHICKEN_BIRYANI_SEQUENCE,
    "auto": AUTO_SEQUENCE,
}


def get_sequence(recipe_id: str) -> list[dict]:
    if recipe_id not in RECIPE_SEQUENCES:
        raise ValueError(f"Unknown recipe: {recipe_id}")
    return RECIPE_SEQUENCES[recipe_id]


def estimate_total_seconds(recipe_id: str) -> int:
    return sum(step["duration"] for step in get_sequence(recipe_id))
