"""
utils.py
========
Utility helpers for the Smart Agriculture Decision Support System.
Provides agronomic guidance, formatting helpers, and constants.

Author  : BSE-6 Student, Bahria University Islamabad
Course  : Artificial Intelligence (CLO-2 OEL)
Version : 1.0.0
"""

import os
import json
from datetime import datetime
 
# ─────────────────────────────────────────────
# Cluster → Agronomic Profile Mapping
# ─────────────────────────────────────────────
CLUSTER_PROFILES = {
    0: {
        "name"    : "High-Nutrient Tropical Zone",
        "color"   : "#2ecc71",
        "icon"    : "🌿",
        "guidance": (
            "Soil in this zone shows elevated NPK ratios, high humidity, and warm "
            "temperatures — ideal for high-demand tropical crops such as banana, "
            "papaya, and sugarcane. Prioritise irrigation scheduling; excess rainfall "
            "may cause leaching of Potassium."
        ),
        "crops"   : ["banana", "papaya", "watermelon", "coconut"],
        "actions" : [
            "Apply balanced NPK fertiliser at planting stage.",
            "Monitor soil moisture weekly; maintain field capacity.",
            "Conduct foliar spray for micro-nutrients mid-season.",
        ]
    },
    1: {
        "name"    : "Arid Low-Phosphorus Zone",
        "color"   : "#e67e22",
        "icon"    : "🌵",
        "guidance": (
            "Characterised by low rainfall, moderate temperature, and below-average "
            "phosphorus levels. Best suited for drought-tolerant pulses (mothbeans, "
            "mungbean) and coarse cereals. Implement drip irrigation to conserve "
            "water resources."
        ),
        "crops"   : ["mothbeans", "mungbean", "lentil", "chickpea"],
        "actions" : [
            "Apply single super-phosphate to correct P deficiency.",
            "Use drip/sprinkler irrigation; avoid flood irrigation.",
            "Incorporate organic compost to improve water retention.",
        ]
    },
    2: {
        "name"    : "Moderate Temperate Zone",
        "color"   : "#3498db",
        "icon"    : "🌾",
        "guidance": (
            "Well-balanced NPK, moderate rainfall, and temperate climate make this "
            "zone highly versatile. Rice, maize, and wheat perform excellently. Rotate "
            "cereals with legumes to maintain soil nitrogen naturally."
        ),
        "crops"   : ["rice", "maize", "jute", "cotton"],
        "actions" : [
            "Practise cereal-legume crop rotation annually.",
            "Apply Urea split (50% basal, 50% top-dress at tillering).",
            "Test soil pH each season; apply lime if pH < 5.5.",
        ]
    },
    3: {
        "name"    : "High-Potassium Orchard Zone",
        "color"   : "#9b59b6",
        "icon"    : "🍎",
        "guidance": (
            "Elevated potassium and phosphorus with cooler temperatures define this "
            "zone, which is optimal for fruit orchards (apple, grapes, mango, orange). "
            "Maintain slightly acidic pH (5.8–6.5) for maximum nutrient availability."
        ),
        "crops"   : ["apple", "grapes", "mango", "orange", "pomegranate"],
        "actions" : [
            "Apply Muriate of Potash before flowering stage.",
            "Maintain pH 5.8–6.5; use sulphur amendment if pH > 6.8.",
            "Schedule dormant pruning and integrated pest management.",
        ]
    },
    4: {
        "name"    : "High-Humidity Wetland Zone",
        "color"   : "#1abc9c",
        "icon"    : "💧",
        "guidance": (
            "Very high humidity paired with moderate NPK and ample rainfall. Ideal "
            "for moisture-loving crops such as rice (paddy), jute, and coffee. "
            "Ensure adequate drainage to prevent waterlogging and root diseases."
        ),
        "crops"   : ["rice", "jute", "coffee", "blackgram"],
        "actions" : [
            "Construct field drainage channels before sowing.",
            "Apply Zinc Sulphate (25 kg/ha) for paddy crops.",
            "Monitor for fungal diseases; apply prophylactic fungicide.",
        ]
    },
}


CROP_EMOJIS = {
    'rice':'🌾','maize':'🌽','chickpea':'🫘','kidneybeans':'🫘',
    'pigeonpeas':'🫘','mothbeans':'🫘','mungbean':'🫘','blackgram':'🫘',
    'lentil':'🫘','pomegranate':'🍎','banana':'🍌','mango':'🥭',
    'grapes':'🍇','watermelon':'🍉','muskmelon':'🍈','apple':'🍎',
    'orange':'🍊','papaya':'🍑','coconut':'🥥','cotton':'🌸',
    'jute':'🌿','coffee':'☕',
}

