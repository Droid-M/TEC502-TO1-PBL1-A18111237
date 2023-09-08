def compare_dicts(old, new, watched_keys):
    modified_values = {}
    for key in watched_keys:
        if key in old and key in new:
            if old[key] != new[key]:
                modified_values[key] = (old[key], new[key])
    return modified_values