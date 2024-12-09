CREATE DATABASE hotel_management;

USE hotel_management;

CREATE TABLE rooms (
    roomNumber INT PRIMARY KEY AUTO_INCREMENT,
    roomType VARCHAR(20),
    price DECIMAL(10, 2),
    availability BOOLEAN
);

CREATE TABLE customers (
    customerId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    contactInfo VARCHAR(255),
    paymentMethod VARCHAR(50)
);

CREATE TABLE reservations (
    reservationId INT AUTO_INCREMENT PRIMARY KEY,
    customerId INT,
    roomNumber INT,
    checkInDate DATE,
    checkOutDate DATE,
    FOREIGN KEY (customerId) REFERENCES customers(customerId),
    FOREIGN KEY (roomNumber) REFERENCES rooms(roomNumber)
);

CREATE TABLE bills (
    billId INT AUTO_INCREMENT PRIMARY KEY,
    customerId INT,
    reservationId INT,
    totalAmount DECIMAL(10, 2),
    taxes DECIMAL(10, 2),
    discounts DECIMAL(10, 2),
    paymentStatus VARCHAR(50),
    FOREIGN KEY (customerId) REFERENCES customers(customerId),
    FOREIGN KEY (reservationId) REFERENCES reservations(reservationId)
);
