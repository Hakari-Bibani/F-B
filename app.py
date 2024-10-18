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
        if 'image1' in globals() and 'image2' in globals() and image1 is not None and image2 is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.image(image1, use_column_width=True)
                st.caption("م.هەکاری جلال")
            with col2:
                st.image(image2, use_column_width=True)
                st.caption("گروپی تێلێگرام")

        col1, col2, col3 = st.columns(3)

        with col1:
            self.delta_tf_input = st.text_input("ΔTf:", key="delta_tf")
            self.kf_input = st.text_input("Kf:", key="kf")
            self.molality_input = st.text_input("**molality:**", key="molality")

        with col2:
            self.t_solution_input = st.text_input("**پلەی بەستنی گیراوە:**", key="t_solution")
            self.t_solution_unit = st.selectbox("یەکە:", ["Celsius", "Kelvin"], key="t_solution_unit")
            self.t_solvent_input = st.text_input("**پلەی بەستنی توێنەر:**", key="t_solvent")
            self.t_solvent_unit = st.selectbox("یەکە:", ["Celsius", "Kelvin"], key="t_solvent_unit")

        with col3:
            self.mass_solute_input = st.text_input("**بارستەی تواوە:**", key="mass_solute")
            self.mass_solute_unit = st.selectbox("یەکە:", ["grams", "kilograms"], key="mass_solute_unit")
            self.mr_input = st.text_input("**بارستەی مۆڵی  Mr:**", key="mr")
            self.moles_solute_input = st.text_input("**مۆڵی تواوە:**", key="moles_solute")
            self.kg_solvent_input = st.text_input("**بارستەی توێنەر:**", key="kg_solvent")
            self.kg_solvent_unit = st.selectbox("یەکە:", ["grams", "kilograms"], key="kg_solvent_unit")

        col1, col2 = st.columns(2)
        with col1:
            self.calculate_button = st.button("**ژمێرکاری**", key="calculate")
        with col2:
            self.clear_button = st.button("**سڕینەوە**", key="clear")

        if self.calculate_button:
            self.calculate()
        if self.clear_button:
            self.clear_inputs()

    def clear_inputs(self):
        for key in st.session_state.keys():
            if key.startswith(('delta_tf', 'kf', 'molality', 't_solution', 't_solvent', 'mass_solute', 'mr', 'moles_solute', 'kg_solvent')):
                st.session_state[key] = ""

    def calculate(self):
        st.write("هەنگاوەکانی ژمێرکاری")
        st.write("-" * 50)
        # Implement calculation logic here
        st.write("Calculation logic to be implemented")
        st.write("-" * 50)

class BoilingPointCalculator:
    def __init__(self):
        st.title("بەرزبوونەوەی پلەی کوڵان: ژمێرکاری بۆ تواوەی نا ئەلیکترۆلیتی ")
        self.create_layout()

    def create_layout(self):
        # Implement similar layout as FreezingPointCalculator
        st.write("Boiling Point Calculator layout to be implemented")

    def calculate(self):
        st.write("Boiling Point calculation logic to be implemented")

def main():
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
