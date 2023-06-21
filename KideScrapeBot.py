from dependencies.selenium import webdriver
from dependencies.selenium.webdriver.support.ui import Select
from dependencies.bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import os

# Global variables for event_var, quantity_entry, and ticket_type_var
event_var = None
quantity_entry = None
ticket_type_var = None
CHROME_DRIVER_PATH = 'C:/Projects/kideScrapeBot/chromedriver.exe'
ticket_type_label = None

def get_event_names():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Set the PATH environment variable
    os.environ['PATH'] += os.pathsep + 'C:/Projects/kideScrapeBot'

    # Create the WebDriver instance
    driver = webdriver.Chrome(options=options)

    driver.get('https://kide.app/events')
    # Wait for the page to load
    time.sleep(5)

    # Extract event names from the HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    event_links = soup.find_all('a', class_='o-tile o-tile--clickable o-tile--shadow o-margin-bottom--sm')
    event_names = [link.text.strip() for link in event_links]

    # Quit the driver
    driver.quit()

    return event_names

def get_ticket_types(event_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome()

    driver.get(event_url)
    # Wait for the page to load
    time.sleep(5)

    # Extract ticket types from the HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ticket_types_elements = soup.find_all('div', class_='o-item o-align-items--flex-start')

    ticket_types = []
    for ticket_type in ticket_types_elements:
        name_element = ticket_type.find(class_='o-text__heading')
        price_element = ticket_type.find(class_='o-chip o-chip--sm o-color--validation-success')

        if name_element and price_element:  # Check if elements exist before extracting text
            name = name_element.text.strip()
            price = price_element.text.strip()
            ticket_types.append({'name': name, 'price': price})

    # Quit the driver
    driver.quit()

    return ticket_types


def update_ticket_types():
    global ticket_type_dropdown, ticket_type_var

    event_url = event_var.get()
    ticket_types = get_ticket_types(event_url)

    # Clear the previous options
    ticket_type_dropdown['menu'].delete(0, 'end')

    # Add the new ticket types as options
    if ticket_types:
        for ticket_type in ticket_types:
            ticket_type_dropdown['menu'].add_command(
                label=f"{ticket_type['name']} - {ticket_type['price']}",
                command=lambda type=ticket_type: ticket_type_var.set(type['name'])
            )

        # Set the default selected ticket type
        ticket_type_var.set(ticket_types[0]['name'])
    else:
        print("No ticket types available")

def buy_ticket():
    event_url = event_var.get()
    num_tickets = int(quantity_entry.get())
    ticket_type = ticket_type_var.get()

    # Initialize the WebDriver (replace 'path_to_chromedriver' with the actual path)
    driver = webdriver.Chrome('C:/Projects/kideScrapeBot/chromedriver.exe')

def start_bot():
    Thread(target=buy_ticket).start()

def create_ui():
    global event_var, quantity_entry, ticket_type_dropdown, ticket_type_var

    # Create the main window
    root = tk.Tk()

    # Set the window title
    root.title('Kide Scrape Bot')

    global ticket_type_label
    ticket_type_label = tk.Label(root, text='Ticket Type:')
    ticket_type_label.pack()

    # Create and pack the event URL entry widget
    url_label = tk.Label(root, text='Event URL:')
    url_label.pack()

    event_var = tk.StringVar()
    url_entry = tk.Entry(root, textvariable=event_var)
    url_entry.pack()

    # Create and pack the quantity entry widget
    quantity_label = tk.Label(root, text='Quantity:')
    quantity_label.pack()

    # Create the ticket type dropdown menu
    ticket_type_label = tk.Label(root, text='Ticket Type:')
    ticket_type_label.pack()

    ticket_type_var = tk.StringVar(root)

    ticket_type_dropdown = ttk.OptionMenu(root, ticket_type_var, ())
    ticket_type_dropdown.pack()

    # Create and pack the Next button
    next_button = tk.Button(root, text='Next', command=show_dropdown)
    next_button.pack()

    # Create and pack the Buy button
    buy_button = tk.Button(root, text='Buy Ticket', command=start_bot)
    buy_button.pack()

    # Start the Tkinter event loop
    root.mainloop()

def show_dropdown():
    global event_var, ticket_type_label, ticket_type_dropdown

    event_url = event_var.get()

    # Run the update_ticket_types() function in a separate thread
    Thread(target=update_ticket_types).start()

    ticket_type_label.pack()
    ticket_type_dropdown.pack()

# Run the UI
create_ui()
