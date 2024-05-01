import streamlit as st

st.set_page_config(
    layout="wide",
    theme={"base": "light"}
)
# title of the app  
st.title('Prescribing diabetes self-management classes')

st.header('Optimal Policy Trees')

st.info('The parameter lambda allows you to control the trade-off between physical health and mental health of the patient. lambda = 0 means that the algorithm will only consider physical health, while lambda = 1 means that the algorithm will only consider mental health.')

# slider bar
x = st.slider('Lambda', min_value=0.0, max_value=1.0, value=0.4, step=0.2)

file = "results/tree1205_lambda="+str(x)
open(file, 'r').read()
st.components.v1.html(open(file, 'r').read(), height=600, width=1500)



st.header('Questionnaire')


st.components.v1.html(open("results/questions_lambda="+str(x), 'r').read(), height=500, width=1000)
