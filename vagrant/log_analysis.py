import psycopg2


def top_articles(cursor):
    """Returns the top 3 visited articles"""
    cursor.execute("select articles.title, count(log.path) as num \
        from articles left join log on '/article/' || articles.slug \
        = log.path group by articles.title order by num desc limit 3;")
    return cursor.fetchall()


def top_authors(cursor):
    """Returns the top 3 visited articles"""
    cursor.execute("select articles.title, count(log.path) as num \
        from articles left join log on '/article/' || articles.slug \
        = log.path group by articles.title order by num desc limit 3;")
    return cursor.fetchall()


def bad_responses(cursor):
    """Returns the top 3 visited articles"""
    cursor.execute("select response_200.day, (cast(response_not_200.num \
        as decimal) / cast(response_200.num as decimal)) AS percent from \
        response_200 left join response_not_200 on response_200.day = \
        response_not_200.day where (cast(response_not_200.num as decimal) \
        / cast(response_200.num as decimal)) > 0.01;")
    return cursor.fetchall()


def create_views(cursor):
    """Returns the top 3 visited articles"""
    cursor.execute("create view top_authors as select articles.author, \
        count (log.path) as num from articles left join log on '/article/'\
        || articles.slug = log.path group by articles.author order by \
        num desc limit 3;")
    cursor.execute("create view response_not_200 as select \
        date_trunc('day', log.time) as day, count(log.status) \
        as num from log where log.status != '200 OK' group by \
        day order by num desc;")
    return cursor.fetchall()
