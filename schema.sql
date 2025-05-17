-- Drop the database if it exists
DROP DATABASE IF EXISTS cms;
-- Create the database
CREATE DATABASE cms;
BEGIN;
USE cms;
DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS USERPROFILES;
DROP TABLE IF EXISTS CATEGORY;
DROP TABLE IF EXISTS CLEANINGSERVICE;
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS REPORT;
DROP TABLE IF EXISTS SHORTLIST;

-- Renamed ROLES to USERPROFILE
CREATE TABLE USERPROFILE (
    role_id INT AUTO_INCREMENT,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    roleStatus BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (role_id)
);

-- Merged USERS and USERPROFILES
CREATE TABLE USERS (
    userID INT AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(256) NOT NULL,
    role_id INT,  -- FK to USERPROFILE
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    address VARCHAR(255),
    phone VARCHAR(20),
    isActive BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (userID),
    FOREIGN KEY (role_id) REFERENCES USERPROFILE(role_id)
);


-- Category Table 
CREATE TABLE CATEGORY (
    categoryID INT AUTO_INCREMENT,
    name VARCHAR(100),
    description TEXT,
    categoryStatus BOOLEAN DEFAULT TRUE,
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (categoryID)
);
-- CleaningService Table 
CREATE TABLE CLEANINGSERVICE (
    serviceID INT AUTO_INCREMENT,
    cleanerID INT,
    categoryID INT,
    title VARCHAR(100),
    description TEXT,
    price DECIMAL(10,2),
    serviceStatus BOOLEAN DEFAULT TRUE,
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (serviceID),
    FOREIGN KEY (cleanerID) REFERENCES USERS(userID),
    FOREIGN KEY (categoryID) REFERENCES CATEGORY(categoryID)
);
-- Shortlist Table
CREATE TABLE SHORTLIST (
    shortlistID INT AUTO_INCREMENT,
    homeownerID INT,
    serviceID INT,
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (shortlistID),
    FOREIGN KEY (homeownerID) REFERENCES USERS(userID),
    FOREIGN KEY (serviceID) REFERENCES CLEANINGSERVICE(serviceID)
);
-- Booking Table with new bookingHour column
CREATE TABLE BOOKING (
    bookingID INT AUTO_INCREMENT,
    homeownerID INT,
    serviceID INT,
    cleanerID INT,
    bookingDate DATE,
    bookingHour INT,
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    totalPrice DECIMAL(10,2),
    bookingStatus VARCHAR(50),
    PRIMARY KEY (bookingID),
    FOREIGN KEY (homeownerID) REFERENCES USERS(userID),
    FOREIGN KEY (serviceID) REFERENCES CLEANINGSERVICE(serviceID),
    FOREIGN KEY (cleanerID) REFERENCES USERS(userID)
);
-- Updated Report Table
CREATE TABLE REPORT (
    reportID INT AUTO_INCREMENT,
    reportType ENUM('Daily Report', 'Weekly Report', 'Monthly Report'),
    reportData TEXT,
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (reportID)
);

-- Insert into USERPROFILE (previously ROLES)
INSERT INTO USERPROFILE (role_name, description, roleStatus) VALUES
('Homeowner', 'Can request cleaning services', 1),
('Cleaner', 'Provides cleaning services', 1),
('Platform manager', 'Manages the platform', 1),
('User admin', 'Manages users', 1);

-- Insert into USERS (merged data)
INSERT INTO USERS (email, password, role_id, first_name, last_name, address, phone) VALUES
('mya@gmail.com', 'mya123', 1, 'Mya', 'Tan', '123 Clementi Rd', '8756441'),
('mary@gmail.com', 'mary345', 2, 'Mary', 'Lim', '457 Boonlay Dr', '8955467'),
('alex@gmail.com', 'alex567', 2, 'Alex', 'Chen', '221 Tampines Ave', '8355521'),
('sarah@gmail.com', 'sarah789', 1, 'Sarah', 'Wong', '55 Holland Rd', '9125560'),
('james@gmail.com', 'james223', 1, 'James', 'Koh', '89 Orchard Rd', '8644789'),
('peter@gmail.com', 'peter456', 3, 'Peter', 'Lee', '886 Bedok North', '8895746'),
('john@gmail.com', 'john678', 4, 'John', 'Wong', '11 Ang Mo Kio Ave', '7755894');

