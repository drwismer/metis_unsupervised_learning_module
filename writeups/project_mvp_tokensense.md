# Project MVP - TokenSense

TokenSense is a web application tracking the pulse of the Bitcoin market through sentiment analysis, clustering techniques, and topic modeling. Follow the link below to view the application. Be sure to click the dropdown menu in the sidebar to see all of the available dashboards. I've also included a few screenshots below.

[Link to TokenSense](https://share.streamlit.io/drwismer/metis_unsupervised_learning_module/main/tokensense.py)

### Gaussian Mixture Sentiment Clustering

The image below shows dates clustered by a variety of price, activity, and sentiment metrics. As you can see, the blue cluster (0) tends to fall on days where price is near its prior peak, whereas the purple cluster (5) tends to fall on days where price is low relative to its prior peak.

<img src="../sentiment_images/gaussian_mixture_clusters.png" width=1600>

### Topic Polarity vs. Sentiment

Topics were determined using Gensim to process nearly 19,000 Bitcoin news articles. TextBlob was used to assign polarity (positivity/negativity) and subjectivity (opinionated-ness) to individual articles. The image below shows the average article polarity and subjectivity by dominant topic

<img src="../sentiment_images/pol_vs_subj.png" width=1200>
