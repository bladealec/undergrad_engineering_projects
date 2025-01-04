# Battery Capacity and Safety Planner

def calculate_watt_hours(voltage, capacity):
    """
    Calculate the watt-hours of a battery pack.
    :param voltage: Voltage of the battery (V)
    :param capacity: Capacity of the battery (mAh)
    :return: Watt-hours (Wh)
    """
    return (voltage * capacity) / 1000  # Convert mAh to Ah and calculate Wh

def check_compliance(watt_hours, limit=100):
    """
    Check if the battery is compliant with FAA regulations.
    :param watt_hours: Watt-hours of the battery
    :param limit: Maximum allowable watt-hours (default 100 Wh)
    :return: Compliance status (True/False) and message
    """
    if watt_hours <= limit:
        return True, f"Compliant! The battery has {watt_hours:.2f} Wh, within the {limit} Wh limit."
    else:
        return False, f"Not Compliant! The battery has {watt_hours:.2f} Wh, exceeding the {limit} Wh limit."

def suggest_alternative(voltage, watt_hours, limit=100):
    """
    Suggest alternative configurations to meet FAA compliance.
    :param voltage: Voltage of the battery (V)
    :param watt_hours: Current watt-hours
    :param limit: Maximum allowable watt-hours (default 100 Wh)
    :return: Suggested configurations
    """
    suggested_capacity = (limit * 1000) / voltage  # Convert Ah to mAh
    return f"To comply, consider reducing the capacity to {suggested_capacity:.0f} mAh."

def main():
    print("Battery Capacity and Safety Planner")
    print("-" * 40)
    
    try:
        # Input battery specs
        voltage = float(input("Enter battery voltage (V): "))
        capacity = float(input("Enter battery capacity (mAh): "))
        
        # Calculate watt-hours
        watt_hours = calculate_watt_hours(voltage, capacity)
        
        # Check compliance
        compliant, message = check_compliance(watt_hours)
        print(message)
        
        # Suggest alternatives if not compliant
        if not compliant:
            suggestion = suggest_alternative(voltage, watt_hours)
            print(suggestion)
    except ValueError:
        print("Invalid input! Please enter numeric values for voltage and capacity.")
    
if __name__ == "__main__":
    main()
