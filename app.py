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

    def create_layout(self):
        # Display the images at the top of the layout if they were loaded successfully
        if image1 is not None and image2 is not None:
            st.image([image1, image2], width=100)  # Adjust width as needed
        
        col1, col2, col3 = st.columns(3)
        # ... rest of the method remains the same ...

class BoilingPointCalculator:
    def __init__(self):
        st.title("بەرزبوونەوەی پلەی کوڵان: ژمێرکاری بۆ تواوەی نا ئەلیکترۆلیتی ")
        self.create_layout()

    def create_layout(self):
        # Display the images at the top of the layout if they were loaded successfully
        if image1 is not None and image2 is not None:
            st.image([image1, image2], width=100)  # Adjust width as needed
        
        col1, col2, col3 = st.columns(3)
        # ... rest of the method remains the same ...

# Main app function
def main():
    # Load images
    global image1, image2
    image1, image2 = load_images()

    st.sidebar.title("Choose Calculator")
    calculator_type = st.sidebar.radio("Select the calculator:", ("Freezing Point", "Boiling Point"))

    if calculator_type == "Freezing Point":
        FreezingPointCalculator()
    elif calculator_type == "Boiling Point":
        BoilingPointCalculator()

if __name__ == "__main__":
    main()
