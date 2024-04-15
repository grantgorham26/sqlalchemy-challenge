# sqlalchemy-challenge

## Purpose
The purpose of this mini project was to use sqlalchemy to obtain weather data from a sqlite database then create a Flask application to create an API with stats such as average temperature and precipitation. Using sqlalchemy I was able to query for stats such as precipitation and temperature. I was also able to filter by various weather stations and dates. Some of these stats were then visualized using plots. 


### Part 1: Analyze and Explore the Climate Data
To begin part 1 of the project I first imported the needed dependencies such as sqlalchemy, matplotlib, and pandas to name a few. Once this was complete the tables from the sqlite databases needed to be reflected into sqlalchemy then saved. The first query that was completed was to look at the precipitation from the past year. I utilized chatgpt to helpwrite this query. Once this query was complete I converted it into a pandas dataframe then used this dataframe to create a line plot of the precipitation from the last year of the sqlite database. Another query was created to look at the max,min and avg temp at the most active station on the island. I used chatgpt to help optimize the orignal query that I wrote. The final query that I made was similar to the first query but instead it looks at temperature rather than precipitation. 
<img width="715" alt="Screenshot 2024-04-15 at 2 57 15 PM" src="https://github.com/grantgorham26/sqlalchemy-challenge/assets/154031840/dcb2f7ac-51da-4ecb-bdf0-eecbca2ad427">


### Part 2: Design Your Climate App
To start part 2 of the project I again started by importing the needed dependencies. For the app I was creating I needed sqlalchemy, datetime and flask along with certain functions of these libraries. I began by reflecting the sqlite database into sqlalchemy. The app would have 5 different endpoints which were listed on the welcome page as well as a quick description of the app. The first endpoint of the app had precipitation data from the last year of the database. The second endpoint included data about the 9 weather stations. The third one looked at the temperatures of the most active station. the fourth and fifth were very similar except once end point involved having a start and end date as parameters while the other only had a start date as a parameter. These last two endpoints looked at the average, minimum and maximum temperature of a specified date range. To help optimize my last two endpoints I used chatgpt to essetially combine them so that I was not reperating myself so much. 
![Screenshot 2024-04-15 at 2 55 28 PM](https://github.com/grantgorham26/sqlalchemy-challenge/assets/154031840/9f0ead33-c6fd-4e13-a679-d06bdb9f152b)
<img width="1710" alt="Screenshot 2024-04-15 at 2 55 05 PM" src="https://github.com/grantgorham26/sqlalchemy-challenge/assets/154031840/ac7c6934-1de8-4013-9a18-5380e0257ca1">
