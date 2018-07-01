import ast
from nltk import pos_tag, word_tokenize
import yaml
import logging.config

from utils import flatten_list, collect_files_in_dir, split_under_score_to_words
from utils import pick_top_from_iterable

from parsers import py_files_parser

with open('../etc/log_settings.yml', 'rt') as f:
    config = yaml.load(f.read())
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


def create_syntax_trees(inspected_path, programming_language):
    syntax_trees = []
    parsers_mapping = {'python': py_files_parser}
    parser = parsers_mapping.get(programming_language.lower())
    if not parser:
        print('Нет подходящего парсера для языка {}'.format(programming_language))
        logger.error('Нет подходящего парсера для языка {}'.format(programming_language))
        exit(1)
    target_files = collect_files_in_dir(inspected_path, programming_language)
    for t_file in target_files:
        tree = parser(t_file)
        syntax_trees.append(tree)
    return syntax_trees


def check_part_of_speech(part_of_speech, tagged):
    if not tagged:
        return False
    pos_mapping = {'noun': 'NN', 'verb': 'VB'}
    pos = pos_mapping.get(part_of_speech.lower())
    if not pos:
        print('Указана неверная часть речи {}'.format(part_of_speech))
        logger.error('Указана неверная часть речи {}'.format(part_of_speech))
        exit(1)
    return pos in tagged[1]


def _collect_names_in_tree(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def _get_all_names_from_trees(trees):
    func_names = [n for n in flatten_list([_collect_names_in_tree(t) for t in trees]) if
                  not (n.startswith('__') and n.endswith('__'))]
    return flatten_list([split_under_score_to_words(func_name) for func_name in func_names])


def _get_funcs_names_from_trees(trees):
    node_names = [[node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                  for tree in trees]
    func_names = [n for n in flatten_list(node_names) if not (n.startswith('__') and n.endswith('__'))]
    return func_names


def _get_local_names_from_trees(trees):
    func_nodes = flatten_list([[node.body for node in ast.walk(t) if isinstance(node, ast.FunctionDef)] for t in trees])
    local_names = flatten_list([[a.targets[0].id for a in n if isinstance(a, ast.Assign)] for n in func_nodes])
    return local_names


def get_names_from_trees(trees, target='all'):
    funcs_mapping = {'all': _get_all_names_from_trees,
                     'funcs': _get_funcs_names_from_trees,
                     'locals': _get_local_names_from_trees}
    target_func = funcs_mapping.get(target)
    if not target_func:
        print('Отсутствует подходящая функция для получения названий объектов {}'.format(target))
        logger.error('Отсутствует подходящая функция для получения названий объектов {}'.format(target))
        exit(1)
    result = target_func(trees)
    return result


def filter_words_by_part_of_speech(part_of_speech, name):
    words = split_under_score_to_words(name)
    tags = pos_tag(word_tokenize(' '.join(words)))
    return [t[0] for t in tags if check_part_of_speech(part_of_speech, t)]


def pick_top_words_by_part_of_speech(path, program_lang, target, part_of_speech, top_size=3):
    trees = create_syntax_trees(path, program_lang)
    func_names = get_names_from_trees(trees, target)
    words = flatten_list([filter_words_by_part_of_speech(part_of_speech, n) for n in func_names])
    return pick_top_from_iterable(words, top_size)
