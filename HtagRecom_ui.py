import streamlit as st
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain import PromptTemplate

header      = st.container()
description = st.container()
features    = st.container()
output      = st.container()

def generate_hashtags(tweet,number):
    llm = OpenAI(temperature=1)
    tool_names = ["serpapi"]
    tools = load_tools(tool_names)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=False)
    
    template = """ Generate {number} unique creative hashtags that are relevant to the tweet provided below so that the tweet is trending. The user of the hashtags is a 
    non profit organization called Stop The Traffik (STT) who is helping end human trafficking across the globe and hence the hashtags generated needs to be inline with that of a professional media outlet. 
    If no relevant hashtags can be generated, answer with "No hashtags could be generated for this tweet. Apologies for the inconvenience".

    Tweet: {tweet}

    Hashtags: """

    prompt_template = PromptTemplate(
        input_variables=["tweet","number"],
        template=template
    )
    recommended_hashtags = agent.run(prompt_template.format(
                                    tweet=tweet,
                                    number = number_of_hashtags
                                ))

    return (recommended_hashtags)

def main():
    with header:
        st.markdown(""" <style> .title { font-size:35px ; font-family: 'Futura'; color: #fcb900;} </style> """, unsafe_allow_html=True)
        st.markdown('<p class="title">Hashtag Recommender for tweets</p>', unsafe_allow_html=True)

    with description:
        st.markdown(""" <style> .desc { font-size:15px ; font-family: 'Futura'; color: #ffffff;} </style> """, unsafe_allow_html=True)
        st.markdown('<p class="desc">This tool is developed to help the user generate relevant hashtags for any tweet</p>', unsafe_allow_html=True)

    with features:
        tweet                   = {}
        tweet['text']           =  st.text_area('Enter the tweet text')
        tweet['hashtag_number'] =  st.selectbox('Enter the number of hashtags to be generated',( '0', '1', '2', '3','4', '5', '6', '7','8', '9', '10'),10) 
    with output:
        st.markdown(""" <style> .outp { font-size:15px ; font-family: 'Futura'; color: #ffffff;} </style> """, unsafe_allow_html=True)
        st.markdown('<p class="outp">Recommended hashtags are:</p>', unsafe_allow_html=True)

    if tweet['text'] is not "":
        if st.button('Click here to generate hashtags'):    
            with output:
                hashtags = generate_hashtags(tweet['text'],tweet['hashtag_number'])
                st.write(hashtags)
    
if __name__ == "__main__":
    main() 