from dbi import db


async def get_client_by_client_id(client_id: str):
    return await db.fetchrow(
        """
        SELECT client_name, client_id, client_secret
        FROM clients
        WHERE client_id = :client_id
        """,
        **{"client_id": client_id}
    )


async def get_user_by_login(login: str):
    return await db.fetchrow(
        """
        SELECT login, password, name
        FROM users
        WHERE login = :login
        """,
        **{"login": login}
    )


async def create_auth_code(code: str, login: str, expires_at: str):
    return await db.execute(
        """
        INSERT INTO oauth_codes (code, login, expires_at)
        VALUES 
        (
            :code,
            :login,
            :expires_at
        )
        """,
        **{
            "code": code,
            "login": login,
            "expires_at": expires_at,
        }
    )


async def get_auth_code(code: str):
    return await db.fetchrow(
        """
        SELECT login, expires_at
        FROM oauth_codes
        WHERE code = :code
        """,
        **{"code": code}
    )


async def delete_auth_code(code: str):
    return await db.execute(
        """
        DELETE
        FROM oauth_codes
        WHERE code = :code
        """,
        **{"code": code}
    )