-- Insert CATEGORY
INSERT INTO CATEGORY (name, description, categoryStatus) VALUES
('General Cleaning', 'Basic home and office cleaning services', 1),
('Deep Cleaning', 'Intensive cleaning services including carpet and windows', 1),
('Move-in/Move-out', 'Comprehensive cleaning for property transitions', 1),
('Specialty Services', 'Specialized cleaning for specific items or areas', 1);

-- Insert CLEANINGSERVICE
INSERT INTO CLEANINGSERVICE (cleanerID, categoryID, title, description, price, serviceStatus) VALUES
(2, 1, 'Basic Home Cleaning', 'Regular cleaning of living spaces', 80.00, 1),
(2, 2, 'Full House Deep Clean', 'Complete house cleaning including windows', 150.00, 1),
(2, 3, 'Move-out Special', 'Thorough cleaning when moving out', 200.00, 1),
(3, 1, 'Office Cleaning', 'Regular cleaning for office spaces', 100.00, 1),
(3, 2, 'Spring Cleaning', 'Intensive seasonal cleaning', 180.00, 1),
(3, 4, 'Carpet Cleaning', 'Deep cleaning of carpets and rugs', 120.00, 1);

-- Insert BOOKING with bookingHour and updated totalPrice calculation
INSERT INTO BOOKING (homeownerID, serviceID, cleanerID, bookingDate, bookingHour, totalPrice, bookingStatus) VALUES
-- Today (May 2, 2025) and yesterday bookings
(1, 1, 2, '2025-05-02', 1, 80.00 * 1, 'Confirmed'),
(4, 2, 2, '2025-05-02', 2, 150.00 * 2, 'Pending'),
(5, 4, 3, '2025-05-02', 2, 100.00 * 2, 'Confirmed'),
(1, 5, 3, '2025-05-01', 3, 180.00 * 3, 'Completed'),
(4, 3, 2, '2025-05-01', 2, 200.00 * 2, 'Completed'),

-- Bookings from earlier this week
(5, 6, 3, '2025-04-30', 1, 120.00 * 1, 'Completed'),
(1, 2, 2, '2025-04-29', 3, 150.00 * 3, 'Completed'),
(4, 4, 3, '2025-04-28', 2, 100.00 * 2, 'Completed'),

-- Bookings from last week
(5, 1, 2, '2025-04-25', 1, 80.00 * 1, 'Completed'),
(1, 5, 3, '2025-04-24', 2, 180.00 * 2, 'Completed'),
(4, 3, 2, '2025-04-23', 3, 200.00 * 3, 'Completed'),

-- Bookings from earlier this month
(5, 6, 3, '2025-04-17', 1, 120.00 * 1, 'Completed'),
(1, 2, 2, '2025-04-14', 2, 150.00 * 2, 'Completed'),
(4, 1, 2, '2025-04-10', 1, 80.00 * 1, 'Completed'),
(5, 4, 3, '2025-04-07', 2, 100.00 * 2, 'Completed');

-- Insert SHORTLIST items
INSERT INTO SHORTLIST (homeownerID, serviceID) VALUES
(1, 1),
(1, 2),
(1, 3),
(4, 2),
(4, 4),
(5, 1),
(5, 5);

-- Generate Daily Report with fixed date
INSERT INTO REPORT (reportType, reportData, create_at) 
VALUES 
(
  'Daily Report', 
  JSON_OBJECT(
    'report_date', '2025-05-02',

    'total_bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-02'),
    'total_revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-02'),

    'confirmed_bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-02' AND bookingStatus = 'Confirmed'),
    'pending_bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-02' AND bookingStatus = 'Pending'),
    'completed_bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-02' AND bookingStatus = 'Completed'),
    'cancelled_bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-02' AND bookingStatus = 'Cancelled'),

    'service_distribution', JSON_OBJECT(
      'Basic Home Cleaning', (SELECT COUNT(*) FROM BOOKING WHERE serviceID = 1 AND DATE(bookingDate) = '2025-05-02'),
      'Full House Deep Clean', (SELECT COUNT(*) FROM BOOKING WHERE serviceID = 2 AND DATE(bookingDate) = '2025-05-02'),
      'Office Cleaning', (SELECT COUNT(*) FROM BOOKING WHERE serviceID = 4 AND DATE(bookingDate) = '2025-05-02')
    ),

    'predicted_next_day_bookings', 3,
    'predicted_next_day_revenue', 150.75  -- Replace with actual predicted value
  ),
  '2025-05-02 12:00:00'
);

