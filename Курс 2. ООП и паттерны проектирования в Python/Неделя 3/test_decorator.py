# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:24:31 2020

@author: Govor_000
"""
import unittest
from classdecorator import * 

class TestFactorize(unittest.TestCase):
    """
    Класс для тестирования реализации декоратора класса Hero
    """
    def test_init(self):
        """
        Проверяет начальную инициализацию
        """
        hero = Hero()
        
        self.assertEqual(hero.get_positive_effects(), [])
        self.assertEqual(hero.get_negative_effects(), [])
        self.assertEqual(hero.get_stats(), {
            "HP": 128,  # health points
            "MP": 42,  # magic points, 
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость 
            "Luck": 1  # удача
        })
    
    
    def test_setting_one_pos_eff(self):
        hero = Hero()
        brs1 = Berserk(hero)
        
        self.assertEqual(brs1.get_positive_effects(), ['Berserk'])
        self.assertEqual(brs1.get_negative_effects(), [])
        self.assertEqual(brs1.get_stats(),{
                'HP': 178,
                'MP': 42,
                'SP': 100,
                'Strength': 22,
                'Perception': 1,
                'Endurance': 15,
                'Charisma': -1,
                'Intelligence': 0,
                'Agility': 15,
                'Luck': 8
        })

    def test_setting_two_pos_and_one_neg_eff(self):
        hero = Hero()
        brs1 = Berserk(hero)
        brs2 = Berserk(brs1)
        cur1 = Curse(brs2)

        self.assertEqual(cur1.get_positive_effects(), ['Berserk', 'Berserk'])
        self.assertEqual(cur1.get_negative_effects(), ['Curse'])
        self.assertEqual(cur1.get_stats(),{
                'HP': 228,
                'MP': 42,
                'SP': 100,
                'Strength': 27,
                'Perception': -4,
                'Endurance': 20,
                'Charisma': -6,
                'Intelligence': -5,
                'Agility': 20,
                'Luck': 13
        })
        
    def test_discrading_eff(self):
        hero = Hero()
        brs1 = Berserk(hero)
        brs2 = Berserk(brs1)
        cur1 = Curse(brs2)
        cur1.base = brs1  # снимаем эффект Berserk
    
        self.assertEqual(cur1.get_positive_effects(), ['Berserk'])
        self.assertEqual(cur1.get_negative_effects(), ['Curse'])
        self.assertEqual(cur1.get_stats(),{
                'HP': 178,
                'MP': 42,
                'SP': 100,
                'Strength': 20,
                'Perception': -1,
                'Endurance': 13,
                'Charisma': -3,
                'Intelligence': -2,
                'Agility': 13,
                'Luck': 6
        })
    
    def test_discrading_central_eff(self):
        hero = Hero()
        brs1 = Berserk(hero)
        bls1 = Blessing(brs1)
        brs2 = Berserk(bls1)
        brs2.base = brs1  # снимаем эффект Blessing
            
        self.assertEqual(brs2.get_positive_effects(), ['Berserk','Berserk'])
        self.assertEqual(brs2.get_negative_effects(), [])
        self.assertEqual(brs2.get_stats(),{
                'HP': 228,
                'MP': 42,
                'SP': 100,
                'Strength': 29,
                'Perception': -2,
                'Endurance': 22,
                'Charisma': -4,
                'Intelligence': -3,
                'Agility': 22,
                'Luck': 15
        })


if __name__ == "__main__":
    unittest.main()