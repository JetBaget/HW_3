Описание
---------
Библиотека, содержащая набор инструментов для анализа имен функций в .py-файлах.
Имеет следующий функционал:
- получение топа популярных слов, используемых в названиях
- возможность клонировать GIT-репозитории для последующего их анализа
- выбор цели анализа (функции/локальные переменные)
- выбор способа сохранения результатов анализа (вывод в консоль, csv, json)

Установка
---------
Для использования библиотеки необходимо зайти в директорию, куда вы хотите выкачать файлы и выполнить команду:    

         git clone https://github.com/JetBaget/HW_3

После этого вы должны увидеть следующие файлы:
- names_analyzer/__init__.py
- names_analyzer/syntax_analyze.py
- names_analyzer/ustils.py
- names_analyzer/exceptions.py
- requirements.txt
- README.md

Зависимости
---------
В файле requirements.txt описаны зависимости для данной библиотеки.
В частности, библиотека nltk (natural language toolkit), необходимая для синтаксического анализа.
При первом запуске для работы nltk может потребоваться выполнить следующие команды в интерпретаторе python3:
        >> import nltk
        >> nltk.download('averaged_perceptron_tagger')
        >> nltk.download('punkt')
        
Быстрый старт:
---------
Откройте файл func_names_analyzer/analyzer.py и запустите его в интерпретаторе python3.

      Топ используемых слов:
      =======================
      | save           |  4 |
      | run            |  1 |
      | ensure         |  1 |
      =======================
      
