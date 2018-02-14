import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

def load(directory, filename):
    filepath = os.path.join(root_dir, directory, filename + '.csv')
    with open(filepath) as f:
        mode = next(f).strip()
        f_iter = (line.strip() for line in f)
        if mode in ['list', 'set']:
            return eval(mode)(f_iter)
        raise Exception('{} Not implemented yet'.format(mode))
