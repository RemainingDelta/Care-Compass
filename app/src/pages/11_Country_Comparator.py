import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from tkinter import *  

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title("Country Comparator")

#CHANGE CODE
root = Tk()  
root.geometry("200x200")  

def show():  
    lbl.config(text=opt.get())  

# Dropdown options  
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]  

# Selected option variable  
opt = StringVar(value="Monday")  

# Dropdown menu  
OptionMenu(root, opt, *days).pack()  

# Button to update label  
Button(root, text="Click Me", command=show).pack()  

lbl = Label(root, text=" ")  
lbl.pack()  

root.mainloop()  
