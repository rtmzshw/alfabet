import psycopg2

conn = psycopg2.connect(database="postgres", password="alfabet" ,user="postgres", )
conn.autocommit = True

def exec_query(sql: str):
    cursor = conn.cursor()
    print(sql)
    cursor.execute(sql)
    response = cursor.fetchone()
    cursor.close()
    return response