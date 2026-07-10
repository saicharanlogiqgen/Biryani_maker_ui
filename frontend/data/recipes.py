"""Recipe definitions for Dumchef."""

RICE_STAGES = [
    {"title": "Preparing ingredients", "description": "Measuring rice and seasoning", "duration_pct": 10},
    {"title": "Heating", "description": "Bringing water to a gentle boil", "duration_pct": 15},
    {"title": "Adding ingredients", "description": "Adding rice and aromatics to the pot", "duration_pct": 15},
    {"title": "Mixing", "description": "Stirring gently for even cooking", "duration_pct": 10},
    {"title": "Cooking", "description": "Simmering until rice is fluffy", "duration_pct": 35},
    {"title": "Finalizing", "description": "Resting and steaming off heat", "duration_pct": 10},
    {"title": "Ready to Serve", "description": "Rice is perfectly cooked!", "duration_pct": 5},
]

RICE_OPTIONS = {
    "plain_rice": {
        "id": "plain_rice",
        "title": "Plain Rice",
        "emoji": "🍚",
        "icon_color": "#ffb300",
        "description": "Simple steamed basmati rice",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Water", "quantity": "4 cups"},
            {"name": "Salt", "quantity": "1 tsp"},
            {"name": "Ghee", "quantity": "1 tbsp"},
        ],
    },
    "bagara_rice": {
        "id": "bagara_rice",
        "title": "Bagara Rice",
        "emoji": "🌿",
        "icon_color": "#ff8a00",
        "description": "Hyderabadi-style tempered rice",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Water", "quantity": "4 cups"},
            {"name": "Onions", "quantity": "1 medium, sliced"},
            {"name": "Ginger-garlic paste", "quantity": "1 tsp"},
            {"name": "Green chilies", "quantity": "2 pcs"},
            {"name": "Mint leaves", "quantity": "2 tbsp"},
            {"name": "Coriander leaves", "quantity": "2 tbsp"},
            {"name": "Whole spices", "quantity": "bay leaf, cloves, cardamom"},
            {"name": "Ghee / oil", "quantity": "2 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "jeera_rice": {
        "id": "jeera_rice",
        "title": "Jeera Rice",
        "emoji": "✨",
        "icon_color": "#ff6a00",
        "description": "Fragrant cumin-tempered rice",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Water", "quantity": "4 cups"},
            {"name": "Cumin seeds (jeera)", "quantity": "1.5 tsp"},
            {"name": "Ghee", "quantity": "2 tbsp"},
            {"name": "Bay leaf", "quantity": "1 leaf"},
            {"name": "Salt", "quantity": "1 tsp"},
        ],
    },
}

