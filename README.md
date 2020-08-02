# Project Wecan
## Team
* Lakshya A Agarwal
* Manak Bisht
* Anuj
* Pranay Jain
* Karishma Sinha

## Application domain
We will work on making a derivative of ​Kanban-Trello based workflow management tool​. Its
purpose is to provide a smart space to manage sequential, delegated work within an
organisation.
Functionality
Essentially, it works by providing multiple boards to organisations (each detailed within one
database). The multiple boards can represent projects undertaken by the organisation. A board
is created by an admin user. Each board will have multiple lists which represent the different
tasks that comprise the project. Each list itself will have an owner user. Each list has multiple
cards. The cards represent subtasks under each core task. Each card will have associated data.
The data can be a simple string, or even a binary file containing information regarding the task
to be done. Once a subtask is completed the card is marked as done.
Possible Features
● There is an option to move a card from one list to another
● Each card will have an owner user.
● Each card, list, board will have associated labels.
● A card has an associated deadline
● Comments can be added to cards
● Cards could be deleted.


Bonus Feature
● A user interface based on ​Telegram and Slack​. A chatbot will be created which provides
the features of the system in a very easily accessible manner to the user without the
need to visit any website or install additional software. The user can check on their
pending works, and create new items as required. A task management system should be
very very accessible, and a communication app like telegram, which is a widely used
platform is the perfect place for such a system to operate in.
● A completely ​containerised application​. The system will be built with the concept of
containers in mind. Wecan will be deployable with a single command. The system would
follow the principles of atomicity, such that different containers contain the chatbot and
the database. This will prevent an error in one system from affecting the other.
● Use of ​transactions to ensure ACID properties​ during updates and insertions. The
system is resistant to errors. If there is a crash for any reason, the database doesn’t go
into an inconsistent state. ​Error handling​ principals have been followed throughout the
code.
**Identify who would be the stakeholders (minimum 4) and their roles in using your
system/application.**

1. Administrator (Admin)
    1.1. This is the administrator of the whole system, with the ability to create new user
       registrations, delete users, change permissions
2. Board creator/administrator (Head)
    2.1. This is the localised administrator of a project
3. Board member (Member)
    3.1. These are the members working on a project
4. Manager/HR
    4.1. This individual reports on members’ performance on the task.
5. WeCan IT
    5.1. Ensures code of conduct is abided by
**Document it very clearly and crisply so that any non-db background person can
understand your project. (This would be your work in progress (w-in-p) document)
Week-
What are the key questions your system will be answering for each stakeholder, that is,
for what purpose they will be using your system? Write at least 5 questions for each
stakeholder.**
Syntax of the system
_Page 1_
Home screen


Our ​Telegram and Slack interface​ allows the user to interact using a chatbot. The interface is
very simple to use and let’s the user interact with buttons. Since it is in a chat system, it is
accessible from phones/computers/laptops, and a full history of the users actions is also
present.
Upon opening the chatbot, this sequence will follow:
User: /start
Wecan: Hi. Welcome to Wecan. Send /login to begin login process.
User: /login
Wecan: Type username
User: *enters username*
Wecan: Enter password
User: *enters password*
wecan:
Successfully logged in. Hurray
Choose action

1. Show boards
2. Logout
3. Create board
user:
Show boards
wecan:
Select a board, or press "Go Back"
1. Board 1
2. Board 2
3. Board 3
4. Go Back
User:
Board 1
wecan:
You are in Board: Board 1
Choose action for board: Board 1
1. Show Lists
2. Create list
3. Go Back to Main Menu
User:
Show Lists


wecan:
Select a list, or press "Go Back"

1. List 1
2. List 2
3. Go Back
user:
List 2
wecan:
You are in List: List 2
Choose action for list: List 2
1. Show Cards
2. Create Card
3. Go Back to Board
user:
Show Cards
wecan:
Select a card, or press "Go Back"
1. Card 1
2. Card 2
3. Go Back
And so on based on need.
**Responsibility = Admin**
The admin is the creator of the whole organization. In a company, you can think of it as the
founder/CEO.
Admin gets the option of the following commands-
a) Create new Board *****
b) Enter Board *****
c) Delete Board *****
If option is a), then more commands will be asked for making the list (columns) of the board, the
board head can be assigned, multiple board heads can be assigned, cards can be created.


If option is b), then the admin will get a complete view of the board. The admin has the power
to- Reassign the board head, edit / delete anything (list, card), comment on cards.
If option is c), the board will be deleted and users will be unassigned from the board.
Usage of database

1. Management of an organisation’s projects.
    a. Create boards to initiate new projects.
    b. Delete a board upon the completion or dismissal of a project.
