import datetime
from tkinter import messagebox, ttk

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
def go_to_restaurant_page(window_to_destroy):
    # Destroy the current window and show the restaurant page
    window_to_destroy.destroy()
    restaurant_page(login_restaurant, email, password)


def restaurant_page(login_restaurant, email, password):
    # Authenticate the restaurant
    if authenticate_restaurant(email, password):
        # Destroy the login window and show the main page
        login_restaurant.destroy()

        # Destroy entrance page, so you are into next page
        entrance_page.pack_forget()

        def go_to_home(window_to_hide):
            # Hide the current window and show the entrance page
            window_to_hide.pack_forget()
            entrance_page.pack()
            root.update()  # Update the main GUI

        def go_to_restaurant_page(window_to_destroy):
            # Destroy the current window and show the restaurant page
            window_to_destroy.destroy()
            restaurant_page(login_restaurant, email, password)

        def add_back_button(window):
            back_button = tk.Button(window, text="Back", command=lambda: go_to_restaurant_page(window))
            back_button.pack(pady=20, padx=20, side=tk.BOTTOM)

        def display_restaurant_menu():
            # Retrieve the restaurant information and menu from the database based on the logged-in restaurant's email and password
            mycursor.execute("SELECT * FROM Restaurants WHERE email = %s AND password = %s", (email, password))
            restaurant = mycursor.fetchone()

            if restaurant:
                restaurant_id = restaurant[0]
                restaurant_name = restaurant[1]

                # Retrieve the menu items for the restaurant
                mycursor.execute("SELECT * FROM Items WHERE restaurantID = %s", (restaurant_id,))
                menu_items = mycursor.fetchall()

                # Destroy the existing widgets in restaurant_window
                for widget in restaurant_window.winfo_children():
                    widget.destroy()

                # Display the restaurant information
                label = tk.Label(restaurant_window, text=f"Welcome to {restaurant_name}!\nRestaurant Menu:")
                label.pack(pady=20, side=tk.TOP)

                back_button = tk.Button(restaurant_window, text="Back",
                                        command=lambda: go_to_restaurant_page(restaurant_window))
                back_button.pack(pady=20, padx=20, side=tk.BOTTOM)

                # Display the menu items
                for item in menu_items:
                    item_label = tk.Label(restaurant_window, text=f"{item[1]} - ${item[2]:.2f} - {item[3]}")
                    item_label.pack(pady=5)

        def display_daily_balance_sheet():
            # Get the restaurant information based on the logged-in restaurant's email and password
            mycursor.execute("SELECT restaurantID, restaurantName FROM Restaurants WHERE email = %s AND password = %s",
                             (email, password))
            restaurant_info = mycursor.fetchone()

            if restaurant_info:
                restaurant_id = restaurant_info[0]
                restaurant_name = restaurant_info[1]

                # Get the current date
                current_date = datetime.datetime.now().date()

                # Retrieve order details for the current date and specific restaurant
                mycursor.execute("SELECT od.itemID, od.quantity FROM OrderDetails od "
                                 "INNER JOIN Orders o ON od.orderID = o.orderID "
                                 "INNER JOIN Items i ON od.itemID = i.itemID "
                                 "INNER JOIN Restaurants r ON i.restaurantID = r.restaurantID "
                                 "WHERE o.orderDate = %s AND o.customerID IS NULL AND r.restaurantID = %s",
                                 (current_date, restaurant_id))
                order_details = mycursor.fetchall()

                # Destroy existing widgets in restaurant_window
                for widget in restaurant_window.winfo_children():
                    widget.destroy()

                # Display the daily balance sheet
                label = tk.Label(restaurant_window,
                                 text=f"Daily Balance Sheet for {current_date} - Restaurant: {restaurant_name}")
                label.pack(pady=20, side=tk.TOP)

                # Modify the Back button to go back to the restaurant page
                back_button = tk.Button(restaurant_window, text="Back",
                                        command=lambda: go_to_restaurant_page(restaurant_window))
                back_button.pack(pady=20, padx=20, side=tk.BOTTOM)

                # Display order details
                total_revenue = 0.0
                total_quantity = 0
                total_profit = 0.0

                for order_detail in order_details:
                    item_id = order_detail[0]
                    quantity = order_detail[1]

                    # Retrieve item information
                    mycursor.execute("SELECT itemName, price, cost FROM Items WHERE itemID = %s", (item_id,))
                    item_info = mycursor.fetchone()

                    if item_info:
                        item_name = item_info[0]
                        item_price = item_info[1]
                        item_cost = item_info[2]
                        revenue = quantity * item_price
                        profit = quantity * (item_price - item_cost)

                        total_revenue += revenue
                        total_quantity += quantity
                        total_profit += profit

                        order_label = tk.Label(restaurant_window,
                                               text=f"{item_name} - Quantity: {quantity} - Revenue: ${revenue:.2f} - "
                                                    f"Profit: ${profit:.2f}")
                        order_label.pack(pady=5)

                # Display total revenue, total quantity, and total profit
                total_revenue_label = tk.Label(restaurant_window, text=f"Total Revenue: ${total_revenue:.2f}")
                total_revenue_label.pack(pady=5)

                total_quantity_label = tk.Label(restaurant_window, text=f"Total Quantity Sold: {total_quantity}")
                total_quantity_label.pack(pady=5)

                total_profit_label = tk.Label(restaurant_window, text=f"Total Profit: ${total_profit:.2f}")
                total_profit_label.pack(pady=10)

            else:
                messagebox.showerror("Error", "Failed to retrieve restaurant information.")

        def add_item():
            add_item_window = tk.Toplevel(root)
            add_item_window.title("Add Item")
            add_item_window.geometry("900x600")

            item_name_label = tk.Label(add_item_window, text="Item Name:")
            item_name_entry = tk.Entry(add_item_window)

            price_label = tk.Label(add_item_window, text="Price:")
            price_entry = tk.Entry(add_item_window)

            food_type_label = tk.Label(add_item_window, text="Food Type:")
            food_type_entry = tk.Entry(add_item_window)

            add_button = tk.Button(add_item_window, text="Add Item",
                                   command=lambda: add_item_to_menu(item_name_entry.get(), price_entry.get(),
                                                                    food_type_entry.get(), add_item_window))


            item_name_label.pack(pady=10)
            item_name_entry.pack(pady=5)

            price_label.pack(pady=10)
            price_entry.pack(pady=5)

            food_type_label.pack(pady=10)
            food_type_entry.pack(pady=5)

            add_button.pack(pady=20)



        def delete_item():
            delete_item_window = tk.Toplevel(root)
            delete_item_window.title("Delete Item")
            delete_item_window.geometry("300x200")

            item_name_label = tk.Label(delete_item_window, text="Item Name:")
            item_name_entry = tk.Entry(delete_item_window)

            delete_button = tk.Button(delete_item_window, text="Delete Item",
                                      command=lambda: delete_item_from_menu(item_name_entry.get(), delete_item_window))

            item_name_label.pack(pady=10)
            item_name_entry.pack(pady=5)
            delete_button.pack(pady=20)

        def add_item_to_menu(item_name, price, food_type, window):
            # Get the restaurant ID based on the logged-in restaurant's email and password
            mycursor.execute("SELECT restaurantID FROM Restaurants WHERE email = %s AND password = %s",
                             (email, password))
            restaurant_id = mycursor.fetchone()

            if restaurant_id:
                restaurant_id = restaurant_id[0]

                # Add the item to the 'Items' table in the database
                mycursor.execute("INSERT INTO Items (itemName, price, foodType, restaurantID) VALUES (%s, %s, %s, %s)",
                                 (item_name, price, food_type, restaurant_id))
                mydb.commit()

                messagebox.showinfo("Item Added", f"Item '{item_name}' added to the menu.")
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to retrieve restaurant information.")

        def delete_item_from_menu(item_name, window):
            # Get the restaurant ID based on the logged-in restaurant's email and password
            mycursor.execute("SELECT restaurantID FROM Restaurants WHERE email = %s AND password = %s",
                             (email, password))
            restaurant_id = mycursor.fetchone()

            if restaurant_id:
                restaurant_id = restaurant_id[0]

                # Delete the item from the 'Items' table in the database
                mycursor.execute("DELETE FROM Items WHERE restaurantID = %s AND itemName = %s",
                                 (restaurant_id, item_name))
                mydb.commit()

                messagebox.showinfo("Item Deleted", f"Item '{item_name}' deleted from the menu.")
                window.destroy()
            else:
                messagebox.showerror("Error", "Failed to retrieve restaurant information.")

        restaurant_window = tk.Frame(root, padx=1, pady=1)
        restaurant_window.pack(padx=10, pady=10)

        label = tk.Label(restaurant_window, text="Welcome to the Restaurant Main Page!", font=("Helvetica"))
        label.pack(pady=20, side=tk.TOP)

        display_balance_sheet_button = tk.Button(restaurant_window, text="Display Balance Sheet",
                                                 command=display_daily_balance_sheet, width=20, height=5)
        display_menu_button = tk.Button(restaurant_window, text="Display Menu", command=display_restaurant_menu,
                                        width=20, height=5)
        add_item_button = tk.Button(restaurant_window, text="Add Item", command=add_item, width=20, height=5)
        delete_item_button = tk.Button(restaurant_window, text="Delete Item", command=delete_item, width=20, height=5)

        display_balance_sheet_button.pack(pady=10)
        display_menu_button.pack(pady=10)
        add_item_button.pack(pady=10)
        delete_item_button.pack(pady=10)

        home_button = tk.Button(restaurant_window, text="Home", command=lambda: go_to_home(restaurant_window))
        home_button.pack(pady=20, padx=20, side=tk.TOP)


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


