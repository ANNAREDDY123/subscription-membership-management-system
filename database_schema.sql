CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(50)
);

CREATE TABLE members(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    membership_type VARCHAR(50),
    status VARCHAR(50)
);

CREATE TABLE subscriptions(
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    plan_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    amount FLOAT,
    status VARCHAR(50)
);

CREATE TABLE payments(
    id INTEGER PRIMARY KEY,
    subscription_id INTEGER,
    amount FLOAT,
    payment_date DATE,
    payment_method VARCHAR(50)
);
