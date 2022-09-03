from os import getenv
from dotenv import load_dotenv

load_dotenv()


def connect_to(database_name: str):
    return "postgresql://{}:{}@{}:{}/{}".format(
        getenv('DB_USER', 'postgres'),
        getenv('DB_PASS', 'your postgres password'),
        getenv('DB_HOST', 'localhost'),
        getenv('DB_PORT', '5432'),
        database_name
    )


database = getenv('DB_NAME', 'trivia')
test_database = getenv('DB_TEST', 'trivia_test')

DATABASE_URI = connect_to(database)
TEST_DATABASE_URI = connect_to(test_database)
