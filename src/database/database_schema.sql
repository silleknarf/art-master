CREATE TABLE User 
(
    UserId INT AUTO_INCREMENT NOT NULL, 
    Username VARCHAR(40) NOT NULL
)

CREATE TABLE Image
(
    ImageId INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    UserId INT NOT NULL,
    Location VARCHAR(255) NOT NULL
)

CREATE TABLE Round
(
    RoundId INT AUTO_INCREMENT NOT NULL PRIMARY KEY
)

CREATE TABLE RoundImage
(
    RoundImageId INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    RoundId INT NOT NULL,
    ImageId INT NOT NULL
)

CREATE TABLE Rating 
(
    RatingId INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    RoundId INT NOT NULL,
    RoundImageId INT NOT NULL
)