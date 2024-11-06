from SyncDatabase import SyncDatabase
import threading


def writer(db, key, value):
    db.value_set(key, value)
    print(f"Writer set {key} to {value}")


def reader(db, key):
    value = db.value_get(key)
    print(f"Reader got {key}: {value}")


def main():
    my_database = SyncDatabase()
    my_database.value_set('house', '39 lylewood')
    my_database.value_set('city', 'tenafly')
    my_database.value_set('country', 'US')
    my_database.value_set('state', 'new Jersey')

    print("Get 'city':", my_database.value_get('city'))
    my_database.value_delete('city')
    if my_database.value_get('city') is None:
        print("no value")
    else:
        print(my_database.value_get('city'))
    print("\nSaving and loading data...")
    my_database.save()
    my_database.load()

    threads = []
    print("\nStarting concurrent read/write operations...")
    for i in range(5):
        t_write = threading.Thread(target=writer, args=(my_database, f'key{i}', f'value{i}'))
        t_read = threading.Thread(target=reader, args=(my_database, f'key{i}'))
        threads.extend([t_write, t_read])

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Final load to check data consistency
    print("\nFinal data check after concurrent operations...")
    my_database.load()


if __name__ == '__main__':
    main()
