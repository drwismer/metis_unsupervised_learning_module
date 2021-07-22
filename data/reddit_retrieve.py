import praw
import datetime
from itertools import product
import pandas as pd
import re


def scrape_bitcoin_reddit(latest_date):
    """
    For all dates uncaptured dates, scrape Daily Discussion posts in the bitcoin subreddit for comment data.
    Return post data and comment data in separate pandas dataframes.
    """
    
    # Instantiate Reddit and subreddit instances
    reddit = praw.Reddit(client_id='5C838P4VrI5QLg',
                         client_secret='bxH5wSDy4c3UpFCvax2s6l7C34RIRw',
                         user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.',
                         username='slickfingers',
                         password='zikkic2*')

    btc = reddit.subreddit('bitcoin')

    
    # Set up pandas dataframes to be populated with scraped data
    post_columns = ['date', 'title', 'num_comments', 'url']
    posts_df = pd.DataFrame(columns=post_columns)

    comment_columns = ['date', 'timestamp', 'author', 'body', 'upvotes', 'stickied']
    comments_df = pd.DataFrame(columns=comment_columns)


    # Set up date range for looping
    latest_date = latest_date
    today = datetime.datetime.today().date()

    months = ['january',
              'february',
              'march',
              'april',
              'may',
              'june',
              'july',
              'august',
              'september',
              'october',
              'november',
              'december'
             ]

    years = range(latest_date.year, datetime.datetime.now().year + 1)


    # Loop through all month and year combinations within relevant years
    for y, m in product(years, months):
        ym_first_day = datetime.date(y, months.index(m) + 1, 1)

        # Only search Reddit for months that have passed and the current month
        if datetime.datetime.now().date() >= ym_first_day:
            posts = btc.search('daily discussion {} {}'.format(m, str(y)))

            ym_post_df = pd.DataFrame(columns=post_columns)

            # Loop through posts that match search terms
            for post in posts:
                if (re.search('daily discussion', post.title.lower()) and re.search(m, post.title.lower())):
                    title_components = re.split(', | ', post.title)
                    try:
                        date = datetime.date(int(title_components[-1]),
                                             months.index(title_components[-3].lower()) + 1,
                                             int(title_components[-2])
                                            )
                    except ValueError:
                        continue

                    # Find post and comment details for dates between last db date and today (today not included)
                    if (date > latest_date and date < today):
                        # Only loop through top 100 comments per post
                        post.comment_sort = 'top'
                        post.comment_limit = 100
                        comments = post.comments

                        # Get details for each comment and save to the dataframe
                        for comment in comments:
                            try:
                                comment_details = pd.DataFrame([[date, comment.created_utc, comment.author.name, comment.body, comment.score, comment.stickied]],
                                                           columns=comment_columns
                                                          )
                                comments_df = comments_df.append(comment_details)
                            except AttributeError:
                                continue

                        # Get details for each post and save to the intermediate year/month dataframe
                        post_details = pd.DataFrame([[date, post.title, int(post.num_comments), post.url]], columns=post_columns)
                        ym_post_df = ym_post_df.append(post_details)

            # Sort post data for each year/month combination and add to the posts dataframe
            ym_post_df = ym_post_df.sort_values(['date'])
            posts_df = posts_df.append(ym_post_df)
    
    return posts_df, comments_df


    