# Bring in deps
import os
from stable import stableai
import streamlit as st
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain#, SequentialChain 
from langchain.memory import ConversationBufferMemory
from PIL import Image

st.markdown(
    """
    <style>
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } 
    </style>
    """,
    unsafe_allow_html=True
)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.postimg.cc/B6PhwYgZ/Zz05-Nm-M1-Yj-Fj-Yjhl-NDIx-MWVi-ODcz-ZWQz-Yz-Bk-NTFl-NDU4-ZA.jpg");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.set_page_config(page_icon="📖", page_title="Cardventure")
st.markdown(page_bg_img, unsafe_allow_html=True)

#dict for card stack
stack = {
    "four of clubs" : "1st",
    "two of hearts" : "2nd",
    "seven of diamonds" : "3rd",
    "three of clubs" : "4th",
    "four of hearts" : "5th",
    "six of diamonds" : "6th",
    "ace of spades" : "7th",
    "five of hearts" : "8th",
    "nine of spades" : "9th",
    "two of spades" : "10th",
    "queen of hearts" : "11th",
    "three of diamonds" : "12th",
    "queen of clubs" : "13th",
    "eight of hearts" : "14th",
    "six of spades" : "15th",
    "five of spades" : "16th",
    "nine of hearts" : "17th",
    "king of clubs" : "18th",
    "two of diamonds" : "19th",
    "jack of hearts" : "20th",
    "three of spades" : "21st",
    "eight of spades" : "22nd",
    "six of hearts" : "23rd",
    "ten of clubs" : "24th",
    "five of diamonds" : "25th",
    "kind of diamonds" : "26th",
    "two of clubs" : "27th",
    "three of hearts" : "28th",
    "eight of diamonds" : "29th",
    "five of clubs" : "30th",
    "king of spades" : "31st",
    "jack of diamonds" : "32nd",
    "eight of clubs" : "33rd",
    "ten of spades" : "34th",
    "king of hearts" : "35th",
    "jack of clubs" : "36th",
    "seven of spades" : "37th",
    "ten of hearts" : "38th",
    "ace of diamonds" : "39th",
    "four of spades" : "40th",
    "seven of hearts" : "41st",
    "four of diamonds" : "42nd",
    "ace of clubs" : "43rd",
    "nine of clubs" : "44th",
    "jack of spades" : "45th",
    "queen of diamonds" : "46th",
    "seven of clubs" : "47th",
    "queen of spades" : "48th",
    "ten of diamonds" : "49th",
    "six of clubs" : "50th",
    "ace of hearts" : "51st",
    "nine of diamonds" : "52nd",
    "4 of clubs" : "1st",
    "2 of hearts" : "2nd",
    "7 of diamonds" : "3rd",
    "3 of clubs" : "4th",
    "4 of hearts" : "5th",
    "6 of diamonds" : "6th",
    "1 of spades" : "7th",
    "5 of hearts" : "8th",
    "9 of spades" : "9th",
    "2 of spades" : "10th",
    "12 of hearts" : "11th",
    "3 of diamonds" : "12th",
    "12 of clubs" : "13th",
    "8 of hearts" : "14th",
    "6 of spades" : "15th",
    "5 of spades" : "16th",
    "9 of hearts" : "17th",
    "13 of clubs" : "18th",
    "2 of diamonds" : "19th",
    "11 of hearts" : "20th",
    "3 of spades" : "21st",
    "8 of spades" : "22nd",
    "6 of hearts" : "23rd",
    "10 of clubs" : "24th",
    "5 of diamonds" : "25th",
    "13 of diamonds" : "26th",
    "2 of clubs" : "27th",
    "3 of hearts" : "28th",
    "8 of diamonds" : "29th",
    "5 of clubs" : "30th",
    "13 of spades" : "31st",
    "11 of diamonds" : "32nd",
    "8 of clubs" : "33rd",
    "10 of spades" : "34th",
    "13 of hearts" : "35th",
    "11 of clubs" : "36th",
    "7 of spades" : "37th",
    "10 of hearts" : "38th",
    "1 of diamonds" : "39th",
    "4 of spades" : "40th",
    "7 of hearts" : "41st",
    "4 of diamonds" : "42nd",
    "1 of clubs" : "43rd",
    "9 of clubs" : "44th",
    "11 of spades" : "45th",
    "12 of diamonds" : "46th",
    "7 of clubs" : "47th",
    "12 of spades" : "48th",
    "10 of diamonds" : "49th",
    "6 of clubs" : "50th",
    "1 of hearts" : "51st",
    "9 of diamonds" : "52nd",
    "4 of club" : "1st",
    "2 of heart" : "2nd",
    "7 of diamond" : "3rd",
    "3 of club" : "4th",
    "4 of heart" : "5th",
    "6 of diamond" : "6th",
    "1 of spade" : "7th",
    "5 of heart" : "8th",
    "9 of spade" : "9th",
    "2 of spade" : "10th",
    "12 of heart" : "11th",
    "3 of diamond" : "12th",
    "12 of club" : "13th",
    "8 of heart" : "14th",
    "6 of spade" : "15th",
    "5 of spade" : "16th",
    "9 of heart" : "17th",
    "13 of club" : "18th",
    "2 of diamond" : "19th",
    "11 of heart" : "20th",
    "3 of spade" : "21st",
    "8 of spade" : "22nd",
    "6 of heart" : "23rd",
    "10 of club" : "24th",
    "5 of diamond" : "25th",
    "13 of diamond" : "26th",
    "2 of club" : "27th",
    "3 of heart" : "28th",
    "8 of diamond" : "29th",
    "5 of club" : "30th",
    "13 of spade" : "31st",
    "11 of diamond" : "32nd",
    "8 of club" : "33rd",
    "10 of spade" : "34th",
    "13 of heart" : "35th",
    "11 of club" : "36th",
    "7 of spade" : "37th",
    "10 of heart" : "38th",
    "1 of diamond" : "39th",
    "4 of spade" : "40th",
    "7 of heart" : "41st",
    "4 of diamond" : "42nd",
    "1 of club" : "43rd",
    "9 of club" : "44th",
    "11 of spade" : "45th",
    "12 of diamond" : "46th",
    "7 of club" : "47th",
    "12 of spade" : "48th",
    "10 of diamond" : "49th",
    "6 of club" : "50th",
    "1 of heart" : "51st",
    "9 of diamond" : "52nd",
    "4c" : "1st",
    "2h" : "2nd",
    "7d" : "3rd",
    "3c" : "4th",
    "4h" : "5th",
    "6d" : "6th",
    "as" : "7th",
    "5h" : "8th",
    "9s" : "9th",
    "2s" : "10th",
    "qh" : "11th",
    "3d" : "12th",
    "qc" : "13th",
    "8h" : "14th",
    "6s" : "15th",
    "5s" : "16th",
    "9h" : "17th",
    "kc" : "18th",
    "2d" : "19th",
    "jh" : "20th",
    "3s" : "21st",
    "8s" : "22nd",
    "6h" : "23rd",
    "10c" : "24th",
    "5d" : "25th",
    "kd" : "26th",
    "2c" : "27th",
    "3h" : "28th",
    "8d" : "29th",
    "5c" : "30th",
    "ks" : "31st",
    "jd" : "32nd",
    "8c" : "33rd",
    "10s" : "34th",
    "kh" : "35th",
    "jc" : "36th",
    "7s" : "37th",
    "10h" : "38th",
    "ad" : "39th",
    "4s" : "40th",
    "7h" : "41st",
    "4d" : "42nd",
    "ac" : "43rd",
    "9c" : "44th",
    "js" : "45th",
    "qd" : "46th",
    "7c" : "47th",
    "qs" : "48th",
    "10d" : "49th",
    "6c" : "50th",
    "ah" : "51st",
    "9d" : "52nd",
    "four of club" : "1st",
    "two of heart" : "2nd",
    "seven of diamond" : "3rd",
    "three of club" : "4th",
    "four of heart" : "5th",
    "six of diamond" : "6th",
    "ace of spade" : "7th",
    "five of heart" : "8th",
    "nine of spade" : "9th",
    "two of spade" : "10th",
    "queen of heart" : "11th",
    "three of diamond" : "12th",
    "queen of club" : "13th",
    "eight of heart" : "14th",
    "six of spade" : "15th",
    "five of spade" : "16th",
    "nine of heart" : "17th",
    "king of club" : "18th",
    "two of diamond" : "19th",
    "jack of heart" : "20th",
    "three of spade" : "21st",
    "eight of spade" : "22nd",
    "six of heart" : "23rd",
    "ten of club" : "24th",
    "five of diamond" : "25th",
    "kind of diamond" : "26th",
    "two of club" : "27th",
    "three of heart" : "28th",
    "eight of diamond" : "29th",
    "five of club" : "30th",
    "king of spade" : "31st",
    "jack of diamond" : "32nd",
    "eight of club" : "33rd",
    "ten of spade" : "34th",
    "king of heart" : "35th",
    "jack of club" : "36th",
    "seven of spade" : "37th",
    "ten of heart" : "38th",
    "ace of diamond" : "39th",
    "four of spade" : "40th",
    "seven of heart" : "41st",
    "four of diamond" : "42nd",
    "ace of club" : "43rd",
    "nine of club" : "44th",
    "jack of spade" : "45th",
    "queen of diamond" : "46th",
    "seven of club" : "47th",
    "queen of spade" : "48th",
    "ten of diamond" : "49th",
    "six of club" : "50th",
    "ace of heart" : "51st",
    "nine of diamond" : "52nd"
}

