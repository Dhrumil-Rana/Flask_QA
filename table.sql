create table accounts(
	userid int NOT NULL AUTO_INCREMENT,
	username varchar(20) not null,
	password varchar(150) not null,
	role varchar(10) not null,
	primary key(userid)
);

create table posts(
    postID Serial,
    uID int NOT NULL,
    image bytea,
    description varchar(100),
    blocked varchar(50),
    mimetype varchar(50),
    filename varchar(50),
    primary key (postID),
    Constraint fk_accounts 
    Foreign KEY (userid)
    REFERENCES accounts(userid)
);

create table comments(
    commentID Serial PRIMARY KEY ,
    commenterID int NOT NULL,
    textComment varchar(100),
    postID int NOT NULL
);

create table friends(
    "Number" serial primary key,
    "userid" int NOT NULL,
    "friendID" int NOT NULL
);

create table messages(
    msgID Serial PRIMARY KEY,
    senderID int NOT NULL,
    reciverID int NOT NULL,
    msg varchar(100) NOT NULL
);

INSERT INTO accounts(
	username, password, role)
	VALUES ('user', '123', 'U');

INSERT INTO accounts(
	username, password, role)
	VALUES ('admin', 'admin', 'A');

create table posts(
    postID Serial,
    userid int NOT NULL,
    image Binary,
    text varchar(100),
    primary key (postID),
    Constraint fk_accounts 
    Foreign KEY (userid)
    REFERENCES accounts(userid)
);

create table comments(
    commentID Serial PRIMARY KEY ,
    commenterID int NOT NULL,
    textComment varchar(100)
);

create table friends(
    userid int NOT NULL,
    friendID int NOT NULL
);

create table messages(
    msgID Serial PRIMARY KEY,
    senderID int NOT NULL,
    reciverID int NOT NULL,
    msg varchar(100) NOT NULL
);
