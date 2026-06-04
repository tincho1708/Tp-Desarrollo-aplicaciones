import streamlit as st
st.title("papa")
st.subheader("gestion profesional de papas")

nombre = st.text_input("Nombre de la papa:")
if st.button("Saludar"):
    st.write(f"Hola {nombre}, bienvenido a su papa"s)