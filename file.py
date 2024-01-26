import os

def init_file_path():
    #file directory setup: "/data/cache.txt"
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'cache.txt')
    return file_path

def load_previous_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file_path)
            lines = file.readlines()
            return [line.strip() for line in lines]
    except FileNotFoundError:
        print("error")
        return []
    
def save_previous_lines(file_path, lines):
    print("attempting save")
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line + '\n')