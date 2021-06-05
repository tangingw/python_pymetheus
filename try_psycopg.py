import psycopg2


conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="TALLgeese3#",
    host="192.168.200.45"
)

with conn.cursor() as cursor:

    cursor.execute(
        """
        select 1 + 1
        """
    )

    result = cursor.fetchone()
    print(result)