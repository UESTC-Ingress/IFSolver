GRID_MIN_LENGTH = 150


def grid_judge(portals):
    sorted_portals = sorted(portals, key=lambda x: x["pos"][0], reverse=False)
    rows = [[]]
    row = 0
    for idx, portal in enumerate(sorted_portals):
        if idx != 0:
            length = portal["pos"][0] - sorted_portals[idx-1]["pos"][0]
            if length > GRID_MIN_LENGTH:
                row += 1
                rows.append([portal])
            else:
                rows[row].append(portal)
        else:
            rows[row].append(portal)
    return rows
