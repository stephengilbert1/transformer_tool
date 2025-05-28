# Transformer Oil Expansion & Sensor Placement Tool

This CLI tool helps transformer designers and engineers determine the correct mounting height for an IFD sensor, based on thermal expansion of insulating oil inside a transformer tank.

It supports cylindrical and rectangular tanks, unit selection (liters/gallons, cm/inches), and calculates oil rise from ambient to high temperature. The result includes the vertical oil rise and the recommended sensor clearance height.

## 💡 Problem Context

Distribution transformers are partially filled with insulating oil. As the oil heats up, it expands, and its level rises inside the tank. IFD sensors must be installed at least 0.25 inches above the oil level at 140°C. Transformer manufacturers often design around ambient temperatures (20°C or 25°C), so this tool helps calculate how much the oil level rises and where the sensor should be placed.

## ✅ Features

- Supports **rectangular or cylindrical** tank shapes
- Allows input in **inches or cm**, and **liters or gallons**
- Uses a default thermal expansion coefficient (`0.00075`) — editable
- Outputs:
  - Expanded oil volume at high temperature
  - Vertical **oil rise**
  - Recommended **sensor hole center height**
- Clean CLI experience with defaults and error handling

## 📥 Inputs

- Ambient oil volume
- Tank shape + dimensions
- Temperature range (ambient to hot)
- Optional: expansion coefficient, sensor clearance
- Unit selection (length and volume)

## 📤 Outputs

- Expanded volume (liters)
- Oil rise (cm or inches)
- Recommended sensor placement height

## 🛠️ Usage

```bash
python transformer_tool.py
