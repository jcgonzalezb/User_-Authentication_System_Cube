-- Drop database
DROP DATABASE IF EXISTS cubeTestDb;

-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS cubeTestDb;
FLUSH PRIVILEGES;

USE cubeTestDb;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `roleId` varchar(60) NOT NULL,
  `role` varchar(60) NOT NULL,
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `role`
--
LOCK TABLES `role` WRITE;
INSERT INTO `role` VALUES ('1adm','Admin'),('2ru','regular_user');
UNLOCK TABLES;

--
-- Table structure for table `industries`
--

DROP TABLE IF EXISTS `industry`;
CREATE TABLE `industry` (
  `industryId` varchar(60) NOT NULL,
  `industryName` varchar(60) NOT NULL,
  PRIMARY KEY (`industryId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `industry`
--
LOCK TABLES `industry` WRITE;
INSERT INTO `industry` VALUES ('01','Proptech'),('02','LegalTech'),('03','HealthTech'),('04','TravelTech'),('05','FinTech'),('06','MarketPlace'),('07','E-Commerce'),('08','EvenTech'),('09','SAAS');
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `userId` varchar(60) NOT NULL,
  `firstname` varchar(128) NOT NULL,
  `lastname` varchar(128) NOT NULL,
  `cityOfResidence` varchar(128) NOT NULL,
  `countryOfResidence` varchar(128) NOT NULL,
  `photoUrl` varchar(128) NOT NULL,
  `phone` varchar(128) NOT NULL,
  `emailAddress` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `admin` BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--
LOCK TABLES `user` WRITE;
INSERT INTO `user` VALUES
('1c58aa79-cffa-470d-9022-2b0c1ab38d4f','Santiago','Rojas', 'Bogota', 'Colombia','www.google.com', '573111236930', 'sr@cube.ventures', 'sha256$7wHPKBuBjR7cvLL5$45ffc9de6248df9c436fc646c928f2921c39a1500c623ef2de04d88c2b05af0b', 1),
('805f8e9d-1e44-4c84-b3a9-6a86d34f444a','Ana','Buving', 'San Antonio', 'USA', 'www.google.com', '573111233300', '120@gmail.com', 'sha256$pRzF5bkZFUX2StJf$6e9d1a0cbbc176c4b8eb4fdca1392419186e82eaaae8d8774608896a40292bcf', 0),
('82bbeca4-a6fc-480a-9950-2c6454b8d596','complete','access', 'Bogota', 'Colombia','www.google.com', '573111236930', '111@gmail.com', 'sha256$tgphlrrnsDYJUWKo$c98266f95cc86a3fdd5a51fe075685a736be5a98600f88ae8efd148a075745b3', 1),
('e76fb764-e02e-4054-aa41-fab816bf5189','user','access', 'Bogota', 'Colombia','www.google.com', '573111236930', '809@gmail.com', 'sha256$Hn5LCYhGVWgwr7p7$4d82f4508fcabb79230766bff8e509174b50c8618493b4cf5e0ed36b20ed4477', 0),
('22253d96-f805-479c-babc-34e96fb0baf1','Jack','Dole', 'Mexico', 'Mexico DF','www.google.com', '573111437380', '423@gmail.com', 'sha256$PXqYLEm2CWhO8YaZ$548c59848704bed18aa3d4d01d5fa9ae670103823df5c15a9e191f1c6cf4534b', 0)
;
UNLOCK TABLES;


--
-- Table structure for table `startup`
--

DROP TABLE IF EXISTS `startup`;
CREATE TABLE `startup` (
  `startupId` varchar(60) NOT NULL,
  `userId` varchar(60) NOT NULL,
  `name` varchar(128) NOT NULL,
  `photoUrl` varchar(128) NOT NULL,
  `country` varchar(60) NOT NULL,
  `city` varchar(60) NOT NULL,
  `emailAddress` varchar(60) NOT NULL,
  `phone` varchar(60) NOT NULL,
  `founders` SMALLINT NOT NULL,
  `femaleFounders` SMALLINT NOT NULL,
  `industry` varchar(60) NOT NULL,
  `active` BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`startupId`),
  FOREIGN KEY (`industry`) REFERENCES `industry` (`industryId`),
  FOREIGN KEY (`userId`) REFERENCES `user` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `startup`
--
LOCK TABLES `startup` WRITE;
INSERT INTO `startup` VALUES
('start1','805f8e9d-1e44-4c84-b3a9-6a86d34f444a', 'asisvisa','www.google.com', 'USA', 'New York', '123@cube.com', '12105661896', '3', '1', '01', '1'),
('start2','e76fb764-e02e-4054-aa41-fab816bf5189', 'tesla', 'www.google.com', 'USA', 'Silicon Valley', '902@cube.com', '573111234890', '3', '2','03', '1'),
('start3','22253d96-f805-479c-babc-34e96fb0baf1', 'torre', 'www.google.com', 'USA', 'Silicon Valley', '456@cube.com', '12105661896', '2', '1','02', '1');
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `permissionId` varchar(60) NOT NULL,
  `permissionRight` varchar(128) NOT NULL,
  PRIMARY KEY (`permissionId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `permission`
--
LOCK TABLES `permission` WRITE;
INSERT INTO `permission` VALUES ('0A1','admin_right'),('0B2','ruser_right');
UNLOCK TABLES;



--
-- Table structure for table `userRole`
--

DROP TABLE IF EXISTS `userRole`;
CREATE TABLE `userRole` (
  `userId` varchar(60) NOT NULL,
  `roleId` varchar(60) NOT NULL,
  FOREIGN KEY (`userId`) REFERENCES `user` (`userId`),
  FOREIGN KEY (`roleId`) REFERENCES `role` (`roleId`),
  PRIMARY KEY (`userId`, `roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `userRole`
--
LOCK TABLES `userRole` WRITE;
INSERT INTO `userRole` VALUES
('1c58aa79-cffa-470d-9022-2b0c1ab38d4f', '1adm'),
('805f8e9d-1e44-4c84-b3a9-6a86d34f444a','2ru'),
('22253d96-f805-479c-babc-34e96fb0baf1','2ru'),
('82bbeca4-a6fc-480a-9950-2c6454b8d596','1adm'),
('e76fb764-e02e-4054-aa41-fab816bf5189','2ru') ;

UNLOCK TABLES;


--
-- Table structure for table `rolePermission`
--

DROP TABLE IF EXISTS `rolePermission`;
CREATE TABLE `rolePermission` (
  `roleId` varchar(60) NOT NULL,
  `permissionId` varchar(60) NOT NULL,
  FOREIGN KEY (`roleId`) REFERENCES `role` (`roleId`),
  FOREIGN KEY (`permissionId`) REFERENCES `permission` (`permissionId`),
  PRIMARY KEY (`roleId`, `permissionId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rolePermission`
--
LOCK TABLES `rolePermission` WRITE;
INSERT INTO `rolePermission` VALUES ('1adm','0A1'),('2ru','0B2');
UNLOCK TABLES;



--
-- Table structure for table `kpiRegister`
--

DROP TABLE IF EXISTS `kpiRegister`;
CREATE TABLE `kpiRegister` (
  `kpiId` varchar(60) NOT NULL,
  `date` date NOT NULL,
  `startupId` varchar(60) NOT NULL,
  `revenue` FLOAT NOT NULL,
  `ARR` FLOAT NOT NULL,
  `EBITDA` FLOAT NOT NULL,
  `GMV` FLOAT NOT NULL,
  `numberEmployees` SMALLINT NOT NULL,
  `fundRaising` FLOAT NOT NULL,
  `CAC` FLOAT NOT NULL,
  `activeClients` mediumint NOT NULL,
  FOREIGN KEY (`startupId`) REFERENCES `startup` (`startupId`),
  PRIMARY KEY (`kpiId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `kpiRegister`
--
LOCK TABLES `kpiRegister` WRITE;
INSERT INTO `kpiRegister` VALUES
('kpi1','2022-03-21','start1','100000', '20000', '4000', '1000', '20', '100000', '500', '30'),
('kpi2','2022-03-22','start2','200000', '20000', '5000', '2000', '10', '110000', '600', '40'),
('kpi3','2022-03-23','start3','300000', '20000', '6000', '3000', '13', '120000', '700', '50')
;
UNLOCK TABLES;

CREATE USER IF NOT EXISTS '1c58aa79'@'localhost' IDENTIFIED BY 'dasdasd';
CREATE USER IF NOT EXISTS '22253d96'@'localhost' IDENTIFIED BY '78923123';
CREATE USER IF NOT EXISTS '805f8e9d'@'localhost' IDENTIFIED BY '432fwwe4';
CREATE USER IF NOT EXISTS '82bbeca4'@'localhost' IDENTIFIED BY 'fwew323';
CREATE USER IF NOT EXISTS 'e76fb764'@'localhost' IDENTIFIED BY '3423kdqdq';
GRANT ALL PRIVILEGES ON `cubeTestDb`.* TO '1c58aa79'@'localhost' WITH GRANT OPTION;
GRANT SELECT ON `performance_schema`.* TO '1c58aa79'@'localhost';
GRANT SELECT, INSERT, UPDATE ON cubeTestDb.kpiRegister TO '22253d96'@'localhost';
GRANT SELECT, INSERT, UPDATE ON cubeTestDb.kpiRegister TO '805f8e9d'@'localhost';
GRANT SELECT, INSERT, UPDATE ON cubeTestDb.kpiRegister TO '82bbeca4'@'localhost';
GRANT SELECT, INSERT, UPDATE ON cubeTestDb.kpiRegister TO 'e76fb764'@'localhost';
FLUSH PRIVILEGES;
