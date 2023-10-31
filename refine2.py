import json, math

r = 6371

def toR3(lat, long):
    return {
        "x": -math.cos(math.radians(lat)) * math.cos(math.radians(long)) * r,
        "y": math.sin(math.radians(lat)) * r,
        "z": math.cos(math.radians(lat)) * math.sin(math.radians(long)) * r
    }

def sphericalDistance(c1, c2):
    d = math.sqrt( (c1["x"]-c2["x"])**2 + (c1["y"]-c2["y"])**2 + (c1["z"]-c2["z"])**2 )
    return 2*r*math.asin(d/(2*r))

with open("cities.json") as cities_file:
    cities_raw = json.load(cities_file)
    cities_by_country = {}
    cities = {}
    cities_refined  = []
    
    big_cities      = {}
    medium_cities   = {}
    small_cities    = {}
    
    for city_data in cities_raw:
        city = {
            'name': city_data["name"],
            'country': city_data["country_code"],
            'initial_population': city_data["population"],
            'population': city_data["population"],
            'coordinates': city_data["coordinates"],
            'r3_coordinates': toR3(city_data["coordinates"]["lat"], city_data["coordinates"]["lon"])
        }

        if city["initial_population"] >= 500:
            if city["country"] not in cities_by_country:
                cities_by_country[city["country"]] = []
            cities_by_country[city["country"]].append(city)

    for country, cities in cities_by_country.items():
        cities_by_country[country] = sorted(cities_by_country[country], key=lambda x: x["population"], reverse=True)
        dic = {}
        for i, v in enumerate(cities_by_country[country]):
            dic[i] = v
        cities_by_country[country] = dic

    # Merge cities which are right next to each other
    for country, cities in cities_by_country.items():
        for i1 in list(cities):
            if not i1 in cities:
                continue
            city1 = cities[i1]
            cities_in_range = []

            a = 7000
            b = 500000
            c = 960000
            #max_distance = a/(math.log(city1["initial_population"]+b))+c
            max_distance = a*(1/(math.log(b))-1/math.log(city1["initial_population"]+b+c))

            for i2 in list(cities):
                if i2 <= i1:
                    continue
                if not i2 in cities:
                    continue
                city2 = cities[i2]
                if city1["initial_population"] < city2["initial_population"]:
                    continue
                mag = sphericalDistance(city1["r3_coordinates"], city2["r3_coordinates"])
                if mag < max_distance:
                    cities_in_range.append({"magnitude": mag, "city_index": i2})

            if len(cities_in_range) > 1:
                # Sum populations
                for x in cities_in_range:
                    c1 = city1
                    c2 = cities[x["city_index"]]
                    print(f'MERGE (ALL): {c1["name"]} [{c1["country"]}] & {c2["name"]} [{c2["country"]}]'.ljust(50) + f'// {round(x["magnitude"], 0)}km')
                    cities[i1]["population"] += cities[x["city_index"]]["population"]
                    del cities[x["city_index"]]

        # Append cities to final list before saving
        for i in cities:
            del cities[i]["r3_coordinates"]
            del cities[i]["initial_population"]
            cities_refined.append(cities[i])
    
    # Save cities to file
    with open("cities_refined2.json", "w") as cities_refined_file:
        cities_refined_file.write(json.dumps(cities_refined))

    print(len(cities_raw))
    print(len(cities_refined))