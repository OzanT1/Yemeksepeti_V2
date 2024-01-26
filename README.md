The project is an online food ordering system (like 'Yemeksepeti'). It is not connected to the internet, it is a desktop app that uses a local database. There are three user logins. These are for restaurants, for customers and for carriers.

![image](https://github.com/alimertgok/Yemeksepeti_V2/assets/103127960/a31f8aac-3497-4847-8519-e6b550535e86)

![image](https://github.com/alimertgok/Yemeksepeti_V2/assets/103127960/e161d439-ddac-455d-9efd-8bde3fe63a91)

![image](https://github.com/alimertgok/Yemeksepeti_V2/assets/103127960/a4cf1191-cb95-4e98-b195-8f9caac29457)

SQL commands to create the local database:

CREATE TABLE Customers(
    customerID INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(50),
    address VARCHAR(50),
    phoneNumber VARCHAR(50)
);

CREATE TABLE Restaurants(
    restaurantID INT AUTO_INCREMENT PRIMARY KEY,
    restaurantName VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(50),
    address VARCHAR(50),
    phoneNumber VARCHAR(50)
);

CREATE TABLE Items(
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    itemName VARCHAR(50),
    price DECIMAL(5,2),
    foodType VARCHAR(50),
    restaurantID INT,
    FOREIGN KEY (restaurantID) REFERENCES Restaurants (restaurantID)
);

CREATE TABLE Reviews(
    reviewID INT AUTO_INCREMENT PRIMARY KEY,
    itemID INT,
    customerID INT,
    reviewText VARCHAR(250),
    rating INT,
    date DATE,
    FOREIGN KEY (customerID) REFERENCES Customers (customerID),
    FOREIGN KEY (itemID) REFERENCES Items (itemID)
);

CREATE TABLE Carriers(
    carrierID INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(50),
    phoneNumber VARCHAR(50)
);

CREATE TABLE Orders(
    orderID INT AUTO_INCREMENT PRIMARY KEY,
    orderDate DATE,
    paymentMethod VARCHAR(50),
    customerID INT,
    carrierID INT,
    FOREIGN KEY (customerID) REFERENCES Customers (customerID),
    FOREIGN KEY (carrierID) REFERENCES Carriers (carrierID)
);

CREATE TABLE OrderDetails(
    orderDetailsID INT AUTO_INCREMENT PRIMARY KEY,
    orderID INT,
    itemID INT NOT NULL,
    quantity INT,
    FOREIGN KEY (orderID) REFERENCES Orders (orderID),
    FOREIGN KEY (itemID) REFERENCES Items (itemID)
);


![image](https://github.com/alimertgok/Yemeksepeti_V2/assets/103127960/32412b1c-2aba-4d61-9985-193af2de9a2e)

