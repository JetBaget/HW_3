# -*- coding: utf-8 -*-


class ArgsError(Exception):
    """
    Ошибки, связанные с вводом аргументов командной строки
    """
    def __init__(self, message=None):
        self.message = 'Ошибка при вводе аргумента командной строки. {}'.format(message)

    def __str__(self):
        return self.message


class GitCloneRepoError(Exception):
    """
    Ошибки при клонировании GIT-репозитория
    """
    def __init__(self, message=None):
        self.message = 'Ошибка клонирования GIT-репозитория. {}'.format(message)

    def __str__(self):
        return self.message
