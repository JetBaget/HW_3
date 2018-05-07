# -*- coding: utf-8 -8-

import argparse
import os
import sys
from func_names_analyzer.syntax_analyze import pick_top_words_by_speech_part
from func_names_analyzer.utils import save_data, clone_git_repo


if __name__ == '__main__':
    print('Выберете действие:\n1. Получить код из источника\n2. Проанализировать проект в локальной директории\n')
    start = int(input())
    if start == 1:
        print('Выберите источник:\n1. GitHub\n')
        code_source = int(input())
        if code_source == 1:
            git_url = str(input('Введите url-адрес GIT-репозитория: '))
            repo_path = str(input('Введите путь к локальной директории: '))
            clone_git_repo(git_url, repo_path)
    elif start == 2:
        repo_path = str(input('Введите путь к локальному репозиторию с проектом: '))
        if not os.path.exists(repo_path):
            print('Указанный репозиторий не существует в файловой системе')
    print('Выберите часть речи, для которой вы хотите провести анализ:\n1. Глагол\n2. Существительное\n')
    parts_of_speech = {1: 'verb', 2: 'noun'}
    pos = parts_of_speech.get(int(input()))
    if not pos:
        print('Неверное значение')
    print('Определите, какие объекты будут проанализированы:\n1. Имена функций\n2. Локальные переменные\n')
    target = int(input())

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--in_path', nargs='?', default='/root/work_venv/Testing', help='Путь к директории проекта')
    parser.add_argument('-s', '--part_of_speech', nargs='?', default='verb', help='Часть речи для анализа')
    parser.add_argument('-d', '--destination', nargs='?', default='console', help='Куда сохранить результат')
    args = parser.parse_args(sys.argv[1:])

    project_path = args.in_path
    part_of_speech = args.part_of_speech
    saving_dest = args.destination

    if not os.path.exists(project_path):
        print('Указанный путь не существует в файловой системе')
        exit(1)
    data = pick_top_words_by_speech_part(project_path, part_of_speech)
    save_data(saving_dest, data, '/root/work_venv/Testing/DZ_3/my.json')
