create table users(
	id int NOT NULL AUTO_INCREMENT,
	username varchar(20) not null,
	password varchar(20) not null,
	userlevel varchar(10) not null,
	primary key(id)
);

create table posts(
    postID int PRIMARY KEY AUTO INCREMENT,
    userID int NOT NULL,
    image LargeBinary,
    text varchar(100)
    FOREGIN KEY(userID REFERENCES users(id)
));

create table comments(
    commentID int PRIMARY KEY AUTO INCREMENT,
    commenterID int NOT NULL,
    textComment varchar(100)
);

create table friends(
    userID int NOT NULL,
    friendID int NOT NULL
);

create table messages(
    msgID PRIMARY KEY AUTO INCREMENT,
    senderID int NOT NULL,
    reciverID int NOT NULL,
    msg varchar(100) NOT NULL
);