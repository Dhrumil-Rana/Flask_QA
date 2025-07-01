
-- accounts table
CREATE TABLE if NOT EXISTS accounts (
    userid SERIAL PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(150) NOT NULL,
    role VARCHAR(10) NOT NULL,
    steamid VARCHAR(50) DEFAULT NULL,
);

-- posts table
CREATE TABLE IF NOT EXISTS posts (
    postid SERIAL PRIMARY KEY,
    userid INT NOT NULL REFERENCES accounts(userid),
    image BYTEA,
    description VARCHAR(100),
    blocked VARCHAR(50),
    mimetype VARCHAR(50),
    filename VARCHAR(50)
);

-- comments table
CREATE TABLE IF NOT EXISTS comments (
    commentid SERIAL PRIMARY KEY,
    commenterid INT NOT NULL REFERENCES accounts(userid),
    textcomment VARCHAR(100),
    postid INT NOT NULL REFERENCES posts(postid)
);

-- friends table
CREATE TABLE IF NOT EXISTS friends (
    id SERIAL PRIMARY KEY,
    userid INT NOT NULL REFERENCES accounts(userid),
    friendid INT NOT NULL REFERENCES accounts(userid)
);

-- messages table
CREATE TABLE IF NOT EXISTS messages (
    msgid SERIAL PRIMARY KEY,
    senderid INT NOT NULL REFERENCES accounts(userid),
    reciverid INT NOT NULL REFERENCES accounts(userid),
    msg VARCHAR(100) NOT NULL
);

-- Sample data
-- user password: 123
-- admin password: admin
INSERT INTO accounts (username, password, role, steamid) VALUES ('user', '$2b$12$vvKecmIv/9hc7yKC4YCFwOa80STwjtv6O5wGUnFnCc3D6l0H8J/DG', 'U', '76561198155895913');
INSERT INTO accounts (username, password, role, steamid) VALUES ('admin', '$2b$12$jpfd4/5vucEB2.oJ6lLH8uD069hPp6wvziFmDMcH5T.IDVv0rn8eS', 'A', '76561198262264130');

-- check if the tables are created
SELECT * FROM information_schema.tables WHERE table_schema = 'Gamedb';

-- check the data using the query editor in aws rds
select * from "Gamedb".accounts;