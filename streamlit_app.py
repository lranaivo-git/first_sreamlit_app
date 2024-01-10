import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # streamlit.text(fruityvice_response.json())
  
  # Take the json response and normalize it
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  # output it to the screen
  return fruityvice_normalized

#snowflake function
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values('" + new_fruit +"')")
    return "Thanks for adding " + new_fruit

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

try:
  # text box to enter fruit
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get informtion.")
  else:
    streamlit.write('The user entered ', fruit_choice)
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
  
#stop code here
#streamlit.stop()

#snowflake content

streamlit.header('View Our Fruit List - Add your favorites!')
#add a button to load the fruit
if streamlit.button('Get Fruit list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.header("The fuit load list contains")
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

# text box to add a fruit to the list 
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  #streamlit.write('Thanks for adding ', add_my_fruit)
  back_from_funtion = insert_row_snowflake(add_my_fruit)
  my_cnx.close()
  streamlit.text(back_from_funtion)

#my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values('from Streamlit')")
