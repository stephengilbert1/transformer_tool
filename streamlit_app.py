import streamlit as st

st.set_page_config(page_title="Transformer Oil Expansion Tool", layout="centered")

def convert_length_to_meters(value, unit):
    if unit == "cm":
        return value / 100
    elif unit == "in":
        return value * 0.0254
    return value

def convert_volume_to_liters(value, unit):
    if unit == "gallons":
        return value * 3.78541
    return value

def convert_height_from_meters(value, unit):
    if unit == "cm":
        return value * 100
    elif unit == "in":
        return value * 39.3701
    return value

st.title("Transformer Oil Expansion & Sensor Placement Tool")

st.markdown("This tool estimates the rise in oil level due to thermal expansion in a transformer tank and recommends a sensor placement height.")

# Unit selection
length_unit = st.selectbox("Select length unit:", ["cm", "in"])
volume_unit = st.selectbox("Select volume unit:", ["liters", "gallons"])

# Input fields
volume = st.number_input(f"Oil volume at ambient temperature ({volume_unit}):", min_value=0.0)
tank_shape = st.selectbox("Tank shape:", ["rectangular", "cylindrical"])

if tank_shape == "cylindrical":
    diameter = st.number_input(f"Tank diameter ({length_unit}):", min_value=0.0)
    length = None
    width = None
else:
    length = st.number_input(f"Tank length ({length_unit}):", min_value=0.0)
    width = st.number_input(f"Tank width ({length_unit}):", min_value=0.0)
    diameter = None

ambient_temp = st.number_input("Ambient temperature (°C)", value=25.0)
hot_temp = st.number_input("Hot temperature (°C)", value=140.0)

expansion_coeff = st.number_input(
    "Thermal expansion coefficient (per °C)",
    value=0.00075,
    format="%.6f",
    step=0.00001
)

# Set default clearance in meters based on selected unit
if length_unit == "in":
    default_clearance_m = 0.25 * 0.0254  # 0.25 in to meters
elif length_unit == "cm":
    default_clearance_m = 0.635 / 100  # 0.635 cm to meters
else:
    default_clearance_m = 0.00635  # fallback

# Convert default clearance to display unit
default_clearance_display = convert_height_from_meters(default_clearance_m, length_unit)

# Show the input field with proper format and precision
# clearance = st.number_input(
#     f"Sensor clearance above hot oil ({length_unit})",
#     value=default_clearance_display,
#     format="%.5f",
#     step=0.001
# )

# Convert user input back to meters
# clearance_m = convert_length_to_meters(clearance, length_unit)


# Submit button
if st.button("Calculate"):
        # Convert volume and dimensions to base units
    volume_liters = convert_volume_to_liters(volume, volume_unit)

    if tank_shape == "cylindrical":
        radius = convert_length_to_meters(diameter, length_unit) / 2
        cross_section_area = 3.14159 * radius ** 2
    else:
        length_m = convert_length_to_meters(length, length_unit)
        width_m = convert_length_to_meters(width, length_unit)
        cross_section_area = length_m * width_m

    delta_temp = hot_temp - ambient_temp
    expanded_volume = volume_liters * (1 + expansion_coeff * delta_temp)

    ambient_oil_height = volume_liters / 1000 / cross_section_area  # m³ → height in meters
    hot_oil_height = expanded_volume / 1000 / cross_section_area
    oil_rise = hot_oil_height - ambient_oil_height
    sensor_hole_height = hot_oil_height + default_clearance_m

    # Convert heights to chosen unit
    oil_rise_converted = convert_height_from_meters(oil_rise, length_unit)
    sensor_hole_converted = convert_height_from_meters(sensor_hole_height, length_unit)

    # Display results
    # Convert expanded volume to user's unit
    if volume_unit == "gallons":
        expanded_volume_display = expanded_volume / 3.78541
    else:
        expanded_volume_display = expanded_volume

    st.subheader("Results")
    st.write(f"Expanded oil volume: **{expanded_volume_display:.2f} {volume_unit}**")

    st.write(f"Oil rise: **{oil_rise_converted:.2f} {length_unit}**")
    #st.write(f"Recommended sensor hole center height: **{sensor_hole_converted:.2f} {length_unit}**")
