from db import PostgresTable

db = PostgresTable()
db.insert_query("""CREATE TABLE home_orders
(    id SERIAL PRIMARY KEY,
    num integer NOT NULL,
    order_num integer NOT NULL,
    cost_usd integer NOT NULL,
    delivery_time date NOT NULL,
    cost_rub integer
);
""")

