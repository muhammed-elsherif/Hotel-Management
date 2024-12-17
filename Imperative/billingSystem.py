def main():
    print("Welcome to the Hotel Management Billing System")

    # Room types and rates
    room_types = {
        1: {"type": "Single", "rate": 50},
        2: {"type": "Double", "rate": 90},
        3: {"type": "Suite", "rate": 150},
    }

    # Additional services and rates
    services = {
        1: {"service": "Breakfast", "rate": 10},
        2: {"service": "Gym", "rate": 20},
        3: {"service": "Spa", "rate": 50},
    }

    # Collecting guest details
    guest_name = input("Enter guest name: ")

    # Choosing room type
    print("\nRoom Types:")
    for key, value in room_types.items():
        print(f"{key}. {value['type']} - ${value['rate']} per night")

    room_choice = int(input("\nSelect a room type (1-3): "))
    nights = int(input("Enter number of nights: "))

    room_rate = room_types[room_choice]["rate"] * nights

    # Choosing additional services
    print("\nAdditional Services:")
    for key, value in services.items():
        print(f"{key}. {value['service']} - ${value['rate']}")

    service_total = 0
    while True:
        add_service = input("\nDo you want to add a service? (yes/no): ").lower()
        if add_service == "yes":
            service_choice = int(input("Select a service (1-3): "))
            service_total += services[service_choice]["rate"]
        elif add_service == "no":
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    # Adding discounts, taxes, and promotions
    discount_rate = float(input("Enter discount rate (%): ")) / 100
    tax_rate = float(input("Enter tax rate (%): ")) / 100
    promotion = float(input("Enter promotion amount ($): "))

    # Calculating total bill
    subtotal = room_rate + service_total
    discount = subtotal * discount_rate
    taxed_amount = (subtotal - discount) * tax_rate
    total_bill = subtotal - discount + taxed_amount - promotion

    # Displaying the bill
    print("\n--- Bill Summary ---")
    print(f"Guest Name: {guest_name}")
    print(f"Room Type: {room_types[room_choice]['type']}")
    print(f"Nights: {nights}")
    print(f"Room Charges: ${room_rate:.2f}")
    print(f"Additional Services Charges: ${service_total:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount: -${discount:.2f}")
    print(f"Tax: +${taxed_amount:.2f}")
    print(f"Promotion: -${promotion:.2f}")
    print(f"Total Bill: ${total_bill:.2f}")

if __name__ == "__main__":
    main()
