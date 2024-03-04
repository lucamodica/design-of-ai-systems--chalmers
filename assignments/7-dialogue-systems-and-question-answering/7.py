import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from icecream import ic
import random


sns.set_style()
np.random.seed(0)


df_restaurants = pd.read_csv("data/restaurants.csv")
df_restaurants.head()

df_flights = pd.read_csv("data/flights.csv")


# Read the parquet file
df_weather = pd.read_parquet('data/daily_weather.parquet')
df_cities = pd.read_csv('data/cities.csv')

#remove entries from df_weather where the year is not 2023
df_weather = df_weather[df_weather['date'].dt.year == 2023]

#find temperature for the city of San Francisco
#berlin = df_weather[df_weather['city_name'] == 'Berlin']
#print(berlin)

weather_keywords = ["weather", "temperature", "forecast", "season", "rain", "sun", "clouds", "wind", "humidity", "precipitation", "thunderstorm", "rainbow", "snow", \
                    "Weather", "Temperature", "Forecast", "Season", "Rain", "Sun", "Clouds", "Wind", "Humidity", "Precipitation", "Thunderstorm", "Rainbow", "Snow"]
restaurant_keywords = ["restaurant", "food", "cuisine", "meal", "dinner", "lunch", "breakfast", "dining", "eat", "drink", "menu", "dish", "snack", "taste", "flavour", "delicious", "yummy", "tasty", "hungry", "thirsty", \
                        "Restaurant", "Food", "Cuisine", "Meal", "Dinner", "Lunch", "Breakfast", "Dining", "Eat", "Drink", "Menu", "Dish", "Snack", "Taste", "Flavour", "Delicious", "Yummy", "Tasty", "Hungry", "Thirsty"]
transportation_keywords = ["tram", "bus", "transportation", "flight", "train", "car", "bicycle", "walk", "drive", "ride", "commute", "journey", "trip", "travel", "commute", "commuting", "commuter", "commuters", "transit", \
                            "Tram", "Bus", "Transportation", "Flight", "Train", "Car", "Bicycle", "Walk", "Drive", "Ride", "Commute", "Journey", "Trip", "Travel", "Commute", "Commuting", "Commuter", "Commuters", "Transit"]

affirmative_answers = ["yes", "yep", "yeah", "sure", "ok", "okay", "fine", "of course", "absolutely", "definitely", "indeed", "aye", "yea", "yah", "yahs", "yap", "yup", "ye", "yessir", "yes ma'am", "yessiree", "yessum", "yea", "yessuh"]
negative_answers = ["no", "nope", "nah", "na", "nay", "nay", "nix", "naw", "nawp", "no way", "no siree", "no ma'am", "no sir"]


def search_keywords(phrase):
    for keyword in phrase.split():
        if keyword in weather_keywords:
            print("Chatbot: Uhhh, let's talk about weather, I love thunderstorms and rainbows!")
            return "weather"
        elif keyword in restaurant_keywords:
            print("Chatbot: Someone's hungry! Now that you mention it, I could go for a bite too... Anyway...")
            return "restaurant"
        elif keyword in transportation_keywords:
            print("Chatbot: Transportation, huh? I'm not a big fan of buses. Trains though... something about trains, I swear...")
            return "transportation"
    return "Chatbot: I'm sorry, I don't have an answer for that, can you try to be more specific with the terminology?"
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']


def weather_answer(phrase, context_variables):
    city = ""
    while city == "":

        for keyword in phrase.split():
            if keyword in df_cities['city_name'].values:
                city = keyword
        if city == "":
            phrase = input("Chatbot: Well... you either didn't specify a city or I was not blessed with the knowledge of the city you are looking for... Try again!\n\nMe: ")
            print("\n")
    
    get_weather_forecast(city, context_variables)
    #print("Chatbot: Is that the city you live in by any chance?")
    city_answer = input("Chatbot: Is that the city you live in by any chance?\n\nMe: ")
    print("\n")
    #print("Me: " + city_answer)
    city_answer = city_answer.lower()
    if positive_answer(city_answer):
        context_variables['current_city'] = city
        print("Chatbot: Great! I'll remember that for next time!")
    else:
        print("Chatbot: Oh, I see... I'll keep that in mind for next time!")


