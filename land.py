import os
from datetime import datetime

INVOICES_DIR = "invoices"
FINE_PER_MONTH = 500  # Fine amount per month if rental duration exceeds the threshold

def load_lands():
    lands = []
    with open("lands.txt", "r") as file:
        for line in file:
            land_info = line.strip().split(",")
            land = {
                "kitta_number": land_info[0],
                "city": land_info[1],
                "direction": land_info[2],
                "price": int(land_info[3]),
                "availability": land_info[4]
            }
            lands.append(land)
    return lands

def save_lands(lands):
    with open("lands.txt", "w") as file:
        for land in lands:
            file.write(f"{land['kitta_number']},{land['city']},{land['direction']},{land['price']},{land['availability']}\n")

def display_available_lands(lands):
    print("\nAvailable Lands:")
    print("{:<15} {:<15} {:<10} {:<10} {:<15}".format("Kitta Number", "City", "Direction", "Price", "Availability"))
    for land in lands:
        if land["availability"] == "Available":
            print("{:<15} {:<15} {:<10} {:<10} {:<15}".format(land["kitta_number"], land["city"], land["direction"], f"Rs. {land['price']}", land["availability"]))

def generate_invoice(customer_name, customer_email, customer_phone, land, duration_months, total_amount, action):
    if not os.path.exists(INVOICES_DIR):
        os.makedirs(INVOICES_DIR)
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    invoice_file = os.path.join(INVOICES_DIR, f"{customer_name}_{action}_{now}.txt")
    with open(invoice_file, "w") as file:
        file.write("===============================================\n")
        file.write("            TechnoPropertyNepal\n")
        file.write("            Land Rental Invoice\n")
        file.write("===============================================\n\n")
        file.write(f"Customer Name: {customer_name}\n")
        file.write(f"Customer Email: {customer_email}\n")
        file.write(f"Customer Phone: {customer_phone}\n")
        file.write(f"Kitta Number: {land['kitta_number']}\n")
        file.write(f"City/District: {land['city']}\n")
        file.write(f"Land Faced: {land['direction']}\n")
        file.write(f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Duration of Rent: {duration_months} months\n")
        file.write(f"Total Amount: Rs. {total_amount}\n")

def rent_land(lands):
    display_available_lands(lands)
    choice = input("\nEnter the number of the land you want to rent: ")
    land = next((l for l in lands if l["kitta_number"] == choice), None)
    if land:
        if land["availability"] == "Available":
            duration_months = input("Enter the duration of rent (in months): ")
            if duration_months and duration_months.isdigit():
                duration_months = int(duration_months)
                customer_name = input("Enter your name: ")
                customer_email = input("Enter your email: ")
                customer_phone = input("Enter your phone number: ")
                if customer_name and customer_email and customer_phone:
                    total_amount = land["price"] * duration_months
                    land["availability"] = "Not Available"
                    generate_invoice(customer_name, customer_email, customer_phone, land, duration_months, total_amount, action="Rent")
                    print("\nInvoice generated successfully!")
                    print("Land rented successfully!")
                    save_lands(lands)
                    rent_again = input("Do you want to rent another land? (yes/no): ")
                    if rent_again.lower() == "yes":
                        rent_land(lands)
                else:
                    print("\nCustomer name, email, and phone number cannot be empty.")
            else:
                print("\nInvalid input for duration. Please enter a valid numerical value.")
        else:
            print("\nThis land is not available for rent.")
            print("\nYou cannot rent this land at the moment.")
    else:
        print("\nInvalid choice.")

def return_land(lands):
    rented_lands = [land for land in lands if land["availability"] == "Not Available"]
    if not rented_lands:
        print("\nNo lands are currently rented.")
        return
    
    print("\nRented Lands:")
    print("{:<15} {:<15} {:<10} {:<10}".format("Kitta Number", "City", "Direction", "Availability"))
    for land in rented_lands:
        print("{:<15} {:<15} {:<10} {:<10}".format(land["kitta_number"], land["city"], land["direction"], land["availability"]))

    choice = input("\nEnter the number of the land you want to return: ")
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(rented_lands):
            land = rented_lands[choice - 1]
            duration_months = input("Enter the duration of rent (in months): ")
            if duration_months and duration_months.isdigit():
                duration_months = int(duration_months)
                customer_name = input("Enter your name: ")
                customer_email = input("Enter your email: ")
                customer_phone = input("Enter your phone number: ")
                if customer_name and customer_email and customer_phone:
                    total_amount = land["price"] * duration_months
                    if duration_months > 3:  # Check if duration exceeds the specified number of months
                        fine = (duration_months - 3) * FINE_PER_MONTH  # Apply fine
                        total_amount += fine
                        print(f"Fine applied: Rs. {fine}")
                    land["availability"] = "Available"
                    generate_invoice(customer_name, customer_email, customer_phone, land, duration_months, total_amount, action="Return")
                    print("\nInvoice generated successfully!")
                    print("Land returned successfully!")
                    save_lands(lands)
                else:
                    print("\nCustomer name, email, and phone number cannot be empty.")
            else:
                print("\nInvalid input for duration. Please enter a valid numerical value.")
        else:
            print("\nInvalid choice")

def main():
    lands = load_lands()

    print("\n===============================================")
    print("          Welcome to TechnoPropertyNepal")
    print("          Land Rental System")
    print("===============================================\n")

    while True:
        print("\nMenu:")
        print("1. Rent Land")
        print("2. Return Land")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            rent_land(lands)
        elif choice == "2":
            return_land(lands)
        elif choice == "3":
            print("\nThank you for using the Land Rental System. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
