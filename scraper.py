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
print(athlete_image_url)

# Switch to personal bests tab
pb_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div[5]/div/div[1]/ul/li[2]/div')
pb_button.click()


table_present = EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/table/thead/tr/th[1]'))
WebDriverWait(driver=driver, timeout=20).until(table_present)
thead = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[5]/div/div[2]/div/div[2]/div[2]/div[1]/table/thead/tr/th[1]')[0].find_element(By.XPATH, '..').find_element(By.XPATH, '..').get_attribute('class')
print(thead)



# header = ['Athlete Code', 'first name', 'last name', 'Date of Birth', 'Country', 'Image URL', 'Age']
# data = [athlete_code, first_name, last_name, dob_str, country, athlete_image_url, age]

# with open('./data/athlete-stats.csv', 'a', encoding='UTF8') as f:
#     writer = csv.writer(f)

#     # write the header
#     # writer.writerow(header)

#     # write the data
#     writer.writerow(data)

