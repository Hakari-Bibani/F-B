import streamlit as st
import numpy as np
from PIL import Image
import os

def load_images():
    try:
        current_dir = os.path.dirname(__file__)
        image1_path = os.path.join(current_dir, "image1.jpg")
        image2_path = os.path.join(current_dir, "image2.jpg")
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
        return image1, image2
    except FileNotFoundError:
        st.warning("Image files not found. Displaying app without images.")
        return None, None
    except Exception as e:
        st.error(f"An error occurred while loading images: {str(e)}")
        return None, None

class BaseCalculator:
    def __init__(self, title):
        st.title(title)
        self.create_layout()

    def create_layout(self):
        if image1 is not None and image2 is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.image(image1, use_column_width=True)
                st.caption("م.هەکاری جلال")
            with col2:
                st.image(image2, use_column_width=True)
                st.caption("گروپی تێلێگرام")

        col1, col2, col3 = st.columns(3)

        with col1:
            self.delta_t_input = st.text_input(f"Δ{self.t_symbol}:", key=f"delta_{self.t_symbol.lower()}")
            self.k_input = st.text_input(f"K{self.t_symbol}:", key=f"k{self.t_symbol.lower()}")
            self.molality_input = st.text_input("**molality:**", key="molality")

        with col2:
            self.t_solution_input = st.text_input(f"**پلەی {self.process} گیراوە:**", key="t_solution")
            self.t_solution_unit = st.selectbox("یەکە:", ["Celsius", "Kelvin"], key="t_solution_unit")
            self.t_solvent_input = st.text_input(f"**پلەی {self.process} توێنەر:**", key="t_solvent")
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
        keys_to_clear = [
            f"delta_{self.t_symbol.lower()}", f"k{self.t_symbol.lower()}", "molality", "t_solution", "t_solvent",
            "mass_solute", "mr", "moles_solute", "kg_solvent"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]

        for key in keys_to_clear:
            st.session_state[key] = ""

    def get_float_value(self, key):
        try:
            value = st.session_state[key].strip()
            return float(value) if value else None
        except ValueError:
            return None

    def convert_temperature(self, value, from_unit):
        if value is None:
            return None
        if from_unit == 'Kelvin':
            return value - 273.15
        return value

    def convert_mass(self, value, from_unit, to_unit):
        if value is None or from_unit == to_unit:
            return value
        if from_unit == 'grams' and to_unit == 'kilograms':
            return value / 1000
        if from_unit == 'kilograms' and to_unit == 'grams':
            return value * 1000

    def format_value(self, value):
        return f"{value:.4f}" if value is not None else "unknown"

    def show_calculation_step(self, equation, values, result):
        if equation == f'Δ{self.t_symbol} = گیراوە-T - توێنەر-T':
            values_str = f" = {values[0]:.4f} - {values[1]:.4f}"
        else:
            values_str = " = " + " / ".join(f"{v:.4f}" for v in values)
        st.write(f"{equation}{values_str} = {result:.4f}")

    def try_calculate_value(self, inputs, param_name, calculation_func, equation, params_needed):
        if inputs[param_name] is None and all(inputs[p] is not None for p in params_needed):
            values = [inputs[p] for p in params_needed]
            result = calculation_func(*values)
            self.show_calculation_step(equation, values, result)
            inputs[param_name] = result
            return True
        return False

    def calculate(self):
        st.write("هەنگاوەکانی ژمێرکاری")
        st.write("-" * 50)

        inputs = {
            f'delta_{self.t_symbol.lower()}': self.get_float_value(f"delta_{self.t_symbol.lower()}"),
            f'k{self.t_symbol.lower()}': self.get_float_value(f"k{self.t_symbol.lower()}"),
            'molality': self.get_float_value("molality"),
            't_solution': self.get_float_value("t_solution"),
            't_solvent': self.get_float_value("t_solvent"),
            'mass_solute': self.get_float_value("mass_solute"),
            'mr': self.get_float_value("mr"),
            'moles_solute': self.get_float_value("moles_solute"),
            'kg_solvent': self.get_float_value("kg_solvent")
        }

        inputs['t_solution'] = self.convert_temperature(
            inputs['t_solution'],
            st.session_state.t_solution_unit
        )
        inputs['t_solvent'] = self.convert_temperature(
            inputs['t_solvent'],
            st.session_state.t_solvent_unit
        )
        if inputs['mass_solute'] is not None:
            inputs['mass_solute'] = self.convert_mass(
                inputs['mass_solute'],
                st.session_state.mass_solute_unit,
                'grams'
            )
        if inputs['kg_solvent'] is not None:
            inputs['kg_solvent'] = self.convert_mass(
                inputs['kg_solvent'],
                st.session_state.kg_solvent_unit,
                'kilograms'
            )

        calculations = [
            {
                'param': f'delta_{self.t_symbol.lower()}',
                'func': lambda k, m: k * m,
                'equation': f'Δ{self.t_symbol} = K{self.t_symbol} × molality',
                'params': [f'k{self.t_symbol.lower()}', 'molality']
            },
            {
                'param': f'delta_{self.t_symbol.lower()}',
                'func': lambda ts, tsv: ts - tsv,
                'equation': f'Δ{self.t_symbol} = گیراوە-T - توێنەر-T',
                'params': ['t_solution', 't_solvent']
            },
            {
                'param': 'molality',
                'func': lambda dt, k: dt / k,
                'equation': f'molality = Δ{self.t_symbol} / K{self.t_symbol}',
                'params': [f'delta_{self.t_symbol.lower()}', f'k{self.t_symbol.lower()}']
            },
            {
                'param': 'molality',
                'func': lambda mol, kg: mol / kg,
                'equation': 'molality = تواوە-mole / توێنەر-Kg',
                'params': ['moles_solute', 'kg_solvent']
            },
            {
                'param': 'moles_solute',
                'func': lambda mass, mr: mass / mr,
                'equation': 'تواوە-mole = تواوە-mass / Mr',
                'params': ['mass_solute', 'mr']
            },
            {
                'param': 'moles_solute',
                'func': lambda m, kg: m * kg,
                'equation': 'تواوە-mole = molality × توێنەر-Kg',
                'params': ['molality', 'kg_solvent']
            },
            {
                'param': 'mass_solute',
                'func': lambda mol, mr: mol * mr,
                'equation': 'تواوە-mass = تواوە-mole × Mr',
                'params': ['moles_solute', 'mr']
            },
            {
                'param': 'kg_solvent',
                'func': lambda mol, m: mol / m,
                'equation': 'توێنەر-Kg = تواوە-mole / molality',
                'params': ['moles_solute', 'molality']
            },
            {
                'param': 'mr',
                'func': lambda mass, mol: mass / mol,
                'equation': 'Mr = تواوە-mass / تواوە-mole',
                'params': ['mass_solute', 'moles_solute']
            }
        ]

        while True:
            changed = False
            for calc in calculations:
                if self.try_calculate_value(
                    inputs,
                    calc['param'],
                    calc['func'],
                    calc['equation'],
                    calc['params']
                ):
                    changed = True
            if not changed:
                break

        st.write("-" * 50)
        st.write("ئەنجامەکانی کۆتایی:")
        for key, value in inputs.items():
            st.write(f"{key}: {self.format_value(value)}")