PULAO_OPTIONS = {
    "veg_pulao": {
        "id": "veg_pulao",
        "title": "Veg Pulao",
        "emoji": "🥗",
        "icon_color": "#ffb300",
        "description": "Mixed vegetable pulao",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Mixed vegetables", "quantity": "1.5 cups"},
            {"name": "Onion", "quantity": "1 medium"},
            {"name": "Ginger-garlic paste", "quantity": "1 tsp"},
            {"name": "Green peas", "quantity": "1/2 cup"},
            {"name": "Whole spices", "quantity": "bay leaf, cloves, cinnamon"},
            {"name": "Ghee / oil", "quantity": "2 tbsp"},
            {"name": "Water", "quantity": "3.5 cups"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "chicken_pulao": {
        "id": "chicken_pulao",
        "title": "Chicken Pulao",
        "emoji": "🍗",
        "icon_color": "#ff6a00",
        "description": "One-pot chicken pulao",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Chicken", "quantity": "500 g"},
            {"name": "Onions", "quantity": "2 medium"},
            {"name": "Yogurt", "quantity": "1/4 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Green chilies", "quantity": "2 pcs"},
            {"name": "Mint & coriander", "quantity": "2 tbsp each"},
            {"name": "Whole spices", "quantity": "bay leaf, cardamom, cloves"},
            {"name": "Ghee / oil", "quantity": "3 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "mutton_pulao": {
        "id": "mutton_pulao",
        "title": "Mutton Pulao",
        "emoji": "🥩",
        "icon_color": "#c43e00",
        "description": "Aromatic mutton pulao",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Mutton", "quantity": "500 g"},
            {"name": "Onions", "quantity": "2 large"},
            {"name": "Yogurt", "quantity": "1/3 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1.5 tbsp"},
            {"name": "Green chilies", "quantity": "3 pcs"},
            {"name": "Mint & coriander", "quantity": "3 tbsp each"},
            {"name": "Whole spices", "quantity": "bay leaf, cardamom, cloves, cinnamon"},
            {"name": "Ghee / oil", "quantity": "3 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "mushroom_pulao": {
        "id": "mushroom_pulao",
        "title": "Mushroom Pulao",
        "emoji": "🍄",
        "icon_color": "#ff8a00",
        "description": "Flavorful mushroom pulao",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Mushrooms", "quantity": "250 g"},
            {"name": "Onion", "quantity": "1 medium"},
            {"name": "Ginger-garlic paste", "quantity": "1 tsp"},
            {"name": "Green peas", "quantity": "1/2 cup"},
            {"name": "Whole spices", "quantity": "bay leaf, cloves, cardamom"},
            {"name": "Ghee / oil", "quantity": "2 tbsp"},
            {"name": "Water", "quantity": "3.5 cups"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
}

RICE_CATEGORIES = {
    "rice": {
        "id": "rice",
        "title": "Rice",
        "emoji": "🍚",
        "icon_color": "#ffb300",
        "description": "Plain, Bagara, and Jeera rice",
        "items": RICE_OPTIONS,
    },
    "pulao": {
        "id": "pulao",
        "title": "Pulao",
        "emoji": "🥘",
        "icon_color": "#ff6a00",
        "description": "Veg, Chicken, Mutton, and Mushroom pulao",
        "items": PULAO_OPTIONS,
    },
}

CURRY_STAGES = [
    {"title": "Preparing ingredients", "description": "Chopping vegetables and measuring spices", "duration_pct": 12},
    {"title": "Heating", "description": "Heating oil in the cooking vessel", "duration_pct": 10},
    {"title": "Adding ingredients", "description": "Sautéing onions, ginger, and garlic", "duration_pct": 18},
    {"title": "Mixing", "description": "Blending spices with vegetables", "duration_pct": 12},
    {"title": "Cooking", "description": "Simmering curry to develop flavors", "duration_pct": 33},
    {"title": "Finalizing", "description": "Adjusting seasoning and finishing", "duration_pct": 10},
    {"title": "Ready to Serve", "description": "Curry is rich and ready!", "duration_pct": 5},
]

VEG_CURRIES = {
    "paneer_butter_masala": {
        "id": "paneer_butter_masala",
        "title": "Paneer Butter Masala",
        "emoji": "🧀",
        "icon_color": "#ff8a00",
        "description": "Creamy tomato-butter paneer curry",
        "ingredients": [
            {"name": "Paneer", "quantity": "500 g"},
            {"name": "Tomatoes", "quantity": "4 medium"},
            {"name": "Onions", "quantity": "2 medium"},
            {"name": "Butter", "quantity": "3 tbsp"},
            {"name": "Fresh cream", "quantity": "1/2 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Kashmiri chili powder", "quantity": "1 tsp"},
            {"name": "Garam masala", "quantity": "1 tsp"},
            {"name": "Cashews", "quantity": "10 pcs"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "dal_tadka": {
        "id": "dal_tadka",
        "title": "Dal Tadka",
        "emoji": "🥣",
        "icon_color": "#ffb300",
        "description": "Tempered yellow lentil curry",
        "ingredients": [
            {"name": "Toor dal", "quantity": "1.5 cups"},
            {"name": "Onions", "quantity": "1 medium"},
            {"name": "Tomatoes", "quantity": "2 medium"},
            {"name": "Ghee", "quantity": "2 tbsp"},
            {"name": "Cumin seeds", "quantity": "1 tsp"},
            {"name": "Garlic", "quantity": "6 cloves"},
            {"name": "Green chilies", "quantity": "2 pcs"},
            {"name": "Turmeric powder", "quantity": "1/2 tsp"},
            {"name": "Red chili powder", "quantity": "1 tsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "veg_kurma": {
        "id": "veg_kurma",
        "title": "Veg Kurma",
        "emoji": "🥗",
        "icon_color": "#ff6a00",
        "description": "Mild coconut vegetable kurma",
        "ingredients": [
            {"name": "Mixed vegetables", "quantity": "3 cups"},
            {"name": "Onion", "quantity": "1 large"},
            {"name": "Coconut (grated)", "quantity": "1/2 cup"},
            {"name": "Cashews", "quantity": "8 pcs"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Green chilies", "quantity": "2 pcs"},
            {"name": "Kurma masala", "quantity": "2 tsp"},
            {"name": "Cooking oil", "quantity": "2 tbsp"},
            {"name": "Coriander leaves", "quantity": "2 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "palak_paneer": {
        "id": "palak_paneer",
        "title": "Palak Paneer",
        "emoji": "🥬",
        "icon_color": "#c43e00",
        "description": "Spinach gravy with soft paneer",
        "ingredients": [
            {"name": "Spinach (palak)", "quantity": "500 g"},
            {"name": "Paneer", "quantity": "300 g"},
            {"name": "Onion", "quantity": "1 medium"},
            {"name": "Tomato", "quantity": "1 medium"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Green chilies", "quantity": "2 pcs"},
            {"name": "Cumin seeds", "quantity": "1 tsp"},
            {"name": "Garam masala", "quantity": "1/2 tsp"},
            {"name": "Fresh cream", "quantity": "2 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "chana_masala": {
        "id": "chana_masala",
        "title": "Chana Masala",
        "emoji": "🫘",
        "icon_color": "#ff9a1a",
        "description": "Spicy chickpea curry",
        "ingredients": [
            {"name": "Chickpeas (chana)", "quantity": "2 cups cooked"},
            {"name": "Onions", "quantity": "2 medium"},
            {"name": "Tomatoes", "quantity": "2 medium"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Chana masala powder", "quantity": "2 tsp"},
            {"name": "Cumin seeds", "quantity": "1 tsp"},
            {"name": "Red chili powder", "quantity": "1 tsp"},
            {"name": "Amchur powder", "quantity": "1/2 tsp"},
            {"name": "Cooking oil", "quantity": "2 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
}

NON_VEG_CURRIES = {
    "chicken_curry": {
        "id": "chicken_curry",
        "title": "Chicken Curry",
        "emoji": "🍗",
        "icon_color": "#ff6a00",
        "description": "Classic home-style chicken curry",
        "ingredients": [
            {"name": "Chicken", "quantity": "1 kg"},
            {"name": "Onions", "quantity": "3 medium"},
            {"name": "Tomatoes", "quantity": "3 medium"},
            {"name": "Yogurt", "quantity": "1/2 cup"},
            {"name": "Ginger-garlic paste", "quantity": "2 tbsp"},
            {"name": "Chicken masala", "quantity": "2 tbsp"},
            {"name": "Red chili powder", "quantity": "1 tsp"},
            {"name": "Turmeric powder", "quantity": "1/2 tsp"},
            {"name": "Cooking oil", "quantity": "3 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "mutton_curry": {
        "id": "mutton_curry",
        "title": "Mutton Curry",
        "emoji": "🥩",
        "icon_color": "#c43e00",
        "description": "Rich slow-cooked mutton curry",
        "ingredients": [
            {"name": "Mutton", "quantity": "1 kg"},
            {"name": "Onions", "quantity": "4 medium"},
            {"name": "Tomatoes", "quantity": "3 medium"},
            {"name": "Yogurt", "quantity": "1/2 cup"},
            {"name": "Ginger-garlic paste", "quantity": "2 tbsp"},
            {"name": "Mutton masala", "quantity": "2 tbsp"},
            {"name": "Whole spices", "quantity": "bay leaf, cloves, cardamom"},
            {"name": "Red chili powder", "quantity": "1.5 tsp"},
            {"name": "Cooking oil", "quantity": "4 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "egg_curry": {
        "id": "egg_curry",
        "title": "Egg Curry",
        "emoji": "🥚",
        "icon_color": "#ffb300",
        "description": "Spiced boiled-egg curry",
        "ingredients": [
            {"name": "Eggs (boiled)", "quantity": "6 pcs"},
            {"name": "Onions", "quantity": "2 medium"},
            {"name": "Tomatoes", "quantity": "2 medium"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Red chili powder", "quantity": "1 tsp"},
            {"name": "Coriander powder", "quantity": "1 tsp"},
            {"name": "Turmeric powder", "quantity": "1/2 tsp"},
            {"name": "Garam masala", "quantity": "1/2 tsp"},
            {"name": "Cooking oil", "quantity": "2 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "fish_curry": {
        "id": "fish_curry",
        "title": "Fish Curry",
        "emoji": "🐟",
        "icon_color": "#ff8a00",
        "description": "Tangy coastal-style fish curry",
        "ingredients": [
            {"name": "Fish pieces", "quantity": "750 g"},
            {"name": "Onions", "quantity": "2 medium"},
            {"name": "Tomatoes", "quantity": "2 medium"},
            {"name": "Tamarind pulp", "quantity": "2 tbsp"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Red chili powder", "quantity": "1.5 tsp"},
            {"name": "Turmeric powder", "quantity": "1/2 tsp"},
            {"name": "Mustard seeds", "quantity": "1 tsp"},
            {"name": "Cooking oil", "quantity": "3 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "prawn_curry": {
        "id": "prawn_curry",
        "title": "Prawn Curry",
        "emoji": "🦐",
        "icon_color": "#ff9a1a",
        "description": "Coconut prawn masala curry",
        "ingredients": [
            {"name": "Prawns", "quantity": "500 g"},
            {"name": "Onion", "quantity": "1 large"},
            {"name": "Tomato", "quantity": "2 medium"},
            {"name": "Coconut milk", "quantity": "1 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Red chili powder", "quantity": "1 tsp"},
            {"name": "Coriander powder", "quantity": "1 tsp"},
            {"name": "Curry leaves", "quantity": "1 sprig"},
            {"name": "Cooking oil", "quantity": "2 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
}

CURRY_CATEGORIES = {
    "veg": {
        "id": "veg",
        "title": "Veg",
        "emoji": "🥦",
        "icon_color": "#ffb300",
        "description": "Choose from 5 vegetarian curries",
        "items": VEG_CURRIES,
    },
    "non_veg": {
        "id": "non_veg",
        "title": "Non-Veg",
        "emoji": "🍖",
        "icon_color": "#ff6a00",
        "description": "Choose from 5 non-veg curries",
        "items": NON_VEG_CURRIES,
    },
}

BIRYANI_STAGES = [
    {"title": "Preparing ingredients", "description": "Marinating and soaking rice", "duration_pct": 12},
    {"title": "Heating", "description": "Preheating the cooking chamber", "duration_pct": 8},
    {"title": "Adding ingredients", "description": "Layering rice and fillings", "duration_pct": 18},
    {"title": "Mixing", "description": "Distributing spices evenly across layers", "duration_pct": 10},
    {"title": "Cooking", "description": "Dum cooking on low heat", "duration_pct": 37},
    {"title": "Finalizing", "description": "Resting biryani for aroma infusion", "duration_pct": 10},
    {"title": "Ready to Serve", "description": "Biryani is fragrant and ready!", "duration_pct": 5},
]

CHICKEN_BIRYANI_BATCH = {
    "5kg": [
        {"name": "Chicken", "quantity": "5 kg"},
        {"name": "Basmati rice", "quantity": "5 kg"},
        {"name": "Yogurt", "quantity": "1.5 kg"},
        {"name": "Onions", "quantity": "2.5 kg"},
        {"name": "Ginger-garlic paste", "quantity": "500 g"},
        {"name": "Mint leaves", "quantity": "500 g"},
        {"name": "Coriander powder", "quantity": "500 g"},
        {"name": "Green chilies", "quantity": "250 g"},
        {"name": "Cooking oil", "quantity": "1.5 L"},
        {"name": "Ghee", "quantity": "500 ml"},
        {"name": "Biryani masala", "quantity": "200 g"},
        {"name": "Red chili powder", "quantity": "100 g"},
        {"name": "Turmeric powder", "quantity": "25 g"},
        {"name": "Salt", "quantity": "200 g"},
    ],
    "10kg": [
        {"name": "Chicken", "quantity": "10 kg"},
        {"name": "Basmati rice", "quantity": "10 kg"},
        {"name": "Yogurt", "quantity": "3 kg"},
        {"name": "Onions", "quantity": "5 kg"},
        {"name": "Ginger-garlic paste", "quantity": "1 kg"},
        {"name": "Mint leaves", "quantity": "1 kg"},
        {"name": "Coriander powder", "quantity": "1 kg"},
        {"name": "Green chilies", "quantity": "500 g"},
        {"name": "Cooking oil", "quantity": "3 L"},
        {"name": "Ghee", "quantity": "1 L"},
        {"name": "Biryani masala", "quantity": "400 g"},
        {"name": "Red chili powder", "quantity": "200 g"},
        {"name": "Turmeric powder", "quantity": "50 g"},
        {"name": "Salt", "quantity": "400 g"},
    ],
}

VEG_BIRYANIS = {
    "veg_dum_biryani": {
        "id": "veg_dum_biryani",
        "title": "Veg Dum Biryani",
        "emoji": "🍲",
        "icon_color": "#ff8a00",
        "description": "Slow-cooked vegetable dum biryani",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Mixed vegetables", "quantity": "2.5 cups"},
            {"name": "Fried onions", "quantity": "1 cup"},
            {"name": "Yogurt", "quantity": "1/2 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1.5 tbsp"},
            {"name": "Biryani masala", "quantity": "2 tbsp"},
            {"name": "Mint & coriander", "quantity": "1/2 cup each"},
            {"name": "Whole spices", "quantity": "bay leaf, cardamom, cloves"},
            {"name": "Ghee", "quantity": "3 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "paneer_biryani": {
        "id": "paneer_biryani",
        "title": "Paneer Biryani",
        "emoji": "🧀",
        "icon_color": "#ff6a00",
        "description": "Layered paneer biryani",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Paneer", "quantity": "400 g"},
            {"name": "Onions", "quantity": "2 large"},
            {"name": "Yogurt", "quantity": "1/2 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Biryani masala", "quantity": "2 tbsp"},
            {"name": "Mint & coriander", "quantity": "1/2 cup each"},
            {"name": "Ghee", "quantity": "3 tbsp"},
            {"name": "Saffron milk", "quantity": "1/4 cup"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "mushroom_biryani": {
        "id": "mushroom_biryani",
        "title": "Mushroom Biryani",
        "emoji": "🍄",
        "icon_color": "#c43e00",
        "description": "Aromatic mushroom biryani",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Mushrooms", "quantity": "300 g"},
            {"name": "Onions", "quantity": "2 medium"},
            {"name": "Yogurt", "quantity": "1/3 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Biryani masala", "quantity": "1.5 tbsp"},
            {"name": "Mint & coriander", "quantity": "1/3 cup each"},
            {"name": "Ghee", "quantity": "2 tbsp"},
            {"name": "Green peas", "quantity": "1/2 cup"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
}

NON_VEG_BIRYANIS = {
    "chicken_biryani": {
        "id": "chicken_biryani",
        "title": "Chicken Biryani",
        "emoji": "🍗",
        "icon_color": "#ff6a00",
        "description": "Classic chicken biryani",
        "batch_options": ["5kg", "10kg"],
        "default_batch": "5kg",
        "batch_ingredients": CHICKEN_BIRYANI_BATCH,
        "ingredients": CHICKEN_BIRYANI_BATCH["5kg"],
    },
    "mutton_biryani": {
        "id": "mutton_biryani",
        "title": "Mutton Biryani",
        "emoji": "🥩",
        "icon_color": "#ff8a00",
        "description": "Rich mutton layered biryani",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Mutton", "quantity": "750 g"},
            {"name": "Yogurt", "quantity": "1/2 cup"},
            {"name": "Onions", "quantity": "3 large"},
            {"name": "Ginger-garlic paste", "quantity": "2 tbsp"},
            {"name": "Biryani masala", "quantity": "2.5 tbsp"},
            {"name": "Mint & coriander", "quantity": "1/2 cup each"},
            {"name": "Whole spices", "quantity": "bay leaf, cardamom, cloves"},
            {"name": "Ghee", "quantity": "3 tbsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "egg_biryani": {
        "id": "egg_biryani",
        "title": "Egg Biryani",
        "emoji": "🥚",
        "icon_color": "#ffb300",
        "description": "Spiced egg biryani",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Eggs (boiled)", "quantity": "6 pcs"},
            {"name": "Onions", "quantity": "2 large"},
            {"name": "Yogurt", "quantity": "1/3 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Biryani masala", "quantity": "1.5 tbsp"},
            {"name": "Mint & coriander", "quantity": "1/3 cup each"},
            {"name": "Ghee", "quantity": "2 tbsp"},
            {"name": "Red chili powder", "quantity": "1 tsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
    "fish_biryani": {
        "id": "fish_biryani",
        "title": "Fish Biryani",
        "emoji": "🐟",
        "icon_color": "#ff9a1a",
        "description": "Coastal-style fish biryani",
        "ingredients": [
            {"name": "Basmati rice", "quantity": "2 cups"},
            {"name": "Fish pieces", "quantity": "750 g"},
            {"name": "Onions", "quantity": "2 large"},
            {"name": "Yogurt", "quantity": "1/3 cup"},
            {"name": "Ginger-garlic paste", "quantity": "1 tbsp"},
            {"name": "Biryani masala", "quantity": "1.5 tbsp"},
            {"name": "Mint & coriander", "quantity": "1/3 cup each"},
            {"name": "Ghee / oil", "quantity": "3 tbsp"},
            {"name": "Turmeric powder", "quantity": "1/2 tsp"},
            {"name": "Salt", "quantity": "to taste"},
        ],
    },
}

BIRYANI_CATEGORIES = {
    "veg": {
        "id": "veg",
        "title": "Veg",
        "emoji": "🥦",
        "icon_color": "#ffb300",
        "description": "Veg Dum, Paneer, and Mushroom biryani",
        "items": VEG_BIRYANIS,
    },
    "non_veg": {
        "id": "non_veg",
        "title": "Non-Veg",
        "emoji": "🍖",
        "icon_color": "#ff6a00",
        "description": "Chicken, Mutton, Egg, and Fish biryani",
        "items": NON_VEG_BIRYANIS,
    },
}

RECIPES = {
    "cook_rice": {
        "id": "cook_rice",
        "title": "Cook Rice",
        "emoji": "🍚",
        "icon_color": "#ffb300",
        "description": "Select rice or pulao",
        "machine_enabled": False,
        "has_sub_menu": True,
        "total_cook_seconds": 18,
        "ingredients": [],
        "stages": RICE_STAGES,
    },
    "curry": {
        "id": "curry",
        "title": "Curry",
        "emoji": "🍛",
        "icon_color": "#ffb74d",
        "description": "Select veg or non-veg curry",
        "machine_enabled": False,
        "has_sub_menu": True,
        "total_cook_seconds": 22,
        "ingredients": [],
        "stages": CURRY_STAGES,
    },
    "chicken_biryani": {
        "id": "chicken_biryani",
        "title": "Biryani",
        "emoji": "🍗",
        "icon_color": "#ff6a00",
        "description": "Select veg or non-veg biryani",
        "machine_enabled": True,
        "has_sub_menu": True,
        "machine_item_ids": ["chicken_biryani"],
        "total_cook_seconds": 30,
        "ingredients": [],
        "stages": BIRYANI_STAGES,
    },
}


def get_selected_curry(category_id: str | None, curry_id: str | None) -> dict | None:
    if not category_id or not curry_id:
        return None
    category = CURRY_CATEGORIES.get(category_id)
    if not category:
        return None
    return category["items"].get(curry_id)


def get_selected_rice_item(category_id: str | None, item_id: str | None) -> dict | None:
    if not category_id or not item_id:
        return None
    category = RICE_CATEGORIES.get(category_id)
    if not category:
        return None
    return category["items"].get(item_id)


def get_selected_biryani(category_id: str | None, biryani_id: str | None) -> dict | None:
    if not category_id or not biryani_id:
        return None
    category = BIRYANI_CATEGORIES.get(category_id)
    if not category:
        return None
    return category["items"].get(biryani_id)
