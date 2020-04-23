import csv
from datetime import datetime


def write_csv(data_to_write):
    file_name = datetime.strftime(datetime.now(), '%m-%d-%Y %H:%M:%S:%f') + '.csv'
    with open(file_name, mode='w') as open_file:
        data_writer = csv.writer(open_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # TODO convert data_to_write to csv
