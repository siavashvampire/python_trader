-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 09, 2023 at 09:20 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `comp_462`
--

-- --------------------------------------------------------

--
-- Table structure for table `candle`
--

CREATE TABLE `candle` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `candle`
--

INSERT INTO `candle` (`id`, `name`) VALUES
(1, 'M1'),
(2, 'S5');

-- --------------------------------------------------------

--
-- Table structure for table `country`
--

CREATE TABLE `country` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `short_name` varchar(50) DEFAULT NULL,
  `flag_unicode` varchar(50) DEFAULT NULL,
  `currency` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `country`
--

INSERT INTO `country` (`id`, `name`, `short_name`, `flag_unicode`, `currency`) VALUES
(1, 'Ascension Island', NULL, '🇦🇨', NULL),
(2, 'Andorra', NULL, '🇦🇩', NULL),
(3, 'United Arab Emirates', NULL, '🇦🇪', NULL),
(4, 'Afghanistan', NULL, '🇦🇫', NULL),
(5, 'Antigua & Barbuda', NULL, '🇦🇬', NULL),
(6, 'Anguilla', NULL, '🇦🇮', NULL),
(7, 'Albania', NULL, '🇦🇱', NULL),
(8, 'Armenia', NULL, '🇦🇲', NULL),
(9, 'Angola', NULL, '🇦🇴', NULL),
(10, 'Antarctica', NULL, '🇦🇶', NULL),
(11, 'Argentina', NULL, '🇦🇷', NULL),
(12, 'American Samoa', NULL, '🇦🇸', NULL),
(13, 'Austria', NULL, '🇦🇹', NULL),
(14, 'Australia', NULL, '🇦🇺', 'AUD'),
(15, 'Aruba', NULL, '🇦🇼', NULL),
(16, 'Åland Islands', NULL, '🇦🇽', NULL),
(17, 'Azerbaijan', NULL, '🇦🇿', NULL),
(18, 'Bosnia & Herzegovina', NULL, '🇧🇦', NULL),
(19, 'Barbados', NULL, '🇧🇧', NULL),
(20, 'Bangladesh', NULL, '🇧🇩', NULL),
(21, 'Belgium', NULL, '🇧🇪', NULL),
(22, 'Burkina Faso', NULL, '🇧🇫', NULL),
(23, 'Bulgaria', NULL, '🇧🇬', NULL),
(24, 'Bahrain', NULL, '🇧🇭', NULL),
(25, 'Burundi', NULL, '🇧🇮', NULL),
(26, 'Benin', NULL, '🇧🇯', NULL),
(27, 'St. Barthélemy', NULL, '🇧🇱', NULL),
(28, 'Bermuda', NULL, '🇧🇲', NULL),
(29, 'Brunei', NULL, '🇧🇳', NULL),
(30, 'Bolivia', NULL, '🇧🇴', NULL),
(31, 'Caribbean Netherlands', NULL, '🇧🇶', NULL),
(32, 'Brazil', NULL, '🇧🇷', 'BRL'),
(33, 'Bahamas', NULL, '🇧🇸', NULL),
(34, 'Bhutan', NULL, '🇧🇹', NULL),
(35, 'Bouvet Island', NULL, '🇧🇻', NULL),
(36, 'Botswana', NULL, '🇧🇼', NULL),
(37, 'Belarus', NULL, '🇧🇾', NULL),
(38, 'Belize', NULL, '🇧🇿', NULL),
(39, 'Canada', NULL, '🇨🇦', 'CAD'),
(40, 'Cocos (Keeling) Islands', NULL, '🇨🇨', NULL),
(41, 'Congo - Kinshasa', NULL, '🇨🇩', NULL),
(42, 'Central African Republic', NULL, '🇨🇫', NULL),
(43, 'Congo - Brazzaville', NULL, '🇨🇬', NULL),
(44, 'Switzerland', NULL, '🇨🇭', 'CHF'),
(45, 'Côte d’Ivoire', NULL, '🇨🇮', NULL),
(46, 'Cook Islands', NULL, '🇨🇰', NULL),
(47, 'Chile', NULL, '🇨🇱', NULL),
(48, 'Cameroon', NULL, '🇨🇲', NULL),
(49, 'China', NULL, '🇨🇳', NULL),
(50, 'Colombia', NULL, '🇨🇴', NULL),
(51, 'Clipperton Island', NULL, '🇨🇵', NULL),
(52, 'Costa Rica', NULL, '🇨🇷', NULL),
(53, 'Cuba', NULL, '🇨🇺', NULL),
(54, 'Cape Verde', NULL, '🇨🇻', NULL),
(55, 'Curaçao', NULL, '🇨🇼', NULL),
(56, 'Christmas Island', NULL, '🇨🇽', NULL),
(57, 'Cyprus', NULL, '🇨🇾', NULL),
(58, 'Czechia', NULL, '🇨🇿', NULL),
(59, 'Germany', NULL, '🇩🇪', NULL),
(60, 'Diego Garcia', NULL, '🇩🇬', NULL),
(61, 'Djibouti', NULL, '🇩🇯', NULL),
(62, 'Denmark', NULL, '🇩🇰', NULL),
(63, 'Dominica', NULL, '🇩🇲', NULL),
(64, 'Dominican Republic', NULL, '🇩🇴', NULL),
(65, 'Algeria', NULL, '🇩🇿', NULL),
(66, 'Ceuta & Melilla', NULL, '🇪🇦', NULL),
(67, 'Ecuador', NULL, '🇪🇨', NULL),
(68, 'Estonia', NULL, '🇪🇪', NULL),
(69, 'Egypt', NULL, '🇪🇬', NULL),
(70, 'Western Sahara', NULL, '🇪🇭', NULL),
(71, 'Eritrea', NULL, '🇪🇷', NULL),
(72, 'Spain', NULL, '🇪🇸', NULL),
(73, 'Ethiopia', NULL, '🇪🇹', NULL),
(74, 'European Union', NULL, '🇪🇺', 'EUR'),
(75, 'Finland', NULL, '🇫🇮', NULL),
(76, 'Fiji', NULL, '🇫🇯', NULL),
(77, 'Falkland Islands', NULL, '🇫🇰', NULL),
(78, 'Micronesia', NULL, '🇫🇲', NULL),
(79, 'Faroe Islands', NULL, '🇫🇴', NULL),
(80, 'France', NULL, '🇫🇷', NULL),
(81, 'Gabon', NULL, '🇬🇦', NULL),
(82, 'United Kingdom', NULL, '🇬🇧', 'GBP'),
(83, 'Grenada', NULL, '🇬🇩', NULL),
(84, 'Georgia', NULL, '🇬🇪', NULL),
(85, 'French Guiana', NULL, '🇬🇫', NULL),
(86, 'Guernsey', NULL, '🇬🇬', NULL),
(87, 'Ghana', NULL, '🇬🇭', NULL),
(88, 'Gibraltar', NULL, '🇬🇮', NULL),
(89, 'Greenland', NULL, '🇬🇱', NULL),
(90, 'Gambia', NULL, '🇬🇲', NULL),
(91, 'Guinea', NULL, '🇬🇳', NULL),
(92, 'Guadeloupe', NULL, '🇬🇵', NULL),
(93, 'Equatorial Guinea', NULL, '🇬🇶', NULL),
(94, 'Greece', NULL, '🇬🇷', NULL),
(95, 'South Georgia & South Sandwich Islands', NULL, '🇬🇸', NULL),
(96, 'Guatemala', NULL, '🇬🇹', NULL),
(97, 'Guam', NULL, '🇬🇺', NULL),
(98, 'Guinea-Bissau', NULL, '🇬🇼', NULL),
(99, 'Guyana', NULL, '🇬🇾', NULL),
(100, 'Hong Kong SAR China', NULL, '🇭🇰', NULL),
(101, 'Heard & McDonald Islands', NULL, '🇭🇲', NULL),
(102, 'Honduras', NULL, '🇭🇳', NULL),
(103, 'Croatia', NULL, '🇭🇷', NULL),
(104, 'Haiti', NULL, '🇭🇹', NULL),
(105, 'Hungary', NULL, '🇭🇺', NULL),
(106, 'Canary Islands', NULL, '🇮🇨', NULL),
(107, 'Indonesia', NULL, '🇮🇩', NULL),
(108, 'Ireland', NULL, '🇮🇪', NULL),
(109, 'Israel', NULL, '🇮🇱', NULL),
(110, 'Isle of Man', NULL, '🇮🇲', NULL),
(111, 'India', NULL, '🇮🇳', 'INR'),
(112, 'British Indian Ocean Territory', NULL, '🇮🇴', NULL),
(113, 'Iraq', NULL, '🇮🇶', NULL),
(114, 'Iran', NULL, '🇮🇷', NULL),
(115, 'Iceland', NULL, '🇮🇸', NULL),
(116, 'Italy', NULL, '🇮🇹', NULL),
(117, 'Jersey', NULL, '🇯🇪', NULL),
(118, 'Jamaica', NULL, '🇯🇲', NULL),
(119, 'Jordan', NULL, '🇯🇴', NULL),
(120, 'Japan', NULL, '🇯🇵', 'JPY'),
(121, 'Kenya', NULL, '🇰🇪', NULL),
(122, 'Kyrgyzstan', NULL, '🇰🇬', NULL),
(123, 'Cambodia', NULL, '🇰🇭', NULL),
(124, 'Kiribati', NULL, '🇰🇮', NULL),
(125, 'Comoros', NULL, '🇰🇲', NULL),
(126, 'St. Kitts & Nevis', NULL, '🇰🇳', NULL),
(127, 'North Korea', NULL, '🇰🇵', NULL),
(128, 'South Korea', NULL, '🇰🇷', NULL),
(129, 'Kuwait', NULL, '🇰🇼', NULL),
(130, 'Cayman Islands', NULL, '🇰🇾', NULL),
(131, 'Kazakhstan', NULL, '🇰🇿', NULL),
(132, 'Laos', NULL, '🇱🇦', NULL),
(133, 'Lebanon', NULL, '🇱🇧', NULL),
(134, 'St. Lucia', NULL, '🇱🇨', NULL),
(135, 'Liechtenstein', NULL, '🇱🇮', NULL),
(136, 'Sri Lanka', NULL, '🇱🇰', NULL),
(137, 'Liberia', NULL, '🇱🇷', NULL),
(138, 'Lesotho', NULL, '🇱🇸', NULL),
(139, 'Lithuania', NULL, '🇱🇹', NULL),
(140, 'Luxembourg', NULL, '🇱🇺', NULL),
(141, 'Latvia', NULL, '🇱🇻', NULL),
(142, 'Libya', NULL, '🇱🇾', NULL),
(143, 'Morocco', NULL, '🇲🇦', NULL),
(144, 'Monaco', NULL, '🇲🇨', NULL),
(145, 'Moldova', NULL, '🇲🇩', NULL),
(146, 'Montenegro', NULL, '🇲🇪', NULL),
(147, 'St. Martin', NULL, '🇲🇫', NULL),
(148, 'Madagascar', NULL, '🇲🇬', NULL),
(149, 'Marshall Islands', NULL, '🇲🇭', NULL),
(150, 'North Macedonia', NULL, '🇲🇰', NULL),
(151, 'Mali', NULL, '🇲🇱', NULL),
(152, 'Myanmar (Burma)', NULL, '🇲🇲', NULL),
(153, 'Mongolia', NULL, '🇲🇳', NULL),
(154, 'Macao SAR China', NULL, '🇲🇴', NULL),
(155, 'Northern Mariana Islands', NULL, '🇲🇵', NULL),
(156, 'Martinique', NULL, '🇲🇶', NULL),
(157, 'Mauritania', NULL, '🇲🇷', NULL),
(158, 'Montserrat', NULL, '🇲🇸', NULL),
(159, 'Malta', NULL, '🇲🇹', NULL),
(160, 'Mauritius', NULL, '🇲🇺', NULL),
(161, 'Maldives', NULL, '🇲🇻', NULL),
(162, 'Malawi', NULL, '🇲🇼', NULL),
(163, 'Mexico', NULL, '🇲🇽', NULL),
(164, 'Malaysia', NULL, '🇲🇾', NULL),
(165, 'Mozambique', NULL, '🇲🇿', NULL),
(166, 'Namibia', NULL, '🇳🇦', NULL),
(167, 'New Caledonia', NULL, '🇳🇨', NULL),
(168, 'Niger', NULL, '🇳🇪', NULL),
(169, 'Norfolk Island', NULL, '🇳🇫', NULL),
(170, 'Nigeria', NULL, '🇳🇬', NULL),
(171, 'Nicaragua', NULL, '🇳🇮', NULL),
(172, 'Netherlands', NULL, '🇳🇱', NULL),
(173, 'Norway', NULL, '🇳🇴', NULL),
(174, 'Nepal', NULL, '🇳🇵', NULL),
(175, 'Nauru', NULL, '🇳🇷', NULL),
(176, 'Niue', NULL, '🇳🇺', NULL),
(177, 'New Zealand', NULL, '🇳🇿', 'NZD'),
(178, 'Oman', NULL, '🇴🇲', NULL),
(179, 'Panama', NULL, '🇵🇦', NULL),
(180, 'Peru', NULL, '🇵🇪', NULL),
(181, 'French Polynesia', NULL, '🇵🇫', NULL),
(182, 'Papua New Guinea', NULL, '🇵🇬', NULL),
(183, 'Philippines', NULL, '🇵🇭', NULL),
(184, 'Pakistan', NULL, '🇵🇰', NULL),
(185, 'Poland', NULL, '🇵🇱', NULL),
(186, 'St. Pierre & Miquelon', NULL, '🇵🇲', NULL),
(187, 'Pitcairn Islands', NULL, '🇵🇳', NULL),
(188, 'Puerto Rico', NULL, '🇵🇷', NULL),
(189, 'Palestinian Territories', NULL, '🇵🇸', NULL),
(190, 'Portugal', NULL, '🇵🇹', NULL),
(191, 'Palau', NULL, '🇵🇼', NULL),
(192, 'Paraguay', NULL, '🇵🇾', NULL),
(193, 'Qatar', NULL, '🇶🇦', NULL),
(194, 'Réunion', NULL, '🇷🇪', NULL),
(195, 'Romania', NULL, '🇷🇴', NULL),
(196, 'Serbia', NULL, '🇷🇸', NULL),
(197, 'Russia', NULL, '🇷🇺', NULL),
(198, 'Rwanda', NULL, '🇷🇼', NULL),
(199, 'Saudi Arabia', NULL, '🇸🇦', NULL),
(200, 'Solomon Islands', NULL, '🇸🇧', NULL),
(201, 'Seychelles', NULL, '🇸🇨', NULL),
(202, 'Sudan', NULL, '🇸🇩', NULL),
(203, 'Sweden', NULL, '🇸🇪', NULL),
(204, 'Singapore', NULL, '🇸🇬', NULL),
(205, 'St. Helena', NULL, '🇸🇭', NULL),
(206, 'Slovenia', NULL, '🇸🇮', NULL),
(207, 'Svalbard & Jan Mayen', NULL, '🇸🇯', NULL),
(208, 'Slovakia', NULL, '🇸🇰', NULL),
(209, 'Sierra Leone', NULL, '🇸🇱', NULL),
(210, 'San Marino', NULL, '🇸🇲', NULL),
(211, 'Senegal', NULL, '🇸🇳', NULL),
(212, 'Somalia', NULL, '🇸🇴', NULL),
(213, 'Suriname', NULL, '🇸🇷', NULL),
(214, 'South Sudan', NULL, '🇸🇸', NULL),
(215, 'São Tomé & Príncipe', NULL, '🇸🇹', NULL),
(216, 'El Salvador', NULL, '🇸🇻', NULL),
(217, 'Sint Maarten', NULL, '🇸🇽', NULL),
(218, 'Syria', NULL, '🇸🇾', NULL),
(219, 'Eswatini', NULL, '🇸🇿', NULL),
(220, 'Tristan da Cunha', NULL, '🇹🇦', NULL),
(221, 'Turks & Caicos Islands', NULL, '🇹🇨', NULL),
(222, 'Chad', NULL, '🇹🇩', NULL),
(223, 'French Southern Territories', NULL, '🇹🇫', NULL),
(224, 'Togo', NULL, '🇹🇬', NULL),
(225, 'Thailand', NULL, '🇹🇭', NULL),
(226, 'Tajikistan', NULL, '🇹🇯', NULL),
(227, 'Tokelau', NULL, '🇹🇰', NULL),
(228, 'Timor-Leste', NULL, '🇹🇱', NULL),
(229, 'Turkmenistan', NULL, '🇹🇲', NULL),
(230, 'Tunisia', NULL, '🇹🇳', NULL),
(231, 'Tonga', NULL, '🇹🇴', NULL),
(232, 'Turkey', NULL, '🇹🇷', NULL),
(233, 'Trinidad & Tobago', NULL, '🇹🇹', NULL),
(234, 'Tuvalu', NULL, '🇹🇻', NULL),
(235, 'Taiwan', NULL, '🇹🇼', NULL),
(236, 'Tanzania', NULL, '🇹🇿', NULL),
(237, 'Ukraine', NULL, '🇺🇦', NULL),
(238, 'Uganda', NULL, '🇺🇬', NULL),
(239, 'U.S. Outlying Islands', NULL, '🇺🇲', NULL),
(240, 'United Nations', NULL, '🇺🇳', NULL),
(241, 'United States', NULL, '🇺🇸', 'USD'),
(242, 'Uruguay', NULL, '🇺🇾', NULL),
(243, 'Uzbekistan', NULL, '🇺🇿', NULL),
(244, 'Vatican City', NULL, '🇻🇦', NULL),
(245, 'St. Vincent & Grenadines', NULL, '🇻🇨', NULL),
(246, 'Venezuela', NULL, '🇻🇪', NULL),
(247, 'British Virgin Islands', NULL, '🇻🇬', NULL),
(248, 'U.S. Virgin Islands', NULL, '🇻🇮', NULL),
(249, 'Vietnam', NULL, '🇻🇳', NULL),
(250, 'Vanuatu', NULL, '🇻🇺', NULL),
(251, 'Wallis & Futuna', NULL, '🇼🇫', NULL),
(252, 'Samoa', NULL, '🇼🇸', NULL),
(253, 'Kosovo', NULL, '🇽🇰', NULL),
(254, 'Yemen', NULL, '🇾🇪', NULL),
(255, 'Mayotte', NULL, '🇾🇹', NULL),
(256, 'South Africa', NULL, '🇿🇦', NULL),
(257, 'Zambia', NULL, '🇿🇲', NULL),
(258, 'Zimbabwe', NULL, '🇿🇼', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `log`
--

CREATE TABLE `log` (
  `id` int(11) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `trading_id` int(11) DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `text` varchar(50) DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `log_title`
--

CREATE TABLE `log_title` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `log_title`
--

INSERT INTO `log_title` (`id`, `name`) VALUES
(1, 'error');

-- --------------------------------------------------------

--
-- Table structure for table `trading`
--

CREATE TABLE `trading` (
  `id` int(11) NOT NULL,
  `country_from` int(11) DEFAULT NULL,
  `country_to` int(11) DEFAULT NULL,
  `candle` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trading`
--

INSERT INTO `trading` (`id`, `country_from`, `country_to`, `candle`) VALUES
(1, 74, 241, 1),
(2, 82, 241, 1),
(3, 39, 44, 1),
(4, 74, 241, 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `admin_check_flag` tinyint(1) DEFAULT NULL,
  `insert_time` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `admin_check_flag`, `insert_time`) VALUES
(1, 'admin', 'admin', 1, '2023-06-09 21:46:17');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `candle`
--
ALTER TABLE `candle`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `country`
--
ALTER TABLE `country`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `log`
--
ALTER TABLE `log`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `trading_id` (`trading_id`);

--
-- Indexes for table `log_title`
--
ALTER TABLE `log_title`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `trading`
--
ALTER TABLE `trading`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD KEY `country_from` (`country_from`),
  ADD KEY `country_to` (`country_to`),
  ADD KEY `candle` (`candle`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `candle`
--
ALTER TABLE `candle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `country`
--
ALTER TABLE `country`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=260;

--
-- AUTO_INCREMENT for table `log`
--
ALTER TABLE `log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `log_title`
--
ALTER TABLE `log_title`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `trading`
--
ALTER TABLE `trading`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `log`
--
ALTER TABLE `log`
  ADD CONSTRAINT `log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `log_ibfk_2` FOREIGN KEY (`trading_id`) REFERENCES `trading` (`id`);

--
-- Constraints for table `trading`
--
ALTER TABLE `trading`
  ADD CONSTRAINT `trading_ibfk_1` FOREIGN KEY (`country_from`) REFERENCES `country` (`id`),
  ADD CONSTRAINT `trading_ibfk_2` FOREIGN KEY (`country_to`) REFERENCES `country` (`id`),
  ADD CONSTRAINT `trading_ibfk_3` FOREIGN KEY (`candle`) REFERENCES `candle` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
