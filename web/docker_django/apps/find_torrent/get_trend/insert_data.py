import psycopg2


conn = psycopg2.connect(
    database='tfind_db',
    user='tfind',
    password='xok43tra',
    host='192.168.1.241',
    port='5432'
)

cur = conn.cursor()


def insert_trend(trend):
    try:
        # print(trend)
        cur.execute("INSERT INTO find_torrent_trend (title, priority) VALUES (%s, %s)",
                    (trend['title'], 1)
                    )
        conn.commit()
    except Exception as e:
        # http://initd.org/psycopg/docs/connection.html#connection.rollback
        conn.rollback()
        cur.execute("UPDATE find_torrent_trend SET priority=priority+1 WHERE title = (%s)",
                    (trend['title'],)
                    )
        conn.commit()


def update_trend(trend):
    try:
        print(trend)
        cur.execute("UPDATE find_torrent_trend SET (last_check, count_check, priority)=(%s, %s, %s) WHERE title = (%s)",
                    (trend['last_check'], trend['count_check'], trend['priority'], trend['title'])
                    )
        conn.commit()
    except Exception as e:
        print("Database error")
        print(e)
        # http://initd.org/psycopg/docs/connection.html#connection.rollback
        conn.rollback()