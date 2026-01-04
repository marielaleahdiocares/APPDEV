-- bankComparison.sql (CORRECTED)

-- ==========================
-- BANKS TABLE
-- ==========================
CREATE TABLE banks (
    bank_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_code VARCHAR(20) NOT NULL UNIQUE,
    bank_name VARCHAR(255) NOT NULL
);

INSERT INTO banks (bank_code, bank_name) VALUES
('BDO', 'Banco de Oro Unibank, Inc.'),
('LANDBANK', 'Land Bank of the Philippines'),
('METROBANK', 'Metropolitan Bank & Trust Company'),
('BPI', 'Bank of the Philippine Islands'),
('PNB', 'Philippine National Bank'),
('CHINABANK', 'China Banking Corporation'),
('RCBC', 'Rizal Commercial Banking Corporation'),
('SECB', 'Security Bank Corporation'),
('EASTWEST', 'East West Banking Corporation'),
('BOC', 'Bank of Commerce');

-- ==========================
-- SERVICE CATEGORIES TABLE
-- (FIXED: add Investment + make Digital category_id = 5)
-- ==========================
CREATE TABLE service_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

INSERT INTO service_categories (category_name) VALUES
('Deposit and Account Services'),           -- 1
('Payment and Transaction Services'),       -- 2
('Lending and Credit Services'),            -- 3
('Investment and Trust Services'),          -- 4
('Digital and Electronic Banking');         -- 5

-- ==========================
-- SERVICE TYPE TABLE
-- (FIXED: rename PK to avoid confusion with services.service_id)
-- ==========================
CREATE TABLE service_type (
    service_type_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id INT NOT NULL,
    category_id INT NOT NULL,
    description VARCHAR(150) NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES banks(bank_id),
    FOREIGN KEY (category_id) REFERENCES service_categories(category_id)
);

-- Deposit and Account Services (category_id = 1)
INSERT INTO service_type (bank_id, category_id, description) VALUES
(1, 1, 'Kabayan Savings'),
(2, 1, 'Regular Savings'),
(3, 1, 'Savings Account'),
(4, 1, 'Save-Up'),
(5, 1, 'Regular Savings'),
(6, 1, 'Dragon Savings'),
(7, 1, 'GoSavers'),
(8, 1, 'All-Access Account'),
(9, 1, 'Regular Savings'),
(10, 1, 'Savings Account');

-- Payment and Transaction Services (category_id = 2)
INSERT INTO service_type (bank_id, category_id, description) VALUES
(1, 2, 'Bills Payment'),
(2, 2, 'Bills Payment'),
(3, 2, 'Bills Payment'),
(4, 2, 'Bills Pay'),
(5, 2, 'Bills Pay'),
(6, 2, 'Bills Payment'),
(7, 2, 'Checkbooks'),
(8, 2, 'Bills Pay'),
(9, 2, 'Bills Pay'),
(10, 2, 'Bills Pay');

-- Lending and Credit Services (category_id = 3)
INSERT INTO service_type (bank_id, category_id, description) VALUES
(1, 3, 'Personal Loans'),
(2, 3, 'Agricultural Loans'),
(3, 3, 'Home Loans'),
(4, 3, 'Housing Loans'),
(5, 3, 'Housing Loans'),
(6, 3, 'Business Loans'),
(7, 3, 'RCBC Credit Cards'),
(8, 3, 'Home Loans'),
(9, 3, 'Personal Loans'),
(10, 3, 'Business Loans');

-- Investment and Trust Services (category_id = 4)
INSERT INTO service_type (bank_id, category_id, description) VALUES
(1, 4, 'UITFs'),
(2, 4, 'Trust Banking'),
(3, 4, 'UITFs'),
(4, 4, 'ALFM Mutual Funds'),
(5, 4, 'Trust Banking'),
(6, 4, 'Trust Banking'),
(7, 4, 'Wealth Management'),
(8, 4, 'UITFs'),
(9, 4, 'Trust Services'),
(10, 4, 'Trust Banking');

-- Digital and Electronic Banking (category_id = 5)
INSERT INTO service_type (bank_id, category_id, description) VALUES
(1, 5, 'BDO Online App'),
(2, 5, 'LANDBANK iAccess'),
(3, 5, 'Metrobank Mobile App'),
(4, 5, 'BPI App'),
(5, 5, 'PNB Digital App'),
(6, 5, 'China Bank Online'),
(7, 5, 'RCBC Pulz App'),
(8, 5, 'Security Bank Mobile App'),
(9, 5, 'EastWest EasyWay App'),
(10, 5, 'BankCom Mobile Banking');

