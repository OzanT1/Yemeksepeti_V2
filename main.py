from tkinter import messagebox

import mysql.connector
import tkinter as tk
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

mydb = mysql.connector.connect(
    host=config['Database']['host'],
    user=config['Database']['user'],
    password=config['Database']['password'],
    port=config['Database']['port'],
    database=config['Database']['database']
)

mycursor = mydb.cursor()  # is an object to connect mydb


# CHECK IF THE USER ENTER CORRECT EMAIL AND PASSWORD

#       RESTAURANT AUTHENTICATE
def authenticate_restaurant(email, password) -> bool:
    # Execute a query to check if there is a match for the provided email and password
    mycursor.execute("SELECT * FROM Restaurants WHERE email = %s AND password = %s", (email, password))
    restaurant = mycursor.fetchone()

    # Check if a restaurant was found with the provided credentials
    return restaurant is not None


# AFTER CLICKING RESTAURANT ENTRANCE BUTTON, RUN THE RESTAURANT LOGIN PAGE
def restaurant_login():
    login_restaurant = tk.Toplevel(root)
    login_restaurant.title("Restaurant Login")
    login_restaurant.geometry("300x400")

    # Add widgets to the login window
    email_label = tk.Label(login_restaurant, text="Email:")
    password_label = tk.Label(login_restaurant, text="Password:")

    email_entry = tk.Entry(login_restaurant)
    password_entry = tk.Entry(login_restaurant, show='*')

    login_button = tk.Button(login_restaurant, text="Login",
                             command=lambda: restaurant_page(login_restaurant, email_entry.get(), password_entry.get()))
    # Register
    register_label = tk.Label(login_restaurant, text="If you don't have an account, please register")
    register_button = tk.Button(login_restaurant, text="Register", command=register_restaurant)

    email_label.pack(pady=10)
    email_entry.pack(pady=5)

    password_label.pack(pady=10)
    password_entry.pack(pady=5)

    login_button.pack(pady=20)

    register_label.pack(pady=10)
    register_button.pack(pady=10)


# REGISTER RESTAURANT PAGE
def submit_register_restaurant(name, email, password, address, phone_number):
    try:
        # Check if the restaurant is already registered
        mycursor.execute("SELECT * FROM Restaurants WHERE email = %s AND password = %s", (email, password))
        existing_restaurant = mycursor.fetchone()

        if existing_restaurant:
            messagebox.showerror("Authentication Failed", "User already registered")
        else:
            # Insert the new restaurant into the database
            sql_command = "INSERT INTO Restaurants (restaurantName, email, password, address, phoneNumber) VALUES (%s, %s, %s, %s, %s)"

            mycursor.execute(sql_command, (name, email, password, address, phone_number))

            mydb.commit()
            messagebox.showinfo("Registration Successful", "Restaurant registered successfully")

    except Exception as e:
        # Handle any database errors
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        # Close the database connection
        mydb.close()


def register_restaurant():
    register_screen = tk.Toplevel(root)
    register_screen.title("Register")
    register_screen.geometry("500x500")

    # LABELS AND THEIR ENTRIES

    # Restaurant name
    restaurant_name_label = tk.Label(register_screen, text="Name of the restaurant:")

    # Restaurant NAME entry
    restaurant_name_entry = tk.Entry(register_screen)

    # Restaurant EMAIL
    email_label = tk.Label(register_screen, text="Email:")

    # Restaurant EMAIL entry
    email_entry = tk.Entry(register_screen)

    # Restaurant PASSWORD
    password_label = tk.Label(register_screen, text="Password:")

    # Restaurant PASSWORD entry
    password_entry = tk.Entry(register_screen, show='*')

    # Restaurant ADDRESS
    address_label = tk.Label(register_screen, text="Address:")

    # Restaurant ADDRESS entry
    address_entry = tk.Entry(register_screen)

    # Restaurant PHONE NUMBER
    phone_number_label = tk.Label(register_screen, text="Enter phone number:")

    # Restaurant PHONE NUMBER entry
    phone_number_entry = tk.Entry(register_screen)

    # PACKS

    # restaurant name
    restaurant_name_label.pack(pady=10)
    restaurant_name_entry.pack(pady=5)

    # email
    email_label.pack(pady=10)
    email_entry.pack(pady=5)

    # password
    password_label.pack(pady=10)
    password_entry.pack(pady=5)

    # address
    address_label.pack(pady=10)
    address_entry.pack(pady=5)

    # phone number
    phone_number_label.pack(pady=10)
    phone_number_entry.pack(pady=5)

    # Take the restaurant user's details for registration
    submit_button = tk.Button(register_screen, text="Submit",
                              command=lambda: submit_register_restaurant(restaurant_name_entry.get(),
                                                                         email_entry.get(), password_entry.get(),
                                                                         address_entry.get(), phone_number_entry.get()))
    # Submit button
    submit_button.pack(pady=20)


