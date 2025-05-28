def convert_length_to_meters(value, unit):
    if unit == "cm":
        return value / 100
    elif unit == "in":
        return value * 0.0254
    else:
        return value  # already in meters

def main():
    print("\n--- Transformer Oil Expansion & Sensor Placement Tool ---")
    unit_system = input("Choose length unit ('cm' or 'in'): ").strip().lower()
    volume_unit = input("Choose volume unit ('liters' or 'gallons'): ").strip().lower()

    if unit_system not in ("cm", "in"):
        print("Invalid length unit. Please choose 'cm' or 'in'.")
        return
    if volume_unit not in ("liters", "gallons"):
        print("Invalid volume unit. Please choose 'liters' or 'gallons'.")
        return

    try:
        volume = float(input(f"Enter oil volume at ambient temperature ({volume_unit}): "))
        tank_shape = input("Enter tank shape ('cylindrical' or 'rectangular'): ").strip().lower()

        if tank_shape == "cylindrical":
            diameter_raw = float(input(f"Enter tank diameter ({unit_system}): "))
            diameter = convert_length_to_meters(diameter_raw, unit_system)
            length = None
            width = None
        elif tank_shape == "rectangular":
            length_raw = float(input(f"Enter tank length ({unit_system}): "))
            width_raw = float(input(f"Enter tank width ({unit_system}): "))
            length = convert_length_to_meters(length_raw, unit_system)
            width = convert_length_to_meters(width_raw, unit_system)
            diameter = None
        else:
            print("Invalid tank shape.")
            return

        ambient_temp_input = input("Enter ambient temperature [25°C]: ")
        ambient_temp = float(ambient_temp_input) if ambient_temp_input else 25

        hot_temp_input = input("Enter hot temperature [140°C]: ")
        hot_temp = float(hot_temp_input) if hot_temp_input else 140

        coeff_input = input("Enter thermal expansion coefficient [0.00075]: ")
        coeff = float(coeff_input) if coeff_input else 0.00075

        clearance_input = input("Enter clearance above hot oil level (in meters) [0.00635]: ")
        clearance = float(clearance_input) if clearance_input else 0.00635

        print("\nInputs captured successfully. (Calculation logic comes next...)")
        # Convert gallons to liters if needed
        if volume_unit == "gallons":
            volume *= 3.78541  # US gallons to liters

        # For final output conversion (m → cm or in)
        def convert_height(meters):
            if unit_system == "cm":
                return meters * 100
            elif unit_system == "in":
                return meters * 39.3701
            else:
                return meters
         # Step 1: Compute volume expansion
        delta_temp = hot_temp - ambient_temp
        expanded_volume = volume * (1 + coeff * delta_temp)

        # Step 2: Compute cross-sectional area
        if tank_shape == "cylindrical":
            radius = diameter / 2
            cross_section_area = 3.14159 * radius ** 2  # m²
        else:  # rectangular
            cross_section_area = length * width  # m²

        # Step 3: Compute hot oil level
        hot_oil_height = expanded_volume / 1000 / cross_section_area  # convert L → m³
        ambient_oil_height = volume / 1000 / cross_section_area  # m³ → height in meters
        oil_rise = hot_oil_height - ambient_oil_height
        # Step 4: Add clearance for sensor hole center
        sensor_hole_height = hot_oil_height + clearance

        # Step 5: Display results
        print(f"\nExpanded oil volume at {hot_temp}°C: {expanded_volume:.2f} liters")
        print(f"Oil rise from {ambient_temp}°C to {hot_temp}°C: {convert_height(oil_rise):.2f} {unit_system}")

    except ValueError:
        print("❗ Invalid input. Please enter numerical values where required.")

if __name__ == "__main__":
    main()