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

-- query to get the result
select
    c.id "ID",
    concat(max(c.first_name), ' ', max(c.last_name)) "Name",
    max(o.category) "Category",
    group_concat(o.product separator ',') "Products"
from ppanel.client_orders co
left join ppanel.clients c on co.client_id = c.id
left join ppanel.orders o on co.order_id = o.id
where c.age between 18 and 65
group by c.id
having count(co.order_id) = 2 and count(distinct o.category) = 1;