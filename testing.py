import streamlit as st
import pandas as pd
import requests
import base64
import random
#Emoji shower
from streamlit_extras.let_it_rain import rain
#Offset button
from offsetbutton import carbon_offset_button
#Cap's disntace calculation
from distancecalculate import haversine_distance
#Tree image
from treecode import display_tree_images


# Load the airport codes CSV file
airport_data = pd.read_csv("airport-codes.csv")

from apigetting import(
    get_carbon_emissions_flight,
    get_carbon_emissions_vehicles,
    get_train_carbon_emissions,
    get_vehicle_makes,
    get_vehicle_models
)

def flight_calculate_page():
    st.title('Flight Results')

    def flightemoji():
        rain(
            emoji="✈️",
            font_size=54,
            falling_speed=3,
            animation_length="5s",
        )
    flightemoji()

    results = st.session_state.results

    if results:
        # Display flight results
        st.write('Departure Airport:', results.get('departure_airport'))
        st.write('Destination Airport:', results.get('destination_airport'))
        st.write('Carbon Emitted (kg):', results['carbon_emissions'])

        # Calculate number of trees needed to offset CO2 emissions
        co2_emissions = results['carbon_emissions']
        trees_needed = round(co2_emissions / 21.77)
        st.write(f'{trees_needed} trees to offset {co2_emissions} kilograms of CO2.')

        # Calculate and display distance
        st.write('Distance (km):', round(results['distance_km'], 2))

        display_tree_images(trees_needed)

    else:
        st.error("No results available. Please calculate CO2 emissions first.")

    # Display the custom HTML button for offsetting carbon footprint
    button_html = carbon_offset_button()
    st.markdown(button_html, unsafe_allow_html=True)

    # Add return to homepage button
    if st.button('Return to Homepage'):
        st.session_state.page = "Home"

def vehicle_calculate_page():
    st.title('Vehicle Results')
    def caremoji():
        rain(
            emoji="🚗",
            font_size=54,
            falling_speed=3,
            animation_length="5s",
        )
    caremoji()
    # Retrieve results from session state
    results = st.session_state.results

    if results:
        # Display vehicle results
        st.write('Distance:', results.get('distance_value', 'Unknown'), results.get('distance_unit', 'Unknown'))
        st.write('Estimated CO2 Emission (kg):', results.get('carbon_emissions', 'Unknown'))

        # Calculate number of trees needed to offset CO2 emissions
        co2_emissions = results['carbon_emissions']
        trees_needed = round(co2_emissions / 21.77)
        st.write(f'{trees_needed} trees to offset {co2_emissions} kilograms of CO2.')

        # Display tree image corresponding to the number of trees
    display_tree_images(trees_needed)


    # Display the custom HTML button for offsetting carbon footprint
    button_html = carbon_offset_button()
    st.markdown(button_html, unsafe_allow_html=True)

    # Add return to homepage button
    if st.button('Return to Homepage'):
        st.session_state.page = "Home"

def train_calculate_page():
    st.title('Train Results')
    def trainemoji():
        rain(
            emoji="🚂",
            font_size=54,
            falling_speed=3,
            animation_length="5s",
        )
    trainemoji()

    distance_km = st.session_state.train_distance_km

    if distance_km:
        # Call the estimates API for train emissions
        carbon_emissions = get_train_carbon_emissions(distance_km)

        # Calculate number of trees needed to offset CO2 emissions
        trees_needed = round(carbon_emissions / 21.77)

        # Display train results
        st.write("Distance:", distance_km, "km")
        st.write('Estimated CO2 Emission (kg):', carbon_emissions)
        st.write(f'{trees_needed} trees to offset {carbon_emissions} kilograms of CO2.')

    display_tree_images(trees_needed)

    # Display the custom HTML button for offsetting carbon footprint
    button_html = carbon_offset_button()
    st.markdown(button_html, unsafe_allow_html=True)

    # Add return to homepage button
    if st.button('Return to Homepage'):
        st.session_state.page = "Home"

