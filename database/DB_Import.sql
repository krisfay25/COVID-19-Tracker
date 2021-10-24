CREATE DATABASE  IF NOT EXISTS `ri_data` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ri_data`;
-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: ri_data
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `monthly_cases`
--

DROP TABLE IF EXISTS `monthly_cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_cases` (
  `county` varchar(20) NOT NULL,
  `municipality` varchar(20) NOT NULL,
  `mar_2020` int NOT NULL,
  `apr_2020` int NOT NULL,
  `may_2020` int NOT NULL,
  `jun_2020` int NOT NULL,
  `jul_2020` int NOT NULL,
  `aug_2020` int NOT NULL,
  `sep_2020` int NOT NULL,
  `oct_2020` int NOT NULL,
  `nov_2020` int NOT NULL,
  `dec_2020` int NOT NULL,
  `jan_2021` int NOT NULL,
  `feb_2021` int NOT NULL,
  `mar_2021` int NOT NULL,
  `apr_2021` int NOT NULL,
  `may_2021` int NOT NULL,
  `jun_2021` int NOT NULL,
  `jul_2021` int NOT NULL,
  `aug_2021` int NOT NULL,
  `sep_2021` int NOT NULL,
  `total` int NOT NULL,
  PRIMARY KEY (`municipality`),
  UNIQUE KEY `municipality` (`municipality`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monthly_cases`
--