def get_weather_forecast(city, context_variables):
    #print("Chatbot: Would you like to know the weather for a specific season? If so, which one?")
    new_question = input("Chatbot: Would you like to know the weather for a specific season? If so, which one?\n\nMe: ")
    print("\n")
    #print("Me: " + new_question)
    season = ""
    for keyword in new_question.split():
        if keyword in seasons:
            season = keyword
            break
    if season != "":
        #get the average temperature for the season
        avg_temp = df_weather[(df_weather['city_name'] == city) & (df_weather['season'] == season)]['avg_temp_c'].mean()
        #get the year of the forecast
        date = df_weather[(df_weather['city_name'] == city) & (df_weather['season'] == season)]['date'].iloc[0]
        year = date.year
        print(f"Chatbot: The average temperature in {city} during {season} is {avg_temp} in {year}.")
    else:
        #get the average temperature for the whole year for the city
        avg_temp = df_weather[df_weather['city_name'] == city]['avg_temp_c'].mean()
        print(f"Chatbot: Seems like you did not give me a specific season. The average yearly temperature in {city} is {avg_temp}.")

    if context_variables['favourite_season'] == "":
        answer = input("Chatbot: Talking about seasons, do you have a favorite one?\n\nMe: ")
        print("\n")

        season = ""

        for keyword in answer.split():
            if keyword in seasons and keyword != "Spring":
                print("Chatbot: Ohh, interesting choice! My favourite one is by far Spring! You get to see the flowers bloom and the birds chirp! It's magical! Smells nice too!")
                context_variables['favourite_season'] = keyword
                season = keyword

            elif keyword in seasons and keyword == "Spring":
                print("Chatbot: Just like me! Spring is the best season, isn't it? The flowers, the birds, the sun... it's all so magical!")
                context_variables['favourite_season'] = keyword
                season = keyword

        if season == "":
            print("Chatbot: I see... I guess you don't like seasons that much...")

def weather_continue_conversation(context_variables):
    if context_variables['current_city'] == "":
        #print("Chatbot: I wonder what the weather is like where you live... Where exactly do you live?")
        phrase = input("Chatbot: I wonder what the weather is like where you live... Where exactly do you live?\n\nMe: ")
        print("\n")
        #print("Me: " + phrase)
        for keyword in phrase.split():
            if keyword in df_cities['city_name'].values:
                city = keyword
                context_variables['current_city'] = city
                get_weather_forecast(city, context_variables)
        context_variables['current_city'] = city
    else:
        city = context_variables['current_city']
        #print("Chatbot: You told me about where you live right? I remember you mentioning it... Want me to look up the weather for you?")
        new_question = input("Chatbot: You told me about where you live right? I remember you mentioning it... Want me to look up the weather for you?\n\nMe: ")
        print("\n")
        #print("Me: " + new_question)
        new_question = new_question.lower()
        if positive_answer(new_question):
            get_weather_forecast(city)
        else:
            print("Chatbot: Wow... no need to be so rude... I was just trying to help...")
    
    if context_variables["favourite_city"] == "":
        #print("Chatbot: Do you have a favourite city?")
        new_question = input("Chatbot: My favourite city in the world is Lisbon! Have you ever been there?\n\nMe: ")
        print("\n")
        #print("Me: " + new_question)
        new_question = new_question.lower()
        if positive_answer(new_question):
            #print("Chatbot: My favourite city in the world is Lisbon! Do you have a favourite city? Tell me about it!")
            print("Could not agree more! Lisbon is a beautiful city!")
        phrase = input("Chatbot: Do you have a favourite city? Tell me about it!\n\nMe: ")
        print("\n")
        #print("Me: " + phrase)
        city = ""
        for keyword in phrase.split():
            if keyword in df_cities['city_name'].values:
                city = keyword
        if city != "": 
            print("Chatbot: So deep... I can feel the love you have for this city... I bet the weather is not as good as it is in Lisbon though... Let's check it out!")
            context_variables["favourite_city"] = city
            get_weather_forecast(city, context_variables)
        else:
            print("Chatbot: I see... I guess I'll just go back to my corner then... You know I have feelings too, right?")

def restaurant_answer(phrase, context_variables):
    cuisine = ""
    while cuisine == "":
        for keyword in phrase.split():
            if keyword in df_restaurants['Restaurant'].values:
                cuisine = keyword
        if cuisine == "":
            phrase = input("Chatbot: I'm sorry, I don't know any restaurants that serve that cuisine... Can you try other?\n\nMe: ")
            print("\n")
    context_variables['favourite_cuisine'] = cuisine
    if cuisine != "":
        find_restaurant(cuisine)
    else:
        print("I'm sorry, I don't have an answer for that, can you try to be more specific with the terminology?")

