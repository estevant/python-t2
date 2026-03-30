CREATE TABLE users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    mail VARCHAR(100),
    login VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(20) DEFAULT 'user',
    ville VARCHAR(20),
    date_modification_password DATETIME DEFAULT CURRENT_TIMESTAMP
);

select * from users; pour voir la table