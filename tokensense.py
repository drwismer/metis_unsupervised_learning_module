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

def blurb(text, color):
    st.markdown("<p style='text-align: left; color: "+color+";'>"+text+"</p>", unsafe_allow_html=True)


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

st.sidebar.write('---')
st.sidebar.write("""Find the entire Tableau Public workbook on my [Tableau profile](https://public.tableau.com/app/profile/david.wismer).""")

left, middle, right = st.sidebar.beta_columns([0.65, 3, 1])
with middle:
    st.image('sentiment_images/tokensense_logo.png', width=200)


if pages == 'Daily Sentiment Dashboard':
    
    make_title(pages, 'white')
    
    blurb('A date can be selected in the far right container. The red dots in the box plots show the level of each metric for the selected date.', 'white')
    blurb('Use the date range selector to adjust the dates shown. This also adjusts the data fed to the boxplots, color coding, and the remainder of the dashboard.', 'white')
    
    html = """
    <div class='tableauPlaceholder' id='viz1626301166268' style='position: relative'><noscript><a href='#'><img alt='Daily Sentiment ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;DailySentiment&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;DailySentiment' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;DailySentiment&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626301166268');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1581px';vizElement.style.height='1527px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1581px';vizElement.style.height='1527px';} else { vizElement.style.width='100%';vizElement.style.height='4127px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """

    components.html(html, width=1650, height=3000)

if pages == 'Reddit Sentiment':
    
    make_title(pages, 'white')
    
    blurb('This dashboard shows the average comment sentiment for the top 100 comments in the r/Bitcoin Daily Discussion Thread for each date.  ' +
          'Note that the upper and lower bounds reflect one standard deviation from the mean.', 'white')
    blurb('A date can be selected in the far right container. The red dots in the box plots show the level of each metric for the selected date.', 'white')
    blurb('Use the date range selector to adjust the dates shown. This also adjusts the data fed to the boxplots, color coding, and the remainder of the dashboard.', 'white')
    blurb('The Moving Average Days parameter adjusts the bold MA lines.', 'white')
    
    html = """
    <div class='tableauPlaceholder' id='viz1626301294133' style='position: relative'><noscript><a href='#'><img alt='Reddit Sentiment ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;RedditSentiment&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;RedditSentiment' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;RedditSentiment&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626301294133');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1527px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """

    components.html(html, width=1650, height=950)

