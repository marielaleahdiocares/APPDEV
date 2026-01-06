-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 06, 2026 at 02:43 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `satisbank`
--

-- --------------------------------------------------------

--
-- Table structure for table `bank`
--

CREATE TABLE `bank` (
  `bank_id` int(11) NOT NULL,
  `code` varchar(20) NOT NULL,
  `short_name` varchar(60) NOT NULL,
  `full_name` varchar(180) NOT NULL,
  `description` text DEFAULT NULL,
  `logo_filename` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bank`
--

INSERT INTO `bank` (`bank_id`, `code`, `short_name`, `full_name`, `description`, `logo_filename`) VALUES
(1, 'BDO', 'BDO', 'Banco de Oro Unibank, Inc.', 'Largest PH universal bank with extensive branch/ATM network and broad retail services.', 'images/bdo.png'),
(2, 'LANDBANK', 'LandBank', 'Land Bank of the Philippines', 'Government-owned bank focused on inclusive finance and rural/public-sector banking.', 'images/landbank.jpg'),
(3, 'METROBANK', 'Metrobank', 'Metropolitan Bank & Trust Company', 'Universal bank with strong retail and corporate banking presence.', 'images/metrobank.png'),
(4, 'BPI', 'BPI', 'Bank of the Philippine Islands', 'One of the oldest banks in PH, known for strong retail banking and digital services.', 'images/bpi.jpg'),
(5, 'PNB', 'PNB', 'Philippine National Bank', 'Universal bank with long-standing heritage and broad banking services.', 'images/pnb.png'),
(6, 'CHINABANK', 'China Bank', 'China Banking Corporation', 'Established private bank known for conservative banking and stability.', 'images/cb.jpg'),
(7, 'RCBC', 'RCBC', 'Rizal Commercial Banking Corporation', 'Universal bank with retail and digital initiatives.', 'images/rcbc.jpg'),
(8, 'SECB', 'Security Bank', 'Security Bank Corporation', 'Retail-focused bank known for customer service and strong digital offerings.', 'images/secbank.jpeg'),
(9, 'EASTWEST', 'EastWest', 'East West Banking Corporation', 'Growing universal bank with expanding retail presence.', 'images/eastwest.jpg'),
(10, 'BOC', 'Bank of Commerce', 'Bank of Commerce', 'Smaller universal bank regulated by BSP.', 'images/boc.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `banks`
--

CREATE TABLE `banks` (
  `bank_id` int(11) NOT NULL,
  `bank_code` varchar(20) NOT NULL,
  `bank_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `banks`
--

INSERT INTO `banks` (`bank_id`, `bank_code`, `bank_name`) VALUES
(1, 'BDO', 'Banco de Oro Unibank, Inc.'),
(2, 'LANDBANK', 'Land Bank of the Philippines'),
(3, 'METROBANK', 'Metropolitan Bank & Trust Company'),
(4, 'BPI', 'Bank of the Philippine Islands'),
(5, 'PNB', 'Philippine National Bank'),
(6, 'CHINABANK', 'China Banking Corporation'),
(7, 'RCBC', 'Rizal Commercial Banking Corporation'),
(8, 'SECB', 'Security Bank Corporation'),
(9, 'EASTWEST', 'East West Banking Corporation'),
(10, 'BOC', 'Bank of Commerce');

-- --------------------------------------------------------

--
-- Table structure for table `bank_features`
--

CREATE TABLE `bank_features` (
  `feature_id` int(11) NOT NULL,
  `bank_id` int(11) NOT NULL,
  `feature_text` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bank_features`
--

INSERT INTO `bank_features` (`feature_id`, `bank_id`, `feature_text`) VALUES
(1, 1, 'Extensive branch network'),
(2, 1, 'Wide ATM availability'),
(3, 1, 'Strong digital banking'),
(4, 6, 'Starter savings products'),
(5, 2, 'Government-backed stability');

-- --------------------------------------------------------

--
-- Table structure for table `bank_interest_rates`
--

CREATE TABLE `bank_interest_rates` (
  `interest_id` int(11) NOT NULL,
  `bank_id` int(11) NOT NULL,
  `account_type` enum('SAVINGS','TIME_DEPOSIT','CHECKING') NOT NULL,
  `interest_rate` decimal(6,4) DEFAULT NULL,
  `min_initial_deposit` decimal(12,2) DEFAULT NULL,
  `min_balance_to_earn` decimal(12,2) DEFAULT NULL,
  `maintaining_balance` decimal(12,2) DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bank_interest_rates`
--

INSERT INTO `bank_interest_rates` (`interest_id`, `bank_id`, `account_type`, `interest_rate`, `min_initial_deposit`, `min_balance_to_earn`, `maintaining_balance`, `notes`, `source`) VALUES
(1, 1, 'SAVINGS', 0.0625, 500.00, 500.00, 500.00, 'Regular Savings Account', 'BDO-DATA.pdf'),
(2, 1, 'TIME_DEPOSIT', NULL, 1000.00, NULL, NULL, 'Tiered rates depending on amount and tenor', 'BDO-DATA.pdf'),
(3, 1, 'CHECKING', NULL, 5000.00, NULL, NULL, 'Non-interest bearing checking account', 'BDO-DATA.pdf'),
(4, 4, 'SAVINGS', 0.0925, 1.00, 5000.00, NULL, 'MySaveUp – interest earned when daily balance reaches ₱5,000', 'FINAL-BANK-DATA.pdf'),
(5, 4, 'TIME_DEPOSIT', NULL, 1000.00, NULL, NULL, 'Rates depend on term and placement', 'FINAL-BANK-DATA.pdf'),
(6, 4, 'CHECKING', NULL, NULL, NULL, NULL, 'Non-interest bearing checking account', 'FINAL-BANK-DATA.pdf'),
(7, 2, 'SAVINGS', 0.0005, 10000.00, 10000.00, NULL, 'Regular Passbook Savings (0.05% p.a. per August 2025)', 'LandBank Deposit Info PDF'),
(8, 2, 'SAVINGS', 0.0005, 500.00, 2000.00, NULL, 'Savings with ATM (0.05% p.a. per August 2025)', 'LandBank Deposit Info PDF'),
(9, 2, 'SAVINGS', 0.0005, 1.00, NULL, NULL, 'LANDBANK PISO Savings (0.05% p.a. per August 2025)', 'LandBank Deposit Info PDF'),
(10, 4, 'SAVINGS', 0.0006, 3000.00, 3000.00, NULL, 'BPI Saver-Plus Savings (0.0625% p.a.)', 'BPI Deposit Rates'),
(11, 4, 'SAVINGS', 0.0009, 1.00, 5000.00, NULL, 'BPI #SaveUp Savings (0.0925% p.a.)', 'BPI Deposit Rates'),
(12, 4, 'CHECKING', NULL, 10000.00, NULL, NULL, 'BPI Regular & BizLink Checking (no interest)', 'BPI Deposit Rates'),
(13, 6, 'SAVINGS', 0.1250, 100.00, 1000.00, 500.00, 'Easi-Save Account', 'FINAL-BANK-DATA.pdf'),
(14, 5, 'SAVINGS', 0.0010, 1000.00, NULL, NULL, 'PNB base savings (approx typical, varies)', 'PNB official deposits'),
(15, 5, 'CHECKING', NULL, 1000.00, NULL, NULL, 'PNB checking (no published interest)', 'PNB official info'),
(16, 5, 'TIME_DEPOSIT', NULL, 1000.00, NULL, NULL, 'Tiered time deposit rates; varies by term', 'PNB official rates'),
(17, 7, 'SAVINGS', 0.0010, 1000.00, NULL, NULL, 'RCBC base savings (approx typical, varies)', 'RCBC official deposits'),
(18, 7, 'CHECKING', NULL, 10000.00, NULL, NULL, 'RCBC checking (no published interest)', 'RCBC official info'),
(19, 7, 'TIME_DEPOSIT', NULL, 1000.00, NULL, NULL, 'Tiered time deposit rates; varies by term', 'RCBC official rates'),
(20, 8, 'SAVINGS', 0.0010, 1000.00, NULL, NULL, 'Security Bank base savings (approx typical, varies)', 'Security Bank official rates'),
(21, 8, 'CHECKING', NULL, 10000.00, NULL, NULL, 'Security Bank checking (no published interest)', 'Security Bank official info'),
(22, 8, 'TIME_DEPOSIT', NULL, 1000.00, NULL, NULL, 'Tiered time deposit rates; varies by term', 'Security Bank official rates'),
(23, 9, 'SAVINGS', 0.0010, 1000.00, NULL, NULL, 'EastWest base savings (approx typical)', 'EastWest official deposits'),
(24, 9, 'CHECKING', NULL, 10000.00, NULL, NULL, 'EastWest checking (no published interest)', 'EastWest official info'),
(25, 9, 'TIME_DEPOSIT', NULL, 1000.00, NULL, NULL, 'Tiered time deposit rates; varies by term', 'EastWest official rates'),
(26, 10, 'SAVINGS', 0.0010, 1000.00, NULL, NULL, 'BOC base savings (approx typical)', 'Bank of Commerce official info'),
(27, 10, 'CHECKING', NULL, 10000.00, NULL, NULL, 'BOC checking (no published interest)', 'Bank of Commerce official info'),
(28, 10, 'TIME_DEPOSIT', NULL, 1000.00, NULL, NULL, 'Tiered time deposit rates; varies by term', 'BOC official rates');

-- --------------------------------------------------------

--
-- Table structure for table `bank_ratings`
--

CREATE TABLE `bank_ratings` (
  `bank_id` int(11) NOT NULL,
  `satisfaction` decimal(3,1) DEFAULT NULL,
  `satisfaction_source_name` varchar(255) DEFAULT NULL,
  `satisfaction_source_url` varchar(500) DEFAULT NULL,
  `service_quality` decimal(3,1) DEFAULT NULL,
  `service_source_name` varchar(255) DEFAULT NULL,
  `service_source_url` varchar(500) DEFAULT NULL,
  `safety` decimal(3,1) DEFAULT NULL,
  `safety_source_name` varchar(255) DEFAULT NULL,
  `safety_source_url` varchar(500) DEFAULT NULL,
  `avg_score` decimal(3,1) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `evidence_text` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bank_ratings`
--

INSERT INTO `bank_ratings` (`bank_id`, `satisfaction`, `satisfaction_source_name`, `satisfaction_source_url`, `service_quality`, `service_source_name`, `service_source_url`, `safety`, `safety_source_name`, `safety_source_url`, `avg_score`, `source`, `evidence_text`) VALUES
(1, 4.5, 'Brand Finance / customer reach & satisfaction evidence (FINAL PDF)', 'https://brandfinance.com', 4.5, 'Digital banking adoption evidence (FINAL PDF)', NULL, 5.0, 'BSP Total Assets (stability proxy) (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 4.7, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'High satisfaction & reach; strong digital adoption; largest assets = strong stability (per FINAL PDF).'),
(2, 3.5, 'Government-owned stability + general satisfaction evidence (FINAL PDF)', NULL, 3.0, 'Public-sector service quality focus (FINAL PDF)', 'https://www.landbank.com', 5.0, 'BSP Total Assets (stability proxy) (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 3.8, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Govt-owned; extremely stable; moderate service quality focus (per FINAL PDF).'),
(3, 4.0, 'General banking awards & reputation evidence (FINAL PDF)', NULL, 4.0, 'Service/retail banking recognition evidence (FINAL PDF)', NULL, 5.0, 'BSP Total Assets (stability proxy) (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 4.3, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Large universal bank; strong stability via high assets; service quality rated high (per FINAL PDF).'),
(4, 5.0, 'Top-tier retail bank recognition evidence (FINAL PDF)', NULL, 5.0, 'Digital/service excellence evidence (FINAL PDF)', NULL, 5.0, 'BSP Total Assets (stability proxy) (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 5.0, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Top scores across satisfaction/service; very high stability (per FINAL PDF).'),
(5, 4.0, 'General satisfaction evidence (FINAL PDF)', NULL, 3.5, 'Service quality evidence (FINAL PDF)', NULL, 5.0, 'BSP Total Assets (stability proxy) (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 4.2, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Strong stability; moderate-to-high satisfaction; service quality moderate-high (per FINAL PDF).'),
(6, 3.5, 'General satisfaction evidence (FINAL PDF)', NULL, 3.5, 'Service quality evidence (FINAL PDF)', NULL, 4.5, 'Stability based on assets ranking evidence (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 3.8, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Moderate satisfaction/service; high stability (per FINAL PDF).'),
(7, 4.0, 'General satisfaction evidence (FINAL PDF)', NULL, 4.0, 'Service quality evidence (FINAL PDF)', NULL, 4.5, 'Stability based on assets ranking evidence (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 4.2, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Good satisfaction/service; high stability (per FINAL PDF).'),
(8, 5.0, 'High satisfaction evidence (FINAL PDF)', NULL, 5.0, 'High service quality evidence (FINAL PDF)', NULL, 4.5, 'Stability based on assets ranking evidence (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 4.8, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Very high satisfaction/service; high stability (per FINAL PDF).'),
(9, 3.0, 'General satisfaction evidence (FINAL PDF)', NULL, 3.0, 'General service quality evidence (FINAL PDF)', NULL, 4.0, 'Stability based on assets ranking evidence (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 3.3, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Moderate satisfaction/service; high stability (per FINAL PDF).'),
(10, 3.0, 'Limited public rankings; baseline score (FINAL PDF)', NULL, 3.0, 'Limited public rankings; baseline score (FINAL PDF)', NULL, 4.0, 'BSP-regulated universal bank stability evidence (FINAL PDF)', 'https://www.bsp.gov.ph/Statistics/Financial%20Statements/Commercial/assets.aspx', 3.3, 'FINAL-BANK-RATINGS-WITH-SOURCES.pdf', 'Smaller bank; limited public satisfaction rankings; still BSP-regulated and stable (per FINAL PDF).');

-- --------------------------------------------------------

--
-- Table structure for table `bank_service_values`
--

CREATE TABLE `bank_service_values` (
  `bank_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `value_num` decimal(16,4) DEFAULT NULL,
  `value_text` varchar(255) DEFAULT NULL,
  `currency` varchar(10) DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bank_service_values`
--

INSERT INTO `bank_service_values` (`bank_id`, `service_id`, `value_num`, `value_text`, `currency`, `notes`, `source`) VALUES
(1, 1, 0.0625, NULL, NULL, 'Regular Savings', 'BDO-DATA (1).pdf'),
(1, 4, 500.0000, NULL, 'PHP', 'Regular Savings min initial deposit', 'BDO-DATA (1).pdf'),
(1, 5, 500.0000, NULL, 'PHP', 'Regular Savings required min ADB', 'BDO-DATA (1).pdf'),
(1, 6, 100.0000, NULL, 'PHP', 'Service charge below min ADB', 'BDO-DATA (1).pdf'),
(1, 11, 3.5000, NULL, 'USD', NULL, 'BDO-DATA (1).pdf'),
(1, 12, 1.0000, NULL, 'USD', NULL, 'BDO-DATA (1).pdf'),
(1, 13, NULL, 'Below ₱500: ₱25; ₱500-₱25,000: ₱25–₱50; ₱25,001-₱150,000: ₱50–₱100; ₱150,001-₱300,000: ₱100–₱200; ₱300,001-₱500,000: ₱200–₱400; ₱500,001-₱1,000,000: ₱300–₱600; ₱1,000,001+: ₱500–₱800', NULL, 'Interbranch Fund Transfer Fees', 'BDO-DATA (1).pdf'),
(1, 18, 300000.0000, NULL, 'PHP', 'Highest max withdrawal/day shown in BDO limits table', 'BDO-DATA (1).pdf'),
(1, 19, NULL, '₱30 first 3 pages; ₱10 per succeeding page', 'PHP', NULL, 'BDO-DATA (1).pdf'),
(1, 20, 100.0000, NULL, 'PHP', NULL, 'BDO-DATA (1).pdf'),
(2, 1, 0.0500, NULL, NULL, 'Savings Account with ATM', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(2, 4, 500.0000, NULL, 'PHP', 'Minimum initial deposit', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(2, 5, 500.0000, NULL, 'PHP', 'Required minimum ADB', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(2, 6, 200.0000, NULL, 'PHP', 'Monthly service charge below minimum ADB', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(2, 7, 2000.0000, NULL, 'PHP', 'Required daily balance to earn interest', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(4, 1, 0.0925, NULL, NULL, '#MySaveUp', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(4, 4, 1.0000, NULL, 'PHP', '#MySaveUp required initial deposit', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(4, 5, 0.0000, NULL, 'PHP', '#MySaveUp required minimum monthly ADB', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(4, 7, 5000.0000, NULL, 'PHP', '#MySaveUp required daily balance to earn interest', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(5, 14, 50.0000, NULL, 'PHP', 'InstaPay fee', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(5, 15, 30.0000, NULL, 'PHP', 'PESONet fee', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(5, 16, 11.0000, NULL, 'PHP', 'Other-bank ATM withdrawal fee', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(5, 17, 2.0000, NULL, 'PHP', 'Other-bank ATM balance inquiry fee', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(6, 1, 0.1250, NULL, NULL, 'Easi-Save (ATM/Basic)', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(6, 8, 100.0000, NULL, 'PHP', 'One-time account opening fee (Easi-Save Basic)', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(6, 9, 500.0000, NULL, 'PHP', 'Minimum maintaining balance (Easi-Save ATM)', 'FINAL-NA-TALAGA-BANK-DATA.pdf'),
(6, 10, 1000.0000, NULL, 'PHP', 'Minimum balance to earn interest', 'FINAL-NA-TALAGA-BANK-DATA.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `saved_banks`
--

CREATE TABLE `saved_banks` (
  `saved_id` int(11) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `bank_code` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `service`
--

CREATE TABLE `service` (
  `service_id` int(11) NOT NULL,
  `service_key` varchar(60) NOT NULL,
  `name` varchar(180) NOT NULL,
  `category` varchar(80) NOT NULL,
  `value_type` enum('number','text') NOT NULL DEFAULT 'number',
  `unit` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service`
--

INSERT INTO `service` (`service_id`, `service_key`, `name`, `category`, `value_type`, `unit`) VALUES
(1, 'savings_interest_rate_pa', 'Savings interest rate (per annum)', 'Deposit and Account Services', 'number', 'percent'),
(2, 'time_deposit_rate_pa', 'Time deposit interest rate (per annum)', 'Deposit and Account Services', 'text', 'percent'),
(3, 'checking_interest_rate_pa', 'Checking interest rate (per annum)', 'Deposit and Account Services', 'text', 'percent'),
(4, 'savings_min_initial_deposit', 'Minimum initial deposit (savings)', 'Deposit and Account Services', 'number', 'php'),
(5, 'savings_min_adb', 'Required minimum ADB (savings)', 'Deposit and Account Services', 'number', 'php'),
(6, 'savings_below_adb_fee', 'Monthly service charge below min ADB', 'Deposit and Account Services', 'number', 'php'),
(7, 'savings_required_daily_balance', 'Required daily balance to earn interest', 'Deposit and Account Services', 'number', 'php'),
(8, 'account_opening_fee', 'Account opening fee', 'Deposit and Account Services', 'number', 'php'),
(9, 'maintaining_balance', 'Maintaining balance requirement', 'Deposit and Account Services', 'number', 'php'),
(10, 'min_balance_to_earn_interest', 'Minimum balance to earn interest', 'Deposit and Account Services', 'number', 'php'),
(11, 'overseas_atm_withdrawal_fee', 'Overseas ATM withdrawal fee', 'Payment and Transaction Services', 'number', 'usd'),
(12, 'overseas_balance_inquiry_fee', 'Overseas balance inquiry fee', 'Payment and Transaction Services', 'number', 'usd'),
(13, 'ibft_fee_range', 'Interbranch / OTC fund transfer fee range', 'Payment and Transaction Services', 'text', NULL),
(14, 'instapay_fee', 'InstaPay transfer fee', 'Payment and Transaction Services', 'number', 'php'),
(15, 'pesonet_fee', 'PESONet transfer fee', 'Payment and Transaction Services', 'number', 'php'),
(16, 'other_bank_atm_withdrawal_fee', 'Other-bank ATM withdrawal fee', 'Payment and Transaction Services', 'number', 'php'),
(17, 'other_bank_atm_balance_inquiry_fee', 'Other-bank ATM balance inquiry fee', 'Payment and Transaction Services', 'number', 'php'),
(18, 'max_withdrawal_per_day', 'Max ATM withdrawal per day', 'Lending and Credit Services', 'number', 'php'),
(19, 'bank_statement_fee', 'Bank statement fee', 'Investment and Trust Services', 'text', NULL),
(20, 'bank_certification_fee', 'Bank certification fee', 'Investment and Trust Services', 'number', 'php');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `service_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `service_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`service_id`, `category_id`, `service_name`) VALUES
(1, 1, 'Regular Savings (p.a.)'),
(2, 1, 'Time Deposit (p.a.)'),
(3, 2, 'Credit Card Interest'),
(6, 3, 'Auto Loans'),
(4, 3, 'Consumer / Personal Loans'),
(5, 3, 'Home Loans'),
(8, 4, 'Mutual Fund Management Fee'),
(7, 4, 'UITFs (Minimum Investment)'),
(10, 5, 'Transfer Fees (InstaPay)'),
(9, 5, 'Transfer Fees (PESONet)');

-- --------------------------------------------------------

--
-- Table structure for table `service_categories`
--

CREATE TABLE `service_categories` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service_categories`
--

INSERT INTO `service_categories` (`category_id`, `category_name`) VALUES
(1, 'Deposit and Account Services'),
(2, 'Payment and Transaction Services'),
(3, 'Lending and Credit Services'),
(4, 'Investment and Trust Services'),
(5, 'Digital and Electronic Banking');

-- --------------------------------------------------------

--
-- Table structure for table `service_rates`
--

CREATE TABLE `service_rates` (
  `rate_id` int(11) NOT NULL,
  `bank_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `rate_value` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service_rates`
--

INSERT INTO `service_rates` (`rate_id`, `bank_id`, `service_id`, `rate_value`) VALUES
(1, 1, 1, '0.0625%'),
(2, 2, 1, '0.05'),
(3, 3, 1, '0.0625%'),
(4, 4, 1, '0.0625%'),
(5, 5, 1, '~0.10%'),
(6, 6, 1, '~0.125%'),
(7, 7, 1, '0.15% – 0.45%'),
(8, 8, 1, '~0.10% – 1.20%'),
(9, 9, 1, '~0.125%'),
(10, 10, 1, 'Not specified'),
(11, 1, 2, '0.125%–0.500%'),
(12, 2, 2, 'Not specified'),
(13, 3, 2, '0.150%–0.750%'),
(14, 4, 2, 'Not specified'),
(15, 5, 2, 'Up to ~4.5% p.a.'),
(16, 6, 2, 'Not specified'),
(17, 7, 2, '0.500%–1.375%'),
(18, 8, 2, '~0.88%–3.75%'),
(19, 9, 2, '0.10%'),
(20, 10, 2, '0.10%'),
(21, 1, 3, 'Up to ~3.00% per month'),
(22, 2, 3, 'Not specified'),
(23, 3, 3, 'Up to ~3.00% per month'),
(24, 4, 3, 'Up to ~3.00% per month'),
(25, 5, 3, 'Up to ~3.00% per month'),
(26, 6, 3, 'Up to ~3.00% per month'),
(27, 7, 3, 'Up to ~3.00% per month'),
(28, 8, 3, 'Up to ~3.00% per month'),
(29, 9, 3, 'Up to ~3.00% per month'),
(30, 10, 3, 'Not specified'),
(31, 1, 4, '1.20% – 2.50% per month'),
(32, 2, 4, 'Not specified'),
(33, 3, 4, '1.25% – 2.50% per month'),
(34, 4, 4, '1.20% – 2.00% per month'),
(35, 5, 4, 'Not specified'),
(36, 6, 4, 'Not specified'),
(37, 7, 4, '1.00% – 2.00% per month'),
(38, 8, 4, '1.25% – 3.00% per month'),
(39, 9, 4, '1.20% – 2.99% per month'),
(40, 10, 4, 'Not specified'),
(41, 1, 5, '6.25% – 8.50% p.a.'),
(42, 2, 5, '6.00% – 7.50% p.a.'),
(43, 3, 5, '6.50% – 8.75% p.a.'),
(44, 4, 5, '6.25% – 8.25% p.a.'),
(45, 5, 5, '6.00% – 8.00% p.a.'),
(46, 6, 5, '6.50% – 9.00% p.a.'),
(47, 7, 5, '6.25% – 8.50% p.a.'),
(48, 8, 5, '6.75% – 9.00% p.a.'),
(49, 9, 5, '6.50% – 9.25% p.a.'),
(50, 10, 5, 'Not specified'),
(51, 1, 6, '5.25% – 8.50% p.a.'),
(52, 2, 6, '5.00% – 7.50% p.a.'),
(53, 3, 6, '5.75% – 8.75% p.a.'),
(54, 4, 6, '5.25% – 8.25% p.a.'),
(55, 5, 6, '5.50% – 8.50% p.a.'),
(56, 6, 6, '5.75% – 9.00% p.a.'),
(57, 7, 6, '5.50% – 8.75% p.a.'),
(58, 8, 6, '6.00% – 9.25% p.a.'),
(59, 9, 6, '.75% – 9.50% p.a.'),
(60, 10, 6, 'Not specified'),
(61, 1, 7, '₱10,000'),
(62, 2, 7, '₱10,000'),
(63, 3, 7, '₱10,000'),
(64, 4, 7, '₱10,000'),
(65, 5, 7, '₱10,000'),
(66, 6, 7, '₱10,000'),
(67, 7, 7, '₱10,000'),
(68, 8, 7, '₱10,000'),
(69, 9, 7, '₱10,000'),
(70, 10, 7, 'Not specified'),
(71, 1, 8, '~0.50% – 2.00% p.a.'),
(72, 2, 8, '~0.50% – 1.50% p.a.'),
(73, 3, 8, '~0.50% – 2.00% p.a.'),
(74, 4, 8, '~0.75% – 2.00% p.a.'),
(75, 5, 8, '~0.50% – 1.50% p.a.'),
(76, 6, 8, '~0.50% – 2.00% p.a.'),
(77, 7, 8, '~0.75% – 2.00% p.a.'),
(78, 8, 8, '~0.75% – 2.25% p.a.'),
(79, 9, 8, '~0.75% – 2.00% p.a.'),
(80, 10, 8, 'Not specified'),
(81, 1, 9, '₱50.00'),
(82, 2, 9, '₱0.00 – ₱17.00'),
(83, 3, 9, '₱50.00'),
(84, 4, 9, '₱15.00 – ₱50.00'),
(85, 5, 9, '₱20.00'),
(86, 6, 9, '₱20.00'),
(87, 7, 9, '₱10.00'),
(88, 8, 9, '₱15.00'),
(89, 9, 9, 'FREE'),
(90, 10, 9, '₱15.00'),
(91, 1, 10, '₱10.00'),
(92, 2, 10, '₱0.00 – ₱15.00'),
(93, 3, 10, '₱0.00 – ₱25.00'),
(94, 4, 10, '₱0.00 – ₱10.00'),
(95, 5, 10, '₱10.00 – ₱20.00'),
(96, 6, 10, '₱5.00 – ₱15.00'),
(97, 7, 10, '₱8.00 – ₱25.00'),
(98, 8, 10, '₱25.00'),
(99, 9, 10, '₱10.00'),
(100, 10, 10, '₱15.00');

-- --------------------------------------------------------

--
-- Table structure for table `service_type`
--

CREATE TABLE `service_type` (
  `service_type_id` int(11) NOT NULL,
  `bank_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `description` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service_type`
--

INSERT INTO `service_type` (`service_type_id`, `bank_id`, `category_id`, `description`) VALUES
(1, 1, 1, 'Regular Savings Account, Checking / Current Account, Time Deposit Account'),
(2, 2, 1, 'Regular Savings Account, Checking / Current Account, Time Deposit Account'),
(3, 3, 1, 'Regular Savings Account, Checking / Current Account, Time Deposit Account'),
(4, 4, 1, 'Regular Savings Account, Checking / Current Account, Time Deposit Account'),
(5, 5, 1, 'Regular Savings Account, Checking / Current Account, Time Deposit Account'),
(6, 6, 1, 'Regular Savings Account, Checking / Current Account, Time Deposit Account'),
(7, 7, 1, 'Regular Savings Account, All-in-One / Transaction Savings, Time Deposit Account'),
(8, 8, 1, 'Regular Savings Account, All-Access, Time Deposit Accounts'),
(9, 9, 1, 'Regular Savings Account, Checking / Current Account, Time Deposit Account'),
(10, 10, 1, 'Savings Account, Checking / Current Account, Time Deposit Account'),
(11, 1, 2, 'Overseas ATM Withdrawal, Interbranch, Debit Card POS'),
(12, 2, 2, 'Interbank Fund Transfer, ATM Cash Withdrawal, Bills Payment'),
(13, 3, 2, 'Interbank Fund Transfer, Overseas ATM Withdrawal, Debit Card POS / Online Purchase'),
(14, 4, 2, 'Interbank Fund Transfer, Bills Payment, Online Purchase'),
(15, 5, 2, 'Overseas ATM Withdrawal, OTC Fund Transfer, Bills Payment Services'),
(16, 6, 2, 'Interbank Fund Transfer, Debit Card POS, Bills Payment Services'),
(17, 7, 2, 'Interbank Fund Transfer Debit Card POS, ATM Cash Withdrawal'),
(18, 8, 2, 'Interbank Fund Transfer, Debit Card POS, Bills Payment'),
(19, 9, 2, 'Interbank Fund Transfer, Debit Card POS, ATM Cash Withdrawal'),
(20, 10, 2, 'Interbank Fund Transfer, Debit Card POS, Bills Payment'),
(21, 1, 3, 'Credit Card, Consumer Loan, Home Loan'),
(22, 2, 3, 'Agricultural Loans, Personal Loans, Home Loan'),
(23, 3, 3, 'Credit Card, Personal Loan, Home Loan'),
(24, 4, 3, 'Credit Card, Personal Loan, Home Loan'),
(25, 5, 3, 'Personal Loan, Home Loan, Auto Loan'),
(26, 6, 3, 'Credit Card, Business, Home Loan'),
(27, 7, 3, 'Credit Card, Personal Loan, Auto Loan'),
(28, 8, 3, 'Credit Card, Personal Loan, Home Loan'),
(29, 9, 3, 'Credit Card, Auto Loan, Personal Loan'),
(30, 10, 3, 'Business Loan, Personal Loan, Home Loan'),
(31, 1, 4, 'UITFs, Trust & Wealth Management Services, Investment Management'),
(32, 2, 4, 'UITFs, Trust & Fiduciary Services, Government Securities'),
(33, 3, 4, 'UITFs, Trust & Wealth Management Services, Investment Management Services'),
(34, 4, 4, 'UITFs, Trust & Wealth Management Services, Managed Investment Products'),
(35, 5, 4, 'UITFs, Trust & Investment Management Services, Government Securities Investments'),
(36, 6, 4, 'UITFs, Trust & Wealth Management Services, Fixed-Income Investments'),
(37, 7, 4, 'UITFs, Trust & Asset Management Services, Investment Products'),
(38, 8, 4, 'UITFs, Trust & Asset Management Services, Wealth Products'),
(39, 9, 4, 'UITFs, Trust & Investment Management Services, Fixed-Income'),
(40, 10, 4, 'UITFs, Trust & Fiduciary Services, Investment Management Services'),
(41, 1, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment'),
(42, 2, 5, 'Mobile Banking App, Online Fund Transfer, Online Government & Utility Payments'),
(43, 3, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment'),
(44, 4, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment'),
(45, 5, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment'),
(46, 6, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment'),
(47, 7, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment'),
(48, 8, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment'),
(49, 9, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment'),
(50, 10, 5, 'Mobile Banking App, Online Fund Transfer, Online Bills Payment');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `firstName` varchar(100) NOT NULL,
  `lastName` varchar(100) NOT NULL,
  `ContactNo` varchar(100) NOT NULL,
  `Address` varchar(100) NOT NULL,
  `userID` int(100) NOT NULL,
  `CustomerType` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`email`, `password`, `firstName`, `lastName`, `ContactNo`, `Address`, `userID`, `CustomerType`) VALUES
('user@example.com', '12345', 'thom', 'guyo', '09123456789', 'urdaneta city, pangasinan', 1, 'prospective user'),
('king@gmail.com', 'king', 'king', 'casupang', '09876543210', 'pozorrubio, pangasinan', 5, 'prospective'),
('sam@gmail.com', 'sample', 'sample', 'lang', '09876543215', 'urdaneta city, pangasinan', 6, 'existing'),
('king@gmail.com', '123', 'king', 'casupang', '09876543210', 'pozorrubio, pangasinan', 7, 'existing'),
('acosta@gmail.com', '123', 'mike', 'acosta', '09876543212', 'urdaneta city, pangasinan', 8, 'prospective'),
('appdev@gmail.com', '12345', 'jc', 'reyes', '09123456789', 'urdaneta city, pangasinan', 9, 'existing');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bank`
--
ALTER TABLE `bank`
  ADD PRIMARY KEY (`bank_id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `banks`
--
ALTER TABLE `banks`
  ADD PRIMARY KEY (`bank_id`),
  ADD UNIQUE KEY `bank_code` (`bank_code`);

--
-- Indexes for table `bank_features`
--
ALTER TABLE `bank_features`
  ADD PRIMARY KEY (`feature_id`),
  ADD KEY `fk_bank_features_bank` (`bank_id`);

--
-- Indexes for table `bank_interest_rates`
--
ALTER TABLE `bank_interest_rates`
  ADD PRIMARY KEY (`interest_id`),
  ADD KEY `bank_id` (`bank_id`);

--
-- Indexes for table `bank_ratings`
--
ALTER TABLE `bank_ratings`
  ADD PRIMARY KEY (`bank_id`);

--
-- Indexes for table `bank_service_values`
--
ALTER TABLE `bank_service_values`
  ADD PRIMARY KEY (`bank_id`,`service_id`),
  ADD KEY `fk_bsv_service` (`service_id`);

--
-- Indexes for table `saved_banks`
--
ALTER TABLE `saved_banks`
  ADD PRIMARY KEY (`saved_id`),
  ADD UNIQUE KEY `uniq_user_bank` (`user_email`,`bank_code`),
  ADD KEY `idx_user_email` (`user_email`),
  ADD KEY `idx_bank_code` (`bank_code`);

--
-- Indexes for table `service`
--
ALTER TABLE `service`
  ADD PRIMARY KEY (`service_id`),
  ADD UNIQUE KEY `service_key` (`service_key`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`service_id`),
  ADD UNIQUE KEY `category_id` (`category_id`,`service_name`);

--
-- Indexes for table `service_categories`
--
ALTER TABLE `service_categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `service_rates`
--
ALTER TABLE `service_rates`
  ADD PRIMARY KEY (`rate_id`),
  ADD UNIQUE KEY `bank_id` (`bank_id`,`service_id`),
  ADD KEY `service_id` (`service_id`);

--
-- Indexes for table `service_type`
--
ALTER TABLE `service_type`
  ADD PRIMARY KEY (`service_type_id`),
  ADD KEY `bank_id` (`bank_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bank`
--
ALTER TABLE `bank`
  MODIFY `bank_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `banks`
--
ALTER TABLE `banks`
  MODIFY `bank_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `bank_features`
--
ALTER TABLE `bank_features`
  MODIFY `feature_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `bank_interest_rates`
--
ALTER TABLE `bank_interest_rates`
  MODIFY `interest_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `saved_banks`
--
ALTER TABLE `saved_banks`
  MODIFY `saved_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `service`
--
ALTER TABLE `service`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `service_categories`
--
ALTER TABLE `service_categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `service_rates`
--
ALTER TABLE `service_rates`
  MODIFY `rate_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;

--
-- AUTO_INCREMENT for table `service_type`
--
ALTER TABLE `service_type`
  MODIFY `service_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `userID` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bank_features`
--
ALTER TABLE `bank_features`
  ADD CONSTRAINT `fk_bank_features_bank` FOREIGN KEY (`bank_id`) REFERENCES `bank` (`bank_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `bank_interest_rates`
--
ALTER TABLE `bank_interest_rates`
  ADD CONSTRAINT `bank_interest_rates_ibfk_1` FOREIGN KEY (`bank_id`) REFERENCES `banks` (`bank_id`);

--
-- Constraints for table `bank_ratings`
--
ALTER TABLE `bank_ratings`
  ADD CONSTRAINT `fk_bank_ratings_bank` FOREIGN KEY (`bank_id`) REFERENCES `bank` (`bank_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `bank_service_values`
--
ALTER TABLE `bank_service_values`
  ADD CONSTRAINT `fk_bsv_bank` FOREIGN KEY (`bank_id`) REFERENCES `bank` (`bank_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_bsv_service` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `services`
--
ALTER TABLE `services`
  ADD CONSTRAINT `services_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `service_categories` (`category_id`);

--
-- Constraints for table `service_rates`
--
ALTER TABLE `service_rates`
  ADD CONSTRAINT `service_rates_ibfk_1` FOREIGN KEY (`bank_id`) REFERENCES `banks` (`bank_id`),
  ADD CONSTRAINT `service_rates_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`);

--
-- Constraints for table `service_type`
--
ALTER TABLE `service_type`
  ADD CONSTRAINT `service_type_ibfk_1` FOREIGN KEY (`bank_id`) REFERENCES `banks` (`bank_id`),
  ADD CONSTRAINT `service_type_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `service_categories` (`category_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