# AFTER LOGIN, RUN THE RESTAURANT MAIN PAGE
def restaurant_page(login_restaurant, email, password):
    # Authenticate the restaurant
    if authenticate_restaurant(email, password):
        # Destroy the login window and show the main page
        login_restaurant.destroy()

        # Destroy entrance page, so you are into next page
        entrance_page.pack_forget()

        restaurant_window = tk.Frame(root, padx=1, pady=1)
        restaurant_window.pack(padx=10, pady=10)

        # Add widgets to the main page
        label = tk.Label(restaurant_window, text="Welcome to the Restaurant Main Page!")
        label.pack(pady=20, side=tk.TOP)

        home_button = tk.Button(restaurant_window, text="Home", command=lambda: go_to_home(restaurant_window))
        home_button.pack(pady=20, padx=20, side=tk.BOTTOM)

    else:
        messagebox.showerror("Authentication Failed", "Incorrect email or password.")


def restaurant_action():
    restaurant_login()


#       CUSTOMER AUTHENTICATE
def authenticate_customer(email, password):
    mycursor.execute("SELECT * FROM Customers WHERE email = %s AND password = %s", (email, password))
    customer = mycursor.fetchone()
    return customer is not None


# REGISTER CUSTOMER PAGE
def submit_register_customer(first_name, last_name, email, password, address, phone_number):
    try:
        # Check if the customer is already registered
        mycursor.execute("SELECT * FROM Customers WHERE email = %s AND password = %s", (email, password))
        existing_customer = mycursor.fetchone()

        if existing_customer:
            messagebox.showerror("Authentication Failed", "User already registered")
        else:
            # Insert the new customer into the database
            sql_command = "INSERT INTO Customers (firstName, lastName, email, password, address, phoneNumber) VALUES (%s, %s, %s, %s, %s, %s)"

            mycursor.execute(sql_command, (first_name, last_name, email, password, address, phone_number))

            mydb.commit()
            messagebox.showinfo("Registration Successful", "Customer registered successfully")

    except Exception as e:
        # Handle any database errors
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        # Close the database connection
        mydb.close()


def register_customer():
    register_screen = tk.Toplevel(root)
    register_screen.title("Register")
    register_screen.geometry("500x500")

    # LABELS AND THEIR ENTRIES

    # Customer First Name Label
    first_name_label = tk.Label(register_screen, text="Enter your first name:")

    # Customer First Name Entry
    first_name_entry = tk.Entry(register_screen)

    # Customer Last Name Label
    last_name_label = tk.Label(register_screen, text="Enter your last name:")

    # Customer Last Name Entry
    last_name_entry = tk.Entry(register_screen)

    # Customer Email Label
    email_label = tk.Label(register_screen, text="Enter your email:")

    # Customer Email Entry
    email_entry = tk.Entry(register_screen)

    # Customer Password Label
    password_label = tk.Label(register_screen, text="Enter your password")

    # Customer Password Entry
    password_entry = tk.Entry(register_screen, show='*')

    # Customer Address Label
    address_label = tk.Label(register_screen, text="Enter your address:")

    # Customer Address Entry
    address_entry = tk.Entry(register_screen)

    # Customer Phone Number Label
    phone_number_label = tk.Label(register_screen, text="Enter your phone number:")

    # Customer Phone Number Entry
    phone_number_entry = tk.Entry(register_screen)

    # PACKS

    # First Name
    first_name_label.pack(pady=10)
    first_name_entry.pack(pady=5)

    # Last Name
    last_name_label.pack(pady=10)
    last_name_entry.pack(pady=5)

    # Email
    email_label.pack(pady=10)
    email_entry.pack(pady=5)

    # Password
    password_label.pack(pady=10)
    password_entry.pack(pady=5)

    # Address
    address_label.pack(pady=10)
    address_entry.pack(pady=5)

    # Phone Number
    phone_number_label.pack(pady=10)
    phone_number_entry.pack(pady=5)

    # Take the customer's details for registration
    submit_button = tk.Button(register_screen, text="Submit",
                              command=lambda: submit_register_customer(
                                  first_name_entry.get(), last_name_entry.get(), email_entry.get(),
                                  password_entry.get(), address_entry.get(), phone_number_entry.get()))

    submit_button.pack(pady=20)


