 CREATE DATABASE IF NOT EXISTS hotel_management;
USE hotel_management;
 CREATE TABLE IF NOT EXISTS rooms (
    room_number INT PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    status ENUM('available', 'booked', 'checked-in') DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    room_number INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    status ENUM('booked', 'checked-in', 'checked-out') DEFAULT 'booked',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (room_number) REFERENCES rooms(room_number)
);