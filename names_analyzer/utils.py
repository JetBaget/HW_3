# -*- coding: utf-8 -8-

import os
import json
import csv
from collections import Counter
from git import Repo


def flat(_list):
    return [i for v in _list for i in v]


def collect_py_files_in_dir(inspected_path):
    py_files = []
    for root, dirs, files in os.walk(inspected_path, topdown=True):
        for file in files:
            if not file.endswith('.py'):
                continue
            py_files.append(os.path.join(root, file))
    return py_files


def split_under_score_to_words(name):
    return [n for n in name.split('_') if n]


def pick_top_from_iterable(iterable, top_size=3):
    return Counter(iterable).most_common(top_size)


def clone_git_repo(git_url, repo_path):
    Repo.clone_from(git_url, repo_path)


def save_data(type_of_source, data, file_path=None):
    if type_of_source == 'console':
        print('Топ используемых слов:')
        print('=' * 24)
        for pair in data:
            print('| {:15s} | {:2d} |'.format(*pair))
        print('=' * 24)
    elif type_of_source == 'json':
        save_as_json(data, file_path)
    elif type_of_source == 'csv':
        save_as_csv(data, file_path)


def save_as_json(data, file_path):
    with open(file_path, 'w') as f:
        f.write(json.dumps(data))


def save_as_csv(data, file_path):
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        [writer.writerow(d) for d in data]
