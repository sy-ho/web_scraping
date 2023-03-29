from bs4 import BeautifulSoup
import requests 
from csv import writer
with open('condo_rental_KL.csv','w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ['Property Name','Location','Average Size (Squared Feet)', 'Average Rental (MYR)']
    thewriter.writerow(header)

    for i in range(1,251): # 250 pagecount stored at 1 time on mudah.my as of 4/12/2020
      url = f"https://www.mudah.my/kuala-lumpur/apartment-condominium-for-rent?o={i}"
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      lists = soup.find_all('div', class_ ="sc-kxynE etVsVZ")
      for list in lists:
        property_name = list.find('a', class_="sc-fQejPQ fphhPn").text
        location = list.find('span', class_="sc-ebFjAB bKiVTj").text
        avg_size = list.find('div', class_="sc-eInJlc cdnzEh").find_next('div',class_="sc-eInJlc cdnzEh").text.replace(' sq.ft.','')
        avg_rental = list.find('div', class_="sc-jXQZqI dcwjPY").text.replace('RM ','').replace(' per month','')
        info = [property_name,location,avg_size,avg_rental]
        thewriter.writerow(info)
print("done!")