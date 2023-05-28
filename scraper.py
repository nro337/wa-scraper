from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests

driver = Chrome(executable_path='/Users/alico/Documents/chromedriver_mac_arm64/chromedriver')
URL = "https://worldathletics.org/athletes/norway/jakob-ingebrigtsen-14653717"
driver.get(URL)

# print(r.content)

# Accept cookies
element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="c-right"]'))
WebDriverWait(driver=driver, timeout=20).until(element_present)
driver.find_element(By.XPATH, '//*[@id="c-right"]').click()

soup = BeautifulSoup(driver.page_source, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib

first_name:str = soup.find_all("span", {"class": lambda value: value and value.startswith("profileBasicInfo_firstName")})[0].contents[0]
last_name:str = soup.find_all("span", {"class": lambda value: value and value.startswith("profileBasicInfo_lastName")})[0].contents[0].title()
basic_details = soup.find_all("div", {"class": lambda value: value and value.startswith("profileBasicInfo_statValue")})
country:str = basic_details[0].contents[0]
dob_str:str = basic_details[1].contents[0]
athlete_code:str = basic_details[2].contents[0]
athlete_image_url:str = f'https://media.aws.iaaf.org/athletes/{athlete_code}.jpg'
age:int = int(basic_details[3].contents[0])

# Switch to personal bests tab
pb_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[5]/div/div[1]/ul/li[2]/div')
pb_button.click()


table_present = EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/table/thead/tr/th[1]'))
WebDriverWait(driver=driver, timeout=20).until(table_present)
thead = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/table/thead/tr/th[1]')[0].find_element(By.XPATH, '..').find_element(By.XPATH, '..')
tbody = thead.find_elements(By.XPATH, './following-sibling::tbody')[0]

arr = []
tr_array = tbody.find_elements(By.XPATH, './child::*')
for tr in tr_array:
    td_array = tr.find_elements(By.XPATH, './child::*')
    for td in tr_array:
        line = td.text.split(' ')
        # print(line)
        distance:str = f'{line[0]} {line[1]}'
        time:str = ''
        location:str = ''
        date_str:str = ''
        records_arr:list[str] = []
        if line[2][0].isdigit():
          time = f'{line[2]}'
          if line[5][0].isdigit():
             location = f'{line[3]} {line[4]}'
             date_str = f'{line[5]} {line[6]} {line[7]}'
             if not line[8].isdigit():
                records_arr.append(line[8])
             if len(line) == 9:
                continue
             if not line[9].isdigit():
                records_arr.append(line[9])
             
          elif line[6][0].isdigit():
             location = f'{line[3]} {line[4]} {line[5]}'
             date_str = f'{line[6]} {line[7]} {line[8]}'
          elif line[7][0].isdigit():
             location = f'{line[4]} {line[5]} {line[6]}'
             date_str = f'{line[7]} {line[8]} {line[9]}'
          else:
             location = f'{line[5]} {line[6]} {line[7]}'
             date_str = f'{line[8]} {line[9]} {line[10]}'
          print(distance, time, location, date_str, records_arr)
          
        elif line[3][0].isdigit():
           distance += f' {line[2]}'
           time = f'{line[3]}'
           if line[6][0].isdigit():
              location = f'{line[4]} {line[5]}'
              date_str = f'{line[6]} {line[7]} {line[8]}'
           else:
              location = f'{line[4]} {line[5]} {line[6]}'
              date_str = f'{line[7]} {line[8]} {line[9]}'
           print(distance, time, location, date_str, records_arr)

        elif line[4][0].isdigit():
           distance += f' {line[3]}'
           time = f'{line[4]}'
           location = f'{line[5]} {line[6]} {line[7]}'
           print(distance, time, location)

        elif line[5][0].isdigit():
           distance += f' {line[4]}'
           time = f'{line[5]}'
           location = f'{line[6]} {line[7]} {line[8]}'
           print(distance, time, location, date_str, records_arr)
           
        else:
           print(line)
          #  distance += f' {line[3]}'
          #  time = f'{line[4]}'
          #  location = line[5]
          #  print(distance, time, location)
           
        # print(distance, time)
        # arr.append([td.text])
    break
# print(arr)



# header = ['Athlete Code', 'first name', 'last name', 'Date of Birth', 'Country', 'Image URL', 'Age']
# data = [athlete_code, first_name, last_name, dob_str, country, athlete_image_url, age]

# with open('./data/athlete-stats.csv', 'a', encoding='UTF8') as f:
#     writer = csv.writer(f)

#     # write the header
#     # writer.writerow(header)

#     # write the data
#     writer.writerow(data)

