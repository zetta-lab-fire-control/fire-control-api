import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(encoding="utf-8")


class PostgresClient:
    _engine_ = None
    _session_ = None

    _database_url_ = os.getenv("DATABASE_URL")

    Base = declarative_base()

    @classmethod
    def _validate_client_(cls):

        if cls._database_url_ is None:
            raise ValueError("DATABASE_URL environment variable is not set.")

    @classmethod
    def _start_(cls):

        if cls._engine_ is None:
            cls._engine_ = create_engine(
                cls._database_url_, connect_args={"client_encoding": "utf8"}
            )

            cls._session_ = sessionmaker(
                autocommit=False, autoflush=False, bind=cls._engine_
            )

    @classmethod
    def base(cls):
        cls._start_()
        return cls.Base

    @classmethod
    def connect(cls):

        cls._validate_client_()

        cls._start_()

        with cls._engine_.begin() as connection:
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))

        cls.Base.metadata.create_all(bind=cls._engine_)

    @classmethod
    def db(cls):

        cls._start_()

        db = cls._session_()

        try:
            yield db

        finally:
            db.close()
