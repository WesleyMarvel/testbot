-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 10, 2022 at 10:52 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `testbotzim$kudzi`
--

-- --------------------------------------------------------

--
-- Table structure for table `addetails`
--

CREATE TABLE `addetails` (
  `id` int(11) NOT NULL,
  `detail` varchar(700) NOT NULL,
  `images` mediumtext NOT NULL,
  `adcode` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `addetails`
--

INSERT INTO `addetails` (`id`, `detail`, `images`, `adcode`) VALUES
(1, '*ADVERT*: PR1001\r\n*Location*:  Milton Park, Harare\r\n*Monthly Rent*: US$500.00\r\n*Details*:  A Duplex Flat First Floor - 4 Bedrooms, Main en-suite, two bath-toilet with showers, living room. Ground Floor - Modern fitted kitchen, lounge, dinning, and double lock-up garage.\r\n*Extras*: Borehole, Solar Electricity, Secure brick wall, electric gate, garden\r\n*Date Posted*: 21-08-2020\r\n*WhatsApp*: https://wa.me/263774767325?text=Milton%20Park%20US$500', 'https://images.unsplash.com/photo-1464082354059-27db6ce50048?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'PR1001'),
(2, '*ADVERT*: PR1002\r\n*Location*:  Milton Park, Harare\r\n*Monthly Rent*: US$500.00\r\n*Details*:  A Duplex Flat First Floor - 4 Bedrooms, Main en-suite, two bath-toilet with showers, living room. Ground Floor - Modern fitted kitchen, lounge, dinning, and double lock-up garage.\r\n*Extras*: Borehole, Solar Electricity, Secure brick wall, electric gate, garden\r\n*Date Posted*: 21-08-2020\r\n*WhatsApp*: https://wa.me/263774767325?text=Milton%20Park%20US$500', 'https://images.unsplash.com/photo-1464082354059-27db6ce50048?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60', 'PR1002');

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `phonenumber` varchar(30) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `login_status` varchar(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `phonenumber`, `password`, `login_status`) VALUES
(1, '+263713283959', 'iloveyou', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `ads`
--

CREATE TABLE `ads` (
  `id` int(11) NOT NULL,
  `details` varchar(500) NOT NULL,
  `code` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ads`
--

INSERT INTO `ads` (`id`, `details`, `code`) VALUES
(1, '0', '0'),
(2, 'Advert:PR1001\r\nLocation:Harare\r\nRent:$500.00\r\nDate:21-08-2020', 'SRE1'),
(3, 'Advert:PR1002\r\nLocation:Harare,Mbare\r\nRent:$500.00\r\nDate:21-08-2020', 'SRE1');

-- --------------------------------------------------------

--
-- Table structure for table `advert`
--

CREATE TABLE `advert` (
  `id` int(11) NOT NULL,
  `number_id` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `price` varchar(55) NOT NULL,
  `details` varchar(5000) NOT NULL,
  `extras` varchar(1000) NOT NULL,
  `img` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `whatsapp` varchar(255) NOT NULL,
  `code` varchar(100) NOT NULL,
  `adcode` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `advert`
--

INSERT INTO `advert` (`id`, `number_id`, `location`, `price`, `details`, `extras`, `img`, `date`, `whatsapp`, `code`, `adcode`) VALUES
(1, '0785564315', 'Harare', '45', 'hyfh', 'bkhv', 'yvh', 'hvj', 'hvj', 'gvjvj', 'hkvkj'),
(2, '+263713283959', 'Chitungwiza, Harare', '$200', 'To rent is a super market', 'Dry space', 'https://api.twilio.com/2010-04-01/Accounts/AC070ab23e78b76194e43d527c5839941e/Messages/MM3a79aae516c36fe7c26a243b00d61828/Media/ME7acd71add580272e1d87346bc81871bb', '19-May-2022 (12:20:11)', 'https://wa.me/263713283959', 'RP89417', 'S2');

-- --------------------------------------------------------

--
-- Table structure for table `agents`
--

CREATE TABLE `agents` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `agentcode` varchar(255) NOT NULL,
  `number` varchar(255) NOT NULL,
  `idnumber` varchar(255) NOT NULL,
  `address` varchar(500) NOT NULL,
  `image` varchar(255) NOT NULL,
  `smage` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `agents`
--

INSERT INTO `agents` (`id`, `name`, `agentcode`, `number`, `idnumber`, `address`, `image`, `smage`) VALUES
(1, '', '', '00000000', '', '', '', ''),
(2, '', '', '00000000', '', '', '', ''),
(3, ' GRACE CHIWOCHA', 'AG127', '+263774767325', ' 63-374637$76', ' GLEN ROAD, GRANGE', 'https://api.twilio.com/2010-04-01/Accounts/AC71c5e4771b4c9fcab6645fafeec7b5f4/Messages/MM749fea99be7de77252874806f5166f8e/Media/MEa160884ce9dc08aeb3068bc0c229b347', 'https://api.twilio.com/2010-04-01/Accounts/AC71c5e4771b4c9fcab6645fafeec7b5f4/Messages/MMcea363c24acf8c25bb31c8e6727fffad/Media/MEef848aa54d5563da0841c06b5d8a6063'),
(5, ' TAWANDA CHOTO', 'AG642', '+263734277826', ' 636374G48', '* 18 ROAD, MY PLEASANT', 'https://api.twilio.com/2010-04-01/Accounts/AC71c5e4771b4c9fcab6645fafeec7b5f4/Messages/MM8ea46f967c7bbfe2ccf6bfa43f63b7b6/Media/MEf4594651a38ea0cd84427fd25d69dcd8', 'https://api.twilio.com/2010-04-01/Accounts/AC71c5e4771b4c9fcab6645fafeec7b5f4/Messages/MM175b8c32da7c0fdb9d1a6c05d8cf59db/Media/ME5728282c2f95a242b68758cf4f8fb447'),
(6, ' WESLEY MAMBINGE', 'AG2724', '+263785564315', ' 63-2128454-V-47', ' 23063 UNIT L SEKE', 'https://api.twilio.com/2010-04-01/Accounts/ACe0f2a11ce63bac299e2db3dba4944759/Messages/MM5a538c1ec0cd085c6431facdc98b5a3d/Media/ME3d25884a53fb295d50a46902ab03547d', 'https://api.twilio.com/2010-04-01/Accounts/ACe0f2a11ce63bac299e2db3dba4944759/Messages/MM9c36ed9a1e796239912e0acef04a34b6/Media/ME971610afab80822e567dc5eed0789bf8'),
(7, ' JOHN HOKO', 'AG2136', '+263714349795', ' 63-21223-D-63', '  14 MOPANI AVENUE GLEN NORAH, HARARE', 'https://api.twilio.com/2010-04-01/Accounts/ACe0f2a11ce63bac299e2db3dba4944759/Messages/MMaf2ccb70977ada5c060900a8f72e2052/Media/MEffa5aa016622d1b64efa9a5aa3343cfb', 'https://api.twilio.com/2010-04-01/Accounts/ACe0f2a11ce63bac299e2db3dba4944759/Messages/MM901b57ab79096f886466e005df542320/Media/ME67b1b74285fa6e1c35509f06a2fdf688'),
(8, ' WESLEY MAMBINGE', 'AG2724', '+263715008425', ' 63-2128454-V-47', ' 23063 UNIT L SEKE', 'https://api.twilio.com/2010-04-01/Accounts/ACe0f2a11ce63bac299e2db3dba4944759/Messages/MM5a538c1ec0cd085c6431facdc98b5a3d/Media/ME3d25884a53fb295d50a46902ab03547d', 'https://api.twilio.com/2010-04-01/Accounts/ACe0f2a11ce63bac299e2db3dba4944759/Messages/MM9c36ed9a1e796239912e0acef04a34b6/Media/ME971610afab80822e567dc5eed0789bf8'),
(9, ' WESLEY MAMBINGE', 'AG1063', '+263713283959', ' 63-2128454-V-47', ' 23063 UNIT L EXTENSION, CHITUNGWIZA, HARARE', 'https://api.twilio.com/2010-04-01/Accounts/AC070ab23e78b76194e43d527c5839941e/Messages/MM840cc30548952c13e96d1cb981f766b5/Media/ME03775d8f84e7ac72e1742b268731fd01', 'https://api.twilio.com/2010-04-01/Accounts/AC070ab23e78b76194e43d527c5839941e/Messages/MMe0073e3c0ae6ee041c7c62c99675b489/Media/ME18a07be13f61b8364ab3f33b2288e47e');

-- --------------------------------------------------------

--
-- Table structure for table `headimg`
--

CREATE TABLE `headimg` (
  `id` int(11) NOT NULL,
  `img` varchar(500) NOT NULL,
  `img1` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `headimg`
--

INSERT INTO `headimg` (`id`, `img`, `img1`) VALUES
(1, 'https://api.twilio.com/2010-04-01/Accounts/ACe0f2a11ce63bac299e2db3dba4944759/Messages/MM20b3a9fde7940bfe14908ec17a87d290/Media/ME352292e6d00be7ec330a23cd0efe86be', 'https://api.twilio.com/2010-04-01/Accounts/ACe0f2a11ce63bac299e2db3dba4944759/Messages/MMf3d7ff228693b0b3ab1eb52933c75aba/Media/MEa868426ce8de6b43cc4495f7a25d015e');

-- --------------------------------------------------------

--
-- Table structure for table `sre1`
--

CREATE TABLE `sre1` (
  `id` int(11) NOT NULL,
  `Advert` varchar(255) NOT NULL,
  `Location` varchar(255) NOT NULL,
  `Rent` varchar(255) NOT NULL,
  `Details` varchar(255) NOT NULL,
  `Extras` varchar(255) NOT NULL,
  `Date` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6),
  `Whatsapp` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sre1`
--

INSERT INTO `sre1` (`id`, `Advert`, `Location`, `Rent`, `Details`, `Extras`, `Date`, `Whatsapp`) VALUES
(1, 'PR1001', 'Milton Park, Harare', 'US$500.00', 'A Duplex Flat\\nFirst Floor - 4 Bedrooms, Main en-suite, two bath-toilet with showers, living room. Ground Floor - Modern fitted kitchen, lounge, dinning, and double lock-up garage.', 'Borehole, Solar Electricity, Secure brick wall, electric gate, garden', '2020-08-30 22:00:00.000000', 'https://wa.me/263774767325?text=Milton%20Park%20US$500'),
(2, 'P21102', 'harare', '$5000', 'hibyyyfyfyfyhf', 'tbju', '2020-09-08 22:00:00.000000', 'wa.me.');

-- --------------------------------------------------------

--
-- Table structure for table `subscribers`
--

CREATE TABLE `subscribers` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `number` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `reg_time` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `subscribers`
--

INSERT INTO `subscribers` (`id`, `name`, `number`, `status`, `reg_time`) VALUES
(46, ' Wesley Mambinge', '263713283959', 'paid', '2022-08-06 15:30:10.068258'),
(47, ' Munashe Mambinge', '263785564315', 'paid', '2022-07-17 11:43:35.496916');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `addetails`
--
ALTER TABLE `addetails`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ads`
--
ALTER TABLE `ads`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `advert`
--
ALTER TABLE `advert`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `agents`
--
ALTER TABLE `agents`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `headimg`
--
ALTER TABLE `headimg`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sre1`
--
ALTER TABLE `sre1`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `subscribers`
--
ALTER TABLE `subscribers`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `addetails`
--
ALTER TABLE `addetails`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `ads`
--
ALTER TABLE `ads`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `advert`
--
ALTER TABLE `advert`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `agents`
--
ALTER TABLE `agents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `headimg`
--
ALTER TABLE `headimg`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `sre1`
--
ALTER TABLE `sre1`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `subscribers`
--
ALTER TABLE `subscribers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