2. Supervise and inspect the ongoing projects to make informed executive decisions
    regarding new projects and ventures.
       a. View which projects have been completed, and which are underway.
       b. View the progress of a single project by checking the status of various lists and
          get minutes of the work being done under the cards.
3. Orient the direction of a project and ensure quality of work.
    a. Add comments on the cards of any board to give directions
    b. Edit/delete cards and lists on a project board as objectives shift
    c. Move cards in between lists as necessary
4. Assign head manager(s) for each project by adding users to the project Board.
    Managing the hierarchical work assignment in an organisation
       a. add/modify the head manager, members for a project board.
5. Assess if the projects are working temporally efficiently
    a. Assign/modify deadlines oncards of a project board
**Responsibility = Head**
A head is often the Head of some board, (or multiple) and has the powers within that board.
When a head logs in, a list of board_ids is listed (of whose access the head has). The Head has
to enter any one of the board_ids to enter the board.
Once that is done. The head has the following options- Create/edit/delete Lists.
Create/edit/delete Cards. Create/edit/delete comments. Move Cards from one list to another.
Usage of database
1. Management of assigned projects.
a. Create lists to initiate new tasks within a project.
b. Delete lists/ cards upon the completion or dismissal of a task/subtask.
2. Supervise and inspect the ongoing project to ensure timely progress.
a. View which lists have been completed, and which are underway.
b. View the progress of a single list by checking the status of various cards.


3. Orient the direction of the project and ensure quality of work.
    a. Add comments on the cards of the board to give direction.
    b. Edit/delete cards and lists on the project board as objectives shift/deadlines get
       completed.
    c. Move cards in between lists as necessary
4. Assign member(s) for each project. Managing the distribution of work within a project
    a. Add/modify the members working on the project.
    b. Assign lists/cards to members according to corresponding domain of expertise
5. Check if the project is progressing on time
    a. View deadlines on lists/cards of the project board
**Responsibility = Member**
A member has access to some boards (can be one) and has limited power. When a member
logs in, a list of board_ids is listed (of whose access the member has). The member has to enter
any one of the board_ids to enter the board.
Once that is done. The member has the following options- Create/edit/delete its​ **OWN** ​Cards.
Create/edit/delete its​ **OWN** ​Comments. Move its ​ **OWN** ​ cards from one list to another.
Usage of database
1. Management of the project’s assigned tasks.
a. Create cards to initiate new subtasks within the list.
b. Edit/Delete their own card upon the completion or dismissal of a subtask.
2. Survey the progress on the ongoing task
a. View which subtasks have been completed, and which are underway.
b. View the progress of the task by checking the status of the list’s cards.
3. Ensure quality of work by incorporating effective collaboration.
a. Add comments on the assigned card(s).
b. Edit/delete comments as the questions are answered, subtask is
modified.
4. Work in an organised manner
a. Assign/modify the label for the card.
b. Move the card under a list


5. Check if the task’s pace of completion is sufficient
    a. View the deadlines on assigned lists/cards of a project board
**Responsibility = HR**
The HR has access to boards to oversee members’ work performance. When the HR logs in, a
list of board_ids is listed (which the HR is overlooking). The HR has to enter any one of the
board_ids to enter the board.
Once that is done. The HR has the following options- view cards, lists of alloted members. HR
has access to post comments and view the work details of the members.
Usage of database
1. Management of an organisation’s project workers.
a. View the ownership of boards.
2. Inspect the ongoing projects to judge efficiency of project managers
a. View which projects have been completed, and which are underway.
b. View the progress of a single project by checking the status of various
lists
3. Ensure a healthy working environment.
a. Add encouraging comments on the lists/cards of any board to keep the
members involved.
b. View the comments on cards and lists on a project board to ensure
members abide by company’s conversational code of conduct.
c. Post general announcements concerning subscribed members
4. Assess the work of the members on the projects
a. View deadlines met by members
b. Recommend efficient workers (judged on tasks completed in given time)
for promotions/bonuses/employee of the month etc
**Responsibility = WeCan IT Team**
The IT team has access to boards of all organisations to ensure that users are abiding by terms
and conditions of code of conduct on the platform. When they log in, a list of organisations is
listed within which board_ids are listed. One has to enter any one of the board_ids to enter the
board.
Once that is done. The IT has the following options- view cards, comments. IT has access to
view comments and if found, delete objectionable content, remove users found in violation.


Usage of database

1. Ensuring code of conduct.
    a. View the ownership of boards.
    b. View the comments on cards and lists on a project board to ensure
       members abide by company’s conversational code of conduct