elif pages == 'Activity vs. Price':
    
    make_title(pages, 'white')
    
    blurb('This dashboard shows various activity metrics, plotted against Bitcoin price (log scale).  Activity metrics included trading volume (Coinbase), ' +
          'active addresses, Google trends data, and number of Reddit comments on the daily discussion thread.', 'white')
    blurb('A date can be selected in the far right container. The red dots in the box plots show the level of each metric for the selected date.', 'white')
    blurb('Use the date range selector to adjust the dates shown. This also adjusts the data fed to the boxplots, color coding, and the remainder of the dashboard.', 'white')
    
    html = """
     <div class='tableauPlaceholder' id='viz1626302331641' style='position: relative'><noscript><a href='#'><img alt='Activity vs Price ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;ActivityvsPrice&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;ActivityvsPrice' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;ActivityvsPrice&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626302331641');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1577px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1700, height=900)
    
elif pages == 'Sentiment Cluster Analysis':
    
    make_title(pages, 'white')
    
    blurb('This dashboard is the result of machine learning clustering exercise. Colors in the area charts represent the cluster assigned to each date, while the ' +
          'level of each chart represents the level of the relevant metric on that date. Dates are clustered based on price levels, activity metrics, and ' +
          'sentiment metrics. These include Price vs. All-Time High, Net Unrealized Profit/Loss, Net Transfer Volume, Active Addresses, Google Activity, ' +
          'Reddit Activity, Reddit Polarity, Reddit Subjectivity, News Article Polarity, and News Article Subjectivity.', 'white')
    blurb('Clustering methods available include:  K-Means (6 clusters), K-Means (9 clusters), Gaussian Mixture (6 clusters), Hierarchical Agglomerative Clustering ' +
          '(6 clusters).', 'white')
    blurb('Polarity is a measure of positivity/negatitivity. Subjectivity is a measure of how opinionated a comment or article is. These were calculated using TextBlob.',
          'white')
    blurb('Use the date range selector to adjust the dates shown. This also adjusts the data fed to the boxplots, color coding, and the remainder of the dashboard', 'white')
          
    html = """
     <div class='tableauPlaceholder' id='viz1626717865566' style='position: relative'><noscript><a href='#'><img alt='Sentiment Clusters ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;SentimentClusters&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;SentimentClusters' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;SentimentClusters&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626717865566');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1711px';vizElement.style.height='4027px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1711px';vizElement.style.height='4027px';} else { vizElement.style.width='100%';vizElement.style.height='6027px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1700, height=4000)
    
if pages == 'Topic Modeling Over Time':
    
    make_title(pages, 'white')
    
    blurb('Topic modeling was performed using the Gensim library. TextBlob was used to assess polarity, a measure of positivity/negativity of news articles. ', 'white')
    blurb('Highlight topics by clicking on the color coded legend in the far right container or by searching in the Highlight Topic Label box.', 'white')
    blurb('Change the date aggregation to "Month" or "Year" using the Date Level selector.', 'white')
    blurb('Note that the topic Community (Games, Charity) is excluded by default due to a small number of articles producing erratic polarity data. You can add it back by removing. ' +
          'the Topic Label filter.', 'white')
    
    html = """
    <div class='tableauPlaceholder' id='viz1626299015956' style='position: relative'><noscript><a href='#'><img alt='Topic Prevalence and Sentiment ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicPrevalenceandSentiment&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;TopicPrevalenceandSentiment' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicPrevalenceandSentiment&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626299015956');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1689px';vizElement.style.height='2087px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1689px';vizElement.style.height='2087px';} else { vizElement.style.width='100%';vizElement.style.height='1477px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=2000, height=3000)
    
elif pages == 'Topic Polarity vs. Subjectivity':
    
    make_title(pages, 'white')
    
    blurb('Topic modeling was performed using the Gensim library. TextBlob was used to assess polarity, a measure of positivity/negativity, and ' +
          'subjectivity, a measure of how opinionated an article is.', 'white')
    blurb('The size of the bubbles represents the number of articles where the relevant topic had a dominant share (Dominant Articles).', 'white')
    blurb('The Dominant Share % can be adjusted in the far right container. Perhaps you only want to see sentiment metrics for articles made up at least 50% by the '+
          'relevant topic, for example.', 'white')
    
    html = """
    <div class='tableauPlaceholder' id='viz1626286247872' style='position: relative'><noscript><a href='#'><img alt='Topic Polarity and Subjectivity ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicPolarityandSubjectivity&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TokenSense-BitcoinSentimentAnalysis&#47;TopicPolarityandSubjectivity' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;To&#47;TokenSense-BitcoinSentimentAnalysis&#47;TopicPolarityandSubjectivity&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1626286247872');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1500px';vizElement.style.height='927px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1500px';vizElement.style.height='927px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """
    
    components.html(html, width=1500, height=900)

elif pages == 'Topic Deep Dive':
    
    make_title(pages, 'white')
    
    blurb('Take a deep dive into a single Bitcoin topic or combination of topics to view polarity, subjectivity, and prevalence over time.', 'white')
    blurb('Suggested Combinations:  (Crime + Hacks + Lawsuits), (Bitcoin Improvement Proposals + Blockchain Innovation), (Price Analysis + Price Movement), ' +
          ' (Privacy + Security), (Global Adoption + Government Regulation).', 'white')
    blurb('The table on the right, by default, shows the articles that had the highest percentage topic share for the selected topic. Dominant Share % ' +
          'can be adjusted in the far right container, along with the Date Range and the Date Level.', 'white')
    
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
    
    blurb('This visualization shows the results of LDA topic modeling, as visualized by the pyLDAvis python library. Select or hover over a topic to view the ' +
          'most relevant terms for that topic on the right. Hover over the individual terms to see their conditional topic distribution.', 'black')
    st.write("""Follow [this link](https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf) for more LDA visualization information.""")
    
    left, right = st.beta_columns([1, 3])
    
    with left:
        show_plotly(topic_labels_df)        
    
    with right:
        components.html(lda_vis_html, width=1500, height=900)

