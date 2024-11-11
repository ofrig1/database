from SyncDatabase import SyncDatabase
import multiprocessing
import logging


def writer(db, key, value):
    """
    Write a key-value pair to the database
    :param db: An instance of SyncDatabase
    :param key: The key to store in the database
    :param value: The value associated with the key
    """
    logging.info(f"Writer process attempting to set key '{key}' with value '{value}'")
    db.value_set(key, value)
    print(f"Writer set {key} to {value}")
    logging.info(f"Writer process set key '{key}' to '{value}'")


def reader(db, key):
    """
    Read a value associated with a key from the database
    :param db: An instance of SyncDatabase
    :param key: The key to retrieve from the database
    """
    process_id = multiprocessing.current_process().pid  # Get the current thread ID
    logging.info(f"Reader process with ID {process_id} attempting to get key '{key}'")
    value = db.value_get(key)
    print(f"Reader got {key}: {value}")
    if value is not None:
        logging.info(f"Reader process with ID {process_id} retrieved key '{key}' with value '{value}'")
    else:
        logging.warning(f"Reader process with ID {process_id} could not find key '{key}'")


def main():
    """
    Initializes a SyncDatabase instance, performs several write and delete
    operations, saves and loads the database state, and launches concurrent processes
    to read and write data.
    """
    # Set up the multiprocessing context
    ctx = multiprocessing.get_context('spawn')

    # Initialize database and add initial data
    my_database = SyncDatabase(mode='processes')
    my_database.value_set('house', '39 lylewood')
    my_database.value_set('city', 'tenafly')
    my_database.value_set('country', 'US')
    my_database.value_set('state', 'new Jersey')

    # Retrieve and delete a value
    print("Get 'city':", my_database.value_get('city'))
    my_database.value_delete('city')
    if my_database.value_get('city') is None:
        print("no value")
    else:
        print(my_database.value_get('city'))

    # Save and load data
    logging.info("Saving current database state")
    my_database.save()
    logging.info("Loading saved database state")
    my_database.load()

    # Start concurrent read operations
    processes = []
    logging.info("Starting multiple reader processes.")
    for i in range(11):
        p_read = ctx.Process(target=reader, args=(my_database, 'country'))
        processes.append(p_read)

    # Start all processes
    for p in processes:
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Final load to check data consistency
    logging.info("Loading database state after concurrent read operations.")
    my_database.load()

    # Start concurrent read and write operations
    processes = []
    logging.info("Starting concurrent read and write processes.")
    for i in range(4):
        p_read = ctx.Process(target=reader, args=(my_database, 'country'))
        processes.append(p_read)
    p_write = ctx.Process(target=writer, args=(my_database, 'world', 'earth'))
    processes.append(p_write)

    # Start all processes
    for p in processes:
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Final load to check data consistency
    logging.info("Loading final database state after concurrent operations.")
    my_database.load()


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    main()