DROP TABLE IF EXISTS service_rates;
DROP TABLE IF EXISTS services;

-- ==========================
-- SERVICES (from Excel)
-- ==========================
CREATE TABLE services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    service_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES service_categories(category_id),
    UNIQUE (category_id, service_name)
);

INSERT INTO services (category_id, service_name) VALUES
(1, 'Regular Savings (p.a.)'),
(1, 'Passbook Savings (p.a.)'),
(1, 'Tiered / High-Yield Savings'),
(1, 'Basic Deposit Accounts'),

(2, 'Credit Card Interest'),

(3, 'Consumer / Personal Loans'),
(3, 'Home Loans'),
(3, 'Auto Loans'),
(3, 'Business Loans'),
(3, 'Working Capital Loans'),
(3, 'Term Loans'),
(3, 'Trade Financing'),
(3, 'Agricultural Loans'),

(4, 'UITFs (Minimum Investment)'),
(4, 'Mutual Fund Management Fee'),
(4, 'Trust Account Management Fee'),

(5, 'E-money Services');

-- ==========================
-- SERVICE RATES (from Excel)
-- bank_id is based on insertion order above:
-- 1=BPI,2=BDO,3=RCBC,4=LANDBANK,5=METROBANK,6=PNB,7=CHINABANK,8=SECB,9=EASTWEST,10=BOC
-- service_id is based on services insertion order above (1..17)
-- ==========================
CREATE TABLE service_rates (
    rate_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id INT NOT NULL,
    service_id INT NOT NULL,
    rate_value VARCHAR(50) NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES banks(bank_id),
    FOREIGN KEY (service_id) REFERENCES services(service_id),
    UNIQUE (bank_id, service_id)
);

INSERT INTO service_rates (bank_id, service_id, rate_value) VALUES
-- Service 1: Regular Savings (p.a.)
(1, 1, '0.0625%'),
(2, 1, '0.0625%'),
(3, 1, '0.10%'),
(4, 1, '0.10%'),
(5, 1, '0.0625%'),
(6, 1, '0.10%'),
(7, 1, '0.10%'),
(8, 1, '0.10%'),
(9, 1, '0.10%'),
(10, 1, '0.10%'),

-- Service 2: Passbook Savings (p.a.)
(1, 2, '0.0625–0.10%'),
(2, 2, '0.0625–0.10%'),
(3, 2, '0.10%'),
(4, 2, '0.10%'),
(5, 2, '0.0625%'),
(6, 2, '0.10%'),
(7, 2, '0.10%'),
(8, 2, '0.10%'),
(9, 2, '0.10%'),
(10, 2, '0.10%'),

-- Service 3: Tiered / High-Yield Savings
(1, 3, 'Up to 4.0%'),
(2, 3, 'Up to 4.0%'),
(3, 3, 'Up to 6.0%'),
(4, 3, 'N/A'),
(5, 3, 'Up to 3.5%'),
(6, 3, 'Up to 3.0%'),
(7, 3, 'Up to 3.0%'),
(8, 3, 'Up to 4.5%'),
(9, 3, 'Up to 4.0%'),
(10, 3, 'N/A'),

-- Service 4: Basic Deposit Accounts
(1, 4, '0.0625%'),
(2, 4, '0.0625%'),
(3, 4, '0.10%'),
(4, 4, '0.10%'),
(5, 4, '0.0625%'),
(6, 4, '0.10%'),
(7, 4, '0.10%'),
(8, 4, '0.10%'),
(9, 4, '0.10%'),
(10, 4, '0.10%'),

-- Service 5: Credit Card Interest
(1, 5, '24–36% p.a.'),
(2, 5, '24–36% p.a.'),
(3, 5, '24–36% p.a.'),
(4, 5, 'N/A'),
(5, 5, '24–36% p.a.'),
(6, 5, '24–36% p.a.'),
(7, 5, '24–36% p.a.'),
(8, 5, '24–36% p.a.'),
(9, 5, '24–36% p.a.'),
(10, 5, 'N/A'),

-- Service 6: Consumer / Personal Loans
(1, 6, 'Usually free'),
(2, 6, 'Usually free'),
(3, 6, 'Usually free'),
(4, 6, 'Usually free'),
(5, 6, 'Usually free'),
(6, 6, 'Usually free'),
(7, 6, 'Usually free'),
(8, 6, 'Usually free'),
(9, 6, 'Usually free'),
(10, 6, 'Usually free'),

