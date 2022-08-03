from zadanie_models import MenuHandler, InMemoryDatabaseHandler

if __name__ == '__main__':
    with InMemoryDatabaseHandler() as db:

        db.add_item('DummyItem', 3)     # add dummy object to test connection

        user_menu = MenuHandler(db)     # user menu handler instance

        while not user_menu.exit_app():
            user_menu.print_user_menu()           # loop app until user exits
