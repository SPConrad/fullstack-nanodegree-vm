Udacity Full Stack Web Developer Nanodegree - The Backend: Databases & Applications - Log Analysis Project


Necessary components (doesn't HAVE to be in this order, is probably better in this order):

python https://www.python.org/download/releases/2.7/

PostgreSQL https://www.postgresql.org/download/

VirtualBox https://www.virtualbox.org/wiki/Downloads

Vagrant https://www.vagrantup.com/downloads.html

psycopg2 http://initd.org/psycopg/download/

Download VM config here: https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip

Unzip that file

Donwload the database here: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

unzip that to the vagrant directory inside the unzipped directory

Open a terminal

Navigate to the vagrant file in the unzipped directory

Run 'vagrant up' in that directory

After that is finished, run 'vagrant ssh' to connect to the virtual machine

You'll now want to navigate to the /vagrant directory, done by first going down two levels ( cd .. -> cd .. -> cd /vagrant )

Import the database with the following command:

psql -d news -f newsdata.sql

To enter the psql database simply type psql

More detailed instructions and troubleshooting avaialble here https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0

Run these queries to create necessary views before running log_analysis.py 

create view top_authors as select articles.author, count (log.path) as views from articles left join log on '/article/' || articles.slug = log.path group by articles.author order by views desc;

create view top_authors_names as select authors.name, top_authors.views from authors left join top_authors on top_authors.author = authors.id order by top_authors.views desc; 

create view response_not_200 as select date_trunc('day', log.time) as day, count(log.status) as num from log where log.status != '200 OK' group by day order by num desc;

create view response_200 as select date_trunc('day', log.time) as day, count(log.status) as num from log where log.status = '200 OK' group by day order by num desc;


Run log_analysis.py with the following temrinal command: 

python log_analysis.py