-- Service 7: Home Loans
(1, 7, '50–150 PHP'),
(2, 7, '50–150 PHP'),
(3, 7, '50–150 PHP'),
(4, 7, '50–150 PHP'),
(5, 7, '50–150 PHP'),
(6, 7, '50–150 PHP'),
(7, 7, '50–150 PHP'),
(8, 7, '50–150 PHP'),
(9, 7, '50–150 PHP'),
(10, 7, 'N/A'),

-- Service 8: Auto Loans
(1, 8, '0–18 PHP'),
(2, 8, '0–18 PHP'),
(3, 8, '0–18 PHP'),
(4, 8, '0–18 PHP'),
(5, 8, '0–18 PHP'),
(6, 8, '0–18 PHP'),
(7, 8, '0–18 PHP'),
(8, 8, '0–18 PHP'),
(9, 8, '0–18 PHP'),
(10, 8, '0–18 PHP'),

-- Service 9: Business Loans
(1, 9, 'Varies'),
(2, 9, 'Varies'),
(3, 9, 'Varies'),
(4, 9, 'N/A'),
(5, 9, 'Varies'),
(6, 9, 'Varies'),
(7, 9, 'Varies'),
(8, 9, 'Varies'),
(9, 9, 'Varies'),
(10, 9, 'N/A'),

-- Service 10: Working Capital Loans
(1, 10, '6–8.5%'),
(2, 10, '6–8.5%'),
(3, 10, '6–8.5%'),
(4, 10, '6–8.5%'),
(5, 10, '6–8.5%'),
(6, 10, '6–8.5%'),
(7, 10, '6–8.5%'),
(8, 10, '6–8.5%'),
(9, 10, '6–8.5%'),
(10, 10, 'N/A'),

-- Service 11: Term Loans
(1, 11, '7–10%'),
(2, 11, '7–10%'),
(3, 11, '7–10%'),
(4, 11, '7–10%'),
(5, 11, '7–10%'),
(6, 11, '7–10%'),
(7, 11, '7–10%'),
(8, 11, '7–10%'),
(9, 11, '7–10%'),
(10, 11, 'N/A'),

-- Service 12: Trade Financing
(1, 12, '10–30%'),
(2, 12, '10–30%'),
(3, 12, '10–30%'),
(4, 12, '10–30%'),
(5, 12, '10–30%'),
(6, 12, '10–30%'),
(7, 12, '10–30%'),
(8, 12, '10–30%'),
(9, 12, '10–30%'),
(10, 12, 'N/A'),

-- Service 13: Agricultural Loans
(1, 13, '8–15%'),
(2, 13, '8–15%'),
(3, 13, '8–15%'),
(4, 13, '8–15%'),
(5, 13, '8–15%'),
(6, 13, '8–15%'),
(7, 13, '8–15%'),
(8, 13, '8–15%'),
(9, 13, '8–15%'),
(10, 13, 'N/A'),

-- Service 14: UITFs (Minimum Investment)
(1, 14, '0.50–1.50%'),
(2, 14, '0.50–1.50%'),
(3, 14, '0.50–1.50%'),
(4, 14, 'N/A'),
(5, 14, '0.50–1.50%'),
(6, 14, '0.50–1.50%'),
(7, 14, '0.50–1.50%'),
(8, 14, '0.50–1.50%'),
(9, 14, '0.50–1.50%'),
(10, 14, 'N/A'),

-- Service 15: Mutual Fund Management Fee
(1, 15, 'By arrangement'),
(2, 15, 'By arrangement'),
(3, 15, 'By arrangement'),
(4, 15, 'N/A'),
(5, 15, 'By arrangement'),
(6, 15, 'By arrangement'),
(7, 15, 'By arrangement'),
(8, 15, 'By arrangement'),
(9, 15, 'By arrangement'),
(10, 15, 'N/A'),

-- Service 16: Trust Account Management Fee
(1, 16, '0–25 PHP'),
(2, 16, '0–25 PHP'),
(3, 16, '0–25 PHP'),
(4, 16, '0–25 PHP'),
(5, 16, '0–25 PHP'),
(6, 16, '0–25 PHP'),
(7, 16, '0–25 PHP'),
(8, 16, '0–25 PHP'),
(9, 16, '0–25 PHP'),
(10, 16, 'N/A'),

-- Service 17: E-money Services
(1, 17, 'Varies'),
(2, 17, 'Varies'),
(3, 17, 'Varies'),
(4, 17, 'N/A'),
(5, 17, 'Varies'),
(6, 17, 'Varies'),
(7, 17, 'Varies'),
(8, 17, 'Varies'),
(9, 17, 'Varies'),
(10, 17, 'N/A');