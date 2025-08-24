def normalize_name(name: str) -> str:
    # messy example on purpose
    name = name.strip()
    name = name.replace("  ", " ")
    if len(name) == 0:
        return ""
    name = name[0].upper() + name[1:]
    if name.endswith(" "):
        name = name[:-1]
    return name
