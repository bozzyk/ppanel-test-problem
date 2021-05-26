# This repo contains solution for test problems for Perfect Panel company
## Problem #1

Consider given 3 tables:

clients
| id | first_name | last_name | age |
| -- | ---------- | --------- | --- |
| 1  | Petr       | Kurkov    | 31  |
| 2  | Katerina   | Petrova   | 67  |

orders
| id | product                   | category |
| -- | ------------------------- | -------- |
| 1  | Samsung S21               | Mobile   |
| 2  | Dell 15” 1Tb 3.6Gz 32 RAM | PC       |

client_orders
| id | client_id | order_id |
| -- | --------- | -------- |
| 1  | 1         | 2        |
| 2  | 2         | 1        |

Using the tables write a SQL query to get clients with age between 18 and 65 bought only 2 products and only in one category.
Output format:
    ID, Name (first_name last_name), Category, Products (Product 1, Product 2, ...)
     1,                 Ivan Ivanov,   Laptop, Product 1, Product 2

## Problem #1 solution

```sql
select *;
```