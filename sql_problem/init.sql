create database ppanel;

create table ppanel.clients(id integer primary key auto_increment, first_name varchar(50), last_name varchar(50), age integer);
create table ppanel.orders(id integer primary key auto_increment, product varchar(200), category varchar(50));
create table ppanel.client_orders(id integer primary key auto_increment, client_id integer, order_id integer);

load data infile 'clients.csv'
into table ppanel.clients
fields terminated by ','
lines terminated by '\n'
ignore 1 rows;

load data infile 'orders.csv'
into table ppanel.orders
fields terminated by ','
lines terminated by '\n'
ignore 1 rows;

load data infile 'client_orders.csv'
into table ppanel.client_orders
fields terminated by ','
lines terminated by '\n'
ignore 1 rows;

commit;