def home_page():
    st.title("Wie nachhaltig sind Ihre Reisen?")
    st.text("Curious about the environmental impact of your transportation choices?\nOur site visualizes the carbon emissions of different modes of travel, \nhelping you make more informed and eco-friendly decisions.\nJoin us in exploring sustainable transportation options for a greener future!.")
    # add a description of project and maybe a picture

    st.subheader("Which method of transport will you be taking?")
    selected_page = st.selectbox("Select Transport Mode", ("Plane", "Train", "Vehicle"))

    if selected_page == 'Plane':
            ### gif from local file
        file_path = "flightgif.gif"
        file_ = open(file_path,"rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        width = 200

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="flight gif" width="{width}">',
            unsafe_allow_html=True,
        )
        st.subheader("Where are you going on this trip?")
        # Dropdown for selecting departure airport
        departure_airport = st.selectbox('Select Departure Airport', airport_data['iata_code'])

        # Dropdown for selecting destination airport
        destination_airport = st.selectbox('Select Destination Airport', airport_data['iata_code'])

        # add with vehicle/train?

        if st.button('Calculate your CO2 Emission'):
            # Calculate carbon emissions
            carbon_emissions = get_carbon_emissions_flight(departure_airport, destination_airport)

            # Get departure and destination coordinates
            departure_coords = airport_data.loc[airport_data['iata_code'] == departure_airport, 'coordinates'].iloc[0].split(',')
            destination_coords = airport_data.loc[airport_data['iata_code'] == destination_airport, 'coordinates'].iloc[0].split(',')

            departure_lat, departure_lon = map(float, departure_coords)
            destination_lat, destination_lon = map(float, destination_coords)

            # Calculate distance in kilometers
            distance_km = haversine_distance(departure_lat, departure_lon, destination_lat, destination_lon)

            # Store results in session state
            st.session_state.results = {
                'departure_airport': departure_airport,
                'destination_airport': destination_airport,
                'carbon_emissions': carbon_emissions,
                'distance_km': distance_km
            }
            # Redirect to the results page
            st.session_state.page = "Flight Results"

    elif selected_page == 'Train':
        file_path = "traingif.gif"
        file_ = open(file_path,"rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        width = 200

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="train gif" width="{width}">',
            unsafe_allow_html=True,
        )
        # Retrieve distance input from the user
        distance_km = st.number_input('Distance (in kilometers)', value=500.0)
        st.session_state.train_distance_km = distance_km  # Store distance in session state

        if st.button('Calculate CO2 Emission'):
            # Call the function to calculate train emissions
            carbon_emissions = get_train_carbon_emissions(distance_km)

            # Store the calculated emissions and distance in session state
            st.session_state.results = {
                'distance_km': distance_km,
                'carbon_emissions': carbon_emissions
            }
            # Navigate to the train results page
            st.session_state.page = "Train Results"


    elif selected_page == 'Vehicle':
        file_path = "cargif.gif"
        file_ = open(file_path, "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        width = 200

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="car gif" width="{width}">',
            unsafe_allow_html=True,
        )
        st.subheader("Enter vehicle details:")
        # Always show distance unit as kilometers
        distance_unit = 'km'  # or 'km', depending on your preference
        distance_value = st.number_input('Distance Value (in km)', value=100.0)

        # Fetch the vehicle makes
        vehicle_makes = get_vehicle_makes()
        selected_make = st.selectbox('Select Vehicle Make', list(vehicle_makes.keys()))

        vehicle_models = get_vehicle_models(vehicle_makes, selected_make)
        selected_model = st.selectbox('Select Vehicle Model', list(vehicle_models.keys()))

        if st.button('Calculate your CO2 Emission'):
            # Get the vehicle model ID
            vehicle_model_id = vehicle_models[selected_model]

            # Calculate CO2 emissions for vehicle and get car type
            carbon_emissions, car_type = get_carbon_emissions_vehicles(distance_unit, distance_value, vehicle_model_id)

            # Store results in session state
            st.session_state.results = {
                'distance_value': distance_value,
                'distance_unit': distance_unit,
                'carbon_emissions': carbon_emissions,
                'car_type': car_type
            }
            st.session_state.page = "Vehicle Results"

def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Flight Results":
        flight_calculate_page()
    elif st.session_state.page == "Vehicle Results":
        vehicle_calculate_page()
    elif st.session_state.page == "Train Results":
        train_calculate_page()

if __name__ == "__main__":
    main()