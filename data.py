from json import dump, load


def write_data(file_name='', data=[]):
    with open(file_name, 'w') as outfile:
        dump(data, outfile)

def read_data(file_name=''):
    with open(file_name, 'r') as infile:
        return load(infile)

def get_task(message):
    file_name = input(message)
    if file_name is '':
        exit(0)
    # read the task
    task = None
    try:
        task = read_data(file_name)
    except:
        print('ERROR: "incorrect name of file"')
        task = get_task(message)
    return task