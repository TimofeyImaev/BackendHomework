import time
import random
from datetime import datetime, timedelta
from typing import Generator

import psycopg
from psycopg.rows import tuple_row
import clickhouse_connect
from faker import Faker

NUM_ROWS = 1_000_000
BATCH_SIZE = 50_000
SEED = 1488

PG_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "user": "huy",
    "password": "huy123",
    "dbname": "huy"
}

CH_CONFIG = {
    "host": "localhost",
    "port": 8123,
    "username": "default",
    "password": ""
}

fake = Faker()
Faker.seed(SEED)
random.seed(SEED)

CATEGORIES = ["Electronics", "Clothing", "Home", "Sports", "Books", "Toys", "Food", "Beauty"]
REGIONS = ["North", "South", "East", "West", "Central"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "PayPal", "Cash", "Crypto"]


def generate_rows(num_rows: int) -> Generator[tuple, None, None]:
    """Generate order data rows."""
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    for i in range(1, num_rows + 1):
        order_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        yield (
            i,
            random.randint(1, 100000),
            fake.name(),
            random.choice(CATEGORIES),
            fake.word().capitalize(),
            random.randint(1, 10),
            round(random.uniform(5.0, 500.0), 2),
            round(random.uniform(0, 50.0), 2),
            random.choice(REGIONS),
            random.choice(PAYMENT_METHODS),
            order_date,
        )


def setup_postgres():
    """Create PostgreSQL table."""
    conn = psycopg.connect(**PG_CONFIG)
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            customer_name VARCHAR(100),
            category VARCHAR(50),
            product_name VARCHAR(100),
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            discount DECIMAL(10,2),
            region VARCHAR(20),
            payment_method VARCHAR(30),
            order_date TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("PostgreSQL table created")


def setup_clickhouse():
    """Create ClickHouse table."""
    client = clickhouse_connect.get_client(**CH_CONFIG)
    
    client.command("DROP TABLE IF EXISTS orders")
    client.command("""
        CREATE TABLE orders (
            order_id UInt32,
            customer_id UInt32,
            customer_name String,
            category LowCardinality(String),
            product_name String,
            quantity UInt8,
            unit_price Decimal(10,2),
            discount Decimal(10,2),
            region LowCardinality(String),
            payment_method LowCardinality(String),
            order_date DateTime
        ) ENGINE = MergeTree()
        ORDER BY (order_date, category, region)
    """)
    print("ClickHouse table created")


def populate_postgres(rows_generator):
    """Insert data into PostgreSQL."""
    conn = psycopg.connect(**PG_CONFIG)
    cur = conn.cursor()
    
    batch = []
    total = 0
    start = time.time()
    
    for row in rows_generator:
        batch.append(row)
        if len(batch) >= BATCH_SIZE:
            cur.executemany("""
                INSERT INTO orders (order_id, customer_id, customer_name, category, 
                    product_name, quantity, unit_price, discount, region, 
                    payment_method, order_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, batch)
            conn.commit()
            total += len(batch)
            print(f"PostgreSQL: {total:,} rows inserted")
            batch = []
    
    if batch:
        cur.executemany("""
            INSERT INTO orders (order_id, customer_id, customer_name, category, 
                product_name, quantity, unit_price, discount, region, 
                payment_method, order_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, batch)
        conn.commit()
        total += len(batch)
    
    elapsed = time.time() - start
    print(f"PostgreSQL: {total:,} rows in {elapsed:.2f}s ({total/elapsed:,.0f} rows/sec)")
    
    cur.close()
    conn.close()


def populate_clickhouse(rows_generator):
    """Insert data into ClickHouse."""
    client = clickhouse_connect.get_client(**CH_CONFIG)
    
    columns = ['order_id', 'customer_id', 'customer_name', 'category', 
               'product_name', 'quantity', 'unit_price', 'discount', 
               'region', 'payment_method', 'order_date']
    
    batch = []
    total = 0
    start = time.time()
    
    for row in rows_generator:
        batch.append(row)
        if len(batch) >= BATCH_SIZE:
            client.insert('orders', batch, column_names=columns)
            total += len(batch)
            print(f"ClickHouse: {total:,} rows inserted")
            batch = []
    
    if batch:
        client.insert('orders', batch, column_names=columns)
        total += len(batch)
    
    elapsed = time.time() - start
    print(f"ClickHouse: {total:,} rows in {elapsed:.2f}s ({total/elapsed:,.0f} rows/sec)")


def main():
    print(f"=== Populating databases with {NUM_ROWS:,} rows ===\n")
    
    print("Setting up tables...")
    setup_postgres()
    setup_clickhouse()
    print()
    
    print("Populating PostgreSQL...")
    populate_postgres(generate_rows(NUM_ROWS))
    print()
    
    Faker.seed(SEED)
    random.seed(SEED)
    
    print("Populating ClickHouse...")
    populate_clickhouse(generate_rows(NUM_ROWS))
    print()
    
    print("=== Done! Both databases have identical data ===")
    print("\nNow run benchmark_queries.py to compare OLTP vs OLAP performance!")


if __name__ == "__main__":
    main()