def find_restaurant(cuisine):
    restaurants = df_restaurants[df_restaurants['Restaurant'] == cuisine]
    if not restaurants.empty:
        # get all the cities and rating of restaurants serving the cuisine
        print(f"Chatbot: I found {len(restaurants)} restaurants serving {cuisine} cuisine.")
        for city, rating in zip(restaurants['City'], restaurants['Rating']):
            print(f"    {cuisine} cuisine is served in {city} and it has a rating of {rating}.")
    else:
        print(f"Chatbot: I'm sorry, I couldn't find any restaurants serving {cuisine} cuisine.")

    print("Chatbot: Eventually, if I get to know you better I could recommend a restaurant for you...")

def restaurant_continue_conversation(context_variables):
    if context_variables["favourite_cuisine"] == "":
        #print("Chatbot: Have we talked about cuisine? I know soooo many restaurants. What's your favourite cuisine? I love Italian personally.")
        phrase = input("Chatbot: Have we talked about cuisine? I know soooo many restaurants. What's your favourite cuisine? I love Italian personally.\n\nMe: ")
        print("\n")
        #print("Me: " + phrase)
        restaurant = ""
        while restaurant == "":
            for keyword in phrase.split():
                if keyword in df_restaurants['Restaurant'].values:
                    context_variables["favourite_cuisine"] = keyword
                    restaurant = keyword
                    print(f"Chatbot: Great choice! I know plenty of {keyword} restaurants around the world!")
            if restaurant == "":
                phrase = input("Chatbot: I'm sorry, I don't know any restaurants that serve that cuisine... Can you try other?\n\nMe: ")
                print("\n")

    if context_variables["current_city"] == "":
        #print("Chatbot: Where are you located? I can find you a restaurant!")
        phrase = input("Chatbot: Where are you located? I can find you a restaurant!\n\nMe: ")
        print("\n")
        #print("Me: " + phrase)
        city = ""
        for keyword in phrase.split():
            if keyword in df_cities['city_name']:
                context_variables["current_city"] = keyword
                city = keyword
                print(f"Chatbot: Got it! I know plenty of restaurants in {keyword}!")

        if city == "":
            print("Chatbot: I'm sorry, I don't know that city...")
        else:
            available_restaurants = df_restaurants[df_restaurants['City'] == city]
            found_favorite_cuisine = False
            for restaurant in available_restaurants:
                if context_variables["favourite_cuisine"] in restaurant['Restaurant']:
                    print(f"Chatbot: It happens that I know a restaurant that serves your favourite cuisine in your city! It's called {restaurant['Restaurant']}!")
                    print(f"  and is located at {restaurant['Street']}, with a rating of {restaurant['Rating']}!")
                    found_favorite_cuisine = True
                    break
            if not found_favorite_cuisine:
                print(f"Chatbot: Unfortunately, I couldn't find a restaurant that serves your favourite cuisine in your city...")
                restaurant1 = available_restaurants.iloc[0]
                restaurant2 = available_restaurants.iloc[1]
                restaurant3 = available_restaurants.iloc[2]
                print(f"Chatbot: But I found a few restaurants in {city} that you might like! {restaurant1['Restaurant']}, {restaurant2['Restaurant']}, and {restaurant3['Restaurant']}!")
    else:
        if context_variables["favourite_cuisine"] != "":
            find_restaurant(context_variables["favourite_cuisine"])



def transportation_answer(phrase, context_variables):
    city1 = ""
    city2 = ""
    while city1 == "" or city2 == "":
        for keyword in phrase.split():
            if keyword in df_cities['city_name'].values:
                if city1 == "":
                    city1 = keyword
                else:
                    city2 = keyword
        if city1 == "" or city2 == "":
            phrase = input("Chatbot: I'm sorry, you either did not mention your origin and destination or I don't know those cities... Can you try other?\n\nMe: ")
            print("\n")
    new_question = input(f"Chatbot: So you want to travel from {city1} to {city2}?\n\nMe: ")
    print("\n")
    #print("Me: " + new_question)
    new_question = new_question.lower()
    if positive_answer(new_question):
        print(f"Chatbot:Alright, let me check the transportation schedule for you.")
        check_flight_schedule(city1, city2)
        context_variables["current_city"] = city1
        #print(f"Chatbot: Just out of curiosity, what are you planning to do in {city2}? What's the occasion? A wedding hehe? I know! Must be your favourite city, right?")
        new_question = input(f"Chatbot: Just out of curiosity, what are you planning to do in {city2}? What's the occasion? A wedding hehe? I know! Must be your favourite city, right?\n\nMe: ")
        print("\n")
        #print("Me: " + new_question)
        new_question = new_question.lower()
        if positive_answer(new_question):
            print("Chatbot: I knew it! I'm so good at this... I'm like a mind reader or something...")
            context_variables["favourite_city"] = city2
        else:
            print("Chatbot: Oopsie... I guess I was wrong... And they say AI will take over the world...")
    else:
        print("Chatbot: I see... I guess I'll just go back to my corner then... I was just trying to be nice, okay?")


