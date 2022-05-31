from tmdbv3api import TMDb, TV, Movie, Trending

from collections import deque

tmdb = TMDb()
tmdb.api_key = 'ca9447b2f8915badaaef9992f5758183'

tmdb.language = 'ko'
tmdb.debug = True

def TV_Deatail(id):
    tv = TV()
    t = tv.details(id)
   
    # 이미지 
    img_src = ""
    bgImg_src = ""
    if(t.poster_path is None) :
        img_src = "https://via.placeholder.com/300x450"
    elif(t.backdrop_path is None) :
        bgImg_src = None
    else :
        img_src = "https://image.tmdb.org/t/p/original" + t.poster_path
        bgImg_src =  "https://image.tmdb.org/t/p/original" + t.backdrop_path

    #장르
    genres = ""
    genres_list = []
    for i in t.genres:
        genres_list.append(i['name'])
    genres = ', '.join(genres_list)

    # 해당 작품의 OTT
    service = t.networks[0].get('name')

    #딕셔너리화 시키기
    tv_info = dict(title = t.name, overview = t.overview, src = img_src, bg_src = bgImg_src, homepage = t.homepage, average = t.vote_average, genres = genres, service = service, airdate = t.first_air_date)
   
    # 해당 작품과 관련된 추천 작품 출력하기
    t_list = tv.recommendations(id)

    recommended_list = []
    for i , t in enumerate(t_list):
        if( i>= 5):
            break
            #3개 이상 들어가면 종료
        img_src = "https://image.tmdb.org/t/p/original" + t['poster_path']
        recommended_dict = dict(title = t['name'], id = t['id'], src = img_src)
        recommended_list.append(recommended_dict)
    return tv_info, recommended_list

def Movie_Deatail(id):
    mv = Movie()
    m = mv.details(id)

    # 이미지 
    img_src = ""
    bgImg_src = ""
    if(m.poster_path is None) :
        img_src = "https://via.placeholder.com/300x450"
    elif(m.backdrop_path is None) :
        bgImg_src = None
    else :
        img_src = "https://image.tmdb.org/t/p/original" + m.poster_path
        bgImg_src =  "https://image.tmdb.org/t/p/original" + m.backdrop_path

    #장르
    genres = ""
    genres_list = []
    for i in m.genres:
        genres_list.append(i['name'])
    genres = ', '.join(genres_list)


    #딕셔너리화 시키기
    mv_info = dict(title = m.title, overview = m.overview, src = img_src, bg_src = bgImg_src, homepage = m.homepage, average = m.vote_average, genres = genres, airdate = m.release_date)
   
    # 해당 작품과 관련된 추천 작품 출력하기
    m_list = mv.recommendations(id)

    recommended_list = []
    for i , m in enumerate(m_list):
        if( i>= 5):
            break
            #3개 이상 들어가면 종료
        img_src = "https://image.tmdb.org/t/p/original" + m['poster_path']
        recommended_dict = dict(title = m['title'], id = m['id'], src = img_src)
        recommended_list.append(recommended_dict)
    print(mv_info)
    print(recommended_list)
    return mv_info, recommended_list

def Popular_TV():
    tv = TV()

    tv_popular = tv.popular()
    tv_popular_list = [] 

    for index, t in enumerate(tv_popular):
        if(index >= 10):
            break
        img_src = "https://image.tmdb.org/t/p/original" + t['poster_path']
        tv_popular_dict = dict(title = t['name'], id = t['id'], src = img_src) 
            
        tv_popular_list.append(tv_popular_dict)
    return(tv_popular_list)

def TMDB_Trending():
    trending_list = [] 
    trending = Trending()
    shows = trending.all_day()

    for index, t in enumerate(shows):
        if(index >= 10):
            break
        img_src = "https://image.tmdb.org/t/p/original" + t['poster_path']
        trending_dict = dict(media_type = t['media_type'], id = t['id'], src = img_src)

        trending_list.append(trending_dict)
    return trending_list



# Movie_Deatail(619803)

# index html에 아래와 같이 jinja로 구현하기
# for p_data in popular_list:
#     print(p_data['title'])
#     print(p_data['id'])
#     print(p_data['src'])


#https://image.tmdb.org/t/p/original/ 를 붙여 파일 출력시키기