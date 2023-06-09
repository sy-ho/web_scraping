from bs4 import BeautifulSoup
import requests 
import re


from csv import writer
with open('condo_rental_KL.csv','w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header = ['Property Name','Location','Average Size (Squared Feet)', 'Average Rental (MYR)','Num of Bedroom','Num of Bathroom']
    thewriter.writerow(header)
    pages = 1
    
    while pages < 251: # 250 pagecount stored at 1 time on mudah.my as of 4/12/2020
      next_page = True
      if next_page: # if have next page, run the code below
        url = f"https://www.mudah.my/kuala-lumpur/apartment-condominium-for-rent?o={pages}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = str(soup)
        
        tab = r"listing-ad-item-[0-9]+"
        item_lists_id = re.findall(tab,content)

        next_page = r"aria-disabled=\"[a-z]+\""
        next_page_disable= re.findall(next_page,content)
        
        
        # check is next able
        for i in next_page_disable: 
          if "true" in i:
            next_page = False

        pages +=1 


        for lst in item_lists_id:
          item = soup.find_all('div', {"data-testid": lst})
          
          property_name = item[0].findAll('a')[0].get('title')
          location = item[0].findAll('span')[-1].text
          avg_size = item[0].find_all('div', {"title": "Size"})[-1].text.replace(' sq.ft.','')
          avg_rental = item[0].find('div').find_next('div').find_next('div').find_next('div').find_next('div').text.replace('RM ','').replace(' per month','')
          try:
            # bedroom = item[0].find('div', {"title": "Bedrooms"}).text.replace('Bedrooms','')
            bedroom = item[0].find_all('div', {"title": "Bedrooms"})[-1].text.replace('Bedrooms','').replace('Bedroom','')
          except:
            bedroom = None
            # bedroom = item[0].find('div', {"title": "Bedrooms"})[-1].text.replace('Bedrooms','')
          # bedroom = item[0].find_all('div', {"title": "Bedrooms"})[-1].text.replace('Bedrooms ','')
          
          try:
            bathroom = item[0].find_all('div', {"title": "Bathrooms"})[-1].text.replace('Bathrooms','').replace('Bathroom','')
          except:
            bathroom = None
          # bathroom = item[0].find_all('div', {"title": "Bathrooms"})[-1].text.replace('Bathrooms ','')
          info = [property_name,location,avg_size,avg_rental,bedroom,bathroom]
          thewriter.writerow(info)
      
print("done!")
    