2. Issue warnings to users
    a. Send warnings as comments if a user is found in violation of code of
       conduct
    b. Remove users
**Think deeply.. What data entities you require for answering these questions, what would
be their attributes and data types, the relationship between these data entities, ....?
Update your w-in-p document
Week-
Based on the requirements identified in Week 2, create database schema and tables
(your system should have a minimum of 10 tables - one for each data entity, and one for
the relationship between them, if required).
Define the schema for each table, and the constraints, like, Foreign key-Primary key
relationship, Referential Integrity constraints, Domain Integrity constraints, range values,
etc. Update your w-in-p document**
_a card is a weak entity determined by a list which is a weak entity determined by board._
**The UML diagram is on the page that follows.
UML V1.**
_Done at the end._


**Week-
Populate/Update these tables by simulated, but meaningful, data with all constrained as
defined in week 3. Each table should have sizable data.
Data simulation:**
We used python-pandas to automate data simulation for the tables in our database
The following encapsulates the basic assumptions of the data that our database contains:

1. In the USER table
    a. There are 1000 entries
    b. Entries for user_name attribute are unique
2. In the TELEGRAM table
    a. All users have a telegram_handle
    b. Entries for telegram_handle attribute are unique
3. In the ORGANISATION table
    a. There are 50 entries
    b. Entries for organisation_name, organisation_email attributes are unique
4. In the BOARD table
    a. There are 50 entries
    b. Each user is assigned to exactly 4 boards
    c. Entries for board_name attribute are unique
5. In the LIST table
    a. There are 200 lists
    b. Entries in list_name attribute are unique
    c. There are 11 list_labels namely - "top-priority, urgent, unimportant, external,
       estimates, backend, frontend, database, ui, ux, contractors"
6. In the CARD table
    a. There are 800 cards,
    b. Entries in card_name attribute are unique
    c. Each list is assigned 4 cards
    d. card_admin are the same as the corresponding list_admin
    e. Multiple cards can have the same multimedia_id
7. In the ANNOUNCEMENTS table
    a. There are 50 announcements


```
b. All 50 announcements are made by a single board_admin each
c. Multiple announcements can have the same multimedia_id
```
8. In the CARD_COMMENT table
    a. There are 800 comments
    b. Each card contains a comment made by the card_admin
9. In the MULTIMEDIA table
    a. There are 800 multimedia objects
10.The MOVE table
    a. It will be created by the user upon moving cards across lists
    b. It is initially empty
**Week-
Mid-project evaluation 1 (based on your w-in-p document
submission, and evaluation of your database application design).
-----------------------------------XXX---------------------------------------------------------
Week-
Identify the attribute(s) to create Indexes based on your
applications/queries.
Indexing**
Indexing has been achieved in our database in the following manner, based on these attributes
for each table :
1) TABLE ORGANISATION
a) Primary
i) organisation_name
2) TABLE USER
a) Primary
i) user_name
ii) organisation_id
3) TABLE BOARD
a) Primary
i) board_name
ii) board_admin
4) TABLE BOARD_USER
i) board_id


ii) user_id
5) TABLE TELEGRAM
a) Primary
i) user_id
ii) telegram_handle
6) TABLE MULTIMEDIA
a) Primary
7) TABLE ANNOUNCEMENT
a) Primary
i) multimedia_id
ii) board_id
iii) user_id
8) TABLE LIST
a) Primary
i) list_name
ii) board_id
iii) list_admin
9) TABLE CARD
a) Primary
i) card_name
ii) multimedia_id
iii) list_id
iv) card_admin
10)TABLE CARD_COMMENT
a) Primary
i) card_id
ii) user_id
11)TABLE DEADLINE
i) card_id
12)TABLE CARD_MOVE
i) card_id
ii) user_id
iii) moved_from_list_id
iv) moved_to_list_id


### ^


**Write at least 10 queries involving various relational algebraic
operations supporting the application features involving database
access and manipulation.**
Added at the end of the document
**Week-
Write at least 8 embedded SQL queries (PL/SQL), advanced
aggregation functions, etc supporting your application features.**
Added at the end of the document
**Week-
Draw the E-R model for your application and update your w-in-p
document.**



