import argparse
import sys
import logging.config
import yaml

from syntax_analyze import pick_top_words_by_part_of_speech
from utils import save_data, clone_git_repo

with open('../etc/log_settings.yml', 'rt') as f:
    config = yaml.load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--source_type', choices=['local', 'github'],
                        default=('local', None), help='Источник кода, url(опционально)')
    parser.add_argument('-p', '--path', nargs='?', default='.', help='Путь к директории проекта')
    parser.add_argument('-l', '--language', choices=['python'], default='python',
                        help='Язык программирования')
    parser.add_argument('-s', '--part_of_speech', choices=['verb', 'noun'], default='ver',
                        help='Часть речи для анализа')
    parser.add_argument('-o', '--target_object', choices=['funcs', 'locals', 'all'], default='funcs',
                        help='Объекты для анализа')
    parser.add_argument('-d', '--destination', choices=['console', 'json', 'csv'], default='console',
                        help='Способ сохранения результата')
    args = parser.parse_args(sys.argv[1:])

    source_type = args.source_type
    repo_path = args.path
    part_of_speech = args.part_of_speech
    target = args.target_object
    saving_dest = args.destination
    prog_lang = args.language

    prepare_func_mapping = {'github': clone_git_repo}

    prepare_func = prepare_func_mapping.get(source_type[0])
    if prepare_func:
        prepare_func(source_type[1], repo_path)

    for i in range(2):
        try:
            logger.info('Скрипт запущен...')
            logger.info('Параметры запуска: тип источника: {}, путь: {}, язык: {}, часть речи: {},'
                        ' объекты анализа: {}, сохранение в {}'
                        .format(source_type, repo_path, prog_lang, part_of_speech, target, saving_dest))
            data = pick_top_words_by_part_of_speech(repo_path, prog_lang, target, part_of_speech)
            save_data(saving_dest, data)
            logger.info('Работа скрипта успешно завершена')
            break
        except LookupError as err:
            print('Первый запуск. Будут загружены вспомогательные файлы для nltk...')
            logger.info('Первый запуск. Будут загружены вспомогательные файлы для nltk...')
            import nltk
            nltk.download('punkt')
            nltk.download('averaged_perceptron_tagger')
            continue
