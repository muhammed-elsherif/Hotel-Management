from functools import reduce

def get_room_types():
    return {
        1: {"type": "Single", "rate": 50},
        2: {"type": "Double", "rate": 90},
        3: {"type": "Suite", "rate": 150},
    }

def get_services():
    return {
        1: {"service": "Breakfast", "rate": 10},
        2: {"service": "Gym", "rate": 20},
        3: {"service": "Spa", "rate": 50},
    }

def calculate_room_charge(room_types, room_choice, nights):
    return room_types[room_choice]["rate"] * nights

def calculate_service_total(services, selected_services):
    return reduce(lambda total, service: total + services[service]["rate"], selected_services, 0)

def calculate_discount(subtotal, discount_rate):
    return subtotal * discount_rate

def calculate_tax(subtotal, discount, tax_rate):
    return (subtotal - discount) * tax_rate

def calculate_total(subtotal, discount, taxed_amount, promotion):
    return subtotal - discount + taxed_amount - promotion

def main():
    print("Welcome to the Hotel Management Billing System")

    # Data retrieval
    room_types = get_room_types()
    services = get_services()

    # Collect guest details
    guest_name = input("Enter guest name: ")

    # Choose room type
    print("\nRoom Types:")
    for key, value in room_types.items():
        print(f"{key}. {value['type']} - ${value['rate']} per night")

    room_choice = int(input("\nSelect a room type (1-3): "))
    nights = int(input("Enter number of nights: "))
    room_charge = calculate_room_charge(room_types, room_choice, nights)

    # Choose additional services
    print("\nAdditional Services:")
    for key, value in services.items():
        print(f"{key}. {value['service']} - ${value['rate']}")

    selected_services = []
    while True:
        add_service = input("\nDo you want to add a service? (yes/no): ").lower()
        if add_service == "yes":
            service_choice = int(input("Select a service (1-3): "))
            selected_services.append(service_choice)
        elif add_service == "no":
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    service_total = calculate_service_total(services, selected_services)

    # Collect discount, tax, and promotion details
    discount_rate = float(input("Enter discount rate (%): ")) / 100
    tax_rate = float(input("Enter tax rate (%): ")) / 100
    promotion = float(input("Enter promotion amount ($): "))

    # Calculations
    subtotal = room_charge + service_total
    discount = calculate_discount(subtotal, discount_rate)
    taxed_amount = calculate_tax(subtotal, discount, tax_rate)
    total_bill = calculate_total(subtotal, discount, taxed_amount, promotion)

    # Display bill summary
    print("\n--- Bill Summary ---")
    print(f"Guest Name: {guest_name}")
    print(f"Room Type: {room_types[room_choice]['type']}")
    print(f"Nights: {nights}")
    print(f"Room Charges: ${room_charge:.2f}")
    print(f"Additional Services Charges: ${service_total:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount: -${discount:.2f}")
    print(f"Tax: +${taxed_amount:.2f}")
    print(f"Promotion: -${promotion:.2f}")
    print(f"Total Bill: ${total_bill:.2f}")

if __name__ == "__main__":
    main()