def submit_review(item_name, customer_id, review_text, rating, review_window):
    # Retrieve the item ID based on the item name
    sql_cmd_get_item_id = "SELECT itemID FROM Items WHERE itemName = %s"
    mycursor.execute(sql_cmd_get_item_id, (item_name,))
    item_id = mycursor.fetchone()

    if item_id:
        item_id = item_id[0]
        # Insert the review into the Reviews table
        # Assuming you have already defined item_id, customer_id, review_text, and rating
        sql_cmd_insert_review = "INSERT INTO Reviews (itemID, customerID, reviewText, rating, date) VALUES (%s, %s, %s, %s, curdate())"
        mycursor.execute(sql_cmd_insert_review, (item_id, customer_id, review_text, rating))
        mydb.commit()

        messagebox.showinfo("Review Submitted", "Your review has been submitted successfully.")
        review_window.destroy()  # Close the review window upon submission
    else:
        messagebox.showerror("Error", "Item ID not found.")


# Function that works for opening a new window for writing a review text
def open_review_text_window(frame, item_name, customer_id):

    review_frame = tk.Frame(frame)
    review_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # Label for item name
    item_name_label = tk.Label(review_frame, text=f"Review for {item_name}:")
    item_name_label.pack(pady=10)

    # Entry widget for the review text
    review_text_entry = tk.Entry(review_frame, width=30)
    review_text_entry.pack(pady=5)

    # Rating scale
    rating_label = tk.Label(review_frame, text="Rating:")
    rating_scale = tk.Scale(review_frame, from_=0, to=5, orient=tk.HORIZONTAL)
    rating_label.pack(pady=5)
    rating_scale.pack(pady=5)

    # Button to submit the review
    submit_button = tk.Button(review_frame, text="Submit Review", command=lambda: submit_review(item_name, customer_id,
                                                                                                review_text_entry.get(),
                                                                                                rating_scale.get(),
                                                                                                review_frame))
    submit_button.pack(pady=10)


