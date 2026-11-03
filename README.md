# Lab 4B — Inheritance, Polymorphism and Composition

Python solutions for the **10 required tasks** in `Lab 4 Inheritance Polymorphism.docx`. Short answers are comments at the top of each task file. Tests are in the same files, as required. Optional E1–E5 are not included.

## Открыть и проверить

Это отдельный Python-проект, не Android/Kotlin. Открой эту папку в PyCharm или VS Code. В терминале из папки проекта выполни:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

Окружение `.venv` уже создано на этом компьютере. Можно сразу выполнить:

```sh
.venv/bin/python -m pytest -v
```

Одно задание:

```sh
.venv/bin/python -m pytest task01.py -v
```

Здесь результат проверки — список пройденных тестов. Ввод через `readln()` и эмулятор телефона не используются.

## Что находится в файлах

| Файл | Содержание |
| --- | --- |
| task01.py | Абстрактный способ оплаты и Checkout без ветвления по провайдеру |
| task02.py | Абстрактный Notifier и ограничения длины сообщений |
| task03.py | Общий расчёт НДС и переопределение net() |
| task04.py | Журнал аудита через композицию |
| task05.py | Смена роли сотрудника с сохранением личности и истории |
| task06.py | Duck typing и Protocol для записи отчётов |
| task07.py | Неизменяемый Money и операторы с проверкой валют |
| task08.py | Единый search() с необязательными фильтрами |
| task09.py | Mixins, MRO и корректная цепочка super() |
| task10.py | Единый реестр платёжных методов |

## Статические проверки

```sh
.venv/bin/python -m mypy task06.py
.venv/bin/python -m mypy experiments/bad_target.py
.venv/bin/python -m pyflakes experiments/original_search.py
```

Первая команда должна завершиться успешно. Последние две **намеренно должны сообщить ошибки**: объект без write() и повторное определение search(). Эти примеры изолированы в experiments и не входят в рабочие решения.

Методы оплаты в Task 1 считают суммы в сумах, как в исходном задании. Money в Task 7 хранит целое число минимальных денежных единиц (тийины/центы).

Для сдачи нужны task01.py–task10.py, папка experiments, requirements.txt, pytest.ini и документация. Папки .venv и кэши загружать не нужно.
