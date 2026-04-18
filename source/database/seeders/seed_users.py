import os

from contextlib import contextmanager

from clients.postgres import PostgresClient
from core.database.schemas import (
    UserCreateSchema,
    AdminCreateSchema,
    FirefighterCreateSchema,
)
from core.database.cruds import user_crud

from registry.users import users_data


def seed_users_data():

    print("Seeding users data into the database...")

    is_developer_environment = os.getenv("DEV", "false") == "true"

    if is_developer_environment:
        PostgresClient.connect()

        count_inserted = 0

        with contextmanager(PostgresClient.db)() as db:
            for user_data in users_data:
                user_filter = {"email": user_data["email"]}

                existing_user = user_crud.read_by(db=db, **user_filter)

                if existing_user:
                    continue

                if user_data["role"] == "admin":
                    user_create = AdminCreateSchema(**user_data)

                elif user_data["role"] == "firefighter":
                    user_create = FirefighterCreateSchema(**user_data)

                else:
                    user_create = UserCreateSchema(**user_data)

                user_crud.create(db=db, instance=user_create)

                count_inserted += 1

        print(f"Users data seeding completed. {count_inserted} users inserted.")


if __name__ == "__main__":
    seed_users_data()