-- Generate Weekly Report with fixed dates
INSERT INTO REPORT (reportType, reportData, create_at) 
VALUES 
('Weekly Report', 
 JSON_OBJECT(
   'start_date', '2025-04-26',
   'end_date', '2025-05-02',
   'total_bookings', (SELECT COUNT(*) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-26' AND '2025-05-02'),
   'total_revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-26' AND '2025-05-02'),

   'booking_status', JSON_OBJECT(
     'Confirmed', (SELECT COUNT(*) FROM BOOKING WHERE bookingStatus = 'Confirmed' AND bookingDate BETWEEN '2025-04-26' AND '2025-05-02'),
     'Pending', (SELECT COUNT(*) FROM BOOKING WHERE bookingStatus = 'Pending' AND bookingDate BETWEEN '2025-04-26' AND '2025-05-02'),
     'Completed', (SELECT COUNT(*) FROM BOOKING WHERE bookingStatus = 'Completed' AND bookingDate BETWEEN '2025-04-26' AND '2025-05-02'),
     'Cancelled', (SELECT COUNT(*) FROM BOOKING WHERE bookingStatus = 'Cancelled' AND bookingDate BETWEEN '2025-04-26' AND '2025-05-02')
   ),

   'daily_statistics', JSON_OBJECT(
     '2025-04-26', JSON_OBJECT('bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-26'), 'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-26')),
     '2025-04-27', JSON_OBJECT('bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-27'), 'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-27')),
     '2025-04-28', JSON_OBJECT('bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-28'), 'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-28')),
     '2025-04-29', JSON_OBJECT('bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-29'), 'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-29')),
     '2025-04-30', JSON_OBJECT('bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-30'), 'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE DATE(bookingDate) = '2025-04-30')),
     '2025-05-01', JSON_OBJECT('bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-01'), 'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-01')),
     '2025-05-02', JSON_OBJECT('bookings', (SELECT COUNT(*) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-02'), 'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE DATE(bookingDate) = '2025-05-02'))
   ),

   'cleaner_performance', JSON_ARRAY(
     JSON_OBJECT(
       'name', 'Mary Lim',
       'bookings', (SELECT COUNT(*) FROM BOOKING WHERE cleanerID = 2 AND bookingDate BETWEEN '2025-04-26' AND '2025-05-02'),
       'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE cleanerID = 2 AND bookingDate BETWEEN '2025-04-26' AND '2025-05-02')
     ),
     JSON_OBJECT(
       'name', 'Alex Chen',
       'bookings', (SELECT COUNT(*) FROM BOOKING WHERE cleanerID = 3 AND bookingDate BETWEEN '2025-04-26' AND '2025-05-02'),
       'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE cleanerID = 3 AND bookingDate BETWEEN '2025-04-26' AND '2025-05-02')
     )
   ),

   'predicted_next_week_bookings', 17,
   'previous_week_bookings', 9
 ),
 '2025-05-02 13:00:00');


