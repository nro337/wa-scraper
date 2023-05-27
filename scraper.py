from bs4 import BeautifulSoup
import csv
import requests
URL = "https://worldathletics.org/athletes/norway/jakob-ingebrigtsen-14653717"
r = requests.get(URL)

# print(r.content)

soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

first_name:str = soup.find_all("span", {"class": lambda value: value and value.startswith("profileBasicInfo_firstName")})[0].contents[0]
last_name:str = soup.find_all("span", {"class": lambda value: value and value.startswith("profileBasicInfo_lastName")})[0].contents[0].title()
basic_details = soup.find_all("div", {"class": lambda value: value and value.startswith("profileBasicInfo_statValue")})
country:str = basic_details[0].contents[0]
dob_str:str = basic_details[1].contents[0]
athlete_code:str = basic_details[2].contents[0]
athlete_image_url:str = f'https://media.aws.iaaf.org/athletes/{athlete_code}.jpg'
age:int = int(basic_details[3].contents[0])
print(athlete_image_url)


header = ['Athlete Code', 'first name', 'last name', 'Date of Birth', 'Country', 'Image URL', 'Age']
data = [athlete_code, first_name, last_name, dob_str, country, athlete_image_url, age]

with open('./data/athlete-stats.csv', 'a', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    # writer.writerow(header)

    # write the data
    writer.writerow(data)

