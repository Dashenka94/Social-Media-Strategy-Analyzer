import pandas as pd
import plotly.express as px
import datetime as dt
from functions import emoji_list, add_sentiment_analysis, get_sentiment, profiler
from plotly.subplots import make_subplots




main_file = pd.read_csv('/Users/dariatsymbal/PycharmProjects/pythonProject1/master.csv', low_memory=False)
#creating new column
main_file['engagement_rate'] = (main_file['total_interactions']/main_file['followed_by']) * 100

## getting rid of outliers
main_file.drop(main_file[main_file['engagement_rate'] >= 35].index, inplace = True)
main_file.drop(main_file[main_file['engagement_rate'] >= 12].index, inplace = True)

#cleaning data
main_file['followed_by'].replace({',': '', '\$': '', ' ': '', 'N/A': '0', 'inf': '0'}, regex=True)
main_file = main_file.astype({'created_time':'datetime64[ns]'})

#creating new column
main_file['hours'] = main_file['created_time'].dt.hour

print('d')

#creating new column
result = []

for link in main_file['post_link']:
    if 'instagram' in link:
        result.append('instagram')
    elif 'facebook' in link:
        result.append('facebook')
    else:
        pass

main_file['Instagram/Facebook'] = result

## define the highest rating profiles

rating_users = main_file[main_file['profile_username'].isin(main_file.groupby('profile_username')['engagement_rate'].median().sort_values(ascending=False).index)]

rating_users_head = rating_users.head(20)

##getting rid of outliners
df_cleaned = rating_users_head[(rating_users_head['engagement_rate'] <= 0.01) & (rating_users_head['followed_by'] <= 1000000)]

## plot of overview of higest rated profiles
fig = px.scatter(df_cleaned, x="followed_by", y="engagement_rate",
                 color="profile_username",
                 hover_data=['Instagram/Facebook'])
fig.show()
print('k')

## overview of particular profile (correlation of hours and eng rate)
nahdi = profiler(main_file, 'nahdihope')
fig = px.scatter(nahdi, x="hours", y="engagement_rate",
                 color="Instagram/Facebook")

fig.show()

## overview of particular profile (correlation of hours and eng rate)

crunchmadison = profiler(main_file, 'crunchmadison')
fig = px.scatter(crunchmadison, x="hours", y="engagement_rate",
                 color="Instagram/Facebook")
fig.show()



# I created this for faster result
#dasha = main_file.loc[0:100]

#using functions for sentiment analysis
data_for_emojis_analysis = emoji_list(main_file, 'message')

sentiment_analysis = add_sentiment_analysis(main_file, 'message')
sentiment_polarity = get_sentiment('message')
print('l')




# creating 4 bins so we can use the highest rated profiles strategy for further analysis

main_file['group'] = pd.qcut(main_file['engagement_rate'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
result_Q4 = main_file[main_file['group'] == 'Q4']

## creating plot how time of post impacts rate
fig = px.scatter(result_Q4, x="hours", y="engagement_rate",
                 color="post_type",
                 hover_data=['Instagram/Facebook'])
fig.show()
print('g')


## how categories in reels vs carousel impact rate
df_reels = result_Q4[result_Q4['post_type'] == 'Reels']
df_carousels = result_Q4[result_Q4['post_type'] == 'Carousel']

fig_reels = px.scatter(df_reels, x="profie_tag_2", y="engagement_rate", color='Instagram/Facebook', hover_data= 'sentiment')

fig_carousels = px.scatter(df_carousels, x="profie_tag_2", y="engagement_rate", color= 'Instagram/Facebook', hover_data= 'sentiment')

fig = make_subplots(rows=1, cols=2, subplot_titles=("Reels", "Carousels"))

for trace in fig_reels.data:
    fig.add_trace(trace, row=1, col=1)

for trace in fig_carousels.data:
    fig.add_trace(trace, row=1, col=2)

fig.update_layout(height=600, width=1200, title_text="Reels and Carousels Sentiment Analysis")

fig.show()

print('g')


## how sentiment and category impact particular social media
df_inst = result_Q4[result_Q4['Instagram/Facebook'] == 'instagram']
df_fb = result_Q4[result_Q4['Instagram/Facebook'] == 'facebook']

fig_reels = px.scatter(df_inst, x="profie_tag_2", y="engagement_rate", color='sentiment', hover_data= 'sentiment')

fig_carousels = px.scatter(df_fb, x="profie_tag_2", y="engagement_rate", color= 'sentiment', hover_data= 'sentiment')

fig = make_subplots(rows=1, cols=2, subplot_titles=("Inst", "FB"))

for trace in fig_reels.data:
    fig.add_trace(trace, row=1, col=1)

for trace in fig_carousels.data:
    fig.add_trace(trace, row=1, col=2)

fig.update_layout(height=600, width=1200, title_text="inst and fb Sentiment Analysis")

fig.show()

print('g')














print('d')


#main_file['followed_by'].replace({',': '', '\$': '', ' ': '', 'N/A': '0', 'inf': '0'}, regex=True)

print('g')