-- Generate Monthly Report with fixed dates
INSERT INTO REPORT (reportType, reportData, create_at) 
VALUES (
  'Monthly Report', 
  JSON_OBJECT(
    'start_date', '2025-04-03',
    'end_date', '2025-05-02',

    'total_bookings', (SELECT COUNT(*) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
    'total_revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
    'average_booking_value', (SELECT COALESCE(AVG(totalPrice), 0) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),

    'booking_status', JSON_OBJECT(
      'Pending', (SELECT COUNT(*) FROM BOOKING WHERE bookingStatus = 'Pending' AND bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
      'Confirmed', (SELECT COUNT(*) FROM BOOKING WHERE bookingStatus = 'Confirmed' AND bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
      'Completed', (SELECT COUNT(*) FROM BOOKING WHERE bookingStatus = 'Completed' AND bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
      'Cancelled', (SELECT COUNT(*) FROM BOOKING WHERE bookingStatus = 'Cancelled' AND bookingDate BETWEEN '2025-04-03' AND '2025-05-02')
    ),

    'completion_rate', (
      SELECT 
        ROUND(
          100.0 * 
          SUM(CASE WHEN bookingStatus = 'Completed' THEN 1 ELSE 0 END) /
          NULLIF(COUNT(*), 0), 
        2)
      FROM BOOKING 
      WHERE bookingDate BETWEEN '2025-04-03' AND '2025-05-02'
    ),

    'weekly_trends', JSON_ARRAY(
      JSON_OBJECT(
        'week', 1,
        'start_date', '2025-04-03',
        'end_date', '2025-04-09',
        'bookings', (SELECT COUNT(*) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-03' AND '2025-04-09'),
        'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-03' AND '2025-04-09')
      ),
      JSON_OBJECT(
        'week', 2,
        'start_date', '2025-04-10',
        'end_date', '2025-04-16',
        'bookings', (SELECT COUNT(*) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-10' AND '2025-04-16'),
        'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-10' AND '2025-04-16')
      ),
      JSON_OBJECT(
        'week', 3,
        'start_date', '2025-04-17',
        'end_date', '2025-04-24',
        'bookings', (SELECT COUNT(*) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-17' AND '2025-04-24'),
        'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-17' AND '2025-04-24')
      ),
      JSON_OBJECT(
        'week', 4,
        'start_date', '2025-04-25',
        'end_date', '2025-05-02',
        'bookings', (SELECT COUNT(*) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-25' AND '2025-05-02'),
        'revenue', (SELECT COALESCE(SUM(totalPrice), 0) FROM BOOKING WHERE bookingDate BETWEEN '2025-04-25' AND '2025-05-02')
      )
    ),

    'category_performance', JSON_ARRAY(
      JSON_OBJECT(
        'name', 'General Cleaning',
        'bookings', (SELECT COUNT(*) FROM BOOKING b JOIN CLEANINGSERVICE cs ON b.serviceID = cs.serviceID WHERE cs.categoryID = 1 AND b.bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
        'revenue', (SELECT COALESCE(SUM(b.totalPrice), 0) FROM BOOKING b JOIN CLEANINGSERVICE cs ON b.serviceID = cs.serviceID WHERE cs.categoryID = 1 AND b.bookingDate BETWEEN '2025-04-03' AND '2025-05-02')
      ),
      JSON_OBJECT(
        'name', 'Deep Cleaning',
        'bookings', (SELECT COUNT(*) FROM BOOKING b JOIN CLEANINGSERVICE cs ON b.serviceID = cs.serviceID WHERE cs.categoryID = 2 AND b.bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
        'revenue', (SELECT COALESCE(SUM(b.totalPrice), 0) FROM BOOKING b JOIN CLEANINGSERVICE cs ON b.serviceID = cs.serviceID WHERE cs.categoryID = 2 AND b.bookingDate BETWEEN '2025-04-03' AND '2025-05-02')
      ),
      JSON_OBJECT(
        'name', 'Move-in/Move-out',
        'bookings', (SELECT COUNT(*) FROM BOOKING b JOIN CLEANINGSERVICE cs ON b.serviceID = cs.serviceID WHERE cs.categoryID = 3 AND b.bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
        'revenue', (SELECT COALESCE(SUM(b.totalPrice), 0) FROM BOOKING b JOIN CLEANINGSERVICE cs ON b.serviceID = cs.serviceID WHERE cs.categoryID = 3 AND b.bookingDate BETWEEN '2025-04-03' AND '2025-05-02')
      ),
      JSON_OBJECT(
        'name', 'Specialty Services',
        'bookings', (SELECT COUNT(*) FROM BOOKING b JOIN CLEANINGSERVICE cs ON b.serviceID = cs.serviceID WHERE cs.categoryID = 4 AND b.bookingDate BETWEEN '2025-04-03' AND '2025-05-02'),
        'revenue', (SELECT COALESCE(SUM(b.totalPrice), 0) FROM BOOKING b JOIN CLEANINGSERVICE cs ON b.serviceID = cs.serviceID WHERE cs.categoryID = 4 AND b.bookingDate BETWEEN '2025-04-03' AND '2025-05-02')
      )
    ),

    'predicted_next_month_bookings', 4
  ),
  '2025-05-02 14:00:00'
);

COMMIT;