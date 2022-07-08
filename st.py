import streamlit as st
import main

updater = main.updater()


# def onClickUpdate():
#     st.write('Values:', values)
#     bp.update(values[0], values[1])


# page_type = st.radio(
#      "Which sheet do you want to update?",
# #      ('Influencer', 'Business page'))
# page_type = st.sidebar.button('Influencer')
# page_type = st.sidebar.button('Business page')


     
st.title('Price Updater')


# values = st.slider(
#      'Select a range',
#      2, 100, (2, 100), step=1)


@st.cache(suppress_st_warning=True)
def onClickUpdate():
     updater.post_prices(starting_row, ending_row, st)
#      st.sucess('Process Done!')

# st.write('Done!') 
with st.sidebar:
    updating_type = st.sidebar.selectbox(
    "select updating source:",
    ("Data base", "Abzarchi")
)
    st.write(updating_type, 'is selected.')
    starting_row = st.number_input('Insert starting row number', min_value=0, help='You need to enter starting row of your database table')
    st.write('The starting row is: ', starting_row)
    
    ending_row = st.number_input('Insert ending row number', min_value = starting_row + 1, max_value=starting_row + 99)
    st.write('The ending row is: ', ending_row)

    updateButton = st.button('Update Date', on_click=onClickUpdate)
if updating_type == 'Data base':
     st.subheader('Data base')
     st.dataframe(updater.get_data())