**Week-
Continue your previous weeks work.
Assignment will be given this week to submit it in Week 12.
Week-
Continue your previous weeks work.
Identify the key innovative feature and implement it in your application
(for bonus marks).
Week-
Mid-project evaluation 2 (based on your updated (primarily E-R
model) w-in-p document submission, and running (PL/)SQL queries.
Week-
Evaluation of innovative part of your project, if any, by the cross-team
member. The evaluation team will be announced on the same day.
Submission of assignment.**
/usr/local/mysql/bin/mysql -uPranay -p
python checking_connector.py

# NORMALIZATION

## 1NF

**USER** ​(​user_id​, user_name, passwd, full_name, email, telegram_handle, board_id,
organisation_id​, organisation_name, organisation_city, organisation_country,
organisation_country_code, organisation_timezone, organisation_address,
organisation_contact, organisation_email)


**CARD** ​(​card_id​, card_admin, card_name, card_text, multimedia, due_date,
if_completed, ​list_id​, list_name, list_admin, list_label, ​board_id​, board_name,
board_admin)
**CARD_COMMENT** ​(​comment_id​, card_id, user_id, text, creation_time)
​ **ANNOUNCEMENT** ​(​announcement_id​, board_id, user_id, title, body, multimedia,
creation_time)
**CARD_MOVE** ​(​card_id​, ​user_id​, moved_from_list_id, moved_to_ list_id, creation_time)
The above tables are in the first normal form, the​ domain​ of each​ attribute​ contains only
atomic​ values, and the value of each attribute contains only a single value from that
domain.
**2NF**
A database is in the second normal form if it is in the first normal form and it does not
have any ​ _partial dependencies_ ​ i.e. It does not have any​ non-prime attribute​ that is
functionally dependent​ on any​ proper subset​ of any​ candidate key​ of the relation.
In the USER_TABLE, attributes such as ​ _organisation_name_ ​, ​ _organisation_city_ ​,
_organisation_country_ ​, etc are only dependent on ​ _organisation_ ​_id which is a subset of
the primary key. To conform to the second normal form, it is necessary to have two
relations
**USER** ​(​user_id​, user_name, passwd, full_name, email, telegram_handle,
organisation_id​, board_id)
**ORGANISATION** ​(​organisation_id​, organisation_name, organisation_city,
organisation_country, organisation_country_code, organisation_timezone,
organisation_address, organisation_contact, organisation_email)


In the CARD_TABLE, partial dependencies exist, attributes such as ​ _card_name_ ​,
_card_text_ ​, ​ _card_admin_ ​, etc are only functionally dependent on ​ _card_id_ ​. Likewise,
_list_name, list_label_ ​, etc are only dependent on ​ _list_id_ ​. ​ _board_name_ ​, ​ _board_admin_ ​are
only dependent on ​ _board_id_ ​. We will therefore distribute the data over three tables,
**CARD** ​(​card_id​, card_admin, card_name, card_text, multimedia, due_date,
if_completed, list_id)
**LIST** ​(​list_id​, list_name, list_admin, list_label, board_id)
**BOARD** ​(​board_id​, board_name, board_admin)
**CARD_COMMENT** ​, ​ **ANNOUNCEMENT** ​& ​ **CARD_MOVE** ​ remain unchanged.
**3NF**
For a database to be in the third normal form, if it is in the second normal form and has
no ​ _transitive dependencies_ ​. A transitive dependency exists in the table if a non-prime
attribute is functionally dependent on another non-prime attribute. The table is already in
3NF.
**BCNF**
The table is already in BCNF, no prime attribute functionally depends on a non-prime
attribute.
**4NF**
A table in the fourth normal form should not have any multivalued dependencies. X->Y
is a multivalued dependency if for a single value of X, more than one value of Y exists
and Y is independent of the other columns in the relation. In the USER table, a single
_user_id_ ​may correspond to multiple ​ _board_id_ ​s and the ​ _board_id_ ​is independent of the
other columns. We will therefore need to decompose the ORGANISATION_TABLE to,


**USER** ​(​user_id​, user_name, passwd, full_name, email, telegram_handle)
**BOARD_USERS** ​(user_id, board_id)
**Discussion.** ​A single multimedia object may belong to multiple entries.
Therefore, it is better to have another table for storing multimedia objects. Similarly, a
card may have multiple deadlines against it. So, created another table for deadlines.
Also, every user may not have a telegram handle or want to interface with the bot.
Therefore, it was wise to split it into another table.
**UML V**


- UML v


Bonus Feature: Backend architecture
The backend architecture is entirely containerized within 3 separate Docker containers:

1. Bot - Contains the Code for telegram integration
2. Db - Contains the mysql database engine along with the hosted data.


Containerisation ensures the smooth functioning and deployment of the system at minimum
time and also ensures separation of different concerns. Failure on one part of the system
doesn’t affect the other parts in any way.
SQL Queries:
**DDL
Creating tables in the database**
CREATE TABLE ORGANISATION (
organisation_id int NOT NULL auto_increment,
organisation_name varchar(64) NOT NULL,
city varchar (64) NOT NULL,
country varchar(64) NOT NULL,
country_code varchar(8) NOT NULL,
timezone varchar(64) NOT NULL,
address varchar(512) NOT NULL,
contact varchar(16) NOT NULL,
email varchar(128) NOT NULL,
PRIMARY KEY(organisation_id),
UNIQUE KEY(organisation_name)
);
CREATE TABLE USER (
user_id int NOT NULL auto_increment,
user_name varchar(64) NOT NULL,
passwd varchar (128) NOT NULL,
full_name varchar(128) NOT NULL,
email varchar(128) NOT NULL,
organisation_id int NOT NULL,
PRIMARY KEY(user_id),
UNIQUE KEY(user_name),
FOREIGN KEY (organisation_id) REFERENCES
ORGANISATION(organisation_id)
);
CREATE TABLE BOARD (
board_id int NOT NULL auto_increment,
board_name varchar(128) NOT NULL,


board_admin int NOT NULL,
primary key(board_id),
UNIQUE KEY(board_name),
foreign key (board_admin) REFERENCES USER(user_id)
);
CREATE TABLE BOARD_USER (
user_id int NOT NULL,
board_id int NOT NULL,
foreign key (board_id) references BOARD(board_id),
foreign key (user_id) references USER(user_id)
);
CREATE TABLE TELEGRAM (
telegram_id int NOT NULL auto_increment,
telegram_handle varchar(128) NOT NULL,
user_id int NOT NULL,
unique key(user_id),
unique key(telegram_handle),
foreign key (user_id) references USER(user_id),
primary key (telegram_id)
);
CREATE TABLE MULTIMEDIA (
multimedia_id int NOT NULL auto_increment,
multimedia blob NOT NULL,
primary key (multimedia_id)
);
CREATE TABLE ANNOUNCEMENT (
announcement_id int NOT NULL auto_increment,
board_id int NOT NULL,
user_id int NOT NULL,
title varchar(128) NOT NULL,
body varchar(1024) NOT NULL,
multimedia_id int NOT NULL,
creation_time datetime default now(),
foreign key (multimedia_id) references MULTIMEDIA(multimedia_id),
foreign key (board_id) references BOARD(board_id),


foreign key (user_id) references USER(user_id),
primary key (announcement_id)
);
CREATE TABLE LIST(
list_id int NOT NULL auto_increment,
board_id int NOT NULL,
list_admin int NOT NULL,
list_name varchar(128) NOT NULL,
list_label varchar(128) NOT NULL,
foreign key (board_id) references BOARD(board_id),
foreign key (list_admin) references USER(user_id),
UNIQUE KEY(list_name),
primary key (list_id)
);
CREATE TABLE CARD (
card_id int NOT NULL auto_increment,
list_id int NOT NULL,
card_admin int NOT NULL,
card_name varchar(128) NOT NULL,
text varchar(1024) NOT NULL,
multimedia_id int NOT NULL,
foreign key (multimedia_id) references MULTIMEDIA(multimedia_id),
foreign key (list_id) references LIST(list_id),
foreign key (card_admin) references USER(user_id),
UNIQUE KEY(card_name),
primary key (card_id)
);
CREATE TABLE CARD_COMMENT (
comment_id int NOT NULL auto_increment,
card_id int NOT NULL,
user_id int NOT NULL,
text varchar(1024) NOT NULL,
creation_time datetime default now(),
foreign key (card_id) references CARD(card_id),
foreign key (user_id) references USER(user_id),
primary key (comment_id)
);


### CREATE TABLE DEADLINE (

card_id int NOT NULL,
due_date datetime default now(),
if_completed bool not null default 0,
foreign key (card_id) references CARD(card_id)
);
CREATE TABLE CARD_MOVE (
card_id int NOT NULL,
user_id int NOT NULL,
moved_from_list_id int NOT NULL,
moved_to_list_id int NOT NULL,
creation_time datetime default now(),
foreign key (card_id) references CARD(card_id),
foreign key (user_id) references USER(user_id),
foreign key (moved_from_list_id) references LIST(list_id),
foreign key (moved_to_list_id) references LIST(list_id)
);
**DML
SQL QUERIES**

