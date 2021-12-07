CREATE TABLE users (id INTEGER, username TEXT NOT NULL, hash TEXT NOT NULL, PRIMARY KEY(id));
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE minibuses (
    route_id INTEGER NOT NULL,
    district TEXT NOT NULL,
    route_name TEXT NOT NULL,
    company_code TEXT NOT NULL,
    start_name TEXT NOT NULL,
    end_name TEXT NOT NULL,
    url TEXT NOT NULL,
    duration INTEGER NOT NULL,
    price FLOAT NOT NULL,
    route_seq INTEGER NOT NULL
);
CREATE UNIQUE INDEX minibus_idx ON minibuses (route_id, route_seq);
CREATE TABLE user_route_stops (
    route_id INTEGER NOT NULL,
    route_seq INTEGER NOT NULL,
    stop_seq INTEGER NOT NULL,
    user_id INTEGER NOT NULL
);