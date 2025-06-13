import streamlit as st
from modules.nav import SideBarLinks
import requests 
import pandas as pd 
import json 

from modules.style import style_sidebar
style_sidebar()

SideBarLinks()

st.link_button("Care Compass Blog", 'https://arthur-t-huang.github.io/Care-Compass-Blog/')
st.title("Meet our Team Members!")
st.write('\n\n')
st.write("## Anoushka Abroal")
st.link_button('Email: abroal.a@northeastern.edu', 'abroal.a@northeastern.edu')
st.write('Passionate and highly motivated Northeastern honors college student interested in research opportunities to collaborate on real world challenges using AI, machine learning, and data science. Experienced at working on individual research projects as well as team based initiatives. Detail-oriented and project management-focused about completing my projects on time. Self-driven person who enjoys solving technically challenging problems and researching new approaches to traditional solutions. Eager to take on new challenges and enjoys collaborating with others. Focused on how technology can be leveraged for better healthcare research outcomes. Held leadership roles in school and external clubs. Volunteered with technical teams at the American Diabetes Association. Strong communication and task prioritization skills.')

st.write('\n\n')
st.write("## Arthur Huang")
st.link_button('Email: hunag.arth@northeastern.edu', 'huang.arth@northeastern.edu')
st.write('Arthur Huang is a 18 year old male computer science major with an electrical engineering minor at Northeastern University. He is a very adventurous and team oriented individual who is eager to embark on new projects and opportunites regarding software development and artificial intelligence. In his free time, he enjoys golfing, skiing, and cooking.')

st.write('\n\n')
st.write("## Katherine Ahn")
st.link_button('Email: ahn.ka@northeastern.edu', 'ahn.ka@northeastern.edu')
st.write('Katherine Ahn is a rising fourth year Biology and Math major with minors in Data Science and Global Health at Northeastern University. An aspiring Bioinformatician, Katherine is pursuing a Masters in the field following graduation. Katherine has always been greatly interested in the healthcare sector, and her education at Northeastern has provided her with the tools to look at it from a lens she never considered – through a data filled lens.')

st.write('\n\n')
st.write("## Shiven Ajwaliya")
st.link_button('Email: ajwaliya.s@northeastern.edu', 'ajwaliya.s@northeastern.edu')
st.write('Hi, my name is Shiven Ajwaliya, a CS student at Northeastern University who loves learning new things and traveling. I’m passionate about building meaningful tech products, exploring different cultures, and discovering new places through local food and history.')

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")



