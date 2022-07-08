import streamlit as st
import BP2

bp = BP2.BP_Updater()


# def onClickUpdate():
#     st.write('Values:', values)
#     bp.update(values[0], values[1])


# page_type = st.radio(
#      "Which sheet do you want to update?",
# #      ('Influencer', 'Business page'))
# page_type = st.sidebar.button('Influencer')
# page_type = st.sidebar.button('Business page')


     
st.title('Database Updater')


# values = st.slider(
#      'Select a range',
#      2, 100, (2, 100), step=1)


@st.cache(suppress_st_warning=True)
def onClickUpdate():
     bp.update(starting_row, ending_row, st, page_type)
#      st.sucess('Process Done!')

# st.write('Done!') 
with st.sidebar:
    page_type = st.sidebar.selectbox(
    "Which would you like to update?",
    ("Influencer", "Business page")
)
    st.write(page_type, 'is selected.')
    starting_row = st.number_input('Insert starting row number', min_value=0, help='You need to enter starting row of your database table')
    st.write('The starting row is: ', starting_row)
    
    ending_row = st.number_input('Insert ending row number', min_value = starting_row + 1, max_value=10000)
    st.write('The ending row is: ', ending_row)

    updateButton = st.button('Update Date', on_click=onClickUpdate)
if page_type == 'Influencer':
     st.subheader('Influencer.')
     st.dataframe(bp.get_data('Contact influencer'))
elif page_type == 'Business page':
     st.subheader("Business page.")
     st.dataframe(bp.get_data('contact business page'))
elif page_type == 'Telegram':
     st.subheader("Telegram.")
     st.dataframe(bp.get_data('Telegram'))   
