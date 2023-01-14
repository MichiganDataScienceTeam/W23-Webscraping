def read_in_art(file, replace=True):
    with open(file, 'r') as f:
        lines = f.readlines()

    length = max([len(x) for x in lines])

    return_lines = []
    for line in lines:
        if replace:
            line = line.strip()
            line = line.replace(' ', 'H')
            line += ('H' * (length - len(line)))
        else:
            line = line[1:]

        return_lines.append(line)

    return return_lines
