from databricks.sdk import WorkspaceClient
import pg8000.native

WORKSPACE_HOST = "https://dbc-2929c64b-be24.cloud.databricks.com"
WORKSPACE_PROFILE = "foodguard_ai"
PG_HOST = "ep-plain-shape-d84tfnic-pooler.database.us-east-2.cloud.databricks.com"
PG_DATABASE = "foodguard"
PG_USER = "yashwanth.t@ganitinc.com"
ENDPOINT_NAME = "projects/foodguard-ai/branches/production/endpoints/primary"


def main() -> None:
    workspace_client = WorkspaceClient(
        host=WORKSPACE_HOST,
        profile=WORKSPACE_PROFILE,
    )
    credential = workspace_client.postgres.generate_database_credential(endpoint=ENDPOINT_NAME)
    print(f"OAuth database credential obtained; expires at {credential.expire_time}.")

    connection = pg8000.native.Connection(
        user=PG_USER,
        password=credential.token,
        host=PG_HOST,
        port=5432,
        database=PG_DATABASE,
        timeout=120,
    )
    try:
        connection.run("BEGIN")
        try:
            rows = connection.run(
                """
                INSERT INTO public.connection_test (id, label, created_at)
                VALUES (2, :label, CURRENT_TIMESTAMP)
                ON CONFLICT (id) DO UPDATE
                SET label = EXCLUDED.label,
                    created_at = CURRENT_TIMESTAMP
                RETURNING id, label, created_at
                """,
                label="latest login",
            )
            connection.run("COMMIT")
        except Exception:
            connection.run("ROLLBACK")
            raise
    finally:
        connection.close()

    row_id, label, timestamp = rows[0]
    print(f"Updated {PG_DATABASE}.public.connection_test:")
    print(f"id={row_id}, label={label}, created_at={timestamp}")


if __name__ == "__main__":
    main()