class FreezingPointCalculator(BaseCalculator):
    def __init__(self):
        self.t_symbol = "Tf"
        self.process = "بەستن"
        super().__init__("نزمبونەوەی پلەی بەستن: ژمێرکاری بۆ تواوەی نا ئەلیکترۆلیتی")

class BoilingPointCalculator(BaseCalculator):
    def __init__(self):
        self.t_symbol = "Tb"
        self.process = "کوڵان"
        super().__init__("بەرزبوونەوەی پلەی کوڵان: ژمێرکاری بۆ تواوەی نا ئەلیکترۆلیتی")

def main():
    global image1, image2
    image1, image2 = load_images()

    st.sidebar.title("Choose Calculator")
    calculator_type = st.sidebar.radio("Select the calculator:", ("Freezing Point", "Boiling Point"))

    if calculator_type == "Freezing Point":
        FreezingPointCalculator()
    elif calculator_type == "Boiling Point":
        BoilingPointCalculator()

    st.markdown("---")
    st.markdown(""" <p style='text-align: center; color: gray; font-style: italic;'> بۆ یەکەمین جار ئەم جۆرە بەرنامەیە دروستکراوە و گەشەی پێدراوە لە کوردستان و عێراق دا. هیوادارم سوودی لێوەربگرن.
    م. هەکاری جلال محمد </p> """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
