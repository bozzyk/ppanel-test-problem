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
select
    c.id "ID",
    concat(max(c.first_name), ' ', max(c.last_name)) "Name",
    max(o.category) "Category",
    group_concat(o.product separator ',') "Products"
from client_orders co
left join clients c on co.client_id = c.id
left join orders o on co.order_id = o.id
where c.age between 18 and 65
group by c.id
having count(co.order_id) = 2 and count(distinct o.category) = 1;
```

## Problem #2
Implement JSON API using Python to get a lsit of posts from open public Instagram profile.
Multiple clients are allowed to hit the API.
No need in authorization, but no more than 1 request from 1 IP address simultaneously - parallel requests have to be declined.

User is able to send any data for account name, so be aware of invalid ones.

Request format: `<your_domain>/api/v1?method=<method_name>&profile=<username>`
Response format: JSON

API has to support 2 methods:
1. **profile**: Requesting profile info (GET).
    Response in case of success:
    ```json
    {
        "status": "success",
        "code": 200,
        "data": {
            "profile_id": "173560420",
            "avatar_url": "<url>",
            "posts": "3059",
            "followers": "1234",
            "following": "1234"
        }
    }
    ```
    Otherwise:
    ```json
    {
        "status": "error",
        "code": 403,
        "message": "Invalid account name"
    }
    ```

2. **posts**: Requesting posts of given profile id (first 10 pieces)
    Successful response:
    ```json
    {
        "status": "success",
        "code": 200,
        "data": {
            "profile_id": "173560420",
            "avatar_url": "<url>",
            "posts": [
                {
                    "id": "2571529092331506482",
                    "url": "<url>",
                    "preview": "<url>",
                    "likes": "4202387"
                }
            ]
        }
    }
    ```

    Otherwise:
    ```json
    {
        "status": "error",
        "code": 403,
        "message": "Invalid account name"
    }
    ```

    Additional task - to take not first 10 posts but from 11th to 20th

## Problem #2 solution

### Investigation part

Primary idea was to find am I able to use some kind of Instagram API. 
To accomplish that I signed up Facebook Developers portal, but additional permissions are required to get user data.
TO get those permissions you need to describe in what way you are going to use your application and attach a screencast of application usage session.
Then you have to wait for approve from Facebook. So this had to take a while and I decided to parse Instagram manually.
I have found an **Instaloader** tool doing all required operations, like getting user info, extracting posts data e.t.c., but we are not about easy ways.

Let me describe a parsing scenario:
- Get **instagram.com** web page and authorize there;
- Put username to a search field, then take the first result;
    - In case we need to get profile data - just parse it from profile page;
    - If we are about to get posts - iterate over them and get likes amount __(TODO #1: We are unable to get post id from the website)__;

Advantages of described method:
- Experience with Selenium Webdriver
- Simple implementation

Minuses:
- The parser is a way slower than api
- Non-reliable architecture - everything brokes in case of html changed

Usage: #TODO
