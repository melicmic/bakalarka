import datetime

# Vytvoření objektu datetime


def dlouhe_datum():
    custom_format = "%Y-%m-%d %H:%M:%S"
    dt = datetime.datetime.now()
    formatted_datetime = dt.strftime(custom_format)
    return formatted_datetime

def kratke_datum():
    custom_format = "%Y-%m-%d"
    dt = datetime.datetime.now()
    formatted_datetime = dt.strftime(custom_format)
    return formatted_datetime

def rok():
    dt = datetime.datetime.now()
    formatted_datetime = dt.year
    return formatted_datetime

