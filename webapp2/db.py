from DBcm import UseDatabase
import os

datasets = ("dataset_1", "dataset_2")
dataset_path = r""


def ingest(dataset):
    config = {
        "host": "localhost",
        "database": "swimmers_webapp",
        "user": "admin",
        "password": "swimmerspwd"
    }

    files = get_files(dataset)
    if ".DS_Store" in files:
        files.remove(".DS_Store")

    # start db connection
    with UseDatabase(config) as cursor:
        _SQL = """delete from swimmers where id > 0;"""
        cursor.execute(_SQL)

        _SQL = """alter table swimmers auto_increment = 1;"""
        cursor.execute(_SQL)

        _SQL = """delete from events where id > 0;"""
        cursor.execute(_SQL)

        _SQL = """alter table events auto_increment = 1;"""
        cursor.execute(_SQL)

        names = []
        distances = []
        strokes = []

        for f in files:
            f = f.removesuffix(".txt")
            split_text = f.split("-")
            name = split_text[0]
            age = int(split_text[1])

            distance = int(split_text[2].removesuffix("m"))
            stroke = split_text[3]

            if distance not in distances:
                distances.append(distance)
                if stroke not in strokes:
                    strokes.append(stroke)
                    _SQL = f"""insert into events (distance, stroke) values ({distance}, '{stroke}')"""
                    cursor.execute(_SQL)

            if name not in names:
                names.append(name)
                _SQL = f"""insert into swimmers (name, age) values ('{name}', {age});"""
                cursor.execute(_SQL)


def get_files(dataset):
    path = rf"{dataset_path}{dataset}"
    return os.listdir(path)


def read_file(dataset, filename):
    path = rf"{dataset_path}{dataset}/{filename}"
    with open(path) as f:
        return f.readlines()


ingest("dataset_1")