1. ​ **Aggregate query** ​- For an organisation (here id=1) to know what percentage of deadlines are
pending
SELECT
(1-AVG(DEADLINE.if_completed))*100
FROM
DEADLINE,
CARD,
USER
WHERE
DEADLINE.card_id = CARD.card_id
AND CARD.card_admin = USER.user_id
AND USER.organisation_id = 1;
**Group By**
SELECT
CARD.list_id, COUNT(CARD.list_id)
FROM
CARD
GROUP BY CARD.list_id;


### SELECT

USER.organisation_id, COUNT(USER.organisation_id)
FROM
USER
GROUP BY USER.organisation_id;
SELECT
LIST.board_id, COUNT(CARD.list_id)
FROM
CARD,
LIST
WHERE
CARD.list_id = LIST.list_id
GROUP BY LIST.board_id
ORDER BY LIST.board_id ASC;

2. View all deadlines of boards belonging to a user. Replace "1" with your user_id.
SELECT
DEADLINE.card_id, DEADLINE.due_date
FROM
DEADLINE,
CARD,
LIST,
BOARD,
BOARD_USER
WHERE
DEADLINE.if_completed = FALSE
DEADLINE.card_id = CARD.card_id
AND CARD.list_id = LIST.list_id
AND LIST.board_id = BOARD.board_id
AND BOARD.board_id = BOARD_USER.board_id
AND BOARD_USER.user_id = 1;
3. All announcements made in boards of which user is a member
SELECT ANNOUNCEMENT.title from ANNOUNCEMENT, BOARD_USER where
ANNOUNCEMENT.board_id = BOARD_USER.board_id and BOARD_USER.user_id = 1;


