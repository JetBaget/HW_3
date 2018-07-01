import json
import csv


def save_to_display(data, file_path=None):
    print('Топ используемых слов:')
    print('=' * 24)
    for pair in data:
        print('| {:15s} | {:2d} |'.format(*pair))
    print('=' * 24)


def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        f.write(json.dumps(data))


def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        [writer.writerow(d) for d in data]