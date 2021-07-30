from urllib.parse import quote
from .get_soup import get_soup


class Chapter:
    """나무위키에서의 한 쳅터에 대한 클래스입니다."""

    def __init__(self, title, content):
        self._title = title
        self._content = content
        self._parent = None
    
    def set_parent(self, parent_node):
        self._parent = parent_node


class Namuwiki:
    """나무위키에서 'search_text'를 검색한 결과를 저장하는 클래스입니다."""

    def __init__(self, search_text: str):
        """'search_text'는 나무위키에서의 검색어 입니다.
        
        example:
            wiki = Namuwiki('강아지')"""
        
        self._chapters = {}
        
        encode_text = quote(search_text)
        url = f'https://namu.wiki/w/{encode_text}'
        soup = get_soup(url)
        titles = soup.select('.wiki-heading')
        titles = list(map(lambda x: x.text, titles))
        if not titles:
            raise Exception(f"'{search_text}'에 대한 검색결과가 없습니다.")
        contents = soup.select('.wiki-heading-content')
        contents = list(map(lambda x: x.text, contents))
        for idx, title in enumerate(titles):
            self._chapters[title.split('. ')[0]] = Chapter(title.split('[편집]')[0], contents[idx])
    
    def __str__(self):
        """클래스를 출력하면 첫 번째 쳅터(주로 '개요')의 내용을 출력합니다.
        
        example:
            print(wiki)

            >> 어린 개를 일컫는 순우리말이다. (...이하 중략)"""

        summary = self._chapters['1']._content
        return summary
    
    def get_list(self):
        """쳅터의 목록을 list 형태로 가져옵니다.
        
        example:
            print(wiki.get_list)
            
            >> ['1', '1.1', '2', '3', '3.1']"""
        
        return list(self._chapters.keys())

    def get(self, chapter_num):
        """'chapter_num'에 해당하는 내용을 출력합니다.
        
        example:
            print(wiki.get(2)
            
            >> 2. 본래 뜻과 다르게 사용하는 경우
                어린 자식이나 손주를 부르는 말로도 쓰며, (...이하 중략)
            
        참고로, 내용이 존재하지 않을 수도 있습니다."""
        
        title = self._chapters[chapter_num]._title
        content = self._chapters[chapter_num]._content
        if not content:
            content = '(내용이 존재하지 않습니다.)'
        result = {}
        result['title'] = title
        result['content'] = content
        return result


region_table = {
    '전국': 108,
    '서울': 109,
    '인천': 109,
    '경기': 109,
    '부산': 159,
    '울산': 159,
    '경남': 159,
    '대구': 143,
    '경북': 143,
    '광주': 156,
    '전남': 156,
    '전북': 146,
    '대전': 133,
    '세종': 133,
    '충남': 133,
    '충북': 131,
    '강원': 105,
    '제주': 184
}
class Weather:
    """날씨 정보를 가져오는 클래스 입니다."""

    def __init__(self, region: str='전국'):
        """해당 지역의 날씨를 가져옵니다."""

        self._region = region
        self._forecast = ''
        self._today = {}
        self._tomorrow = {}
        self._after_tomorrow = {}

        try:
            region_num = region_table[region]
        except:
            raise Exception(f"""'region'에 들어갈 수 있는 단어는 다음과 같습니다.\n\t{tuple(region_table.keys())}""")
        url = f'https://www.weather.go.kr/w/weather/forecast/short-term.do?stnId={region_num}'
        soup = get_soup(url)
        forecast = soup.find('div', {'class': 'cmp-view-content'}).text
        # self._forecast = forecast[1:-1]
        forecast = forecast.split('\n')[1].split('○')
        self._forecast, self._today['weather'], self._tomorrow['weather'], self._after_tomorrow['weather'] = map(lambda x: x.split(') ')[1], forecast[:4])
        temp_table = soup.find('tbody')
        all_temps = list(map(lambda x: x.text, temp_table.select('td')[:10]))
        self._today['minimum_temp'], self._tomorrow['minimum_temp'], self._after_tomorrow['minimum_temp'] = all_temps[2:5]
        self._today['highst_temp'], self._tomorrow['highst_temp'], self._after_tomorrow['highst_temp'] = all_temps[7:10]
    
    def __str__(self):
        """해당 지역의 단기예보를 반환합니다."""

        return self._forecast
    
    def get_today(self):
        """오늘의 날씨를 반환합니다."""

        return self._today
    
    def get_tomorrow(self):
        """내일의 날씨를 반환합니다."""

        return self._tomorrow
    
    def get_after_tomorrow(self):
        """모레의 날씨를 반환합니다."""

        return self._after_tomorrow


topic_table = {
    '속보': 'newsflash',
    '정치': 'politics',
    '경제': 'economy',
    '사회': 'society',
    '국제': 'international',
    '문화': 'culture',
    '연예': 'entertainment',
    '스포츠': 'sports',
    '풀영상': 'fullvideo',
    '뉴스랭킹': 'newsrank',
    '뉴스룸': 'newsroom',
    '아침&': 'morningand',
    '썰전 라이브': 'ssulzunlive',
    '정치부회의': 'politicaldesk',
}
class News:
    """JTBC뉴스 RSS서비스를 사용해 가져온 뉴스 자료입니다."""

    def __init__(self, topic='뉴스랭킹'):
        f"""'topic'에는 아래와 같은 단어가 들어갈 수 있습니다.\n\t{tuple(topic_table.keys())}"""

        self._topic = topic
        self._articles = []
        self._titles = []
        
        topic_code = topic_table[topic]
        url = f'https://fs.jtbc.joins.com//RSS/{topic_code}.xml'
        soup = get_soup(url, 'xml')
        items = soup.findAll('item')
        for item in items:
            title = item.find('title').text
            link = item.find('link').text
            description = item.find('description').text
            pubDate = item.find('pubDate').text
            article = {
                'title': title,
                'link': link,
                'description': description,
                'pubDate': pubDate
                }
            self._articles.append(article)
            self._titles.append(title)
    
    def __str__(self):
        """가장 최근 기사의 제목을 반환합니다."""

        return self._titles[0]
    
    def get_titles(self, article_num=None):
        """기사들의 목록을 'num'개 만큼 반환합니다."""

        return self._titles[:article_num]

    def get_idx(self):
        "기사 번호에 해당하는 기사 제목을 보여줍니다. 'get_article'을 사용하기 위해 존재합니다."

        article_mapping = {}
        for idx, title in enumerate(self._titles):
            article_mapping[idx] = title
        return article_mapping
    
    def get_article(self, article_idx):
        """기사에 대한 정보를 반환합니다.
        'article_idx'는 해당 기사의 번호이며, 번호는 'get_list'를 통해 조회할 수 있습니다."""

        return self._articles[article_idx]


if __name__ == "__main__":
    # wiki = Namuwiki("강아지")
    # print(wiki)
    # weather = Weather('제주')
    # print(weather)
    news = News()
    print(news.get_article(3))