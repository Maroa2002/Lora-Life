-- Database for the vet booking system
CREATE DATABASE IF NOT EXISTS vet_booking;

USE vet_booking;

-- Main Users Table (Common Fields)
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_role ENUM('farmer', 'vet') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Farmers Table (Additional Fields)
CREATE TABLE IF NOT EXISTS farmers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    farm_name VARCHAR(255) DEFAULT NULL,
    farm_location TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Vets Table (Additional Fields)
CREATE TABLE IF NOT EXISTS vets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    specialization VARCHAR(255) NOT NULL,
    years_experience INT NOT NULL,
    verification_doc VARCHAR(255) NOT NULL,
    clinic_name VARCHAR(255) DEFAULT NULL,
    service_location TEXT NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for faster lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_farmers_user_id ON farmers(user_id);
CREATE INDEX idx_vets_user_id ON vets(user_id);