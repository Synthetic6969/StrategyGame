import json, math

def toR3(lat, long):
    return {
        "x": -math.cos(math.radians(lat)) * math.cos(math.radians(long)),
        "y": math.sin(math.radians(lat)),
        "z": math.cos(math.radians(lat)) * math.sin(math.radians(long))
    }

def R3Magnitude(c1, c2):
    return math.sqrt( (c1["x"]-c2["x"])**2 + (c1["y"]-c2["y"])**2 + (c1["z"]-c2["z"])**2 )

with open("cities.json") as cities_file:
    cities_raw = json.load(cities_file)
    cities_refined = []
    big_cities = []
    small_cities = []
    for city_data in cities_raw:
        city = {
            'name': city_data["name"],
            'country': city_data["country_code"],
            'population': city_data["population"],
            'coordinates': city_data["coordinates"],
            'r3_coordinates': toR3(city_data["coordinates"]["lat"], city_data["coordinates"]["lon"])
        }

        if city_data["population"] >= 500:
            if city["population"] >= 1000000:
                big_cities.append(city)
            else:
                small_cities.append(city)

    for i1, small_city in enumerate(small_cities):
        nearest_big_city = {'magnitude': 10000}
        for i2, big_city in enumerate(big_cities):
            if small_city["country"] != big_city["country"]:
                continue
            mag = R3Magnitude(small_city["r3_coordinates"], big_city["r3_coordinates"])
            if mag > 1000/6371:
                continue
            elif mag < nearest_big_city["magnitude"]:
                nearest_big_city = {"magnitude": mag, "city_index": i2}
        if nearest_big_city["magnitude"] < 1:
            big_cities[nearest_big_city["city_index"]]["population"] += small_city["population"]
            small_cities.pop(i1)

    for small_city in small_cities:
        del small_city["r3_coordinates"]
        cities_refined.append(small_city)
    for big_city in big_cities:
        del big_city["r3_coordinates"]
        cities_refined.append(big_city)
    
    with open("cities_refined.json", "w") as cities_refined_file:
        cities_refined_file.write(json.dumps(cities_refined))

    print(len(cities_raw))
    print(len(cities_refined))