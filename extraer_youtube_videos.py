from googleapiclient.discovery import build

api_key = 'AIzaSyAF8g04z3LmbqO8qG8MaAwVR4khZiDz4-o'
channel_id = 'UCI4_IQktRxCOK4CO4G7e2xQ'

youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_urls(channel_id):
    video_urls = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part='id',
            channelId=channel_id,
            maxResults=300,
            order='date',
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']
                video_urls.append(f"https://www.youtube.com/watch?v={video_id}")

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return video_urls

# Ejecutar y mostrar resultados
urls = get_video_urls(channel_id)

print("URLs de videos del canal:")
for url in urls:
    print(url)
