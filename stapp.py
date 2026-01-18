import streamlit as st

#streamlit run stapp.py
#Title of the app

st.title('Body Mass Index App')

st.image('bmi.jpg', caption = 'Body Mass Index Infographics')

weight = st.number_input('Enter your weight (in KGs)')
status = st.radio ('Select your height format:', ('cms', 'meters', 'feet'))

#Compare the status
if status == 'cms':
    height = st.number_input('Centimeters')
    try: 
        bmi = weight / ((height/100)**2)
    except:
        st.text('Enter some value of height.')
elif status == 'meters':
    height = st.number_input('Meters')
    try: 
        bmi = weight / (height**2)
    except:
        st.text('Enter some value of height.')
else:
    height = st.number_input('Feet')
    try: 
        bmi = weight / ((height/3.28)**2)
    except:
        st.text('Enter some value of height.')


#Check if the button is priced or not
if st.button('Calculate BMI'):
    st.text(f'Your BMI Index is: {bmi}')

    #Give interpretation of BMI index
    if bmi < 16:
        st.error('You are extremely underweight.')
    elif bmi >= 16 and bmi < 18.5:
        st.warning('You are underweight.')
    elif bmi >= 18.5 and bmi < 25:
        st.warning('You are healthy.')
    elif bmi >= 25 and bmi < 30:
        st.warning('You are overweight.')
    else:
        st.warning('You are extremely overweight. Eat some more donuts.')

        