LOCK TABLES `monthly_cases` WRITE;
/*!40000 ALTER TABLE `monthly_cases` DISABLE KEYS */;
INSERT INTO `monthly_cases` VALUES ('Bristol County','Barrington',9,18,18,5,10,3,15,66,186,343,283,103,111,91,22,3,34,98,93,1513),('Bristol County','Bristol',7,43,37,11,31,35,32,95,335,495,546,169,265,173,41,11,28,66,134,2554),('Providence County','Burrillville',9,44,18,6,19,10,27,74,241,541,415,153,156,191,41,3,14,106,114,2182),('Providence County','Central Falls',7,432,351,78,104,131,89,398,769,655,453,155,125,172,54,26,41,163,150,4353),('Washington County','Charlestown',3,10,3,6,10,3,7,18,81,147,104,56,64,36,12,3,27,63,69,720),('Kent County','Coventry',12,74,54,13,37,34,38,163,739,906,724,269,298,320,118,12,59,244,375,4489),('Providence County','Cranston',46,473,300,98,196,235,163,739,2206,2428,1700,690,837,675,225,65,148,607,623,12454),('Providence County','Cumberland',16,128,52,30,36,62,78,228,535,1031,787,331,350,297,110,12,40,264,290,4677),('Kent County','East Greenwich',0,42,19,11,22,24,9,97,287,352,388,140,135,114,43,5,42,116,92,1938),('Providence County','East Providence',20,197,131,39,60,52,60,265,840,1401,997,349,356,373,150,20,75,297,440,6122),('Washington County','Exeter',3,14,9,3,3,8,3,14,93,128,105,40,64,30,9,5,11,45,57,642),('Providence County','Foster',3,9,8,3,3,7,3,30,77,110,114,48,39,43,25,3,8,31,40,597),('Providence County','Glocester',3,20,18,3,3,13,3,43,125,225,164,54,91,89,15,7,13,69,63,1022),('Washington County','Hopkinton',3,9,6,3,7,3,6,14,110,158,142,73,73,54,17,8,17,63,40,801),('Newport County','Jamestown',3,6,5,3,5,3,5,17,53,95,81,21,24,17,5,3,13,24,26,408),('Providence County','Johnston',7,148,112,43,53,65,86,271,812,1060,727,304,283,333,77,18,78,283,279,5039),('Providence County','Lincoln',12,74,57,18,30,34,36,146,426,601,489,170,180,203,46,8,46,158,164,2898),('Newport County','Little Compton',3,7,3,0,3,0,0,11,14,50,48,13,19,25,5,3,5,8,14,227),('Newport County','Middletown',8,17,13,12,21,11,7,40,96,297,295,97,157,172,38,6,38,146,104,1575),('Washington County','Narragansett',3,33,6,3,8,38,90,213,203,319,269,241,223,95,20,5,22,69,117,1977),('Newport County','Newport',9,26,27,35,36,21,30,64,201,425,499,201,265,324,84,13,78,189,183,2710),('Washington County','North Kingstown',10,54,22,12,15,56,34,115,438,500,466,173,268,162,31,9,44,221,233,2863),('Providence County','North Providence',14,269,147,37,97,89,92,333,754,940,704,372,363,306,135,29,62,289,296,5328),('Providence County','North Smithfield',5,17,23,10,20,8,23,67,149,344,278,108,85,104,25,3,37,88,112,1506),('Providence County','Pawtucket',44,796,536,154,269,256,258,878,1870,2191,1691,684,649,721,277,52,132,644,694,12796),('Newport County','Portsmouth',5,18,21,7,7,11,10,55,114,330,382,74,114,116,28,3,41,113,108,1557),('Providence County','Providence',103,2570,1915,666,607,913,947,2069,5134,5554,3983,1858,2037,2102,693,190,386,1227,1596,34550),('Washington County','Richmond',0,16,11,3,3,3,3,19,88,117,106,25,51,26,20,0,18,53,58,619),('Providence County','Scituate',6,22,13,11,12,12,11,51,227,322,222,72,134,95,43,5,24,83,73,1438),('Providence County','Smithfield',8,52,29,15,32,36,39,124,428,602,525,410,511,316,73,7,26,127,162,3522),('Washington County','South Kingstown',9,47,10,7,11,36,43,147,368,520,405,386,453,222,31,9,29,127,141,3001),('Newport County','Tiverton',7,47,25,5,11,14,19,81,141,338,314,130,106,137,27,17,35,96,97,1647),('Bristol County','Warren',3,24,22,7,14,3,9,55,139,329,254,69,59,82,37,3,13,67,102,1289),('Kent County','Warwick',24,235,159,48,113,109,116,459,1638,1913,1521,575,635,578,172,21,132,544,571,9563),('Kent County','West Greenwich',0,12,5,3,5,5,5,41,88,116,144,31,61,47,9,3,7,54,52,685),('Kent County','West Warwick',11,115,66,35,54,42,42,190,660,697,588,224,274,313,86,15,36,197,288,3933),('Washington County','Westerly',10,40,6,10,14,12,37,71,213,410,432,197,178,79,34,9,47,227,219,2245),('Providence County','Woonsocket',8,181,194,71,66,90,60,237,590,1156,1073,328,489,486,196,12,86,472,442,6237);
/*!40000 ALTER TABLE `monthly_cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monthly_vax_nums`
--

DROP TABLE IF EXISTS `monthly_vax_nums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_vax_nums` (
  `county` varchar(20) NOT NULL,
  `municipality` varchar(20) NOT NULL,
  `population` int NOT NULL,
  `dec_2020` int NOT NULL,
  `jan_2021` int NOT NULL,
  `feb_2021` int NOT NULL,
  `mar_2021` int NOT NULL,
  `apr_2021` int NOT NULL,
  `may_2021` int NOT NULL,
  `jun_2021` int NOT NULL,
  `jul_2021` int NOT NULL,
  `aug_2021` int NOT NULL,
  `sep_2021` int NOT NULL,
  `oct_2021` int NOT NULL,
  PRIMARY KEY (`municipality`),
  UNIQUE KEY `municipality` (`municipality`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monthly_vax_nums`
--

LOCK TABLES `monthly_vax_nums` WRITE;
/*!40000 ALTER TABLE `monthly_vax_nums` DISABLE KEYS */;
INSERT INTO `monthly_vax_nums` VALUES ('Bristol County','Barrington',16178,2,148,1205,4816,7031,1794,2705,191,87,289,69),('Bristol County','Bristol',22234,0,192,1359,4451,5571,926,1207,156,156,481,109),('Providence County','Burrillville',16453,0,171,1143,3437,4582,893,1419,182,185,529,113),('Providence County','Central Falls',19382,0,256,1963,3596,1749,598,1707,460,360,1034,221),('Washington County','Charlestown',7780,0,86,702,4435,5552,1133,1826,198,182,471,92),('Kent County','Coventry',34575,0,112,875,3606,5285,1004,1378,243,236,719,162),('Providence County','Cranston',81196,2,162,1191,3608,5324,1085,1531,246,288,796,165),('Providence County','Cumberland',34652,0,126,1148,5153,5322,961,1350,216,177,533,119),('Kent County','East Greenwich',13073,0,139,1105,4021,6049,1645,2641,226,157,576,147),('Providence County','East Providence',47449,2,155,1113,2937,4504,924,1372,276,220,627,133),('Washington County','Exeter',6782,0,135,1013,4428,6079,1018,1238,171,145,542,139),('Providence County','Foster',4689,0,201,1341,3424,4670,993,1539,137,201,436,67),('Providence County','Glocester',10062,0,197,1340,3442,4519,1181,2046,145,247,634,122),('Washington County','Hopkinton',8111,0,92,708,4312,5637,1316,2265,206,243,668,137),('Newport County','Jamestown',5496,0,68,647,5557,6730,1112,1407,109,132,385,83),('Providence County','Johnston',29235,2,157,1127,3703,5042,882,1198,223,274,862,198),('Providence County','Lincoln',21644,2,261,1822,4616,5736,1061,1480,202,214,519,94),('Newport County','Little Compton',3505,0,130,991,4198,5417,770,738,110,1,4,1),('Newport County','Middletown',16078,0,141,1056,4602,5843,1055,1512,195,181,504,105),('Washington County','Narragansett',15550,0,93,796,5226,5925,828,977,143,129,389,86),('Newport County','Newport',24762,0,102,767,3264,4135,789,1263,218,170,517,117),('Washington County','North Kingstown',26207,0,102,867,4913,6267,1119,1524,204,167,513,117),('Providence County','North Providence',32459,2,182,1305,3969,5316,937,1309,263,225,810,204),('Providence County','North Smithfield',12349,0,134,940,4181,5643,961,1369,198,222,550,102),('Providence County','Pawtucket',71756,2,107,848,3501,5141,964,1465,380,270,873,205),('Newport County','Portsmouth',17418,0,120,935,4274,5835,1135,1531,145,130,383,84),('Providence County','Providence',179435,2,92,709,3111,4437,963,1777,410,317,964,217),('Washington County','Richmond',7626,0,86,676,4335,5322,1229,2263,264,213,716,172),('Providence County','Scituate',10603,2,184,1283,4210,5727,1005,1297,150,263,808,183),('Providence County','Smithfield',21630,0,256,1702,3654,5205,897,1076,133,186,526,111),('Washington County','South Kingstown',30735,0,90,771,4605,5059,857,1229,145,178,370,53),('Newport County','Tiverton',15816,0,89,763,4045,4618,756,954,119,122,276,45),('Bristol County','Warren',10488,0,223,1568,4394,5770,1062,1428,171,168,577,142),('Kent County','Warwick',81079,0,129,1071,3955,5206,1046,1442,238,219,657,146),('Kent County','West Greenwich',6179,0,150,1129,4133,5147,913,1247,180,236,591,111),('Kent County','West Warwick',28955,0,91,748,3375,4987,945,1271,235,283,781,162),('Washington County','Westerly',22624,0,121,873,3908,5611,840,956,182,218,565,110),('Providence County','Woonsocket',41539,0,72,513,2327,3611,725,1293,309,251,702,147);
/*!40000 ALTER TABLE `monthly_vax_nums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `municipality`
--

DROP TABLE IF EXISTS `municipality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `municipality` (
  `county` varchar(20) NOT NULL,
  `municipality` varchar(20) NOT NULL,
  `total_cases` int NOT NULL,
  `case_rate_per_100k` int NOT NULL,
  `total_hospital` int NOT NULL,
  `hospital_rate_per_100k` int NOT NULL,
  `total_deaths` int NOT NULL,
  `death_rate_per_100k` int NOT NULL,
  `total_vaccinated` int NOT NULL,
  `vaccinated_rate_per_100k` int NOT NULL,
  PRIMARY KEY (`municipality`),
  UNIQUE KEY `municipality` (`municipality`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `municipality`
--

LOCK TABLES `municipality` WRITE;
/*!40000 ALTER TABLE `municipality` DISABLE KEYS */;
INSERT INTO `municipality` VALUES ('Bristol County','Barrington',1615,9983,89,550,17,105,12466,77055),('Bristol County','Bristol',2850,12818,138,621,77,346,13504,60736),('Providence County','Burrillville',2382,14478,100,608,71,432,9055,55036),('Providence County','Central Falls',4853,25039,271,1398,27,139,12036,62099),('Washington County','Charlestown',745,9576,35,450,3,0,5255,67545),('Kent County','Coventry',4991,14435,295,853,107,309,23148,66950),('Providence County','Cranston',14208,17498,842,1037,159,196,52758,64976),('Providence County','Cumberland',5001,14432,273,788,86,248,22658,65387),('Kent County','East Greenwich',2068,15819,97,742,29,222,10363,79270),('Providence County','East Providence',6819,14371,501,1056,207,436,29842,62893),('Washington County','Exeter',700,10321,42,619,7,103,4527,66750),('Providence County','Foster',621,13244,27,576,6,128,2629,56067),('Providence County','Glocester',1073,10664,39,388,7,70,5946,59094),('Washington County','Hopkinton',825,10171,49,604,3,0,5176,63815),('Newport County','Jamestown',414,7533,12,218,3,0,4177,76001),('Providence County','Johnston',5527,18905,374,1279,167,571,18664,63841),('Providence County','Lincoln',3212,14840,211,975,76,351,14574,67335),('Newport County','Little Compton',232,6619,3,0,3,0,1963,56006),('Newport County','Middletown',1700,10573,78,485,11,68,10706,66588),('Washington County','Narragansett',2003,12881,50,322,9,58,9758,62752),('Newport County','Newport',2847,11497,121,489,14,57,13565,54782),('Washington County','North Kingstown',3152,12027,160,611,83,317,19718,75239),('Providence County','North Providence',5765,17761,399,1229,129,397,20808,64105),('Providence County','North Smithfield',1729,14001,110,891,65,526,8027,65001),('Providence County','Pawtucket',13211,18411,803,1119,135,188,41624,58008),('Newport County','Portsmouth',1637,9398,46,264,10,57,11116,63819),('Providence County','Providence',36035,20082,2536,1413,558,311,105735,58927),('Washington County','Richmond',637,8353,31,407,3,0,5030,65959),('Providence County','Scituate',1463,13798,67,632,6,57,6869,64784),('Providence County','Smithfield',4045,18701,241,1114,155,717,13678,63236),('Washington County','South Kingstown',3175,10330,120,390,38,124,18551,60358),('Newport County','Tiverton',1730,10938,22,139,15,95,7829,49501),('Bristol County','Warren',1465,13968,92,877,55,524,6900,65789),('Kent County','Warwick',10214,12598,644,794,194,239,55658,68647),('Kent County','West Greenwich',707,11442,24,388,3,0,4075,65949),('Kent County','West Warwick',4149,14329,235,812,58,200,18409,63578),('Washington County','Westerly',2411,10657,139,614,36,159,13320,58876),('Providence County','Woonsocket',6855,16503,493,1187,228,549,21042,50656);
/*!40000 ALTER TABLE `municipality` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-24 12:04:13
