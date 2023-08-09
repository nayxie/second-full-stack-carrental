

CREATE TABLE IF NOT EXISTS users
(
UserID INT auto_increment PRIMARY KEY NOT NULL,
Username VARCHAR(30) NOT NULL,
UserPassword VARCHAR(255) NOT NULL,
UserRole VARCHAR(30) NOT NULL,
FirstName VARCHAR(50),
LastName VARCHAR(50),
Address VARCHAR(100),
Email VARCHAR(80) NOT NULL,
Phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS rental_cars
(
CarID INT auto_increment PRIMARY KEY NOT NULL,
CarModel VARCHAR(50) NOT NULL,
Registration VARCHAR(30) NOT NULL,
ProductionYear INT NOT NULL,
Seating INT NOT NULL,
RentalPerDay DECIMAL(10, 2) NOT NULL,
CarImagePath VARCHAR(255)
);

INSERT INTO users (UserID, Username, UserPassword, UserRole, Email)
VALUES 
(1,"maymay","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","admin","may@qq.com"),
(2,"davemoon","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","staff","davemoon@gmail.com"),
(3,"jackdaniel","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","staff","jackdaniel@gmail.com"),
(4,"amoregates","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","staff","amore12345@qq.com"),
(5,"adrienmckenzie","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","customer","mckenzie_adrien@qq.com"),
(6,"cuirongli","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","customer","jasmineli01@gmail.com"),
(7,"lositaloane","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","customer","lositaloane@gmail.com"),
(8,"jakejohnson","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","customer","jakejohnson1990@qq.com"),
(9,"spencerzhang","$2b$12$88pttaI2ZZY.rDdQGNdcieBhIZE8gBKN5UEK5z37kmj5ar46CB1Pe","customer","spencerzhang@qq.com");

INSERT INTO rental_cars VALUES 
(1,"Ford","LMW374",2010,5,45,"img1.png"),
(2,"BMW","M0O123",2011,5,50,"img2.png"),
(3,"Ford","L97S10",2010,5,45,"img3.png"),
(4,"BMW","P12FG4",2007,5,47,NULL),
(5,"Tesla","JH45P7",2020,5,60,NULL),
(6,"Tesla","AW2379",2019,5,60,NULL),
(7,"Audi","LT45P1",2008,5,43,NULL),
(8,"Range Rover","LJ39T",2010,8,66,NULL),
(9,"BMW","DD1374",2008,5,47,NULL),
(10,"Ford","GGH394",2010,5,45,NULL),
(11,"Audi","9T45RR",2008,5,43,NULL),
(12,"Ford","YUU881",2010,5,45,NULL),
(13,"Ford","400SAV",2011,5,45,NULL),
(14,"Range Rover","TEE451",2010,8,66,NULL),
(15,"BMW","QQ123A",2012,5,50,NULL),
(16,"BMW","99VC6",2013,5,50,NULL),
(17,"Toyota","KLJS12",2010,5,48,NULL),
(18,"Toyota","JJ433",2007,5,48,NULL),
(19,"Jeep","PA9997",2014,8,65,NULL),
(20,"Kia","T88F66",2015,5,45,NULL);
