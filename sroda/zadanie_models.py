from abc import ABC, abstractmethod
from enum import Enum
from collections import namedtuple, OrderedDict
from random import randint

# Class for holding record data
InventoryItem = namedtuple('InventoryItem', 'Name Qty')


class DatabaseError(Exception):
    """Exception raised by database handler"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'{self.__class__.__name__} - {self.msg}'


class AbstractDB(ABC):
    """Abstract class for db interface"""

    def __init__(self):
        self.__connected = False

    @abstractmethod
    def connected(self):
        return self.__connected

    @abstractmethod
    def query_all(self):
        pass

    @abstractmethod
    def query_by_id(self, item_id):
        pass

    @abstractmethod
    def add_item(self, item_name, item_qty):
        pass

    @abstractmethod
    def edit_quantity(self, item_id, item_qty):
        pass


class InMemoryDatabaseHandler(AbstractDB):
    """In-memory database storage, based on AbstractDB"""

    def __init__(self):
        super().__init__()
        self.__connected = False
        self.__records = OrderedDict()
        for index, value in enumerate(['Box', 'Shoes', 'Hammer', 'Screwdriver'], 1):
            self.__records[index] = InventoryItem(value, randint(1, 5))

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.disconnect()

    def connect(self):
        """Connects to database"""
        self.__connected = True
        print('DB connection established!')

    def disconnect(self):
        """Disconnects database"""
        self.__connected = False
        print('DB connection closed!')

    def connected(self):
        """Return database connection status (boolean value)"""
        return self.__connected

    def query_all(self):
        """Get all records from database"""
        if self.__connected:
            return self.__records
        else:
            raise DatabaseError('Database not connected')

    def query_by_id(self, item_id):
        """Get object with given ID"""
        if self.__connected:
            return self.__records[item_id]
        else:
            raise DatabaseError('Database not connected')

    def add_item(self, item_name, item_qty):
        """Add item to database"""
        try:
            if item_qty <= 0:
                raise ValueError('Quantity must be greater than 0!')
            self.__records[max(self.__records.keys()) + 1] = InventoryItem(item_name, item_qty)
        except (ValueError, TypeError):
            raise DatabaseError('Invalid data, record not added')

    def edit_quantity(self, item_id, item_qty=0):
        """Edit item quantity"""
        try:
            if item_qty == 0:
                self.__records.pop(item_id)
                print('Item deleted!')
            else:
                self.__records[item_id] = InventoryItem(
                    self.__records[item_id].Name,
                    item_qty)
                print('Item edited!')
        except (ValueError, TypeError, KeyError):
            raise DatabaseError('Invalid data, record not edited')


class State(Enum):
    MAIN = 'main'
    VIEW = 'view'
    ADD = 'add'
    EDIT = 'edit'
    EXPORT_CSV = 'export'
    EXIT = 'exit'
    INVALID = 'inv'

    ADD_CONSOLE = 'console'
    ADD_JSON = 'json'
    ADD_CSV = 'csv'

    def option_description(self):
        """Descriptions for each state"""
        if self == State.MAIN:
            return 'Go to main menu'
        elif self == State.VIEW:
            return 'View all items'
        elif self == State.ADD:
            return 'Add new item'
        elif self == State.EDIT:
            return 'Edit item'
        elif self == State.ADD_CONSOLE:
            return 'Provide item data in console'
        elif self == State.ADD_JSON:
            return 'Provide item data in json file'
        elif self == State.ADD_CSV:
            return 'Provide item data in csv file'
        elif self == State.EXPORT_CSV:
            return 'Exports data to csv'
        elif self == State.EXIT:
            return 'Exit app'

    def option_to_str(self):
        """Print option with its description"""
        return f'     - {self.value}'.ljust(15) + f'-> {self.option_description()}'


class MenuHandler:
    """Class handling user interaction and executing database queries"""
    def __init__(self, db: AbstractDB = None):
        self.__state: State = State.MAIN
        self.__main_actions = [State.VIEW, State.ADD, State.EDIT, State.EXPORT_CSV, State.EXIT]
        self.__view_actions = [State.MAIN]
        self.__add_actions = [State.ADD_CONSOLE, State.ADD_JSON, State.ADD_CSV, State.MAIN]
        self.__add_item_actions = [State.MAIN]
        self.__edit_item_actions = [State.MAIN]

        self.__db = db

    def connect_db(self, db: AbstractDB):
        """Provide a db instance to class"""
        self.__db = db

    def exit_app(self):
        """Check for exit condition"""
        if self.__state == State.EXIT:
            return True
        else:
            return False

    def print_user_menu(self):
        if self.__state == State.MAIN:
            self.__menu_main_content()
        elif self.__state == State.VIEW:
            self.__menu_view_content()
        elif self.__state == State.ADD:
            self.__menu_add_content()
        elif self.__state == State.ADD_CONSOLE:
            self.__menu_add_console_content()
        elif self.__state == State.ADD_JSON or self.__state == State.ADD_CSV:
            print('Not implemented, sorry :)')
            self.__state = State.INVALID
        elif self.__state == State.EXPORT_CSV:
            print('Exporting data...')
        elif self.__state == State.EDIT:
            self.__menu_edit_content()
        elif self.__state == State.INVALID:
            self.__invalid_entry_msg()

        if self.__state != State.INVALID and self.__state != State.EXPORT_CSV:
            option = input('Select option: >> ')

        try:
            if self.__state == State.MAIN:
                if State(option) in self.__main_actions:
                    self.__state = State(option)
                else:
                    self.__state = State.INVALID

            elif self.__state == State.VIEW:
                if State(option) in self.__view_actions:
                    self.__state = State(option)
                else:
                    self.__state = State.INVALID

            elif self.__state == State.ADD:
                if State(option) in self.__add_actions:
                    self.__state = State(option)
                else:
                    self.__state = State.INVALID

            elif self.__state == State.ADD_CONSOLE:
                if option.find(',') != -1:
                    item_name, item_qty = option.split(',')
                    self.__db.add_item(item_name, int(item_qty))
                elif State(option) in self.__add_item_actions:
                    self.__state = State(option)
                else:
                    self.__state = State.INVALID

            elif self.__state == State.EDIT:
                if option.find(',') != -1:
                    item_id, item_qty = option.split(',')
                    item_id = int(item_id.strip())
                    item_qty = item_qty.strip()
                    if item_qty.find('+') != -1 or item_qty.find('-') != -1:
                        record = self.__db.query_by_id(item_id)
                        self.__db.edit_quantity(item_id, record.Qty + int(item_qty))
                    else:
                        self.__db.edit_quantity(item_id, int(item_qty))
                elif option.isnumeric():
                    item_id = int(option.strip())
                    self.__db.edit_quantity(item_id)
                elif State(option) in self.__edit_item_actions:
                    self.__state = State(option)
                else:
                    self.__state = State.INVALID

            elif self.__state == State.EXPORT_CSV:
                records = self.__db.query_all()
                for item_id, record in records.items():
                    print([item_id, record.Name, record.Qty])

                self.__state = State.MAIN

            elif self.__state == State.INVALID:
                self.__state = State.MAIN
        except (ValueError, TypeError):
            self.__state = State.INVALID
        except DatabaseError as e:
            print(e)
            self.__state = State.INVALID

    def __invalid_entry_msg(self):
        print('User entry is not valid, going back to main menu...')

    def __menu_main_content(self):
        print(format('Welcome to inventory app!', '-^50'))
        print('Select what you want to do:')
        for action in self.__main_actions:
            print(action.option_to_str())

    def __menu_view_content(self):
        try:
            records: dict[str, InventoryItem] = self.__db.query_all()
        except DatabaseError as e:
            print(e)
            self.__state = State.INVALID
            return

        header = 'ID'.ljust(8) + 'Name'.ljust(15) + 'Quntity'.ljust(10)
        print(header)
        print(len(header) * '-')
        for item_id, record in records.items():
            item_line = str(item_id).ljust(8) + record.Name.ljust(15) + str(record.Qty).ljust(10)
            print(item_line)

        print('\n')
        print('Select what you want to do:')
        for action in self.__view_actions:
            print(action.option_to_str())

    def __menu_add_content(self):
        print('Select how you want to add new item:')
        for action in self.__add_actions:
            print(action.option_to_str())

    def __menu_add_console_content(self):
        print('Provide item name and quantity separated by comma or')
        for action in self.__add_item_actions:
            print(action.option_to_str())

    def __menu_edit_content(self):
        print('Select item you wish to edit by ID.\n'
              'Input: 3 -> removes ID 3 completely\n'
              'Input: 3, -1 -> substrate 1 from item 3 quantity\n'
              'Input: 3, +1 -> add 1 to item 3 quantity\n'
              'Input: 3, 2 -> set item 3 quantity to 2')
        for action in self.__edit_item_actions:
            print(action.option_to_str())
