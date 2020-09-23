# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 11:53:10 2020

@author: Govor_000
"""
import unittest

def factorize(x):
    """ 
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    pass

class TestFactorize(unittest.TestCase):
    """
    Класс для тестирования функции factorize()
    """
    
    def test_wrong_types_raise_exception(self):
        """
        Проверяет, что передаваемый в функцию аргумент
        типа float или str вызывает исключение TypeError. 
        """
        for x in ('string', 1.5):
            with self.subTest(x=x):
                #    self.assertRaises(TypeError, factorize, x)
                with self.assertRaises(TypeError):
                    factorize(x)

    def test_negative(self):
        """
        Проверяет, что передача в функцию factorize
        отрицательного числа вызывает исключение ValueError. 
        """
        for x in (-1, -10, -100):
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)
        
    def test_zero_and_one_cases(self):
        """
        Проверяет, что при передаче в функцию целых чисел 0 и 1,
        возвращаются соответственно кортежи (0,) и (1,). 
        """
        for x in (0,1):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))             

    def test_simple_numbers(self):
        """
        Проверяет, что для простых чисел возвращается кортеж,
        содержащий одно данное число. 
        """
        for x in (3, 13, 29):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), (x,))             
        
        

    def test_two_simple_multipliers(self):
        """
        Проверяет случаи, когда передаются числа для которых
        функция factorize возвращает кортеж с числом элементов равным 2.
        """
        test_cases = (
            (6, (2, 3)),
            (26, (2, 13)),
            (121, (11, 11)),
        )
        for x, expected in test_cases:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), expected)
        
        

    def test_many_multipliers(self):
        """
        Проверяет случаи, когда передаются числа для которых функция
        factorize возвращает кортеж с числом элементов больше 2. 
        """
        test_cases = (
            (1001, (7, 11, 13)),
            (9699690, (2, 3, 5, 7, 11, 13, 17, 19)),
        )
        for x, expected in test_cases:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), expected)




if __name__ == "__main__":
    unittest.main()