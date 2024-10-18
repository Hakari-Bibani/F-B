import streamlit as st
import numpy as np
from PIL import Image
import os

def load_images():
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(__file__)
        
        # Construct the full path to the images
        image1_path = os.path.join(current_dir, "image1.jpg")
        image2_path = os.path.join(current_dir, "image2.jpg")
        
        # Open the images
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        
        return image1, image2
    except FileNotFoundError:
        st.warning("Image files not found. Displaying app without images.")
        return None, None
    except Exception as e:
        st.error(f"An error occurred while loading images: {str(e)}")
        return None, None

class FreezingPointCalculator:
    def __init__(self):
        st.title("نزمبونەوەی پلەی بەستن: ژمێرکاری بۆ تواوەی نا ئەلیکترۆلیتی")
        self.create_layout()

    # ... (rest of the FreezingPointCalculator class remains unchanged)

class BoilingPointCalculator:
    def __init__(self):
        st.title("بەرزبوونەوەی پلەی کوڵان: ژمێرکاری بۆ تواوەی نا ئەلیکترۆلیتی ")
        self.create_layout()

    # ... (rest of the BoilingPointCalculator class remains unchanged)

def main():
    global image1, image2
    image1, image2 = load_images()

    st.sidebar.title("هەڵبژاردنی ژمێرکاری")
    calculator_type = st.sidebar.radio("هەڵبژاردنی ژمێرکاری:", ("نزمبونەوەی پلەی بەستن", "بەرزبونەوەی پلەی کوڵان"))

    if calculator_type == "نزمبونەوەی پلەی بەستن":
        FreezingPointCalculator()
    elif calculator_type == "بەرزبونەوەی پلەی کوڵان":
        BoilingPointCalculator()

# Add the footer sentence
st.markdown(""" <p style='text-align: center; color: gray; font-style: italic;'> بۆ یەکەمین جار ئەم جۆرە بەرنامەیە دروستکراوە و گەشەی پێدراوە لە کوردستان و عێراق دا. هیوادارم سوودی لێوەربگرن.
م. هەکاری جلال محمد </p> """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
