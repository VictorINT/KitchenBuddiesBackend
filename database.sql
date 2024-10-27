-- Create the database
CREATE DATABASE IF NOT EXISTS api_database;
USE api_database;

-- Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    google_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX(email)
);

-- Communities table (stores information about each community)
CREATE TABLE IF NOT EXISTS Communities (
    community_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX(name)
);

-- UserCommunities table (join table for many-to-many relationship between Users and Communities)
CREATE TABLE IF NOT EXISTS UserCommunities (
    user_id INT NOT NULL,
    community_id INT NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, community_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (community_id) REFERENCES Communities(community_id) ON DELETE CASCADE
);

-- Inventory table (for storing items like utensils and food)
CREATE TABLE IF NOT EXISTS Inventory (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category ENUM('utensil', 'food') NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table (for posts associated with users in specific communities)
CREATE TABLE IF NOT EXISTS Posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    community_id INT NOT NULL,
    dish VARCHAR(150) NOT NULL,
    num_of_people INT,
    hour TIME,
    location VARCHAR(255),
    status ENUM('active', 'archived') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (community_id) REFERENCES Communities(community_id) ON DELETE CASCADE,
    INDEX(user_id),
    INDEX(community_id)
);

-- UserItems table (tracks items each user has in their inventory)
CREATE TABLE IF NOT EXISTS UserItems (
    user_item_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Inventory(item_id) ON DELETE CASCADE
);