4. check_username: "SELECT 1 FROM USER WHERE user_id=\"%s\"",
5. check_login: "SELECT 1 FROM USER WHERE user_id=\"%s\" AND passwd=\"%s\"",
6. list_boards_of_user_where: 'SELECT board_id, board_name FROM BOARD WHERE
board_id IN (SELECT board_id FROM BOARD_USER WHERE user_id="%s" AND
board_id="%s")', # 1.935 sec
7. "list_boards_of_user_join": 'SELECT A.board_id, A.board_name FROM BOARD AS A
INNER JOIN BOARD_USER AS B ON A.board_id=B.board_id WHERE B.user_id="%s"', #
0.072 sec
8. "create_board": 'INSERT INTO BOARD(board_name, board_admin) VALUES (%s, %s)',
9. "add_user_to_board": 'INSERT INTO BOARD_USER(user_id, board_id) VALUES (%s,
%s)',
10. "check_board_without_username": "SELECT 1 FROM BOARD WHERE
board_name=\"%s\" AND board_id=\"%s\"", # Less performant
11. "check_board_with_username": 'SELECT 1 FROM BOARD AS A INNER JOIN
BOARD_USER AS B ON A.board_id=B.board_id WHERE A.board_id="%s" AND
A.board_name="%s" AND B.user_id="%s"', # more performant
12, "get_board_name_by_id": "SELECT board_name FROM BOARD WHERE
board_id=\"%s\"",
13. "create_list": 'INSERT INTO LIST(board_id, list_name, list_admin, list_label) VALUES
("%s", "%s", "%s", "%s")',
14. "list_lists_of_user_board": 'SELECT list_id, list_name FROM LIST WHERE
board_id="%s" AND ("%s", "%s") IN (SELECT user_id, board_id FROM BOARD_USER)',
15. "check_list_with_username": 'SELECT 1 FROM LIST WHERE board_id="%s" AND
list_name="%s" AND list_id="%s" AND ("%s", "%s") IN (SELECT user_id, board_id FROM
BOARD_USER)',
16. "get_list_name_by_id": "SELECT list_name FROM LIST WHERE list_id=\"%s\"",
17. 'list_cards_of_list': 'SELECT card_id, card_name FROM CARD WHERE list_id="%s"
AND 1 IN (SELECT 1 FROM LIST WHERE list_id="%s" AND board_id="%s") AND 1 IN
(SELECT 1 FROM BOARD_USER WHERE board_id="%s" AND user_id="%s")',


18. "check_card_with_username": 'SELECT 1 FROM CARD WHERE card_id="%s" AND
card_name="%s" AND list_id="%s" AND ("%s", "%s") IN (SELECT user_id, board_id FROM
BOARD_USER) AND ("%s", "%s") IN (SELECT list_id, board_id FROM LIST)',
19. 'get_card_name_and_text_by_id': 'SELECT card_name, text FROM CARD where
card_id="%s"',
20. 'get_card_comment_by_card_id': 'SELECT B.full_name, A.text FROM
CARD_COMMENT AS A INNER JOIN USER AS B ON A.user_id=B.user_id WHERE
A.card_id="%s"',
21. 'fetch_pending_deadlines': 'SELECT CARD.card_id, CARD.card_name,
DEADLINE.due_date FROM DEADLINE, CARD, LIST, BOARD, BOARD_USER WHERE
DEADLINE.due_date > CURTIME() AND DEADLINE.if_completed = FALSE AND
DEADLINE.card_id = CARD.card_id AND CARD.list_id = LIST.list_id AND LIST.board_id =
BOARD.board_id AND BOARD.board_id = BOARD_USER.board_id AND
BOARD_USER.user_id="%s"'
**VIEWS**
CREATE VIEW ORGANISATION_BOARDS AS
SELECT
BOARD.board_id,
BOARD.board_name,
USER.user_id,
USER.full_name,
ORGANISATION.organisation_id,
ORGANISATION.organisation_name
FROM
BOARD,
USER,
ORGANISATION
WHERE
BOARD.board_admin = USER.user_id
AND USER.organisation_id = ORGANISATION.organisation_id;
CREATE VIEW ORGANISATION_ANNOUNCEMENTS AS
SELECT
ORGANISATION.organisation_id,
ORGANISATION.organisation_name,
ANNOUNCEMENT.announcement_id,


