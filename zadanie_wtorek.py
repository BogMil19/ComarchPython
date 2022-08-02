from collections import namedtuple, OrderedDict
from random import randint

current_state = 'main'

InventoryItem = namedtuple('InventoryItem', 'Name Qty')
inventory = OrderedDict()
for index, value in enumerate(['Box', 'Shoes', 'Hammer', 'Screwdriver'], 1):
    inventory[index] = InventoryItem(value, randint(1, 5))


def list_all():
    header = 'ID'.ljust(8) + 'Name'.ljust(15) + 'Quntity'.ljust(10)
    print(header)
    print(len(header) * '-')
    for item_id, item in inventory.items():
        item_line = str(item_id).ljust(8) + item.Name.ljust(15) + str(item.Qty).ljust(10)
        print(item_line)
    print('\n\n')


def menu_main():
    print('Welcome to inventory app!\n'
          'Select what you want to do:\n'
          '1 - list all existing inventory\n'
          '2 - add inventory\n'
          '3 - edit inventory\n'
          'x - exit')


def menu_main_handler(option: str):
    if option == '1':
        list_all()
        new_state = 'main'
    elif option == '2':
        new_state = 'add'
    elif option == '3':
        new_state = 'edit'
    elif option == 'x':
        new_state = 'exit'
    else:
        new_state = 'inv'

    return new_state


def menu_add():
    print('Insert name nad quantity separated with a comma (,)\n'
          'or press x to go back')


def menu_add_handler(option):
    new_item = option.split(',')
    if option == 'x':
        new_state = 'main'
    elif len(new_item) != 2:
        new_state = 'inv'
    else:
        try:
            inventory[max(inventory.keys()) + 1] = InventoryItem(new_item[0].strip(), int(new_item[1]))

            print('Item added!\n')
            new_state = 'main'
        except (TypeError, ValueError):
            print('Invalid entry, going back to main menu...\n')
            new_state = 'main'

    return new_state


def menu_edit():
    list_all()
    print('Select item you wish to remove by ID.\n'
          'Input: 3 -> removes ID 3 completely\n'
          'Input: 3, -1 -> substrate 1 from item 3 quantity\n'
          'Input: 3, +1 -> add 1 to item 3 quantity\n'
          'Input: 3, 2 -> set item 3 quantity to 2\n'
          'Input: x -> go back to main menu')


def menu_edit_handler(option):
    if option == 'x':
        new_state = 'main'
    else:
        try:
            item_edit = option.split(',')
            if len(item_edit) == 1:
                inventory.pop(int(item_edit[0]))
                print('Item deleted!\n')
                new_state = 'main'
            elif len(item_edit) == 2:
                item_index = int(item_edit[0])
                new_quantity = item_edit[1].strip()
                if new_quantity[0] == '+' or new_quantity[0] == '-':
                    new_quantity = int(new_quantity)
                    inventory[item_index] = InventoryItem(
                        inventory[item_index].Name,
                        inventory[item_index].Qty + new_quantity)
                    print('Item modified!\n')
                    new_state = 'main'
                else:
                    new_quantity = int(new_quantity)
                    inventory[item_index] = InventoryItem(
                        inventory[item_index].Name,
                        new_quantity)
                    print('Item modified!\n')
                    new_state = 'main'
        except (TypeError, ValueError):
            print('Invalid entry, going back to main menu...\n')
            new_state = 'main'

    return new_state


def cmd_menu_handler(state):
    new_state = 'inv'

    if state == 'main':
        menu_main()
    elif state == 'add':
        menu_add()
    elif state == 'edit':
        menu_edit()
    elif state == 'inv':
        print('Invalid command, going back to main menu...\n')
        new_state = 'main'
        return new_state
    else:
        pass

    option = str(input('Enter your choice: '))
    print('\n')

    if state == 'main':
        new_state = menu_main_handler(option)
    elif state == 'add':
        new_state = menu_add_handler(option)
    elif state == 'edit':
        new_state = menu_edit_handler(option)
    return new_state


def exit_program(state):
    if state == 'exit':
        return True
    else:
        return False


if __name__ == '__main__':

    while True:
        current_state = cmd_menu_handler(current_state)
        if exit_program(current_state):
            break
