DEFECT_TYPES = [
    "Short Circuit",
    "Open Circuit",
    "Solder Bridge",
    "Missing Component",
]

BADGE_MAP: dict[str, str] = {
    "Short Circuit":     "badge-red",
    "Open Circuit":      "badge-yellow",
    "Solder Bridge":     "badge-yellow",
    "Missing Component": "badge-blue",
}

DEFECT_COLORS: dict[str, tuple[int, int, int]] = {
    "Short Circuit":     (255,  50,  50),
    "Open Circuit":      (255, 165,   0),
    "Solder Bridge":     (255, 220,   0),
    "Missing Component": (  0, 165, 255),
}
