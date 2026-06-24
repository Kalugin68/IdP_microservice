from dbi import db


async def create_client(client_name: str, client_id: str, client_secret: str):
    return await db.execute(
        """
        INSERT INTO clients (client_name, client_id, client_secret)
        VALUES 
        (
            :client_name,
            :client_id,
            :client_secret
        )
        """,
        client_name=client_name,
        client_id=client_id,
        client_secret=client_secret
    )
