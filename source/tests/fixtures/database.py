import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from clients.postgres import PostgresClient

URL: str | None = os.getenv("DATABASE_URL")


@pytest.fixture(scope="session")
def engine():

    return create_engine(URL, connect_args={"client_encoding": "utf8"})


@pytest.fixture(scope="session", autouse=True)
def setup_database(engine):

    Base = PostgresClient.Base

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):

    connection = engine.connect()

    transaction = connection.begin()

    local = sessionmaker(
        bind=connection,
        autocommit=False,
        autoflush=False,
        join_transaction_mode="create_savepoint",
    )

    session = local()

    yield session

    session.close()

    transaction.rollback()

    connection.close()
