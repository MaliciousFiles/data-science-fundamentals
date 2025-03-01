data = {}
# {year: {month: {zipcode: {class: int}, wastewater: int, water: int, temp_max: int, temp_min: int, humidity: int, precipitation: int}, population: int}}

with open("Commercial Consumption.csv") as f1:
    with open("Residential Consumption.csv") as f2:
        for line in f1.read().split("\n")[1:] + f2.read().split("\n")[1:]:
            if not line: continue
            line = line.split(",")

            year = line[0][:-2]
            month = line[0][-2:]
            zipcode = line[1]
            clss = line[2]
            gallons = float(line[3])

            if year not in data:
                data[year] = {}
            if month not in data[year]:
                data[year][month] = {}
            if zipcode not in data[year][month]:
                data[year][month][zipcode] = {}
            if clss not in data[year][month][zipcode]:
                data[year][month][zipcode][clss] = 0
            data[year][month][zipcode][clss] += gallons

with open("Population.csv") as f:
    for line in f.read().split("\n")[1:]:
        if not line: continue
        line = line.split(",")

        year = line[0]
        pop = int(line[4])

        if year in data: data[year]['population'] = pop

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
with open("W+WW Treated.csv") as f:
    for line in f.read().split("\n")[1:]:
        if not line: continue
        line = line.split(",")
        if not line[4]: continue

        year = line[0]
        month = str(MONTHS.index(line[1])).rjust(2, '0')
        water_type = line[3].lower()
        gallons = float(line[4])*1_000_000

        if year not in data or month not in data[year]: continue
        if water_type not in data[year][month]:
            data[year][month][water_type] = 0
        data[year][month][water_type] += gallons

curYear = ""
curMonth = ""
curTempMax = []
curTempMin = []
curHumidity = []
curPrecip = []
with open("Weather.csv") as f:
    for line in f.read().split("\n")[1:]:
        if not line: continue
        line = line.split(",")

        year = line[1].split("-")[0]
        month = line[1].split("-")[1]
        if year not in data or month not in data[year]: continue

        if year != curYear or month != curMonth:
            if curYear:
                data[curYear][curMonth]['temp_max'] = sum(curTempMax)/len(curTempMax)
                data[curYear][curMonth]['temp_min'] = sum(curTempMin)/len(curTempMin)
                data[curYear][curMonth]['humidity'] = sum(curHumidity)/len(curHumidity)
                data[curYear][curMonth]['precipitation'] = sum(curPrecip)/len(curPrecip)

            curYear = year
            curMonth = month
            curTempMax = []
            curTempMin = []
            curHumidity = []
            curPrecip = []

        curTempMax.append(float(line[2]))
        curTempMin.append(float(line[3]))
        curHumidity.append(float(line[9]))
        curPrecip.append(float(line[10] or "0"))

data_str = "year,month,zipcode,class,gallons,wastewater,water,temp_max,temp_min,humidity,precipitation,population\n"
for year in data:
    population = data[year]['population']
    for month in data[year]:
        if month == 'population': continue

        wastewater = data[year][month]['wastewater'] if 'wastewater' in data[year][month] else ''
        water = data[year][month]['water'] if 'water' in data[year][month] else ''
        temp_max = data[year][month]['temp_max'] if 'temp_max' in data[year][month] else ''
        temp_min = data[year][month]['temp_min'] if 'temp_min' in data[year][month] else ''
        humidity = data[year][month]['humidity'] if 'humidity' in data[year][month] else ''
        precipitation = data[year][month]['precipitation'] if 'precipitation' in data[year][month] else ''

        for zipcode in data[year][month]:
            if zipcode in ['wastewater', 'water', 'temp_max', 'temp_min', 'humidity', 'precipitation']: continue
            for clss in data[year][month][zipcode]:
                data_str += f"{year},{month},{zipcode},{clss},{data[year][month][zipcode][clss]},{wastewater},{water},{temp_max},{temp_min},{humidity},{precipitation},{population}\n"

with open("proj7_data.csv", "w") as f:
    f.write(data_str)