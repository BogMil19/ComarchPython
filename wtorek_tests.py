import unittest
from zadanie_wtorek import menu_main_handler, InventoryItem, OrderedDict, menu_add_handler, menu_edit_handler

class WtorekTestCase(unittest.TestCase):

    def test_main_menu_navigation(self):
        valid_options = ['1', '2', '3', 'x']
        for valid_option in valid_options:
            with self.subTest(msg=f'Testing main menu option {valid_option}'):
                assert menu_main_handler(valid_option) != 'inv'

        invalid_options = ['a', 'dsf', 'exit']
        for invalid_option in invalid_options:
            with self.subTest(msg=f'Testing main menu option {invalid_option}'):
                assert menu_main_handler(invalid_option) == 'inv'

    def test_add_item(self):
        inventory_db = OrderedDict()
        inventory_db[1] = InventoryItem('Book', 3)

        with self.subTest(msg=f'Testing add menu - database connection'):
            menu_add_handler('Hammer, 2', inventory_db)
            assert len(inventory_db) == 2
        with self.subTest(msg=f'Testing add menu - response after adding item'):
            response = menu_add_handler('Shoes, 2', inventory_db)
            assert response == 'main'
        with self.subTest(msg=f'Testing add menu - invalid entry'):
            response = menu_add_handler('Shoes', inventory_db)
            assert response == 'inv'
        with self.subTest(msg=f'Testing add menu - invalid entry'):
            response = menu_add_handler('Shoes, "asd"', inventory_db)
            assert response == 'inv'
        with self.subTest(msg=f'Testing add menu - go back to main menu'):
            response = menu_add_handler('x', inventory_db)
            assert response == 'main'

    def test_edit_item(self):
        inventory_db = OrderedDict()
        inventory_db[1] = InventoryItem('Book', 3)

        response = menu_edit_handler('1', inventory_db)
        with self.subTest(msg=f'Testing edit menu - database connection'):
            assert len(inventory_db) == 0
        with self.subTest(msg=f'Testing edit menu - response after editing item'):
            assert response == 'main'

        inventory_db[2] = InventoryItem('Hammer', 1)
        menu_edit_handler('2, +5', inventory_db)
        with self.subTest(msg=f'Testing edit menu - add x to Qty'):
            assert inventory_db[2].Qty == 6

        menu_edit_handler('2, -2', inventory_db)
        with self.subTest(msg=f'Testing edit menu - sub x from Qty'):
            assert inventory_db[2].Qty == 4

        menu_edit_handler('2, 2', inventory_db)
        with self.subTest(msg=f'Testing edit menu - set x to Qty'):
            assert inventory_db[2].Qty == 2

        with self.subTest(msg=f'Testing edit menu - invalid entry'):
            response = menu_edit_handler('4', inventory_db)
            assert response == 'inv'
        with self.subTest(msg=f'Testing add menu - invalid entry'):
            response = menu_edit_handler('2, "asd"', inventory_db)
            assert response == 'inv'
        with self.subTest(msg=f'Testing add menu - go back to main menu'):
            response = menu_edit_handler('x', inventory_db)
            assert response == 'main'
