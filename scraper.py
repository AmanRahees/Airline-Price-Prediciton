from time import sleep
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import numpy as np

# path to chromedriver
chromedriver_path =  "C:/Users/amanr/Desktop/DS Poject Planning/chromedriver.exe"

# get user input for routes
origin = input("From?")
destination = input("To?")

print("\nRoute:")
print(f"{origin} => {destination}")


# get user input for period (start and end date)
start_date = np.datetime64(input('Start Date, Please use YYYY-MM-DD format only '))
end_date = np.datetime64(input('End Date, Please use YYYY-MM-DD format only '))
days = end_date - start_date
num_days = days.item().days

airline = []
prices = []
duration_list = []
stops_list = []
departure_list = []
arrival_list = []
class_list = []

def get_airlines(soup):    
    airlines = soup.find_all('div',class_='J0g6-operator-text',text=True)
    for i in airlines:
        airline.append(i.text)
    return airline
    
def get_departure(soup):
    times = soup.find_all('div', class_='vmXl vmXl-mod-variant-large')
    for time_div in times:
        span = time_div.find('span')
        if span:
            time_text = span.text
            departure_list.append(time_text)
    return departure_list

def get_arrival(soup):
    times = soup.find_all('div', class_='vmXl vmXl-mod-variant-large')
    for time_div in times:
        spans = time_div.find_all('span')
        for i in range(len(spans)):
            if spans[i].get('class') and 'aOlM' in spans[i]['class']:
                if i+1 < len(spans):
                    time_text = spans[i+1].text.strip().split('+')[0]
                    arrival_list.append(time_text)
    return arrival_list

def get_class(soup):
    classes = soup.find_all('div', class_='aC3z-name')
    for i in classes:
        print(i.text)
        if len(airline) > len(class_list):
            class_list.append(i.text)
    return class_list

def get_total_stops(soup):
    stops = soup.find_all('div',class_='vmXl vmXl-mod-variant-default')
    for i in stops:
        for j in i.find_all('span',class_='JWEO-stops-text'):
               stops_list.append(j.text)
    return stops_list

def get_price(soup):
    price = soup.find_all('div',class_='f8F1-price-text-container')
    for i in price:
        for j in i.find_all('div', class_='f8F1-price-text'):
            prices.append(j.text)
    return prices

def get_duration(soup):
    duration = soup.find_all('div' , class_='xdW8 xdW8-mod-full-airport')
    for i in duration:
        for j in i.find_all('div',class_='vmXl vmXl-mod-variant-default'):
            duration_list.append(j.text)
    return duration_list


def load_more():
    try:
        show_more_button = driver.find_element(By.CLASS_NAME,'show-more-button')
        show_more_button.click()
        driver.implicitly_wait(10)
        print('loaded')
    except:
        pass

data = pd.DataFrame()

for i in range(num_days+1):
    url = f"https://www.kayak.co.in/flights/{origin}-{destination}/{start_date+i}"

    # launching the driver
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(url)
    sleep(2)

    for j in range(5):
        load_more()

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    airlines = get_airlines(soup)
    total_stops = get_total_stops(soup)
    prices = get_price(soup)
    duration = get_duration(soup)
    departure = get_departure(soup)
    arrival = get_arrival(soup)
    classes = get_class(soup)
    print(len(airlines))
    print(len(total_stops))
    print(len(prices))
    print(len(duration))
    print(len(departure))
    print(len(arrival))
    print(len(classes))
    driver.quit()
    df = pd.DataFrame({
        'Airline': airlines,
        'Departure Time': departure,
        'Arrival Time': arrival,
        'Duration': duration,
        'Total stops' : total_stops,
        'Price' : prices,
        'Date' : start_date+i,
        'Class' : classes,
        'Origin' : origin,
        'Destination' : destination,
    })
    data = pd.concat([data, df])

data = data.replace('\n','', regex=True)
data = data.reset_index(drop = True)
data.to_csv(f'Data/{origin}_{destination}.csv',index=False)
print(f"Succesfully saved {origin} => {destination} route as {origin}_{destination}.csv ")