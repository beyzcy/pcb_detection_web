DEFECT_TYPES = [
    "Short Circuit",
    "Open Circuit",
    "Missing Hole",
    "Mouse Bite",
    "Spur",
    "Excess Copper",
]

BADGE_MAP: dict[str, str] = {
    "Short Circuit": "badge-red",
    "Open Circuit":  "badge-red",
    "Missing Hole":  "badge-yellow",
    "Mouse Bite":    "badge-yellow",
    "Spur":          "badge-yellow",
    "Excess Copper": "badge-blue",
}

DEFECT_COLORS: dict[str, tuple[int, int, int]] = {
    "Short Circuit": (255,  50,  50),
    "Open Circuit":  (255, 120,   0),
    "Missing Hole":  (255, 210,   0),
    "Mouse Bite":    (200, 100, 255),
    "Spur":          (  0, 200, 100),
    "Excess Copper": (  0, 165, 255),
}
