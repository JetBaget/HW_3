import ast
import logging.config
import yaml
import os


with open('../etc/log_settings.yml', 'rt') as f:
    config = yaml.load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


def py_files_parser(py_file):
    logger.info('- {}'.format(os.path.basename(py_file)))
    tree = None
    with open(py_file, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        tree = ast.parse(main_file_content)
    except SyntaxError as err:
        print('Ошибка парсинга файла {}: {}'.format(py_file, err))
        logger.error('Ошибка парсинга файла {}: {}'.format(py_file, err))
        exit(1)
    return tree

