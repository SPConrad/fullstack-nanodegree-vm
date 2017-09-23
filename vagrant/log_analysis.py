#!/usr/bin/env python
import psycopg2

def get_query(query):
    db = psycopg2.connect(dbname="news")
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results

top_article_results = get_query("select articles.title, count(log.path) as num \
        from articles left join log on '/article/' || articles.slug \
        = log.path group by articles.title order by num desc limit 3;")

print("\nWhat are the most popular articles of all time?\n")
for article, views in top_article_results:
    print("    {} -- {} views".format(article, views))

top_author_results = get_query("select authors.name from authors join top_authors on authors.id = top_authors.author;")


print("\nWho are the most popular authors of all time?\n")
for name in top_author_results:
    print("    {}".format(name))


#Oh boy.
#This is nightmare. 
#Se
bad_responses_more_than_1_percent = get_query("select to_char(response_200.day, 'Month DD, YYYY'), (cast(response_not_200.num as \
        decimal) / (cast(response_200.num as decimal) + \
        cast(response_not_200.num as decimal))) AS percent from \
        response_200 left join response_not_200 on response_200.day = \
        response_not_200.day where (cast(response_not_200.num as decimal) \
        / (cast(response_200.num as decimal) + cast(response_not_200.num as\
         decimal))) > 0.01;")

#Print out results displaying days that had more than 1% of responses result in a 404 error.
#Technically the question wants anything that wasn't a 200, but the only options are 200 or 404, so....
print("\nOn what days did more than 1% of responses return a 404 error?\n")
for day, percent in bad_responses_more_than_1_percent:
    print("  On {} approxiamtely {}% resulted in 404s".format(day, ( round ( ( percent * 100 ) , 2 ) ) ) )
    #I was finding the above line a bit hard to parse so I spread the parens a bit