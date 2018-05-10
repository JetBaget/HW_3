# -*- coding: utf-8 -*-

import ast
from nltk import pos_tag, word_tokenize

from names_analyzer.utils import flat, collect_pyfiles_in_path, \
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

    :param part_of_speech:          часть речи
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


def _collect_names_in_tree(tree):
    """
    Возвращает список всех имен, содержащихся в синтаксическом дереве

    :param tree:            Объект дерева
    :return:                list
    """
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def _get_all_names_from_path(project_path):
    """
    Возвращает все названия, кроме защищенных

    :param project_path:    Путь к директории с проектом
    :return:                list
    """
    trees = create_syntax_trees(project_path)
    func_names = [n for n in flat([_collect_names_in_tree(t) for t in trees]) if
                  not (n.startswith('__') and n.endswith('__'))]
    return flat([split_under_score_to_words(func_name) for func_name in func_names])


def _get_funcs_names_from_path(project_path):
    """
    Возвращает все названия функций, кроме защищенных

    :param project_path:    Путь к директории с проектом
    :return:                list
    """
    trees = create_syntax_trees(project_path)
    names = [f for f in flat([[node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                              for tree in trees]) if not (f.startswith('__') and f.endswith('__'))]
    return names


def _get_locals_names_from_path(project_path):
    """
    Возвращает список названий локальных переменных, объявленных
    внутри функций

    :param project_path:           Путь к директории с проектом
    :return:
    """
    trees = create_syntax_trees(project_path)
    func_nodes = flat([[node.body for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees])
    locals = flat([[a.targets[0].id for a in n if isinstance(a, ast.Assign)] for n in func_nodes])
    return locals


def get_names_from_path(project_path, target='all'):
    """
    Возвращает список названий функций, локальных переменных, или всех имен
    в зависимости от значения параметра target

    :param project_path:            Путь к репозиторию с проектом
    :param target:                  Цель анализа
    :return:
    """
    result = None
    if target == 'all':
        result = _get_all_names_from_path(project_path)
    elif target == 'funcs':
        result = _get_funcs_names_from_path(project_path)
    elif target == 'locals':
        result = _get_locals_names_from_path(project_path)
    return result


def filter_words_by_part_of_speech(part_of_speech, name):
    """
    Фильтрует слова по части речи

    :param part_of_speech:          Часть речи
    :param name:                    Слово
    :return:                        Список слов соответствующей части речи
    """
    words = split_under_score_to_words(name)
    tags = pos_tag(word_tokenize(' '.join(words)))
    return [t[0] for t in tags if check_part_of_speech(part_of_speech, t)]


def pick_top_words_by_part_of_speech(path, target, part_of_speech, top_size=3):
    """
    Делает выборку самых популярных глаголов

    :param path:                Путь к директории
    :param target:              Цель анализа
    :param part_of_speech:      Часть речи
    :param top_size:            Объём выборки
    :return:                    list of tuples
    """
    func_names = get_names_from_path(path, target)
    words = flat([filter_words_by_part_of_speech(part_of_speech, n) for n in func_names])
    return pick_top_from_iterable(words, top_size)