ANNOUNCEMENT.board_id,
ANNOUNCEMENT.title,
ANNOUNCEMENT.body,
ANNOUNCEMENT.multimedia_id,
ANNOUNCEMENT.creation_time
FROM
USER,
ANNOUNCEMENT,
ORGANISATION
WHERE
USER.user_id = ANNOUNCEMENT.user_id
AND USER.organisation_id = ORGANISATION.organisation_id;
CREATE VIEW ORGANISATION_DEADLINES AS
SELECT
DEADLINE.card_id,
CARD.card_name,
CARD.text,
CARD.multimedia_id,
DEADLINE.due_date,
CARD.card_admin,
USER.full_name,
ORGANISATION.organisation_id,
ORGANISATION.organisation_name
FROM
DEADLINE,
CARD,
USER,
ORGANISATION
WHERE
DEADLINE.card_id = CARD.card_id
AND DEADLINE.if_completed = FALSE
AND CARD.card_admin = USER.user_id
AND USER.organisation_id = ORGANISATION.organisation_id;
**Basic functionality/access of stakeholders**

1. **[DML] Admin**


1.1. Register Organisation in System
1.1.1. INSERT INTO ORGANISATIONS VALUES (1,
demoOganisationNameOne, demoCity, demoCountry, demoCountryCode
ABC, GMT+5:30, demoAddress, demoContact, demoEmail@gmail.com);
1.2. Create new board
1.2.1. INSERT INTO BOARDS VALUES (1, demoBoardNameOne, 1,1);
1.2.2. INSERT INTO BOARDS VALUES (2, demoBoardNameTwo, 1,1);
1.3. Enter Users in Board
1.3.1. INSERT INTO BOARD_USERS VALUES (1,1);
1.3.2. INSERT INTO BOARD_USERS VALUES (2,1);
1.4. Make lists in board
1.4.1. INSERT INTO LISTS VALUES (1, 1, demoListNameOne,1, LabelOne);
1.4.2. INSERT INTO LISTS VALUES (1, 2, demoListNameTwo,1, LabelTwo);
1.5. Make cards in list
1.5.1. INSERT INTO CARDS VALUES (1, 1, demoCardOne,1, DemoText, 1);
1.5.2. INSERT INTO CARDS VALUES (1, 2, demoCardTwo,1, DemoText, 1);
1.6. Add comments in card
1.6.1. INSERT INTO COMMENTS VALUES (1, 1, 1, demoCommentOne,
2020-04-29 19:13:20​);
1.7. Move cards to different list
1.7.1. UPDATE CARDS SET list_id = 2;
INSERT INTO MOVES VALUES (1, 1, 1, 2, ​2020-04-29 19:13:20​);
1.8. Edit Board
1.8.1. UPDATE BOARDS SET name = 'UpdatedBoardName' WHERE id = 1;
1.9. Edit Lists
1.9.1. ​UPDATE LISTS SET name = 'UpdatedListName' WHERE id = 1;
1.10. Edit Cards
1.10.1. UPDATE CARDS SET name = 'UpdatedCardName', text
=’UpdatedDemoText’ WHERE id = 1;
1.11. Delete Board
1.11.1. DELETE FROM BOARDS WHERE id=1;
1.12. Delete List
1.12.1. DELETE FROM LISTS WHERE id=1;
1.13. Delete Card
1.13.1. DELETE FROM CARDS WHERE id=1;
1.14. Add Deadlines
1.14.1. INSERT INTO DEADLINES VALUES (1, ​2020-04-30 23:59:59, false​);
1.15. View Board


