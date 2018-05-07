# -*- coding: utf-8 -*-

import ast
from nltk import pos_tag, word_tokenize

from func_names_analyzer.utils import flat, collect_pyfiles_in_path, \
    split_under_score_to_words, pick_top_from_iterable


def create_syntax_trees(inspected_path, with_file_names=False, with_file_content=False):
    """
    Возвращает список абстрактных синтаксических деревьев для всех .py файлов,
    содержащихся в указанной директории/поддиректориях.
    В зависимости от значений ключей with_file_names, with_file_content добавляется
    информация об имени файла и его содержимом, соответственно.

    :param inspected_path:              Путь к директории, где будет выполняться поиск .py-файлов
    :param with_file_names:             Флаг, добавляющий название файла
    :param with_file_content:           Флаг, добавляющий содержимое файла
    :return:                            list
    """
    trees = []
    py_files = collect_pyfiles_in_path(inspected_path)
    for py_file in py_files:
        with open(py_file, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        try:
            tree = ast.parse(main_file_content)
            tree_data = tree
            if with_file_names and with_file_content:
                tree_data = (py_file, main_file_content, tree)
            elif with_file_names:
                tree_data = (py_file, tree)
            trees.append(tree_data)
        except SyntaxError:
            pass
    return trees


def check_part_of_speech(part_of_speech, tagged):
    """
    Прповеряет слово на соответствие части речи

    :param part_of_speech:          часть речи (str)
    :param tagged:                  кортеж (слово, тег части речи)
    :return:                        boolean
    """
    result = None
    if not tagged:
        return False
    if part_of_speech.lower() == 'noun':
        result = 'NN' in tagged[1]
    elif part_of_speech.lower() == 'verb':
        result = tagged[1] in ['VB']
    return result


def get_all_names_from_tree(tree):
    """
    Возвращает список всех имен, содержащихся в синтаксическом дереве

    :param tree:            Объект дерева
    :return:                list
    """
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def select_speech_part_words(part_of_speech, name):
    """
    Извлекает из названий функций глаголы

    :param part_of_speech:          Часть речи
    :param name:                    Название (str)
    :return:                        Список слов, соответствующей части речи
    """
    words = split_under_score_to_words(name)
    tags = pos_tag(word_tokenize(' '.join(words)))
    return [t[0] for t in tags if check_part_of_speech(part_of_speech, t)]


def get_all_names_in_path(path):
    """
    Возвращает все названия, кроме защищенных

    :param path:            Путь к директории
    :return:                list
    """
    trees = create_syntax_trees(path)
    func_names = [n for n in flat([get_all_names_from_tree(t) for t in trees]) if
                  not (n.startswith('__') and n.endswith('__'))]
    return flat([split_under_score_to_words(func_name) for func_name in func_names])


def get_all_func_names_in_path(path):
    """
    Возвращает все названия функций, кроме защищенных

    :param path:            Путь к директории
    :return:                list
    """
    trees = create_syntax_trees(path)
    names = [f for f in flat([[node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                              for tree in trees]) if not (f.startswith('__') and f.endswith('__'))]
    return names


def pick_top_func_names(path, top_size=3):
    """
    Делает выборку самых популярных названий функций

    :param path:                Путь к директории
    :param top_size:            Объём выборки
    :return:                    list of tuples
    """
    func_names = get_all_func_names_in_path(path)
    return pick_top_from_iterable(func_names, top_size)


def pick_top_words_by_speech_part(path, part_of_speech, top_size=3):
    """
    Делает выборку самых популярных глаголов

    :param path:                Путь к директории
    :param part_of_speech:      Часть речи
    :param top_size:            Объём выборки
    :return:                    list of tuples
    """
    func_names = get_all_func_names_in_path(path)
    verbs = flat([select_speech_part_words(part_of_speech, n) for n in func_names])
    return pick_top_from_iterable(verbs, top_size)


# Нужно доработать скрипт из первого задания. Вот что он должен уметь:

# * клонировать репозитории с Гитхаба;
# * выдавать статистику самых частых слов по глаголам или существительным (в зависимости от параметра отчёта);
# выдавать статистику самых частых слов названия функций или локальных переменных внутри функций (в зависимости от параметра отчёта);
# * выводить результат в консоль, json-файл или csv-файл (в зависимости от параметра отчёта);
# * принимать все аргументы через консольный интерфейс.
# При доработке предусмотреть, что вскоре в программу понадобится добавлять:

    # получение кода из других мест, не только с Гитхаба;
    # парсеры других ЯП, не только Python;
    # сохранение в кучу разных форматов;
    # более сложные типы отчётов (не только частота частей речи в различных местах кода).
