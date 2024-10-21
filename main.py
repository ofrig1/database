from SerializeDatabase import SyncDatabase


def main():
    my_database = SyncDatabase()
    my_database.value_set('house', '39 lylewood')
    my_database.value_set('city', 'tenafly')
    print(my_database.value_get('city'))
    my_database.value_delete('city')
    if my_database.value_get('city') is None:
        print("no value")
    else:
        print(my_database.value_get('city'))
    my_database.save()
    my_database.load()


if __name__ == '__main__':
    main()