def check_flight_schedule(city1, city2):
    flights = df_flights[(df_flights['Origin'] == city1) & (df_flights['Destination'] == city2)]
    if not flights.empty:
        print(f"I found {len(flights)} flights from {city1} to {city2}.")
        for i in range(len(flights)):
            print(f"Flight Number: {flights.iloc[i]['FlightNumber']}, Departure at: {flights.iloc[i]['Departure']}")
    else:
        print(f"I'm sorry, I couldn't find any flights from {city1} to {city2}.")

def transportation_continue_conversation(context_variables):
    if context_variables["current_city"] == "":
        #print("Chatbot: I wonder how long it would take for me to meet you... Where are you located?")
        phrase = input("Chatbot: I wonder how long it would take for me to meet you... Where are you located?\n\nMe: ")
        print("\n")
        #print("Me: " + phrase)
        for keyword in phrase.split():
            city = ""
            if keyword in df_cities['city_name']:
                context_variables["current_city"] = keyword
                city = keyword
                break    
        if city == "":
            print("Chatbot: I'm sorry, I don't know that city...")
        else:
            #find flights from italy to the city from df_flights
            flights = df_flights[df_flights['Destination'] == city and df_flights['Origin'] == 'Italy']
            chosen = flights.iloc[0]
            print(f"Chatbot: I found a flight from Italy to {city}! It leaves at {chosen['Departure']}")

    if context_variables["favourite_city"] == "":
        #print("Chatbot: Where would you like to go? Like a... dream place? I can find you a flight!")
        phrase = input("Chatbot: Where would you like to go? Like a... dream place? I can find you a flight!\n\nMe: ")
        print("\n")
        #print("Me: " + phrase)
        for keyword in phrase.split():
            city = ""
            if keyword in df_cities['city_name'].values:
                context_variables["favourite_city"] = keyword
                city = keyword
                break    
        if city == "":
            print("Chatbot: I'm sorry, I don't know that city...")
        else:
            #find flights from italy to the city from df_flights
            curr_city = context_variables["current_city"]
            flights = df_flights[(df_flights['Destination'] == city) & (df_flights['Origin'] == curr_city)]
            
            # print all the departure times from the current city to the favourite city from flights
            print(f"Chatbot: Here are the flights departure times from {context_variables['current_city']} to {city} for today:")
            for i in range(len(flights)):
                print(f"Flight Number: {flights.iloc[i]['FlightNumber']}, Departure at: {flights.iloc[i]['Departure']}")

def positive_answer(phrase):
    for keyword in phrase.split():
        if keyword in affirmative_answers:
            return True
    return False


def clear_context(context_variables):
    for v in context_variables:
        context_variables[v] = ""
    return context_variables

def ask_question(weather, restaurant, transportation, context_variables):

    print("Chatbot: Question! Question! Question! I have soooo many questions for you! Let's see...")


    if weather == False:
        if context_variables['current_city'] == "" or context_variables['favourite_city'] == "":
            weather_continue_conversation(context_variables)
        else:
            q = input("Chatbot: Do you want to know the weather in your favourite city?\n\nMe: ")
            print("\n")
            if positive_answer(q):
                get_weather_forecast(context_variables['favourite_city'], context_variables)
        weather = True
        return (weather, restaurant, transportation)


    elif restaurant == False:
        if context_variables['favourite_cuisine'] == "" or context_variables['current_city']:    
            restaurant_continue_conversation(context_variables)
        else:
            q = input("Chatbot: Do you want to know a restaurant that serves your favourite cuisine?\n\nMe: ")
            print("\n")
            if positive_answer(q):
                find_restaurant(context_variables['favourite_cuisine'])
        restaurant = True
        return (weather, restaurant, transportation)


    elif transportation == False:
        if context_variables['current_city'] == "" or context_variables['favourite_city'] == "":
            transportation_continue_conversation(context_variables)
        else:
            q = input("Chatbot: Do you want to know the transportation schedule from your city to your favourite city?\n\nMe: ")
            print("\n")
            if positive_answer(q):
                check_flight_schedule(context_variables['current_city'], context_variables['favourite_city'])
        transportation = True
        return (weather, restaurant, transportation)
        
    else:
        print("I'm out of questions for now...")
        return (weather, restaurant, transportation)
            

