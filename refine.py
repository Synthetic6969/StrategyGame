import json, math

r = 6371

def toR3(lat, long):
    return {
        "x": -math.cos(math.radians(lat)) * math.cos(math.radians(long)) * r,
        "y": math.sin(math.radians(lat)) * r,
        "z": math.cos(math.radians(lat)) * math.sin(math.radians(long)) * r
    }

def R3Magnitude(c1, c2):
    return math.sqrt( (c1["x"]-c2["x"])**2 + (c1["y"]-c2["y"])**2 + (c1["z"]-c2["z"])**2 )

def sphericalDistance(d):
    return 2*r*math.asin(d/(2*r))

def getMag(c1, c2):
    return sphericalDistance(R3Magnitude(c1, c2))

with open("cities.json") as cities_file:
    cities_raw = json.load(cities_file)
    cities_refined  = []
    
    big_cities      = {}
    medium_cities   = {}
    small_cities    = {}
    
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
                big_cities[len(big_cities)] = city
            elif city["population"] >= 500000:
                medium_cities[len(medium_cities)] = city
            else:
                small_cities[len(small_cities)] = city

    # Merge large cities which are right next to each other (for new york mainly)
    for i1 in list(big_cities):
        if not i1 in big_cities:
            continue
        city1 = big_cities[i1]
        cities_in_range = []

        for i2 in list(big_cities):
            if not i2 in big_cities:
                continue
            city2 = big_cities[i2]
            if city1 == city2:
                continue
            if city1["country"] != city2["country"]:
                continue
            mag = getMag(city1["r3_coordinates"], city2["r3_coordinates"])
            if mag < 100:
                cities_in_range.append({"magnitude": mag, "city_index": i2})

        if len(cities_in_range) > 1:
            # Get biggest near city
            nearest_big_city = cities_in_range[0]
            for x in cities_in_range:
                if x["magnitude"] < nearest_big_city["magnitude"]:
                    nearest_big_city = x
            # Sum populations
            cities_in_range.append({"magnitude": mag, "city_index": i1})
            for x in cities_in_range:
                if x["city_index"] == nearest_big_city["city_index"]:
                    continue
                c1 = big_cities[nearest_big_city["city_index"]]
                c2 = big_cities[x["city_index"]]
                print(f'MERGE (BIG): {c1["name"]} [{c1["country"]}] & {c2["name"]} [{c2["country"]}]')
                big_cities[nearest_big_city["city_index"]]["population"] += big_cities[x["city_index"]]["population"]
                del big_cities[x["city_index"]]

    # Merge medium cities which are right next to each other (for new york mainly)
    for i1 in list(medium_cities):
        if not i1 in medium_cities:
            continue
        city1 = medium_cities[i1]
        cities_in_range = []

        for i2 in list(medium_cities):
            if not i2 in medium_cities:
                continue
            city2 = medium_cities[i2]
            if city1 == city2:
                continue
            if city1["country"] != city2["country"]:
                continue
            mag = getMag(city1["r3_coordinates"], city2["r3_coordinates"])
            if mag < 100:
                cities_in_range.append({"magnitude": mag, "city_index": i2})

        if len(cities_in_range) > 1:
            # Get biggest near city
            nearest_medium_city = cities_in_range[0]
            for x in cities_in_range:
                if x["magnitude"] < nearest_medium_city["magnitude"]:
                    nearest_medium_city = x
            # Sum populations
            cities_in_range.append({"magnitude": mag, "city_index": i1})
            for x in cities_in_range:
                if x["city_index"] == nearest_medium_city["city_index"]:
                    continue
                c1 = medium_cities[nearest_medium_city["city_index"]]
                c2 = medium_cities[x["city_index"]]
                print(f'MERGE (MEDIUM): {c1["name"]} [{c1["country"]}] & {c2["name"]} [{c2["country"]}]')
                medium_cities[nearest_medium_city["city_index"]]["population"] += medium_cities[x["city_index"]]["population"]
                del medium_cities[x["city_index"]]

    # Merge small cities which are right next to each other (for new york mainly)
    for i1 in list(small_cities):
        if not i1 in small_cities:
            continue
        city1 = small_cities[i1]
        cities_in_range = []

        for i2 in list(small_cities):
            if not i2 in small_cities:
                continue
            city2 = small_cities[i2]
            if city1 == city2:
                continue
            if city1["country"] != city2["country"]:
                continue
            mag = getMag(city1["r3_coordinates"], city2["r3_coordinates"])
            if mag < 100:
                cities_in_range.append({"magnitude": mag, "city_index": i2})

        if len(cities_in_range) > 1:
            # Get biggest near city
            nearest_small_city = cities_in_range[0]
            for x in cities_in_range:
                if x["magnitude"] < nearest_small_city["magnitude"]:
                    nearest_small_city = x
            # Sum populations
            cities_in_range.append({"magnitude": mag, "city_index": i1})
            for x in cities_in_range:
                if x["city_index"] == nearest_small_city["city_index"]:
                    continue
                c1 = small_cities[nearest_small_city["city_index"]]
                c2 = small_cities[x["city_index"]]
                print(f'MERGE (SMALL): {c1["name"]} [{c1["country"]}] & {c2["name"]} [{c2["country"]}]')
                small_cities[nearest_small_city["city_index"]]["population"] += small_cities[x["city_index"]]["population"]
                del small_cities[x["city_index"]]

    # Append cities to final list before saving
    for i in small_cities:
        del small_cities[i]["r3_coordinates"]
        cities_refined.append(small_cities[i])
    for i in medium_cities:
        del medium_cities[i]["r3_coordinates"]
        cities_refined.append(medium_cities[i])
    for i in big_cities:
        del big_cities[i]["r3_coordinates"]
        cities_refined.append(big_cities[i])
    
    # Save cities to file
    with open("cities_refined.json", "w") as cities_refined_file:
        cities_refined_file.write(json.dumps(cities_refined))

    print(len(cities_raw))
    print(len(cities_refined))