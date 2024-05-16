import requests

def get_carbon_emissions_flight(departure, destination):
    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
        "Authorization": "Bearer IIEaBrVaxGPN1GGQW59RxA",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "flight",
        "legs": [{
            "departure_airport": departure,
            "destination_airport": destination
        }],
        "distance_unit": "km"  # Default distance unit to kilometers
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        data = response.json()
        return data['data']['attributes']['carbon_kg']
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

def get_carbon_emissions_vehicles(distance_unit, distance_value, vehicle_model_id):
    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
        "Authorization": "Bearer IIEaBrVaxGPN1GGQW59RxA",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "vehicle",
        "distance_unit": distance_unit,
        "distance_value": distance_value,
        "vehicle_model_id": vehicle_model_id
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        data = response.json()
        attributes = data['data']['attributes']
        carbon_emissions = attributes['carbon_kg']
        car_type = f"{attributes['vehicle_make']} {attributes['vehicle_model']} ({attributes['vehicle_year']})"
        return carbon_emissions, car_type
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

def get_train_carbon_emissions(distance_km):
    url = "https://www.carboninterface.com/api/v1/estimates"
    headers = {
        "Authorization": "Bearer IIEaBrVaxGPN1GGQW59RxA",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "shipping",
        "weight_value": 75,
        "weight_unit": "kg",
        "distance_unit": "km",
        "distance_value": distance_km,
        "transport_method":"train"
        
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        data = response.json()
        attributes = data['data']['attributes']
        carbon_emissions = attributes['carbon_kg']
        return carbon_emissions
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

def get_vehicle_makes():
    url = "https://www.carboninterface.com/api/v1/vehicle_makes"
    headers = {
        "Authorization": "Bearer IIEaBrVaxGPN1GGQW59RxA",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        vehicle_makes_data = response.json()
        vehicle_makes = {make['data']['attributes']['name']: make['data']['id'] for make in vehicle_makes_data}
        return vehicle_makes
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}

def get_vehicle_models(vehicle_makes, selected_make):
    # Fetch the vehicle models based on the selected make
    url = f"https://www.carboninterface.com/api/v1/vehicle_makes/{vehicle_makes[selected_make]}/vehicle_models"
    headers = {
        "Authorization": "Bearer IIEaBrVaxGPN1GGQW59RxA",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        vehicle_models_data = response.json()
        vehicle_models = {model['data']['attributes']['name']: model['data']['id'] for model in vehicle_models_data}
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        vehicle_models = {}
    return vehicle_models
