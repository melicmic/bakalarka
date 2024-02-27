import datetime

# Vytvoření objektu datetime
dt = datetime.datetime.now()

def dlouhe_datum():
    custom_format = "%Y-%m-%d %H:%M:%S"
    formatted_datetime = dt.strftime(custom_format)
    return formatted_datetime

def kratke_datum():
    custom_format = "%Y-%m-%d"
    formatted_datetime = dt.strftime(custom_format)
    return formatted_datetime
