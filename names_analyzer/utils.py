import os
from collections import Counter
from git import Repo
import logging.config
import yaml

from data_savers import save_to_display, save_to_csv, save_to_json

with open('../etc/log_settings.yml', 'rt') as f:
    config = yaml.load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


def flatten_list(_list):
    return [i for v in _list for i in v]


def collect_files_in_dir(inspected_path, programming_language):
    format_mapping = {'python': '.py'}
    file_format = format_mapping.get(programming_language.lower())
    if not file_format:
        print('Отсутствует обработчик файлов языка {}'.format(programming_language))
        logger.error('Отсутствует обработчик файлов для языка {}'.format(programming_language))
    collected_files = []
    for root, dirs, files in os.walk(inspected_path, topdown=True):
        for file in files:
            if not file.endswith(file_format):
                continue
            collected_files.append(os.path.join(root, file))
    return collected_files


def split_under_score_to_words(name):
    return [n for n in name.split('_') if n]


def pick_top_from_iterable(iterable, top_size=3):
    return Counter(iterable).most_common(top_size)


def clone_git_repo(git_url, repo_path):
    try:
        Repo.clone_from(git_url, repo_path)
    except Exception as err:
        print('Ошибка в процессе клонирования GIT-репозитория: {}'.format(err))
        logger.error('Ошибка в процессе клонирования GIT-репозитория: {}'.format(err))


def save_data(type_of_source, data, file_path=None):
    savers_mapping = {'console': save_to_display,
                      'csv': save_to_csv,
                      'json': save_to_json}
    saver = savers_mapping.get(type_of_source)
    if not saver:
        print('Отсутствует функция для сохранения в {}'.format(type_of_source))
        logger.error('Отсутствует функция для сохранения в {}'.format(type_of_source))
    saver(data, file_path)