# Function that works for selecting the order
def show_selected_ordered_items(frame, ordered_items_listbox, customer_id):
    # Get the selected item from the Listbox
    selected_item_index = ordered_items_listbox.curselection()

    if selected_item_index:
        selected_item = ordered_items_listbox.get(selected_item_index)
        print(f"Selected Item: {selected_item}")

        # Open a new window for writing a review
        open_review_text_window(frame, selected_item, customer_id)

    else:
        messagebox.showwarning("No Selection", "Please select an item.")


# Function to display ordered items
def display_ordered_items(frame, items, customer_id):
    # Clear any existing widgets in the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a Listbox to display items
    ordered_items_listbox = tk.Listbox(frame, selectmode=tk.SINGLE)
    ordered_items_listbox.pack(expand=True, fill=tk.BOTH)

    # Populate the Listbox with items
    for item in items:
        ordered_items_listbox.insert(tk.END, item[0])

        # Bind the show_selected_ordered_items function to the selection event (Double Click)
        ordered_items_listbox.bind("<<ListboxSelect>>",
                                   lambda event: show_selected_ordered_items(frame, ordered_items_listbox, customer_id))


# Customer can make a review for each item also for each restaurant
def make_review_button_pressed(customer_id: int) -> None:
    review_window = tk.Toplevel(root)
    review_window.title("Review Page")
    review_window.geometry("500x500")

    make_review_frame = tk.Frame(review_window)
    make_review_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # Reach the customer's orders item "Name"
    sql_cmd = "SELECT DISTINCT OrderDetails.itemID, Items.itemName FROM Orders, OrderDetails, Items WHERE Orders.orderID = OrderDetails.orderID  AND OrderDetails.itemID = Items.itemID AND customerID = %s"
    mycursor.execute(sql_cmd, (customer_id,))
    items_name = mycursor.fetchall()

    if items_name:
        # Display ordered items for that customer
        display_ordered_items(make_review_frame, items_name, customer_id)