```
1.15.1. SELECT * FROM BOARDS WHERE organisation_id=1;
1.16. View Lists
1.16.1. SELECT * FROM LISTS WHERE board_id=1;
1.17. View Cards
1.17.1. SELECT * FROM CARDS WHERE list_id=1;
```
2. **Head**
    2.1. Enter Users in Board
       2.1.1. INSERT INTO BOARD_USERS VALUES (1,1);
       2.1.2. INSERT INTO BOARD_USERS VALUES (2,1);
    2.2. Make lists in board
       2.2.1. INSERT INTO LISTS VALUES (1, 1, demoListNameOne,1, LabelOne);
       2.2.2. INSERT INTO LISTS VALUES (1, 2, demoListNameTwo,1, LabelTwo);
    2.3. Make cards in list
       2.3.1. INSERT INTO CARDS VALUES (1, 1, demoCardOne,1, DemoText, 1);
       2.3.2. INSERT INTO CARDS VALUES (1, 2, demoCardTwo,1, DemoText, 1);
    2.4. Add comments in card
       2.4.1. INSERT INTO COMMENTS VALUES (1, 1, 1, demoCommentOne,
          2020-04-29 19:13:20​);
    2.5. Edit Board
       2.5.1. UPDATE BOARDS SET name = 'UpdatedBoardName' WHERE id = 1;
    2.6. Edit Lists
       2.6.1. ​UPDATE LISTS SET name = 'UpdatedListName' WHERE id = 1;
    2.7. Edit Cards
       2.7.1. UPDATE CARDS SET name = 'UpdatedCardName', text
          =’UpdatedDemoText’ WHERE id = 1;
    2.8. Add Deadlines
       2.8.1. INSERT INTO DEADLINES VALUES (1, ​2020-04-30 23:59:59, false​);
    2.9.
2.10. Delete List
2.10.1. DELETE FROM LISTS WHERE id=1;
2.11. Delete Card
2.11.1. DELETE FROM CARDS WHERE id=1;


```
2.12. View Lists
2.12.1. SELECT * FROM LISTS WHERE board_id=1;
2.13. Move cards to different list
2.13.1. UPDATE CARDS SET list_id = 2;
INSERT INTO MOVES VALUES (1, 1, 1, 2, ​2020-04-29 19:13:20​);
2.14. View Cards
2.14.1. SELECT * FROM CARDS WHERE list_id=1;
```
3. **Member**
    3.1. Make cards in list
       3.1.1. INSERT INTO CARDS VALUES (1, 1, demoCardOne,1, DemoText, 1);
       3.1.2. INSERT INTO CARDS VALUES (1, 2, demoCardTwo,1, DemoText, 1);
    3.2. Add comments in card
       3.2.1. INSERT INTO COMMENTS VALUES (1, 1, 1, demoCommentOne,
          2020-04-29 19:13:20​);
    3.3. Edit Cards
       3.3.1. UPDATE CARDS SET name = 'UpdatedCardName', text
          =’UpdatedDemoText’ WHERE id = 1;
    3.4. Delete Card
       3.4.1. DELETE FROM CARDS WHERE id=1;
    3.5. View Cards
       3.5.1. SELECT * FROM CARDS WHERE list_id=1;
4. **HR**
    4.1. Make Announcements
       4.1.1. INSERT INTO ANNOUNCEMENTS VALUES (1, 1, AnnouncementTitle,
          AnnouncementBody, 1, ​2020-04-29 19:13:20​);
    4.2. View Board
       4.2.1. SELECT * FROM BOARDS WHERE organisation_id=1;
    4.3. View Lists
       4.3.1. SELECT * FROM LISTS WHERE board_id=1;
    4.4. Add comments in card


```
4.4.1. INSERT INTO COMMENTS VALUES (1, 1, 1, demoCommentOne,
2020-04-29 19:13:20​);
4.5. View Cards
4.5.1. SELECT * FROM CARDS WHERE list_id=1;
```
5. **WeCan IT Team**
    5.1. Delete Board
       5.1.1. DELETE FROM BOARDS WHERE id=1;
    5.2. Delete List
       5.2.1. DELETE FROM LISTS WHERE id=1;
    5.3. Delete Card
       5.3.1. DELETE FROM CARDS WHERE id=1;
    5.4. Add comments in card
       5.4.1. INSERT INTO COMMENTS VALUES (1, 1, 1, demoCommentOne,
          2020-04-29 19:13:20​);
    5.5. View Board
       5.5.1. SELECT * FROM BOARDS WHERE organisation_id=1;
    5.6. View Lists
       5.6.1. SELECT * FROM LISTS WHERE board_id=1;
    5.7. View Cards
       5.7.1. SELECT * FROM CARDS WHERE list_id=1;
    5.8. Filter Card containing certain(unwanted word):
       5.8.1. SELECT CARD.card_id FROM CARD WHERE CARD.text REGEXP
          "<word>";


