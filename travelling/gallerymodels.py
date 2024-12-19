create database locations

create table locations.places (
    id INT AUTO_INCREMENT PRIMARY KEY,         -- Unique identifier
    name VARCHAR(255) NOT NULL,                -- Name of the place
    location VARCHAR(255) NOT NULL,            -- Country or location
    description TEXT,                          -- Description of the place
    image VARCHAR(255)                         -- Path or URL to the image
);
INSERT INTO locations.places (name, location, description, image) VALUES
('Paris', 'France', 'Known for the Eiffel Tower, art, and its romantic ambiance.', 'images/paris.jpg'),
('Kyoto', 'Japan', 'Famous for its temples, traditional tea houses, and cherry blossoms.', 'images/kyoto.jpg'),
('Rome', 'Italy', 'Known for the Colosseum, rich history, and Italian cuisine.', 'images/rome.jpg'),
('Cape Town', 'South Africa', 'Famous for Table Mountain, beaches, and stunning landscapes.', 'images/cape_town.jpg'),
('Sydney', 'Australia', 'Home to the iconic Opera House and beautiful harbor views.', 'images/sydney.jpg'),
('New York City', 'USA', 'Famous for the Statue of Liberty, Times Square, and Central Park.', 'images/new_york.jpg'),
('Dubai', 'UAE', 'Known for luxury shopping, ultramodern architecture, and lively nightlife.', 'images/dubai.jpg'),
('Venice', 'Italy', 'Unique for its canals, gondolas, and beautiful architecture.', 'images/venice.jpg'),
('London', 'United Kingdom', 'Known for the Big Ben, Buckingham Palace, and the River Thames.', 'images/london.jpg'),
('Bangkok', 'Thailand', 'Famous for vibrant street life, cultural landmarks, and grand palaces.', 'images/bangkok.jpg'),
('Barcelona', 'Spain', 'Known for the architecture of Antoni Gaudí, including the Sagrada Familia.', 'images/barcelona.jpg'),
('Machu Picchu', 'Peru', 'Ancient Inca city set high in the Andes Mountains, known for its stunning views.', 'images/machu_picchu.jpg'),
('Istanbul', 'Turkey', 'Known for its historic sites such as the Hagia Sophia and Blue Mosque.', 'images/istanbul.jpg'),
('Santorini', 'Greece', 'Famous for its whitewashed buildings, crystal-clear waters, and sunsets.', 'images/santorini.jpg'),
('Berlin', 'Germany', 'Known for its historical landmarks such as the Berlin Wall and Brandenburg Gate.', 'images/berlin.jpg'),
('Athens', 'Greece', 'Famous for ancient monuments like the Acropolis and Parthenon.', 'images/athens.jpg');

select * from locations.places;
