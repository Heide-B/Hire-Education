import streamlit as st
import pandas as pd
import numpy as np
import base64
import spacy
import re
import random
nlp = spacy.load("en_core_web_sm")

df_all = pd.read_csv("courses_clean.csv", index_col=0)
df = pd.read_csv("combined.csv")


def find_job(response, job_titles):
    jobs = pd.DataFrame()
    jobs = df[df['Dominant_Topic'] == response].reset_index()
    for num in range(5):
        job_id = random.randint(0,len(jobs))
        job_titles.append(jobs['title'].iloc[job_id])
    return job_titles

def search_courses(to_search):
    search = df[df['title'] == to_search]['Dominant_Topic'].unique()
    search = ''.join(search)
    ## Input search keyword here
    search_in = nlp(search.lower())
    
    if search == 'Data Engineering':
        search_terms = ['developer','analyst','sap','engineer','java','sql','.net','manager','salesforce','web']
    elif search == 'Modelling/Analysis':
        search_terms = ['use','product','least','modeling','analytical','portfolio','statistic','excel','environment','machine']
    elif search == 'Data Storytelling':
        search_terms = ['machine','use','visualization','portfolio','python','product','sql','tableau','vendor','member']
    elif search == 'Business Application':
        search_terms = ['marketing','update','evaluation','resolve','message','budgets','upload','activities','kpis forecast','predict']

    ## Getting the nlp similarity score of each term in "search_terms" and "search_in" 
#    results = pd.DataFrame()
#    for term in search_terms:
#        t = nlp(term)
#        score = t.similarity(search_in)
#        t = {'term': term,'score':score}
#        results = results.append(t, ignore_index = True)
#    top_terms = results.sort_values(by="score",ascending=False).head(3)["term"].values.tolist()

    ## The top 3 skills based on similarity to aid in filtering
#    courses = pd.DataFrame()
#    for term in top_terms:
#        tmp = df_all[df_all["skill"] == term]
#        courses = pd.concat([courses,tmp],ignore_index=True)

    ## Filtering the courses in two steps. 
    ## [1] Get the similarity of search item and the course title,
    ## [2] Sort courses based on comments_score and rating
    ## [3] Sort courses based on similarity score and drop duplicates based on title
    
    for term in search_terms:
        t = nlp(term)
        for i in range(len(df_all)):
            score = t.similarity(df_all['title'][i])
            df_all['similarity'][i] = score
#    df_all['similarity'] = df_all['title'].apply(lambda x: nlp(x.lower()).similarity(search_terms[1]) )
    
    similarity_df = df_all.sort_values(by=["comments_score","rating"],ascending=False)
    similarity_df = similarity_df.sort_values(by=["similarity"],ascending=False).drop_duplicates(subset=["title"]).head(3)

    # Pretty output mehehe
    for _,row in similarity_df.iterrows():
        st.markdown(f"""## {(row["title"])}""")
        st.write(f"""Enrollees: {int(row["student"])}""")
        st.write(f"""    Price: ${row["price"].replace("$","")}""")
        st.write(f"""   Rating: {round(row["rating"],2)}""")
        st.write(f"""    Skill: {row["skill"]}""")
        st.write(f"""     Link: {(row["link"]).replace("//course","/course")}""")
        st.write(f"""Sentiment: {row["sentiment"]}""")
        st.write(f""" Comments: {re.sub("  ","",row["comments"])}""")
        st.markdown("""---""")


my_page = st.sidebar.radio('Page Navigation',['The Goal','The Data','Our Methods','Hire Education Recommender'])

main_bg = "bg1.png"
main_bg_ext = "png"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.subheader('The Team')
st.sidebar.write('Beverly Lumbera')
st.sidebar.write('Eunice Grullo')
st.sidebar.write('Heide Balcera')
st.sidebar.write('Bym Buhain')
st.sidebar.write('Dan Pablo')
st.sidebar.write('Jay Silverio')


st.sidebar.subheader('The Mentor')
st.sidebar.write('Patrisha Estrada')

if my_page == 'The Goal':
    st.title("Hire Education")
    st.header("Learn the skills you need for the job you want")

    st.write('<iframe src="https://docs.google.com/presentation/d/e/2PACX-1vThSZklr6j_oC1Dpv3VVaC6g7Wmuo05_bIN0nz2BMYyiXfMAvtaxbpBV7IILGBbVQuyzlxg6GcMYKin/embed?start=false&loop=false&delayms=3000" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>',unsafe_allow_html=True)
    
elif my_page == 'The Data':
    st.title("What Data Do We Use")
    st.write('To ensure that we recommend you only the highest quality courses to learn the most in demand skills as declared by the current job market, we carefully selected the data that we use for our models and engine.')
    st.header("Job Sites Data")
    st.subheader("From Jobstreet and Monster")

    st.write(df.head(20))
    
    st.header("Course Sites Data")
    st.subheader("From Coursera and Udemy")

    st.write(df_all.head(20))

elif my_page == 'Our Methods':
    st.title("Data")
    st.header("Public School Data in the Philippines")

    st.write(df.head(20))

elif my_page == 'Hire Education Recommender':
    st.title("Hire Education Recommender Engine")
    st.header("Learn the skills you need for the job you want")

    response = st.selectbox('Choose Your Field of Specialization', ['','Data Engineering','Modelling/Analysis','Data Storytelling','Business Application'])
    if response != '':
        job_titles=[]
        find_job(response, job_titles)
        user_input = st.selectbox('Choose Your Potential Job!', job_titles)
        "Here are some courses to help you get hired as a/n: ", user_input
        if user_input != '':
            search_courses(user_input)
