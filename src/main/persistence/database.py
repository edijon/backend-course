from sqlmodel import SQLModel, create_engine, Session


DATABASE_USER = "user"
DATABASE_PASSWORD = "password"
DATABASE_NAME = "dbname"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