def customer_login():
    login_customer = tk.Toplevel(root)
    login_customer.title("Customer Login")
    login_customer.geometry("300x400")

    email_label = tk.Label(login_customer, text="Email:")
    password_label = tk.Label(login_customer, text="Password:")

    email_entry = tk.Entry(login_customer)
    password_entry = tk.Entry(login_customer, show='*')

    login_button = tk.Button(login_customer, text="Login",
                             command=lambda: customer_page(login_customer, email_entry.get(), password_entry.get()))

    # Register
    register_label = tk.Label(login_customer, text="If you don't have an account, please register")
    register_button = tk.Button(login_customer, text="Register", command=register_customer)

    email_label.pack(pady=10)
    email_entry.pack(pady=5)

    password_label.pack(pady=10)
    password_entry.pack(pady=5)

    login_button.pack(pady=20)

    register_label.pack(pady=10)
    register_button.pack(pady=10)


def customer_page(login_customer, email, password):
    def show_selected_restaurant_items(event):
        # Clear the existing items in items_listbox
        items_listbox.delete(0, tk.END)

        # Get the selected restaurant
        selected_restaurant = str(restaurants_listbox.get(restaurants_listbox.curselection()))

        # Fetch items for the selected restaurant from the database
        sql = f"SELECT Items.itemName FROM Items INNER JOIN Restaurants ON Items.restaurantID = Restaurants.restaurantID WHERE Restaurants.restaurantName = '{selected_restaurant}'"
        mycursor.execute(sql)

        # Insert fetched items into the items_listbox
        for item in mycursor.fetchall():
            items_listbox.insert(tk.END, item[0])

    if authenticate_customer(email, password):

        login_customer.destroy()

        entrance_page.pack_forget()

        customer_frame = tk.Frame(root, padx=10, pady=10, bg="red")
        customer_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        home_button = tk.Button(customer_frame, text="Home", command=lambda: go_to_home(customer_frame))
        home_button.pack(pady=20, padx=20, side=tk.TOP)

        restaurants_list_frame = tk.Frame(customer_frame, padx=10, pady=10, bg="black")
        restaurants_list_frame.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the list of restaurants
        scrollbar = tk.Scrollbar(restaurants_list_frame, orient=tk.VERTICAL)

        # Listbox to display the restaurants
        restaurants_listbox = tk.Listbox(restaurants_list_frame, yscrollcommand=scrollbar.set)
        restaurants_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar to work with the Listbox
        scrollbar.config(command=restaurants_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        sql = "SELECT restaurantName FROM Restaurants"
        mycursor.execute(sql)

        restaurants = []

        # Get from database
        for name in mycursor.fetchall():
            restaurants.append(name[0])

        # Insert restaurants into the Listbox
        for restaurant in restaurants:
            restaurants_listbox.insert(tk.END, restaurant)

        # Bind the show_selected_restaurant_items function to the selection event
        restaurants_listbox.bind("<<ListboxSelect>>", show_selected_restaurant_items)



        items_list_frame = tk.Frame(customer_frame, padx=10, pady=10, bg="blue")
        items_list_frame.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=1)

        basket_list_frame = tk.Frame(customer_frame, padx=10, pady=10, bg="black")
        basket_list_frame.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Listbox to display the items
        items_listbox = tk.Listbox(items_list_frame)
        items_listbox.pack(fill=tk.BOTH, expand=True)

        customer_basket = []


    else:
        messagebox.showerror("Authentication Failed", "Incorrect email or password.")


def customer_action():
    customer_login()


#       CARRIER AUTHENTICATE
def authenticate_carrier(email, password):
    mycursor.execute("SELECT * FROM Carriers WHERE email = %s AND password = %s", (email, password))
    carrier = mycursor.fetchone()
    return carrier is not None


# REGISTER CARRIER PAGE
def submit_register_carrier(first_name, last_name, email, password, phone_number):
    try:
        # Check if the carrier is already registered
        mycursor.execute("SELECT * FROM Carriers WHERE email = %s AND password = %s", (email, password))
        existing_carrier = mycursor.fetchone()

        if existing_carrier:
            messagebox.showerror("Authentication Failed", "User already registered")
        else:
            # Insert the new carrier into the database
            sql_command = "INSERT INTO Carriers (firstName, lastName, email, password, phoneNumber) VALUES (%s, %s, %s, %s, %s)"

            mycursor.execute(sql_command, (first_name, last_name, email, password, phone_number))

            mydb.commit()
            messagebox.showinfo("Registration Successful", "Carrier registered successfully")

    except Exception as e:
        # Handle any database errors
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    finally:
        # Close the database connection
        mydb.close()


