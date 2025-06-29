import streamlit as st

def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9

def celsius_to_kelvin(c):
    return c + 273.15

def kelvin_to_celsius(k):
    return k - 273.15

def convert_temperature(temp, input_scale):
    if input_scale == "Celsius":
        f = celsius_to_fahrenheit(temp)
        k = celsius_to_kelvin(temp)
        return f, k
    elif input_scale == "Fahrenheit":
        c = fahrenheit_to_celsius(temp)
        k = celsius_to_kelvin(c)
        return c, k
    elif input_scale == "Kelvin":
        c = kelvin_to_celsius(temp)
        f = celsius_to_fahrenheit(c)
        return c, f

def main():
    st.title("🌡️ Temperature Conversion Program")
    st.write("Convert temperatures between Celsius, Fahrenheit, and Kelvin scales.")
    
    # Input section
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.number_input("Enter temperature value:", value=25.0)
    with col2:
        scale = st.selectbox("Select temperature scale:", 
                           ["Celsius", "Fahrenheit", "Kelvin"])
    
    # Conversion and output
    if st.button("Convert"):
        if scale == "Celsius":
            fahrenheit, kelvin = convert_temperature(temperature, scale)
            st.success(f"**Converted Temperatures:**")
            st.info(f"Fahrenheit: {fahrenheit:.2f} °F")
            st.info(f"Kelvin: {kelvin:.2f} K")
        elif scale == "Fahrenheit":
            celsius, kelvin = convert_temperature(temperature, scale)
            st.success(f"**Converted Temperatures:**")
            st.info(f"Celsius: {celsius:.2f} °C")
            st.info(f"Kelvin: {kelvin:.2f} K")
        elif scale == "Kelvin":
            celsius, fahrenheit = convert_temperature(temperature, scale)
            st.success(f"**Converted Temperatures:**")
            st.info(f"Celsius: {celsius:.2f} °C")
            st.info(f"Fahrenheit: {fahrenheit:.2f} °F")

if __name__ == "__main__":
    main()