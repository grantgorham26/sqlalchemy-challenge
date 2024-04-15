# sqlalchemy-challenge

## Purpose
The purpose of this mini project was to use sqlalchemy to obtain weather data from a sqlite database then create a Flask application to create an API with stats such as average temperature and precipitation. Using sqlalchemy I was able to query for stats such as precipitation and temperature. I was also able to filter by various weather stations and dates. Some of these stats were then visualized using plots. 


### Part 1: Analyze and Explore the Climate Data
To begin part 1 of the project I first imported the needed dependencies such as sqlalchemy, matplotlib, and pandas to name a few. Once this was complete the tables from the sqlite databases needed to be reflected into sqlalchemy then saved. The first query that was completed was to look at the precipitation from the past year. I utilized chatgpt to helpwrite this query. Once this query was complete I converted it into a pandas dataframe then used this dataframe to create a line plot of the precipitation from the last year of the sqlite database. Another query was created to look at the max,min and avg temp at the most active station on the island. I used chatgpt to help optimize the orignal query that I wrote. The final query that I made was similar to the first query but instead it looks at temperature rather than precipitation. 

### Part 2: Design Your Climate App
