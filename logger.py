

def log_line(line):
    try:
        if line[-1] != '\n':
            line += '\n'
    except TypeError:
        line = str(line)
    with open('log.txt', 'a') as fh:
        fh.write(line)