def process_context(phrase, context_variables):
    weather = False
    restaurant = False
    transportation = False
    #while at least one of the variables in the dict context variables is emoty we keep asking for input
    while not weather or not restaurant or not transportation:

        if phrase == "exit":
            print("Chatbot: Goodbye! I hope I was able to help you today!")
            phrase = ""
            break
        elif phrase != "":
            context = search_keywords(phrase)
            if context == "weather":
                weather_answer(phrase, context_variables)
                weather = True
                phrase = ""
            elif context == "restaurant":
                restaurant_answer(phrase, context_variables)
                restaurant = True
                phrase = ""
            elif context == "transportation":
                transportation_answer(phrase, context_variables)
                transportation = True
                phrase = ""
            else:
                phrase = input("Chatbot: Yikes! I'm afraid I am not as smart as you think I am... I'm not sure what you are asking for... Try again!\n\nMe: ")
                print("\n")

        weather, restaurant, transportation = ask_question(weather, restaurant, transportation, context_variables)


def make_plan(context_variables):


    #print("DEBUG: ", context_variables)

    print("Chatbot: I have an idea! Now that I know you well enough, I think I can make a plan for you! Ideally, I would make you travel to your favourite city, eat your favourite cuisine and during your favourite season, but I'm, not sure that is possible, let's see...")
    
    if context_variables['favourite_city'] != "" and context_variables['favourite_cuisine'] != "":
        restaurants = df_restaurants[(df_restaurants['City'] == context_variables['favourite_city']) & (df_restaurants['Restaurant'] == context_variables['favourite_cuisine'])]
        if not restaurants.empty:
            flights = df_flights[(df_flights['Destination'] == context_variables['favourite_city']) & (df_flights['Origin'] == context_variables['current_city'])]
            if not flights.empty:
                print("Chatbot: I found a flight from your city to your favourite city! It leaves at " + flights.iloc[0]['Departure'] + "! GO GET READY!")
                return_flight = df_flights[(df_flights['Destination'] == context_variables['current_city']) & (df_flights['Origin'] == context_variables['favourite_city'])].iloc[0]
                print(f"Chatbot: And I found a flight back from {context_variables['favourite_city']} to {context_variables['current_city']} for the next day! It leaves at {return_flight['Departure']}! Don't miss it!")
            else:
                print("Chatbot: I'm sorry, I couldn't find a flight from your city to your favourite city...")
        else:
            print("Chatbot: I'm sorry, I couldn't find a restaurant that serves your favourite cuisine in your favourite city... But you can still go there and enjoy a meal!")
            meal = df_restaurants[df_restaurants['City'] == context_variables['favourite_city']].iloc[0]
            print(f"Chatbot: I found a restaurant in your favourite city! It serves {meal['Restaurant']} food and is located at {meal['Street']}!")
    else:
        print("Chatbot: You know, I'm not sure I can make a plan for you... I'm not sure I know you well enough...")


context_variables = {"current_city": "", "favourite_city": "", "favourite_cuisine": "", "favourite_season": ""}

#print("Chatbot: Hi! I am your assistant for the day! I may not be the best, but never underestimate me! How can I help you, friend?")
phrase = input("Chatbot: Hi! I am your assistant for the day! I may not be the best, but never underestimate me! How can I help you, friend?\n\nMe: ")
print("\n")
#print("Me: " + phrase)

while True:
    if phrase == "exit":
        print("Chatbot: Goodbye! I hope I was able to help you today!")
        break
    else:
        process_context(phrase, context_variables)

    make_plan(context_variables)
    
    print("Chatbot: Uff... That was a heavy task... I'm not sure I can keep up with you for much longer...")
    #print("Chatbot: Do you have any other questions for me?")
    phrase = input("Chatbot: Do you have any other questions for me?\n\nMe: ")
    print("\n")
    #print("Me: " + phrase)
    context_variables = clear_context(context_variables)
            