CROP_DESCRIPTIONS = {
    'rice'       : 'High water demand; paddy or upland varieties',
    'maize'      : 'Versatile cereal; needs good drainage',
    'chickpea'   : 'Pulse crop; fixes atmospheric nitrogen',
    'kidneybeans': 'Legume; cool temperate preferred',
    'pigeonpeas' : 'Drought-tolerant pulse; intercrop friendly',
    'mothbeans'  : 'Highly drought-resistant; arid zones',
    'mungbean'   : 'Short-duration pulse; warm humid',
    'blackgram'  : 'Pulse; prefers loamy well-drained soil',
    'lentil'     : 'Cool-season legume; minimal water need',
    'pomegranate': 'Fruit; tolerates mild drought',
    'banana'     : 'High-yield fruit; tropical humid zones',
    'mango'      : 'Tropical deciduous fruit tree',
    'grapes'     : 'Vine crop; high K requirement',
    'watermelon' : 'Summer fruit; long growing season',
    'muskmelon'  : 'Low rainfall; sandy loam preferred',
    'apple'      : 'Temperate fruit; chilling hours required',
    'orange'     : 'Citrus; sub-tropical climate',
    'papaya'     : 'Fast-growing tropical fruit',
    'coconut'    : 'Palm; coastal and humid tropics',
    'cotton'     : 'Fibre crop; high nitrogen demand',
    'jute'       : 'Fibre crop; waterlogged fertile soils',
    'coffee'     : 'Beverage crop; shaded humid highlands',
}


def get_cluster_profile(cluster_id: int) -> dict:
    return CLUSTER_PROFILES.get(cluster_id, CLUSTER_PROFILES[0])


def get_crop_emoji(crop: str) -> str:
    return CROP_EMOJIS.get(crop.lower(), '🌱')


def get_crop_description(crop: str) -> str:
    return CROP_DESCRIPTIONS.get(crop.lower(), 'Agricultural crop')


def format_metrics_dt(metrics: dict) -> str:
    return (
        f"  Accuracy   : {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)\n"
        f"  Precision  : {metrics['precision']:.4f}\n"
        f"  Recall     : {metrics['recall']:.4f}\n"
        f"  F1-Score   : {metrics['f1']:.4f}\n"
    )


def format_metrics_reg(metrics: dict) -> str:
    return (
        f"  RMSE  : {metrics['rmse']:.4f} q/ha\n"
        f"  MAE   : {metrics['mae']:.4f} q/ha\n"
        f"  R²    : {metrics['r2']:.4f}\n"
    )


def format_metrics_clust(metrics: dict) -> str:
    return (
        f"  Silhouette      : {metrics['silhouette']:.4f}\n"
        f"  Davies-Bouldin  : {metrics['davies_bouldin']:.4f}\n"
        f"  Inertia         : {metrics['inertia']:.1f}\n"
    )


def save_metrics_json(all_metrics: dict, results_dir: str):
    os.makedirs(results_dir, exist_ok=True)
    ts   = datetime.now().strftime('%Y%m%d_%H%M%S')
    path = os.path.join(results_dir, f'metrics_{ts}.json')

    serialisable = {}
    for key, val in all_metrics.items():
        serialisable[key] = {
            k: (v.tolist() if hasattr(v, 'tolist') else v)
            for k, v in val.items()
            if not isinstance(v, dict)
        }
    with open(path, 'w') as f:
        json.dump(serialisable, f, indent=2)
    print(f"[✓] Metrics saved → {path}")


def get_input_ranges():
    """Return valid input ranges for GUI validation."""
    return {
        'N'          : (0,   140),
        'P'          : (5,   145),
        'K'          : (5,   205),
        'temperature': (8,    44),
        'humidity'   : (14,  100),
        'ph'         : (3.5, 9.9),
        'rainfall'   : (20,  300),
    }


def validate_inputs(values: dict) -> tuple[bool, str]:
    """Return (is_valid, error_message)."""
    ranges = get_input_ranges()
    for key, val in values.items():
        lo, hi = ranges[key]
        if not (lo <= val <= hi):
            return False, f"'{key}' must be between {lo} and {hi}. Got {val}."
    return True, ""
