### IMPORTANTE: Esto ya quedó obsoleto puesto que metacritic cambió su diseño web
# Los datos parseados los había exportado a archivos externos, por lo que se puede hacer aún el análisis posterior
###


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# Creo una clase para los juegos, con los atributos de interés: Nombre, plataforma, reviews (texto y nota) y género. 

class Game:
    def __init__(self, link):
        self.link=link
    
    
    def name(self):        
        url=self.link        
        user_agent = {'User-agent': 'Mozilla/5.0'}        
        response = requests.get(url, headers = user_agent)        
        soup = BeautifulSoup(response.text, 'html.parser')        
        return soup.find('h1').get_text()

    
    def platform(self):
        url=self.link        
        user_agent = {'User-agent': 'Mozilla/5.0'}        
        response = requests.get(url, headers = user_agent)        
        soup = BeautifulSoup(response.text, 'html.parser')        
        return soup.find('span', {'class':'platform'}).get_text().strip()

    def reviews(self):        
        revdict={'name': [], 'score':[],'text':[]}        
        url=self.link            
        user_agent = {'User-agent': 'Mozilla/5.0'}            
        response = requests.get(url, headers = user_agent)            
        soup = BeautifulSoup(response.text, 'html.parser')          
        temp=soup.find('li', {'class':'page last_page'})        
        if temp==None:
            paginas = 1
        else:
            paginas = int(re.findall("\d+", temp.get_text())[0])        
    
        for page in range(paginas+1):            
            url=self.link+'?page='+str(page)            
            user_agent = {'User-agent': 'Mozilla/5.0'}            
            response = requests.get(url, headers = user_agent)            
            soup = BeautifulSoup(response.text, 'html.parser')         

            for review in soup.find_all('div', class_='review_content'):                
                if review.find('div', class_='name') == None:                    
                    break 

                revdict['name'].append(review.find('div', class_='name'))
                revdict['score'].append(review.find('div', class_='review_grade').find('div').text)

                if review.find('span', class_='blurb blurb_expanded'):
                    revdict['text'].append(review.find('span', class_='blurb blurb_expanded').text)
                else:
                    revdict['text'].append(review.find('div',class_='review_body').text)
                    
        df=pd.DataFrame(revdict)    
        df['score']=df['score'].apply(int)
    
        return df
            
    
    def genre(self):        
        url=self.link[:-12]
        user_agent = {'User-agent': 'Mozilla/5.0'}            
        response = requests.get(url, headers = user_agent)            
        soup = BeautifulSoup(response.text, 'html.parser')        
        temp=soup.find_all('li', {'class':'summary_detail product_genre'})[0].get_text().split()[1:]        
        return [i.replace(',','') for i in temp]

        
        
        
### saco los datos para distintos juegos
        
games_list=[Game('https://www.metacritic.com/game/switch/the-legend-of-zelda-breath-of-the-wild/user-reviews'),
            Game('https://www.metacritic.com/game/switch/super-mario-odyssey/user-reviews'),
            Game('https://www.metacritic.com/game/playstation-4/persona-5-royal/user-reviews'),
            Game('https://www.metacritic.com/game/playstation-4/the-last-of-us-remastered/user-reviews'),
            Game('https://www.metacritic.com/game/playstation-4/god-of-war/user-reviews'),
            ]


## DataFrame con todos los juegos

allgames_df=pd.DataFrame(index=[i.name() for i in games_list])

allgames_df['genre']=[i.genre() for i in games_list]
allgames_df['platform']=[i.platform() for i in games_list]
allgames_df['scores']=[i.reviews()['score'] for i in games_list]
allgames_df['texts']=[i.reviews()['text'] for i in games_list]

allgames_df.to_csv('allgames.csv')  
        