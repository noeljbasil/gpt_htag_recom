import streamlit as st
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain import PromptTemplate
from langchain import LLMChain

header      = st.container()
description = st.container()
features    = st.container()
output      = st.container()

def generate_hashtags(tweet,number):
    llm = OpenAI(temperature=1)
    tool_names = ["serpapi"]
    tools = load_tools(tool_names)
    gpt = OpenAI(model_name='gpt-3.5-turbo')
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True) #agent that will combine LLMs power with google search
    
    template = """ Generate {number} unique creative hashtags that are relevant to the tweet provided below so that the tweet is trending. The user of the hashtags is a 
    non profit organization called Stop The Traffik (STT) who is helping end human trafficking across the globe and hence the hashtags generated needs to be inline with that of a professional media outlet. 
    If no relevant hashtags can be generated, answer with "No hashtags could be generated for this tweet. Apologies for the inconvenience".
    Tweet: {tweet}
    Hashtags: """

    prompt_template = PromptTemplate(
        input_variables=["tweet","number"],
        template=template
    )

    #next we define the vanilla gpt model which will be used incase agent fails to provide a valid result
    llm_chain = LLMChain(
                                    prompt=prompt_template,
                                    llm=gpt
                                )
    
    try:
        recommended_hashtags = agent.run(prompt_template.format(
                                        tweet=tweet,
                                        number = number
                                    ))
    # If no hashtags were recommended by the agent, or if it maxed out of iterations to try, we will just used the power of davinci model alone to generate the hashtags
        if recommended_hashtags == "No hashtags could be generated for this tweet. Apologies for the inconvenience." or recommended_hashtags == "Agent stopped due to max iterations.":
            recommended_hashtags = llm_chain.run({'tweet':tweet,'number':number})
        else:
            pass
    except:
        recommended_hashtags = llm_chain.run({'tweet':tweet,'number':number})
    if recommended_hashtags == "":
           recommended_hashtags = "No hashtags could be generated for this tweet at this moment. Kindly try again later."
    return (recommended_hashtags)

def main():
    with header:
        st.markdown(""" <style> .title { font-size:35px ; font-family: 'Futura'; color: #fcb900;} </style> """, unsafe_allow_html=True)
        st.markdown('<p class="title">Hashtag Recommender for tweets</p>', unsafe_allow_html=True)

    with description:
        st.markdown(""" <style> .desc { font-size:15px ; font-family: 'Futura'; color: #000000;} </style> """, unsafe_allow_html=True)
        st.markdown('<p class="desc">This tool is developed to help the user generate relevant hashtags for tweets</p>', unsafe_allow_html=True)

    with features:
        tweet                   = {}
        tweet['text']           =  st.text_area('Enter the tweet text')
        tweet['hashtag_number'] =  st.selectbox('Enter the number of hashtags to be generated',( '0', '1', '2', '3','4', '5', '6', '7','8', '9', '10'),10) 
    with output:
        st.markdown(""" <style> .outp { font-size:15px ; font-family: 'Futura'; color: #000000;} </style> """, unsafe_allow_html=True)
        st.markdown('<p class="outp">Recommended hashtags are:</p>', unsafe_allow_html=True)

    if st.button('Click here to generate hashtags'):
        if tweet['text'] != "":
            with st.spinner("Generating hashtags..."):
                with output:
                    hashtags = generate_hashtags(tweet['text'],tweet['hashtag_number'])
                    st.write(hashtags)
        else:
            st.error("Enter tweet to proceed")
if __name__ == "__main__":
    main() 
