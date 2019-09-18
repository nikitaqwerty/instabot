import os
import sqlite3

DIR = os.path.dirname(os.path.abspath(__file__))

SELECT_FROM_PROFILE_WHERE_NAME = "SELECT * FROM profiles WHERE name = :name"

INSERT_INTO_PROFILE = "INSERT INTO profiles (name) VALUES (?)"

SQL_CREATE_ACTIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS `actions` (
        `acoount_name` TEXT NOT NULL,
        `target_id` TEXT NOT NULL,
        `like` INTEGER NOT NULL,
        `comment` INTEGER NOT NULL,
        `follow` INTEGER NOT NULL,
        `unfollow` INTEGER NOT NULL,
        `story_view` INTEGER NOT NULL,
        `timestamp` DATETIME NOT NULL);"""


def get_database(make=False):
    address = validate_database_address()

    if not os.path.isfile(address) or make:
        create_database(address)

    return address


def create_database(address):
    try:
        connection = sqlite3.connect(address)
        with connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            create_tables(
                cursor,
                [
                    'actions'
                ],
            )

            connection.commit()

    except Exception as exc:
        print(
            f"Wah! Error occurred while getting a DB {str(exc)}"
        )
    finally:
        if connection:
            # close the open connection
            connection.close()


def create_tables(cursor, tables):
    if "actions" in tables:
        cursor.execute(SQL_CREATE_ACTIONS_TABLE)


def verify_database_directories(address):
    db_dir = os.path.dirname(address)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)


def validate_database_address():
    address = DIR
    if not address.endswith(".db"):
        slash = "\\" if "\\" in address else "/"
        address = address if address.endswith(slash) else address + slash
        address += "instapy.db"
    verify_database_directories(address)
    return address


def add_action(target_id='test', actions=None):
    if actions is None:
        actions = {'like': '0', 'comment': '0', 'follow': '0', 'unfollow': '0', 'story_view': '0'}
    db = get_database()
    conn = sqlite3.connect(db)
    with conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        sql = "INSERT INTO actions VALUES (?, ?, ?, ?, ?, ?, STRFTIME('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))"
        cur.execute(sql,
                    (
                        target_id,
                        actions["like"],
                        actions["comment"],
                        actions["follow"],
                        actions["unfollow"],
                        actions["story_view"],
                    ),
                    )
        conn.commit()


if __name__ == '__main__':
    add_action()