def register_carrier():
    register_screen = tk.Toplevel(root)
    register_screen.title("Register")
    register_screen.geometry("500x500")

    # LABELS AND THEIR ENTRIES

    # Carrier First Name Label
    first_name_label = tk.Label(register_screen, text="Enter your first name:")

    # Carrier First Name Entry
    first_name_entry = tk.Entry(register_screen)

    # Carrier Last Name Label
    last_name_label = tk.Label(register_screen, text="Enter your last name:")

    # Carrier Last Name Entry
    last_name_entry = tk.Entry(register_screen)

    # Carrier Email Label
    email_label = tk.Label(register_screen, text="Enter your email:")

    # Carrier Email Entry
    email_entry = tk.Entry(register_screen)

    # Carrier Password Label
    password_label = tk.Label(register_screen, text="Enter your password")

    # Carrier Password Entry
    password_entry = tk.Entry(register_screen, show='*')

    # Carrier Phone Number Label
    phone_number_label = tk.Label(register_screen, text="Enter your phone number:")

    # Carrier Phone Number Entry
    phone_number_entry = tk.Entry(register_screen)

    # PACKS

    # First Name
    first_name_label.pack(pady=10)
    first_name_entry.pack(pady=5)

    # Last Name
    last_name_label.pack(pady=10)
    last_name_entry.pack(pady=5)

    # Email
    email_label.pack(pady=10)
    email_entry.pack(pady=5)

    # Password
    password_label.pack(pady=10)
    password_entry.pack(pady=5)

    # Phone Number
    phone_number_label.pack(pady=10)
    phone_number_entry.pack(pady=5)

    # Take the customer's details for registration
    submit_button = tk.Button(register_screen, text="Submit",
                              command=lambda: submit_register_carrier(
                                  first_name_entry.get(), last_name_entry.get(), email_entry.get(),
                                  password_entry.get(), phone_number_entry.get()))

    submit_button.pack(pady=20)


def carrier_login():
    login_carrier = tk.Toplevel(root)
    login_carrier.title("Carrier Login")
    login_carrier.geometry("300x400")

    email_label = tk.Label(login_carrier, text="Email:")
    password_label = tk.Label(login_carrier, text="Password:")

    email_entry = tk.Entry(login_carrier)
    password_entry = tk.Entry(login_carrier, show='*')

    login_button = tk.Button(login_carrier, text="Login",
                             command=lambda: carrier_page(login_carrier, email_entry.get(), password_entry.get()))

    # Register
    register_label = tk.Label(login_carrier, text="If you don't have an account, please register")
    register_button = tk.Button(login_carrier, text="Register", command=register_carrier)

    email_label.pack(pady=10)
    email_entry.pack(pady=5)

    password_label.pack(pady=10)
    password_entry.pack(pady=5)

    login_button.pack(pady=20)

    register_label.pack(pady=10)
    register_button.pack(pady=10)


def carrier_page(login_carrier, email, password):
    if authenticate_carrier(email, password):

        login_carrier.destroy()

        entrance_page.pack_forget()

        carrier_window = tk.Frame(root, padx=1, pady=1)
        carrier_window.pack(padx=10, pady=10)

        # Add widgets to the main page
        label = tk.Label(carrier_window, text="Welcome to the Carrier Main Page!")
        label.pack(pady=20, side=tk.TOP)

        home_button = tk.Button(carrier_window, text="Home", command=lambda: go_to_home(carrier_window))
        home_button.pack(pady=20, padx=20, side=tk.BOTTOM)

    else:
        messagebox.showerror("Authentication Failed", "Incorrect email or password.")


def carrier_action():
    carrier_login()


def go_to_home(current_page):
    current_page.pack_forget()
    entrance_page.pack()


def main():
    global root
    global entrance_page

    root = tk.Tk()
    root.geometry("1300x600")
    root.title("Yemeksepeti")

    entrance_page = tk.Frame(root, padx=1, pady=1)
    entrance_page.pack(padx=10, pady=10)

    # BUTTONS IN the MAIN PAGE
    restaurant_entrance_button = tk.Button(entrance_page, text="Restaurant Entrance", command=restaurant_action,
                                           width=20,
                                           height=10)
    customer_entrance_button = tk.Button(entrance_page, text="Customer Entrance", command=customer_action, width=20,
                                         height=10)
    carrier_entrance_button = tk.Button(entrance_page, text="Carrier Entrance", command=carrier_action, width=20,
                                        height=10)

    restaurant_entrance_button.pack()
    customer_entrance_button.pack()
    carrier_entrance_button.pack()

    root.mainloop()


main()
