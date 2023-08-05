import random
import time
import mysql.connector

# Function to generate random subscriptions data
def generate_subscriptions(last_run_time):
    subscriptions = []
    for _ in range(10):
        start_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(random.randint(int(last_run_time), int(time.time()))))
        start_timestamp = int(time.mktime(time.strptime(start_date, "%Y-%m-%d %H:%M:%S")))
        expiration_timestamp = start_timestamp + 28 * 24 * 60 * 60  # Adding 28 days in seconds
        expiration_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expiration_timestamp))
        subscription = {
            "subscription_id": random.randint(1, 10000),
            "user_id": random.randint(1, 100),
            "subscription_type": random.choice(["basic", "premium"]),
            "start_date": start_date,
            "expiration_date": expiration_date,
        }
        subscriptions.append(subscription)
    return subscriptions

# Function to create the subscriptions table
def create_table(conn):
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS subscriptions (
        subscription_id INT PRIMARY KEY,
        user_id INT,
        subscription_type VARCHAR(255),
        start_date TIMESTAMP,
        expiration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(query)
    conn.commit()

    cursor.close()

# Function to save data to MySQL database using mysql-connector
def save_to_mysql(subscriptions):
    conn = mysql.connector.connect(
        user="root",
        password="root",
        host="127.0.0.1",  # Change this to your MySQL host
        port=3307,
        database="alex"
    )

    # Create the table if it doesn't exist
    create_table(conn)

    cursor = conn.cursor()

    for subscription in subscriptions:
        query = """
            INSERT INTO subscriptions (subscription_id, user_id, subscription_type, start_date, expiration_date)
            VALUES (%s, %s,%s, %s, %s)
        """
        values = (
            subscription["subscription_id"],
            subscription["user_id"],
            subscription["subscription_type"],
            subscription["start_date"],
            subscription["expiration_date"]
        )
        cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

interval_seconds = 6 * 60 * 60  # 6 hours in seconds

last_run_time = time.time() - interval_seconds

while True:
    current_time = time.time()
    subscriptions_data = generate_subscriptions(last_run_time)

    # Insert data into MySQL using mysql-connector
    save_to_mysql(subscriptions_data)

    print(f"Subscriptions data updated at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(interval_seconds)

