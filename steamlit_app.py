# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())


cnx = st.connection("snowflake")
session = cnx.session() 

# Write directly to the app
st.title(f"Customize your smoothie! :cup_with_straw:")
st.write(
    "Choose the fruits you want in your smoothie!"
)


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be: ', name_on_order)


ingredient_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe,
    max_selections=5
)

if ingredient_list and name_on_order:
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """
    time_to_insert = st.button('Submit order')
    #st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
