# game_review_analysis
Obtención, estudio y clasificación de reviews de un videojuego.  

Las reviews se obtuvieron usando la librería BeautifulSoup para parsear la web de reviews "Metacritic", de la forma que se ve en "old_scraper.py". Notar que esto ya ha quedado obsoleto debido al cambio en diseño web de Metacritic. 

Se utilizaron las reviews obtenidas para intentar predecir, a partir de un texto, si la nota correspondiente supera o no cierto umbral. Para ello se usó un modelo de Regresión Logistica, usando la librería de scikit-learn.
Dicho análisis se encuentra explicado en el notebook "review_discrimination.ipynb". 

Este proyecto fue realizado pura y exclusivamente con fines didácticos. 
