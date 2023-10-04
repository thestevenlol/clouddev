import os

directory = "../../pydata/swimdata"

def get_names():
    filenames = []
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            if filename.endswith(".txt"):
                filenames.append(filename)

    return filenames

def split_filename(filename):
    return filename.removesuffix(".txt").split("-")

def get_name(name):
    files = []
    for f in get_names():
        s = split_filename(f)
        if s[0].lower() == name.lower():
            files.append(f) 

    return files

def get_lengths(files, length):
    lengths = None
    for f in files:
        s = split_filename(f)
        if s[2].lower() == length.lower():
            lengths = f

    return lengths

def get_types(files, t):
    types = []
    for f in files:
        s = split_filename(f)
        if s[3].lower() == t.lower():
            types.append(f)

    return types

def read_times(filename):
    with open(os.path.join(directory, filename), "r") as f:
        return f.read()
    
def split_times(times):
    return times.split(",")

def menu():
    printed = []
    names = [];
    print("Please choose a name...")
    i = 0
    for filename in get_names():
        arr = split_filename(filename=filename)
        if arr[0] in printed:
            continue
        i = i + 1
        print(f'{i}. {arr[0]}, {arr[1]}')
        printed.append(arr[0])

    for printedFile in printed:
        name = printedFile.split('-')[0]
        names.append(name)

    choice = input("Please enter a swimmer number: ")
    print(choice)
    while (int(choice) < 1 or int(choice) > i):
        print("Invalid swimmer number!")
        choice = input("Please enter a swimmer number: ")

    name = choice
    print(names[int(name) - 1])
    print("Choose a swimming distance...")
    named_files = get_name(name)
    print(named_files)

menu()