openai.api_key = os.getenv("OPENAI_API_KEY")

# App framework
st.title('🪄 WondertaleGPT 🃏')
prompt = st.text_input('What card is on your mind?')

if prompt != '':
    try:
        number = stack[prompt.lower()]
    except:
        print("You chose wrong! Magician is never wrong! Try another Card.")

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='write a book title for a novel which could contain this playing card in the book: {topic} but do not explicitly call out in the book title'
)

#script_template = PromptTemplate(
#    input_variables = ['title'], 
#    template='write me 8 chapter subtitles based on this book title: {title}. Do not include any playing card in any of the subtitles.'
#)

story_template = PromptTemplate(
    input_variables = ['topic','title','number'], 
    template='with this book title: {title}, write a 150 words original story involving a playing card: {topic} and a address at {number} Street. Make sure there is no other addresses, playing cards, or numbers in the story. Make sure the card comes before the address in the story.'
)

summary_template = PromptTemplate(
    input_variables = ['story'], 
    template='write image generation prompt for the main scene of the story STORY: {story}.'
)

# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
#script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
story_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
summary_memory = ConversationBufferMemory(input_key='story', memory_key='chat_history')

# Llms
llm = OpenAI(temperature=0.9) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
#script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)
story_chain = LLMChain(llm=llm, prompt=story_template, verbose=True, output_key='story', memory=story_memory)
summary_chain = LLMChain(llm=llm, prompt=summary_template, verbose=True, output_key='summary', memory=summary_memory)

#Show stuff to the screen if there's a prompt
try:
    if prompt and number: 
        title = title_chain.run(prompt)
        #script = script_chain.run(title=title)
        story = story_chain.run(topic=prompt, title=title, number=number)
        summary = summary_chain.run(story=story)
        
    
        # imageprompt = str(summary) + ' in futuristic style'
    
        # response = openai.Image.create(
        #     prompt=imageprompt,
        #     n=1,
        #     size="256x256"
        # )
        # image_url = response['data'][0]['url']
    
        # st.image(image_url)
        image = stableai(str(summary))
        #image = Image.open('/Users/yzlbc8/cardventure/992446758.png')
    
        st.write(title)
        st.image(image)
        #st.write(script)
        st.write(story)
        #st.write(summary)
    
        # with st.expander('Title History'): 
        #     st.info(title_memory.buffer)
    
        # with st.expander('Script History'): 
        #     st.info(script_memory.buffer)
except:
    st.write("You chose wrong! Magician is never wrong! Try another Card.")