def customer_page(login_customer, email, password):
    restaurants = []  # Has tuples of (id, name)

    def show_selected_restaurant_items(event):
        # Clear the existing items in items_listbox
        items_listbox.delete(0, tk.END)

        # Get the selected restaurant
        selected_restaurant_id = int(restaurants_listbox.get(restaurants_listbox.curselection())[0])

        # Fetch items for the selected restaurant from the database
        sql = f"SELECT Items.itemID, Items.itemName, Items.price, Items.foodType FROM Items INNER JOIN Restaurants ON Items.restaurantID = Restaurants.restaurantID WHERE Restaurants.restaurantID = {selected_restaurant_id}"
        mycursor.execute(sql)

        # Insert fetched items into the items_listbox
        for item in mycursor.fetchall():
            items_listbox.insert(tk.END, item)

    customer_basket = []
    def add_to_basket(event):  # WORK IN PROGRESS
        selected_item = items_listbox.get(items_listbox.curselection())

        # Add the selected item to the basket
        basket_listbox.insert(tk.END, selected_item)

        # Calculate the total price in the basket
        total_price = 0.0

        # Check the structure of the tuples in basket_listbox
        basket_content = basket_listbox.get(0, tk.END)
        for item in basket_content:
            price_index = 2
            total_price += float(item[price_index])

        total_price_label.config(text=f"Total Price: ${total_price}")

    def end_purchase():
        selected_payment_option = payment_combobox.get()
        selected_items = basket_listbox.get(0, tk.END)

        # Inserting order to the database
        sql_cmd = "insert into Orders(orderDate, paymentMethod, customerID) values(CURRENT_DATE(), %s, %s)"
        mycursor.execute(sql_cmd, (selected_payment_option, customer_id))
        mydb.commit()

        messagebox.showinfo(title="Payment Info", message="Order completed")

        # Filling OrderDetails



        print(f"Selected Payment Option: {selected_payment_option}")
        print("Items in the Basket:")
        for item in selected_items:
            print(item)

    if authenticate_customer(email, password):

        login_customer.destroy()

        entrance_page.pack_forget()

        customer_frame = tk.Frame(root, padx=10, pady=10, bg="grey")
        customer_frame.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        home_button = tk.Button(customer_frame, text="Home", command=lambda: go_to_home(customer_frame))
        home_button.pack(pady=20, padx=20, side=tk.TOP)

        restaurants_list_frame = tk.Frame(customer_frame, padx=10, pady=10)
        restaurants_list_frame.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        restaurants_label = tk.Label(restaurants_list_frame, text="Restaurants", fg="red")
        restaurants_label.pack()

        # Scrollbar for the list of restaurants
        scrollbar = tk.Scrollbar(restaurants_list_frame, orient=tk.VERTICAL)

        # Listbox to display the restaurants
        restaurants_listbox = tk.Listbox(restaurants_list_frame, yscrollcommand=scrollbar.set)
        restaurants_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar to work with the Listbox
        scrollbar.config(command=restaurants_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        sql = "SELECT restaurantID, restaurantName FROM Restaurants"
        mycursor.execute(sql)

        # Get from database
        for name in mycursor.fetchall():
            restaurants.append(name)

        # Insert restaurants into the Listbox
        for restaurant in restaurants:
            restaurants_listbox.insert(tk.END, restaurant)

        # Bind the show_selected_restaurant_items function to the selection event
        restaurants_listbox.bind("<<ListboxSelect>>", show_selected_restaurant_items)

        items_list_frame = tk.Frame(customer_frame, padx=10, pady=10)
        items_list_frame.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=1)

        items_label = tk.Label(items_list_frame, text="Products", fg="red")
        items_label.pack()

        # Get customerID
        sql_cmd = f"select customerID from Customers where email = '{str(email)}' and password = '{str(password)}'"
        mycursor.execute(sql_cmd)

        customer_id = int(mycursor.fetchone()[0])

        make_review_button = tk.Button(items_list_frame, text="Make a review", command= lambda:make_review_button_pressed(customer_id))
        make_review_button.pack()

        basket_list_frame = tk.Frame(customer_frame, padx=10, pady=10)
        basket_list_frame.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=1)

        display_reviews_button = tk.Button(basket_list_frame, text="Display Reviews")  # command will be entered.
        display_reviews_button.pack()

        # Listbox to display the items
        items_listbox = tk.Listbox(items_list_frame)
        items_listbox.pack(fill=tk.BOTH, expand=True)

        # Bind the add_to_basket function to the selection event
        items_listbox.bind("<<ListboxSelect>>", add_to_basket)

        # Listbox to display the basket
        basket_listbox = tk.Listbox(basket_list_frame)
        basket_listbox.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        total_price_label = tk.Label(basket_list_frame, text="Total Price: $0")
        total_price_label.pack()

        end_purchase_button = tk.Button(basket_list_frame, text="End Purchase", command=end_purchase)
        end_purchase_button.pack(side=tk.TOP)

        # Create Combobox for payment options
        payment_options = ['Cash', 'Credit Card']
        payment_combobox = ttk.Combobox(basket_list_frame, values=payment_options)
        payment_combobox.set(payment_options[0])  # Set the default value
        payment_combobox.pack(pady=10)





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


