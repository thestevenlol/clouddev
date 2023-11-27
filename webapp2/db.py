from DBcm import UseDatabase
import os
from datetime import datetime, timedelta

dataset_path = r""


def ingest(dataset, debug):
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
        if debug:
            _SQL = """delete from times where swimmer_id > 0;"""
            cursor.execute(_SQL)

            _SQL = """delete from swimmers where id > 0;"""
            cursor.execute(_SQL)

            _SQL = """alter table swimmers auto_increment = 1;"""
            cursor.execute(_SQL)

            _SQL = """delete from events where id > 0;"""
            cursor.execute(_SQL)

            _SQL = """alter table events auto_increment = 1;"""
            cursor.execute(_SQL)

        swimmer_table_data = set()
        events_table_data = set()

        names = []
        events = set()



            # if (distance, stroke) not in events:
            #     events.add((distance, stroke))
            #     _SQL = f"""insert into events (distance, stroke) values ({distance}, '{stroke}');"""
            #     cursor.execute(_SQL)
            #
            # if name not in names:
            #     names.append(name)
            #     _SQL = f"""insert into swimmers (name, age) values ('{name}', {age});"""
            #     cursor.execute(_SQL)
            #
            # _SQL = f"""select id from swimmers where name = '{name}' and age = {int(age)};"""
            # cursor.execute(_SQL)
            # swimmer_id = cursor.fetchone()[0]
            # if swimmer_id is None:
            #     pass
            #
            # _SQL = f"""select id from events where distance = {distance} and stroke = '{stroke}';"""
            # cursor.execute(_SQL)
            # event_id = cursor.fetchone()[0]
            #
            # lines = read_file(dataset, f"{f}.txt")
            # for line in lines:
            #     line = line.removesuffix("\n")
            #     times = line.split(",")
            #     for time in times:
            #         _SQL = f"""insert into times (swimmer_id, event_id, time) values ({swimmer_id}, {event_id}, '{time}');"""
            #         cursor.execute(_SQL)



def get_files(dataset):
    path = rf"{dataset_path}{dataset}"
    return os.listdir(path)


def read_file(dataset, filename):
    path = rf"{dataset_path}{dataset}/{filename}"
    with open(path) as f:
        return f.readlines()


ingest("dataset_2", True)