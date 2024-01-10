import streamlit
import pandas
import requests

streamlit.title('My parents new healthy Diner')

streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥑 Kale, Spinach & Rocket Smoothie')
streamlit.text('🍞 Hard boiled Free Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#load data from s3 bucket
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display table
streamlit.dataframe(fruits_to_show)

#display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())
