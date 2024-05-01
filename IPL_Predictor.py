import base64
import streamlit as st
import pickle
import pandas as pd
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("background.jpg")
# data:image/png;base64,{img}
page_bg_img = f"""

<style>

[data-testid="stFullScreenFrame"]{{
display:flex;
align-items:center;
justify-content:center;
}}

[data-testid="stFullScreenFrame"] > div{{
width: 140px !important;
}}

[data-baseweb="select"] > div {{
background-color: white !important;
color:black !important;
}}

[data-baseweb="select"] > div > div > div > input{{
color:black !important;
}}

[data-baseweb="select"] > div > div > svg{{
color:black !important;
}}

[data-testid="stNumberInput"]{{
outline : none !important;
}}

[data-testid="stNumberInputContainer"] {{
height : 50px;
background-color : white;
outline : none;
border: 2px solid black;
}}

[data-testid="stNumberInputContainer"]:focus-within {{
border:2px solid blue;
}}

[data-testid="stNumberInputContainer"] > div > button {{
outline : none !important;
color:black;
background-color:white !important;
}}

[data-testid="stNumberInputContainer"] > div > button:hover {{
outline : none !important;
color:red;
background-color:green !important;
}}

[data-testid="stNumberInputContainer"] > div > div{{
outline : none !important;
background-color:white;
}}

[data-testid="stNumberInputContainer"] > div > div > input{{
font-size:22px;
color:black;
}}

[data-testid="stButton"] > button {{
background-color:transparent !important;
border: 2px solid white;
color:white;
}}

[data-testid="stButton"] > button:hover {{
background-color:white !important;
border: none;
color:black !important;
border-radius:0px;
transition : 400ms ease-in-out;
}}

[data-testid="stButton"] > button:focus {{
background-color:transparent !important;
border: 2px solid white !important;
color:white !important;
}}

[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
width: 100%;
height:100%
background-repeat: no-repeat;
background-attachment: fixed;
background-size: cover;
}}

[data-testid="stSidebar"] > div:first-child {{
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
color:white;
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}

[data-testid="stMarkdownContainer"] > div > h2 > div > span{{
    color:red;
}}

</style>
"""
teams =['--- Select ---',
        'Chennai Super Kings',
        'Delhi Capitals',
        'Gujarat Titans',
        'Kolkata Knight Riders',
        'Lucknow Super Giants',
        'Mumbai Indians',
        'Punjab Kings',
        'Rajasthan Royals',
        'Royal Challengers Bangalore',
        'Sunrisers Hyderabad']


venues =['--- Select ---','Eden Gardens','Wankhede Stadium','M Chinnaswamy Stadium','Feroz Shah Kotla',
'Dubai International Cricket Stadium','MA Chidambaram Stadium, Chepauk','Sawai Mansingh Stadium',
'Rajiv Gandhi International Stadium, Uppal','Punjab Cricket Association Stadium, Mohali',
'Wankhede Stadium, Mumbai','Sheikh Zayed Stadium','Sharjah Cricket Stadium','Dr DY Patil Sports Academy, Mumbai',
'Brabourne Stadium, Mumbai','Kingsmead',
'Rajiv Gandhi International Stadium',
'M.Chinnaswamy Stadium',
'Maharashtra Cricket Association Stadium',
'Arun Jaitley Stadium',
'Dr DY Patil Sports Academy',
'Maharashtra Cricket Association Stadium, Pune',
'Sardar Patel Stadium, Motera',
'SuperSport Park',
'Brabourne Stadium',
'MA Chidambaram Stadium, Chepauk, Chennai',
'Punjab Cricket Association IS Bindra Stadium',
'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
'Himachal Pradesh Cricket Association Stadium',
'MA Chidambaram Stadium',
'Punjab Cricket Association IS Bindra Stadium, Mohali',
'New Wanderers Stadium',
'Zayed Cricket Stadium, Abu Dhabi',
'Holkar Cricket Stadium',
'JSCA International Stadium Complex',
"St George's Park",
'Narendra Modi Stadium, Ahmedabad',
'Subrata Roy Sahara Stadium',
'Newlands',
'Barabati Stadium',
'Shaheed Veer Narayan Singh International Stadium',
'Arun Jaitley Stadium, Delhi',
'Saurashtra Cricket Association Stadium',
'Vidarbha Cricket Association Stadium, Jamtha',
'De Beers Diamond Oval',
'Buffalo Park',
'Eden Gardens, Kolkata',
'OUTsurance Oval',
'Nehru Stadium',
'Green Park'
]

pipe = pickle.load(open('pipe.pkl','rb'))


st.markdown(page_bg_img, unsafe_allow_html=True)
st.image('Indian-Premier-League-Logo.png')
st.markdown("""
    # **IPL MATCH PREDICTION**            
""")

col1, col2 = st.columns(2)

with col1:
   
   batting_team =  st.selectbox('Select Batting Team',teams)

with col2:
    if batting_team == '--- select ---':
        bowling_team = st.selectbox('Select Bowling Team', teams)
    else:
        filtered_teams = [team for team in teams if team != batting_team]
        bowling_team = st.selectbox('Select Bowling Team', filtered_teams)

venue = st.selectbox('Select Venue',venues)

target = st.number_input('Target',step=1,min_value=1)

col1,col2,col3 = st.columns(3)

with col1:
    score = st.number_input('Score',step=1,min_value=0)
with col2:
    overs = st.number_input("Over Completed",step=1,min_value=0,max_value=19)
with col3:
    wickets = st.number_input("wicktes down",step=1,min_value=0,max_value=10)

if st.button('Predict Winning Probability'):
    try:
        runs_left = target - score
        balls_left = 120 - (overs*6)
        wickets = 10-wickets
        crr = score/overs
        rrr = runs_left/(balls_left/6)
        input_data = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'venue':[venue],'required_runs':[runs_left],'balls_left':[balls_left],'wickets_remaining':[wickets],'total_run_x':[target],'crr':[crr],'req_rr':[rrr]})
        result = pipe.predict_proba(input_data)
        loss = result[0][0]
        win =  result[0][1]
        st.header(batting_team + " = "+str(round(win*100)) + "%")
        st.header(bowling_team + " = "+str(round(loss*100)) + "%")
        st.header("Current Run Rate = " + str(round(crr)))
        st.header("Required Run Rate = " + str(round(rrr)))
    except:
        st.header("Some error occured. Please check inputs!!")
