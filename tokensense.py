# ----------------- Import Libraries and Data ----------------- #

import streamlit as st
import streamlit.components.v1 as components

import plotly.graph_objects as go
import pandas as pd

import pickle

# Load the pyLDAvis pickle
with open('sentiment_pickles/pickle_pyLDAvis.pickle', 'rb') as read_file:
    lda_vis_html = pickle.load(read_file)

# Load topic labes\ls
topic_labels_df = pd.read_csv('sentiment_pickles/topic_labels.csv')

# ----------------- Streamlit Formatting ----------------- #

# Wide layout
st.set_page_config(layout='wide')

st.markdown(
    """
    <style>
    .reportview-container {
        background-image: linear-gradient(to bottom right, #000000, #0c0c0c, #1f1f1f, #444444, #676767, #989898, #adadad);
        color: #110022;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ----------------- Streamlit Functions ----------------- #

def make_title(pages, color):
    st.image('sentiment_images/tokensense_title.png', width=500)
    st.markdown("<h1 style='text-align: left; color: "+color+";'>"+pages+"</h1>", unsafe_allow_html=True)


def show_plotly(df):
    series_list = [df[col] for col in df]
    fig = go.Figure(data=[go.Table(header=dict(values=list(df.columns),
                                               fill_color='#b90202',
                                               font_color='#FFFFFF',
                                               align='left',
                                               font=dict(color='#000000', size=14),
                                               line=dict(color='#000000'),
                                               height=30),
                                   cells=dict(values=series_list,
                                              fill_color='#FFFFFF',
                                              align='left',
                                              font=dict(color='#000000', size=12),
                                              line=dict(color='#000000'),
                                              height=30),
                                   columnwidth=[1, 2]
                                  )])
    
    fig.update_layout(margin=dict(l=5, r=5, t=10), paper_bgcolor='rgba(0,0,0,0)', height=1000)
    st.plotly_chart(fig, use_container_width=True)
    
    
# ----------------- Streamlit Page Construction ----------------- #

pages = st.sidebar.selectbox('',
                             ('Daily Sentiment Dashboard', 
                              'Reddit Sentiment',
                              'Activity vs. Price',
                              'Sentiment Cluster Analysis',
                              'Topic Modeling Over Time', 
                              'Topic Polarity vs. Subjectivity',
                              'Topic Deep Dive',
                              'Latent Dirichlet Allocation Viz'
                             ))
st.sidebar.write('---')
st.sidebar.write("""TokenSense was built by David Wismer. Find me on [LinkedIn](https://www.linkedin.com/in/david-wismer-0a940656/).""")

st.sidebar.write('---')
st.sidebar.write("""Visit my [Github](https://github.com/drwismer) to see how the app was built. You'll also find notebooks detailing data collection, EDA, and the modeling process.""")

left, middle, right = st.sidebar.beta_columns([0.65, 3, 1])
with middle:
    st.image('sentiment_images/tokensense_logo.png', width=200)


if pages == 'Daily Sentiment Dashboard':
    
    make_title(pages, 'white')
    
    html = """
    <div class='tableauPlaceholder' id='viz1626301166268' style='position: relative'><noscript><a href='#'><img alt='Daily Sentiment ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;DailySentiment&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;DailySentiment' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;DailySentiment&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626301166268');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1581px';vizElement.style.height='1527px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1581px';vizElement.style.height='1527px';} else { vizElement.style.width='100%';vizElement.style.height='4127px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """

    components.html(html, width=1650, height=3000)

if pages == 'Reddit Sentiment':
    
    make_title(pages, 'white')
    
    html = """
    <div class='tableauPlaceholder' id='viz1626301294133' style='position: relative'><noscript><a href='#'><img alt='Reddit Sentiment ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;RedditSentiment&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;RedditSentiment' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;RedditSentiment&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626301294133');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1527px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """

    components.html(html, width=1650, height=950)

elif pages == 'Activity vs. Price':
    
    make_title(pages, 'white')
    
    html = """
     <div class='tableauPlaceholder' id='viz1626302331641' style='position: relative'><noscript><a href='#'><img alt='Activity vs Price ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;ActivityvsPrice&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;ActivityvsPrice' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;ActivityvsPrice&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626302331641');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1577px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1700, height=900)
    
elif pages == 'Sentiment Cluster Analysis':
    
    make_title(pages, 'white')
    
    html = """
     <div class='tableauPlaceholder' id='viz1626717865566' style='position: relative'><noscript><a href='#'><img alt='Sentiment Clusters ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;SentimentClusters&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;SentimentClusters' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;SentimentClusters&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626717865566');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1711px';vizElement.style.height='4027px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1711px';vizElement.style.height='4027px';} else { vizElement.style.width='100%';vizElement.style.height='6027px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1700, height=4000)
    
if pages == 'Topic Modeling Over Time':
    
    make_title(pages, 'white')
    
    html = """
    <div class='tableauPlaceholder' id='viz1626299015956' style='position: relative'><noscript><a href='#'><img alt='Topic Prevalence and Sentiment ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicPrevalenceandSentiment&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;TopicPrevalenceandSentiment' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicPrevalenceandSentiment&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626299015956');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1689px';vizElement.style.height='2087px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1689px';vizElement.style.height='2087px';} else { vizElement.style.width='100%';vizElement.style.height='1477px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=2000, height=3000)
    
elif pages == 'Topic Polarity vs. Subjectivity':
    
    make_title(pages, 'white')
    
    html = """
    <div class='tableauPlaceholder' id='viz1626286247872' style='position: relative'><noscript><a href='#'><img alt='Topic Polarity and Subjectivity ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicPolarityandSubjectivity&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;TopicPolarityandSubjectivity' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicPolarityandSubjectivity&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626286247872');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1500px';vizElement.style.height='927px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1500px';vizElement.style.height='927px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1500, height=900)

elif pages == 'Topic Deep Dive':
    
    make_title(pages, 'white')
    
    html = """
     <div class='tableauPlaceholder' id='viz1626299532726' style='position: relative'><noscript><a href='#'><img alt='Topic Deep Dive ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicDeepDive&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;TopicDeepDive' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicDeepDive&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626299532726');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1710px';vizElement.style.height='1027px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1710px';vizElement.style.height='1027px';} else { vizElement.style.width='100%';vizElement.style.height='1477px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1710, height=1000)
    
elif pages == 'Latent Dirichlet Allocation Viz':
    
    st.markdown(
        """
        <style>
        .reportview-container {
            background-image: linear-gradient(to bottom, #000000 0%, #0c0c0c 5%, #1f1f1f 10%, #444444 14%, #676767 17%, #989898 20%, #a0a0a0 22%, #cbcbcb 24%, #ffffff 25%);
            color: #110022;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    make_title(pages, 'red')
    
    left, right = st.beta_columns([1, 3])
    
    with left:
        show_plotly(topic_labels_df)        
    
    with right:
        components.html(lda_vis_html, width=1500, height=900)

