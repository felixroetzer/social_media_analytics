
# FIND VIRAL CONTENT VIRAL

import requests
import json
import urllib.request

# replace by the instagram pages, you want to analyze!!!
example_usernames = ['barstoolsports', 'fuckboyproblem.s', 'humor', 'itsallmaad', 'itsallleaked', 'blockbanter', 'fupla', 'moist', 'ftb', 'pickuplines', 'hoodclipsofficials', 'houseofhighlights', 'clips', 'isyoufunny']

def getcreds():
    creds = dict()
    creds['access_token'] = 'XXX_YOUR_ACCESS_TOKEN_XXX'
    creds['client_id'] = 'XXX_YOUR_CLIENT_ID_XXX'
    creds['client_secret'] = 'XXX_YOUR_CLIENT_SECRETXXX'
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['version'] = 'v18.0'
    creds['debug'] = 'no'
    creds['endpoint_base'] = creds['graph_domain'] + creds['version'] + '/'
    creds['page_id'] = 'XXX_ANALYZED_PAGE_ID_XXX'
    creds['instagram_account_id'] = 'XXX_INSTAGRAM_ACCOUNT_ID_XXX'
    creds['media_id'] = 'XXX_MEDIA_ID_XXX'


    return creds

def make_api_call(url):
    data = requests.get(url=url)
    response = json.loads(data.text)
    return response

def get_basic_account_info(username):
    creds = getcreds()
    url = creds['endpoint_base'] + '/' + creds['instagram_account_id'] + f'?fields=business_discovery.username({username})' + '{followers_count, media_count, media, id, ig_id}&access_token=' + creds['access_token']
    return make_api_call(url)

def get_medias_data(username):
    creds = getcreds()
    url = creds['endpoint_base'] + '/' + creds['instagram_account_id'] + f'?fields=business_discovery.username({username})' + '{media.limit(150){username, like_count, caption, media_url, comments_count, timestamp, media_type}}&access_token=' + creds['access_token']
    return make_api_call(url)

def get_user_media():
    creds = getcreds()
    url = creds['endpoint_base'] + '/' + creds['instagram_account_id'] + '/media'
    return make_api_call(url)

def get_media_insights(id):
    creds = getcreds()
    url = creds['endpoint_base'] + str(id) + '?fields=id, caption&access_token=' + creds['access_token']
    return make_api_call(url)


top_10_list = []
def find_most_liked_media():

    for username in example_usernames:
        medias_data = get_medias_data(username)

        likes_list = []
        for i, likes in enumerate(medias_data['business_discovery']['media']['data']):
            if 'like_count' in likes:
                likes['iteration'] = i
                likes_list.append(likes)

        sorted_likes_list = sorted(likes_list, key=lambda x: x['like_count'], reverse=True)
        top_10_posts_by_likes = sorted_likes_list[:10]
        top_20_posts_by_likes = sorted_likes_list[:20]

        if len(medias_data['business_discovery']['media']['data']) > 50:
            top_10_percent_posts = sorted_likes_list[:int(len(medias_data['business_discovery']['media']['data'])/10)+1]
            top_5_percent_posts = sorted_likes_list[:int(len(medias_data['business_discovery']['media']['data'])/20)+1]

        print(top_10_posts_by_likes)
        top_10_list.append(top_10_posts_by_likes)



#### DOWNLOAD THE VIDEOS BY ITS URL

def download_best_videos():

    for video in top_10_list:
        like_count = video[0]['like_count']
        try:
            url = video[0]['media_url']
        except KeyError:
            url = video[1]['media_url']
        name = video[0]['id']
        name=name+".mp4"
        try:
            print("Downloading starts...\n")
            print(name)
            print(like_count)
            urllib.request.urlretrieve(url, name)
            print("Download completed..!!")
        except Exception as e:
            print(e)


'''
print(get_media_insights(likes_list[0]['id']))
print(get_media_insights(top_10_posts_by_likes[0]['id']))'''


'''
for id in top_10_posts_by_likes:
    get_media_insights(id)'''

