

CREATE TABLE IF NOT EXISTS users
(
UserID INT auto_increment PRIMARY KEY NOT NULL,
Username VARCHAR(30) NOT NULL,
UserPassword VARCHAR(30) NOT NULL,
UserRole VARCHAR(30) NOT NULL,
FirstName VARCHAR(50) NOT NULL,
LastName VARCHAR(50) NOT NULL,
Address VARCHAR(100) NOT NULL,
Email VARCHAR(80) NOT NULL,
Phone VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS rental_cars
(
CarID INT auto_increment PRIMARY KEY NOT NULL,
UserID INT NOT NULL,
CarModel VARCHAR(50) NOT NULL,
Registration VARCHAR(30) NOT NULL,
ProductionYear YEAR NOT NULL,
Seating INT NOT NULL,
RentalPerDay FLOAT NOT NULL,
CarImage BLOB,
FOREIGN KEY (UserID) REFERENCES users(UserID)
ON UPDATE CASCADE
ON DELETE CASCADE 
);

INSERT INTO users VALUES 
(1,"nayxie","123456","admin","Nanyue","Xie","12 Rosedale Road, Avondale, Auckland","nayxie@qq.com","0275642341"),
(2,"davemoon","123456","staff","Dave","Moon","1 Bank Road, Johnsonville, Wellington","davemoon@gmail.com","02678888842"),
(3,"jackdaniel","123456","staff","Jack","Daniel","7 Moe Avenue, Avondale, Auckland","jackdaniel@gmail.com","020042341"),
(4,"amoregates","123456","staff","Amore","Gates","124 Moonshine Hill, Devonport, Auckland","amore12345@qq.com","0290123472"),
(5,"adrienmckenzie","123456","customer","Adrien","McKenzie","19 Gillen Road, Green Bay, Auckland","mckenzie_adrien@qq.com","028955541"),
(6,"cuirongli","123456","customer","Cuirong","Li","12 Dunevon Cressent, Onehunga, Auckland","jasmineli01@gmail.com","027662341"),
(7,"lositaloane","123456","customer","Losita","Loane","123 Silverlane Avenue, Te Aro, Wellington","lositaloane@gmail.com","0215642764"),
(8,"jakejohnson","123456","customer","Jake","Johnson","34 Daisy Street, Epsom, Auckland","jakejohnson1990@qq.com","02134530064"),
(9,"spencerzhang","123456","customer","Spencer","Zhang","112 Watersdown Road, Mt Eden, Auckland","spencerzhang@qq.com","0251143410");

INSERT INTO rental_cars VALUES 
(1,5,"Ford","LMW374",2010,5,45,NULL),
(2,6,"BMW","M0O123",2011,5,50,NULL),
(3,5,"Ford","L97S10",2010,5,45,NULL),
(4,6,"BMW","P12FG4",2007,5,47,NULL),
(5,9,"Tesla","JH45P7",2020,5,60,NULL),
(6,9,"Tesla","AW2379",2019,5,60,NULL),
(7,5,"Audi","LT45P1",2008,5,43,NULL),
(8,9,"Range Rover","LJ39T",2010,8,66,NULL),
(9,9,"BMW","DD1374",2008,5,47,NULL),
(10,5,"Ford","GGH394",2010,5,45,NULL),
(11,7,"Audi","9T45RR",2008,5,43,NULL),
(12,7,"Ford","YUU881",2010,5,45,NULL),
(13,7,"Ford","400SAV",2011,5,45,NULL),
(14,7,"Range Rover","TEE451",2010,8,66,NULL),
(15,6,"BMW","QQ123A",2012,5,50,NULL),
(16,6,"BMW","99VC6",2013,5,50,NULL),
(17,6,"Toyota","KLJS12",2010,5,48,NULL),
(18,8,"Toyota","JJ433",2007,5,48,NULL),
(19,8,"Jeep","PA9997",2014,8,65,NULL),
(20,8,"Kia","T88F66",2015,5,45,NULL);










