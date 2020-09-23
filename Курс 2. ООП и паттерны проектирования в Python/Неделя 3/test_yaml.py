# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 13:57:02 2020

@author: Govor_000
"""
"""
 Когда происходит загрузка (по существу создание объектов на основании yaml), 
 используются уже определенные конструкторы типов данных 
 (например: для списков, чисел , словарей). Если мы определили свой класс 
 в коде, то мы не сможем использовать указание на него в yaml файле, так 
 конструктор для него отсутствует. Для исправления этой ситуации возможны два варианта:
     
первый - не изменяя определения пользовательского класса 
(не внося изменения в код нашего класса), определить функцию конструктор,
 которая будет загружать данные и на основе их создавать экземпляр необходимого
 типа данных и возвращать его. Далее, эту созданную функцию нужно зарегистрировать 
 (добавить к существующим конструкторам) с помощью функции add_constructor.
 
второй - добавить в реализацию класса нужного нам типа данных 
(в код нашего класса), атрибут класса yaml_tag и метод класса с названием 
from_yaml, который по существу делает тоже самое, что и функция конструктор 
из первого варианта. При этом нужно соблюсти еще одно условие - класс должен 
наследоваться от yaml.YAMLObject.

Вот пара примеров:

"""



# демонстрация загрузки yaml по первому варианту
# важное замечание версия PyYAML - 3.13
import yaml


# класс определяющий пользовательский тип данных
class ExampleClass:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f'ExampleClass, value - {self.value}'


# функция конструктор для типа данных ExampleClass
def constuctor_example_class(loader, node):
    # получаем данные из yaml
    value = loader.construct_mapping(node)
    # необходимо выбрать из полученные данных необходимые
    # для создания экземпляра класса ExampleClass
    return ExampleClass(*value)


# регистрируем конструктор
yaml.add_constructor('!example_class', constuctor_example_class)
# yaml строка
document = """!example_class {5}"""
# выполняем загрузку
obj = yaml.load(document)
# выведем полученный объект, ожидаем строку
# ExampleClass, value - 5
print(obj)

# класс определяющий пользовательский тип данных
class ExampleClass1(yaml.YAMLObject):  # <-- добавим родительский класс yaml.YAMLObject
    yaml_tag = '!example_class1'  # <-- добавим тег

    @classmethod
    def from_yaml(cls, loader, node):  # <-- добавим метод класса from_yaml
        # получаем данные из yaml
        value = loader.construct_mapping(node)
        # необходимо выбрать из полученные данных необходимые
        # для создания экземпляра класса ExampleClass
        return ExampleClass(*value)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'ExampleClass1, value - {self.value}'


# yaml строка
document = """
examples:
    - !example_class1 {}
    - value: [10, 10]
    - !example_class {10}
"""
# выполняем загрузку
obj = yaml.load(document)
# выведем полученный объект, ожидаем строку
# ExampleClass, value - 7
print(obj)