# Carrier Main Page
def carrier_page(login_carrier, email, password):
    # Authenticate the carrier
    if authenticate_carrier(email, password):
        # Destroy the login window and show the main page
        login_carrier.destroy()

        # Destroy entrance page, so you are into the next page
        entrance_page.pack_forget()

        # Retrieve the carrier ID based on the logged-in carrier's email and password
        mycursor.execute("SELECT carrierID FROM Carriers WHERE email = %s AND password = %s", (email, password))
        carrier_info = mycursor.fetchone()

        carrier_id = carrier_info[0]

        # Initialize carrier_window
        carrier_window = tk.Frame(root, padx=1, pady=1)
        carrier_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        label = tk.Label(carrier_window, text="Welcome to the Carrier Main Page!")
        label.pack(pady=20, side=tk.TOP)

        # Function to handle the "Select Order" button click
        def select_order(order_id):
            # Get the selected order ID
            mycursor.execute("SELECT COUNT(orderID) FROM Orders WHERE carrierID IS NULL AND orderID = %s", (order_id,))
            my_tuple = mycursor.fetchone()

            if my_tuple[0] != 0:
                # Update the order with the carrier's ID
                mycursor.execute("UPDATE Orders SET carrierID = %s WHERE orderID = %s", (carrier_id, order_id))
                mydb.commit()

                # Inform the carrier about the successful selection
                messagebox.showinfo("Order Selected", f"Order {order_id} has been assigned to you.")

                # Update the UI by redisplaying the orders
                display_orders()

            else:
                # Handle the case where no order ID is entered
                messagebox.showerror("Error", "Please enter a valid Order ID.")

        # Function to display available and assigned orders
        def display_orders():
            # Retrieve available orders from the database
            mycursor.execute("SELECT orderID, orderDate, paymentMethod FROM Orders WHERE carrierID IS NULL")
            available_orders = mycursor.fetchall()

            # Retrieve assigned orders for the current carrier
            mycursor.execute("SELECT orderID, orderDate, paymentMethod FROM Orders WHERE carrierID = %s", (carrier_id,))
            assigned_orders = mycursor.fetchall()

            # Destroy existing widgets in carrier_window
            for widget in carrier_window.winfo_children():
                widget.destroy()

            # Display available orders on the left side of the carrier_window with a scrollbar
            available_orders_frame = tk.Frame(carrier_window)
            available_orders_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

            available_orders_label = tk.Label(available_orders_frame, text="Available Orders")
            available_orders_label.pack(pady=10)

            available_orders_listbox = tk.Listbox(available_orders_frame, selectmode=tk.SINGLE)
            available_orders_listbox.pack(side=tk.LEFT, pady=5, fill=tk.BOTH, expand=True)

            available_orders_scrollbar = tk.Scrollbar(available_orders_frame, orient=tk.VERTICAL,
                                                      command=available_orders_listbox.yview)
            available_orders_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            available_orders_listbox.config(yscrollcommand=available_orders_scrollbar.set)

            for order in available_orders:
                order_text = f"Order ID: {order[0]} - Date: {order[1]} - Payment Method: {order[2]}"
                available_orders_listbox.insert(tk.END, order_text)

            # Display assigned orders in the middle of the carrier_window
            assigned_orders_frame = tk.Frame(carrier_window)
            assigned_orders_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

            assigned_orders_label = tk.Label(assigned_orders_frame, text="Assigned Orders")
            assigned_orders_label.pack(pady=10)

            assigned_orders_listbox = tk.Listbox(assigned_orders_frame, selectmode=tk.SINGLE)
            assigned_orders_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

            for order in assigned_orders:
                order_text = f"Order ID: {order[0]} - Date: {order[1]} - Payment Method: {order[2]}"
                assigned_orders_listbox.insert(tk.END, order_text)

            home_button = tk.Button(carrier_window, text="Home", command=lambda: go_to_home(carrier_window), width=20,
                                    height=5)
            home_button.pack(pady=20, padx=20, side=tk.BOTTOM)

            # Display the entry widget for order ID
            selected_order_label = tk.Label(carrier_window, text="Enter Order ID:")
            selected_order_label.pack(side=tk.LEFT, padx=10, pady=10)

            selected_order_entry = tk.Entry(carrier_window)
            selected_order_entry.pack(side=tk.LEFT, padx=10, pady=10)

            # Display the "Select Order" button on the right side of the carrier_window
            select_order_button = tk.Button(carrier_window, text="Select Order",
                                            command=lambda: select_order(selected_order_entry.get()))
            select_order_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Display available orders, assigned orders, and "Select Order" button
        display_orders()

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
