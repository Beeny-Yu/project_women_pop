import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

#랭킹 차트 뽑아내는 함수
def melon_age_search(age):
    
    titles = []
    artists = []
    genres = []
    lyrics = []
    
    cnt = 0
    
    age_url = 'https://www.melon.com/chart/age/list.htm'
    params = {
        'idx': 2,
        'chartType': 'YE',
        'chartGenre': 'KPOP',
        'chartDate': age,
        'moved': 'Y',
    }
    
    headers = {
        'Referer': 'https://www.melon.com/index.htm',
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                       (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36')
    }
    
    html = requests.get(age_url, params = params, headers = headers)
    print(html)
    soup = BeautifulSoup(html.text, 'html.parser')
    
    
    
    for tag in soup.select('.t_left'):
        try:
            #제목
            playsong = tag.select_one('.rank01 a[href*=playSong]')
            title = playsong['title']
            js = playsong['href']
            titles.append(title)
            
            #아티스트
            artist_detail = tag.select_one('.rank02 .checkEllipsis a')
            artist = artist_detail.text
            artists.append(artist)
            
            
            #앨범명
#             album_detail = tag.select_one('.rank03 a')
#             album = album_detail.text
            
                  
        except:
            continue
    
        # JavaScript 부분에서 songIds 추출 (정규표현식 사용)
        # 숫자 부분을 ()로 묶어 그룹화, ')'기호는 이스케이프 처리
        matched = re.search(r",'(\d+)'\);", js)
        if matched:
            song_id = matched.group(1)
            song_url = 'https://www.melon.com/song/detail.htm?songId=' + song_id
        
        #print(title, js, album, song_url)
        
        html = requests.get(song_url, headers = headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        
        #장르 
        genre = soup.find('dl',{'class':'list'}).get_text()
        genre = genre.split('\n')[6]
        genres.append(genre)
       
    
        #가사
        tag = soup.find(id='d_video_summary')
        tag = str(tag)
        tag = tag.replace('<div class="lyric" id="d_video_summary">', '').\
            replace('<!-- height:auto; 로 변경시, 확장됨 -->', '').\
            replace('<br/>', '/').replace('</div>', '').strip()
        lyrics.append(tag)    
        
        ### 추출 건수 제어를 위해 if문에서 cnt 사용
        cnt += 1
        if cnt == 100:
            break
        ###
        
    info_dict = {'Year':age,
                 'Title':titles,
                 'Artist':artists,
                 'Genre': genres,
                 'Lyric':lyrics}
    df_song = pd.DataFrame(info_dict)
    return df_song
 
#함수 실행
melon_age_search(2017)

#csv로 추출
melon_age_search(2017).to_csv("2017.csv")