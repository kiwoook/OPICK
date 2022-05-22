from tmdbv3api import TMDb
from tmdbv3api import TV

tmdb = TMDb()
tmdb.api_key = 'ca9447b2f8915badaaef9992f5758183'

tmdb.language = 'ko'
tmdb.debug = True

def TV_Deatail(id):
    tv = TV()
    t = tv.details(id)

    img_src = "https://image.tmdb.org/t/p/original/" + t.poster_path
    tv_info = dict(title = t.name, overview = t.overview, src = img_src, homepage = t.homepage, average = t.vote_average)

    # 해당 작품과 관련된 추천 작품 출력하기
    t_list = tv.recommendations(id)

    for t in t_list:
        print(t['name'])
        print("식별 번호 : ", t['id'])

    return (tv_info)

TV_Deatail(52814)

#https://image.tmdb.org/t/p/original/ 를 붙여 파일 출력시키기