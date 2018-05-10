# -*- coding: utf-8 -8-

import argparse
import sys

from names_analyzer.syntax_analyze import pick_top_words_by_part_of_speech
from names_analyzer.utils import save_data, clone_git_repo
from names_analyzer.exceptions import GitCloneRepoError


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add_code', choices=[True, False], default=False,
                        help='Признак необходимости получить код из внешнего источника')
    parser.add_argument('-p', '--path', nargs='?', default=None, help='Путь к директории проекта')
    parser.add_argument('-s', '--part_of_speech', choices=['verb', 'noun'], nargs='?', default='verb', help='Часть речи для анализа')
    parser.add_argument('-t', '--analyze_target', choices=['funcs', 'locals', 'all'], nargs='?', default='funcs',
                        help='Объекты для анализа')
    parser.add_argument('-d', '--destination', choices=['console', 'json', 'csv'], nargs='?', default='console',
                        help='Куда сохранить результат')
    args = parser.parse_args(sys.argv[1:])

    add_code = args.add_code
    repo_path = args.path
    part_of_speech = args.part_of_speech
    target = args.analyze_target
    saving_dest = args.destination

    data = pick_top_words_by_part_of_speech(repo_path, target, part_of_speech)
    save_data(saving_dest, data)