############################################ IMPORT LIBRARIES ################################################
import streamlit as st
import PIL.Image
from urllib.request import urlopen
import numpy as np
import pandas as pd
import fastai
from fastai.vision import *

##############################################################################################################
################################################ SIDEBAR #####################################################
##############################################################################################################

######################## Contact Me link ################################
st.sidebar.markdown(
    """<a style='display: block; text-align: right;' href="https://github.com/AparGarg99"><b>Contact Me</b></a>
    """,
    unsafe_allow_html=True,
)

######################## Take user input image ###########################
st.sidebar.title('User Input Parameters')
st.sidebar.warning("""Please upload image OR enter image URL""")
uploaded_file = st.sidebar.file_uploader("Upload image", type=['png', 'jpg'])
sample_url = 'https://www.recipetineats.com/wp-content/uploads/2016/08/Churros_9-SQ.jpg'
url = st.sidebar.text_input('Enter image url','')

try:

  if uploaded_file is None and url=='':
    img = PIL.Image.open(urlopen(str(sample_url)))
    image = open_image(urlopen(str(sample_url)))

  elif uploaded_file is not None and url=='':
    img = PIL.Image.open(uploaded_file)
    image = open_image(uploaded_file)
  

  elif uploaded_file is None and url!='':
    img = PIL.Image.open(urlopen(str(url)))
    image = open_image(urlopen(str(url)))

  elif uploaded_file is not None and url!='':

    # check validity of image url
    check = False
    try:
      x = PIL.Image.open(urlopen(str(url)))
    except:
      check = True
      
    # if url is valid -> open sample image
    # if url is invalid -> open uploaded image
    if(check == False):
      st.sidebar.error("You have chosen two images...try again !!")
      img = PIL.Image.open(urlopen(sample_url))
      image = open_image(urlopen(str(sample_url)))

    elif(check == True):
      st.sidebar.error("Invalid URL...opening uploaded image !!")
      img = PIL.Image.open(uploaded_file)
      image = open_image(uploaded_file)
      
except:
  st.sidebar.error("Invalid URL...try again !!")
  img = PIL.Image.open(urlopen(sample_url))
  image = open_image(urlopen(str(sample_url)))


##############################################################################################################
########################################## BACKEND PREDICTION ################################################
##############################################################################################################

data = ['apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 'beignets', 
        'bibimbap', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 
        'carrot_cake', 'ceviche', 'cheese_plate', 'cheesecake', 'chicken_curry', 'chicken_quesadilla', 'chicken_wings', 
        'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee',
        'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'edamame', 'eggs_benedict', 'escargots', 'falafel', 
        'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 
        'fried_rice', 'frozen_yogurt', 'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon',
        'guacamole', 'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'lasagna', 
        'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup', 'mussels', 'nachos', 'omelette', 
        'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes', 'panna_cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine', 
        'prime_rib', 'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sashimi', 'scallops', 
        'seaweed_salad', 'shrimp_and_grits', 'spaghetti_bolognese', 'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake',
        'sushi', 'tacos', 'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles']
        

learn = load_learner('/content/drive/MyDrive/')
pred_class,pred_idx,outputs = learn.predict(image)
pred = data[int(pred_idx)]

##############################################################################################################
################################################ MAIN PAGE ###################################################
##############################################################################################################

###################### Display title of the project #######################
st.markdown("<h1 style='text-align: center; color: #DBDE0A; font-size:500%; font-family:Brush Script MT, cursive;'>Food Mania</h1>", unsafe_allow_html=True)
st.write('')

######################## Display app description ##########################
expander_bar = st.beta_expander("About App")
expander_bar.markdown('''
	* This project uses a Deep CNN to classify images of 101 food classes.
	* Dataset : https://www.kaggle.com/kmader/food41?select=images
	* Code : https://github.com/AparGarg99/Food_Mania
		''')
st.write('')

######################## Display user input image #########################
st.markdown("<p style= 'color: #DBDE0A; font-size:190%;'>Image you've selected</p>", unsafe_allow_html=True)

img = img.resize((224,224))
st.image(img)
st.write('')

#################### Display model predicted food class ###################
st.markdown("<p style= 'color: #DBDE0A; font-size:190%;'>Prediction</p>", unsafe_allow_html=True)

st.write(pred.replace('_', ' ').title())
st.write('')

#################### Display extra info about prediction ##################
x ='Learn more about "{}"'.format(pred.replace('_', ' ').title())
st.markdown("<p style= 'color: #DBDE0A; font-size:190%;'>"+x+"</p>", unsafe_allow_html=True)

link1 = 'https://en.wikipedia.org/wiki/' + pred.lower()
link1 = f'<a href="{link1}" target="_blank">{"link"}</a>'

link2 ='https://www.google.com/search?q={}&tbm=isch'.format(pred.lower().replace('_', '+'))
link2 = f'<a href="{link2}" target="_blank">{"link"}</a>'

df = pd.DataFrame(zip(['Wikipedia','Google Images'],[link1,link2]),columns=['Website Name','Webpage Link'])
df = df.to_html(escape=False)

st.write(df, unsafe_allow_html=True)