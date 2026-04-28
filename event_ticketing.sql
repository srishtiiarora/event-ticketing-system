-- Create database
CREATE DATABASE IF NOT EXISTS event_ticketing;
USE event_ticketing;

-- 1. Students Table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(50)
);

INSERT INTO students VALUES
(1, 'Riya Sharma', 'riya@example.com', 'pass123'),
(2, 'Aarav Mehta', 'aarav@example.com', 'pass456'),
(3, 'Neha Patel', 'neha@example.com', 'pass789'),
(4, 'Vikram Singh', 'vikram@example.com', 'pass111'),
(5, 'Ananya Gupta', 'ananya@example.com', 'pass222'),
(6, 'Sarthak Jain', 'sarthak@example.com', 'pass333'),
(7, 'Mehul Shah', 'mehul@example.com', 'pass444'),
(8, 'Ishita Kapoor', 'ishita@example.com', 'pass555'),
(9, 'Kabir Arora', 'kabir@example.com', 'pass666'),
(10, 'Tanvi Agarwal', 'tanvi@example.com', 'pass777');

-- 2. Event Categories Table
CREATE TABLE event_categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100)
);

INSERT INTO event_categories VALUES
(1, 'Technical'),
(2, 'Cultural'),
(3, 'Sports'),
(4, 'Workshops'),
(5, 'Seminar'),
(6, 'Music'),
(7, 'Dance'),
(8, 'Coding'),
(9, 'Robotics'),
(10, 'Gaming');

-- 3. Events Table
CREATE TABLE events (
    event_id INT PRIMARY KEY,
    event_name VARCHAR(100),
    category_id INT,
    date DATE,
    venue VARCHAR(100),
    description VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES event_categories(category_id)
);

INSERT INTO events VALUES
(1, 'Coding Contest', 1, '2024-12-05', 'Lab 2', 'Competitive coding event'),
(2, 'Dance Battle', 2, '2024-12-10', 'Auditorium', 'Inter-college dance competition'),
(3, 'Football Match', 3, '2024-12-15', 'Ground', 'Friendly football match'),
(4, 'AI Workshop', 4, '2024-12-20', 'Hall 1', 'Intro to AI'),
(5, 'Tech Seminar', 5, '2024-12-08', 'Seminar Hall', 'Tech talk by industry expert'),
(6, 'Singing Competition', 6, '2024-12-12', 'Auditorium', 'Solo and group singing'),
(7, 'Flash Mob', 7, '2024-12-18', 'Courtyard', 'Instant dance performance'),
(8, 'Robotics Expo', 9, '2024-12-22', 'Lab 5', 'Robotics model presentation'),
(9, 'Gaming Tournament', 10, '2024-12-25', 'Computer Lab', 'Valorant + BGMI'),
(10, 'Python Bootcamp', 4, '2024-12-30', 'Hall 3', 'Hands-on python training');

-- 4. Registrations Table
CREATE TABLE registrations (
    reg_id INT PRIMARY KEY,
    student_id INT,
    event_id INT,
    qr_code VARCHAR(255),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

INSERT INTO registrations VALUES
(1, 1, 1, 'QR1'),
(2, 2, 3, 'QR2'),
(3, 3, 2, 'QR3'),
(4, 4, 4, 'QR4'),
(5, 5, 5, 'QR5'),
(6, 6, 1, 'QR6'),
(7, 7, 8, 'QR7'),
(8, 8, 9, 'QR8'),
(9, 9, 10, 'QR9'),
(10, 10, 6, 'QR10');

-- 5. Check-ins Table
CREATE TABLE checkins (
    checkin_id INT PRIMARY KEY,
    reg_id INT,
    checkin_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reg_id) REFERENCES registrations(reg_id)
);

INSERT INTO checkins VALUES
(1, 1, '2024-12-05 10:00:00'),
(2, 2, '2024-12-15 14:00:00'),
(3, 3, '2024-12-10 12:00:00'),
(4, 4, '2024-12-20 09:30:00'),
(5, 5, '2024-12-08 11:00:00'),
(6, 6, '2024-12-05 10:10:00'),
(7, 7, '2024-12-22 13:20:00'),
(8, 8, '2024-12-25 15:40:00'),
(9, 9, '2024-12-30 09:45:00'),
(10, 10, '2024-12-12 11:55:00');