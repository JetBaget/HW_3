# -*- coding: utf-8 -8-

import os
import json
import csv
from collections import Counter
from git import Repo


def flat(_list):
    """
    Разворачивает вложенные массивы в один список
    [[1,2], [3,4,5], [6]] -> [1,2,3,4,5,6]

    :param _list:           Список, содержащий вложенные массивы
    :return:                Список элементов вложенных массивов
    """
    return [i for v in _list for i in v]


def collect_pyfiles_in_path(inspected_path):
    """
    Возвращает список .py-файлов, найденных рекурсивно в директории dir_path

    :param inspected_path:      Путь к директории, где будет выполняться поиск .py-файлов
    :return:                    list
    """
    pathes_to_pyfiles = []
    for root, dirs, files in os.walk(inspected_path, topdown=True):
        for file in files:
            if not file.endswith('.py'):
                continue
            pathes_to_pyfiles.append(os.path.join(root, file))
            if len(pathes_to_pyfiles) == 100:
                break
    return pathes_to_pyfiles


def split_under_score_to_words(name):
    """
    Разбивает название в snake_case на слова

    :param name:            Название в snake_case
    :return:                list
    """
    return [n for n in name.split('_') if n]


def pick_top_from_iterable(iterable, top_size=3):
    """
    Возвращает наиболее часто встречающиеся элементы последовательности.
    Размер выборки задается параметром top_size (по умолчанию равен 5)

    :param iterable:            Объект с поддержкой протокола итератора
    :param top_size:            Объём выборки
    :return:                    Список кортежей
    """
    return Counter(iterable).most_common(top_size)


def clone_git_repo(git_url, repo_path):
    """
    Выполняет клонирование git-репозитория в указанную директорию

    :param repo_dir_name:               Директория в файловой системе
    :param git_url:                     url git-репозитория
    :return:                            None
    """
    Repo.clone_from(git_url, repo_path)


def save_data(type_of_source, data, file_path=None):
    """
    Сохраняет (отображает в консоли) данные, представляющие
    собой список кортежей [(слово, количество), ...]

    :return:            None
    """
    if type_of_source == 'console':
        print('Наиболее часто используемые слова:')
        print('=' * 24)
        for pair in data:
            print('| {:15s} | {:2d} |'.format(*pair))
        print('=' * 24)
    elif type_of_source == 'json':
        save_as_json(data, file_path)
    elif type_of_source == 'csv':
        save_as_csv(data, file_path)


def save_as_json(data, file_path):
    """
    Сохраняет данные в json-файл

    :param data:            Список кортежей
    :param file_path:       Путь к файлу в файловой системе
    :return:                None
    """
    with open(file_path, 'w') as f:
        f.write(json.dumps(data))


def save_as_csv(data, file_path):
    """
    Сохраняет данные в csv-файл

    :param data:            Список кортежей
    :param file_path:       Путь к файлу в файловой системе
    :return:                None
    """
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        [writer.writerow(d) for d in data]
