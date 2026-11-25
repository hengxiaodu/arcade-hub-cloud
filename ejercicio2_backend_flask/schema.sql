DROP TABLE IF EXISTS games;

CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    platform VARCHAR(100) NOT NULL,
    rating NUMERIC(3, 1) DEFAULT 0.0,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Videojuegos iniciales de prueba
INSERT INTO games (title, genre, platform, rating, image_url) VALUES
('Valorant', 'Shooter táctico', 'PC', 8.5, 'https://dummyimage.com/300x180/0f1923/fff&text=Valorant'),
('League of Legends', 'MOBA', 'PC', 9.0, 'https://dummyimage.com/300x180/091428/c89b3c&text=LoL'),
('FIFA 24', 'Deportes', 'PS5/Xbox/PC', 7.5, 'https://dummyimage.com/300x180/1a1a1a/fff&text=FIFA+24'),
('Fortnite', 'Battle Royale', 'Multiplataforma', 8.0, 'https://dummyimage.com/300x180/2b2d42/fff&text=Fortnite'),
('Among Us', 'Party / Social', 'PC/Mobile/Switch', 8.2, 'https://dummyimage.com/300x180/c1121f/fff&text=Among+Us');