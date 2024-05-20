import csv


def read_csv(path):
    try:
        with open(path) as csvfile:
            file_reader = csv.reader(csvfile, delimiter=' ')
            for row in file_reader:
                print(', '.join(row))
    except:
         print('invalid path')

        

