from dbi import db


async def get_client_by_client_id(client_id: str):
    return await db.fetchrow(
        """
        SELECT client_name, client_id, client_secret
        FROM clients
        WHERE client_id = :client_id
        """,
        client_id=client_id
    )


async def get_user_by_login(login: str):
    return await db.fetchrow(
        """
        SELECT login, password, name
        FROM users
        WHERE login = :login
        """,
        login=login
    )
