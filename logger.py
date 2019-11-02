

def log_line(line):
    if line[-1] != '\n':
        line += '\n'
    with open('log.txt', 'a') as fh:
        fh.write(line)