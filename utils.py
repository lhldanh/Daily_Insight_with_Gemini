from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_vnexpress(keyword):
    # URL gốc của trang tìm kiếm
    base_url = "https://timkiem.vnexpress.net/"
    
    # Mã hóa từ khóa để đảm bảo các ký tự đặc biệt được xử lý đúng
    encoded_keyword = urllib.parse.quote(keyword)
    
    # Tạo URL đầy đủ với tham số tìm kiếm
    search_url = f"{base_url}?q={encoded_keyword}&cate_code=&media_type=all&latest=&fromdate=&todate=&date_format=day&"
    
    # Thiết lập headers để giả lập trình duyệt
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    
    try:
        # Thực hiện request
        response = requests.get(search_url, headers=headers)
        
        # Kiểm tra kết quả request
        response.raise_for_status()
        
        # In ra nội dung hoặc xử lý kết quả
        soup = BeautifulSoup(response.text, 'html.parser')

    # Find all articles with the 'data-url' attribute
        articles = soup.find_all('article', class_='item-news item-news-common')

        # Extract and print all 'data-url' attributes
        data_urls = [article['data-url'] for article in articles if 'data-url' in article.attrs]

        return data_urls
    
    except requests.RequestException as e:
        print(f"Lỗi khi thực hiện tìm kiếm: {e}")
        return None

client = OpenAI(
    base_url='http://localhost:11434/v1/',

    # required but ignored
    api_key='ollama',
)
def summary(content, model="llama3.2"):
    completion = client.completions.create(
        model=model,
        prompt=f"Tóm tắt tin tức này cho tôi trong vòng 5 câu\n{content}",
    )
    return completion.choices[0].text


def list_of_model():
    models = [model.id for model in client.models.list().data]
    return tuple(models)

def fetch_news_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        title = soup.find("h1", class_='title-detail').text
        content = "\n".join([p.text for p in paragraphs])
        return (title, content)
    else:
        return "Không thể lấy nội dung từ URL này."
print(summary(fetch_news_content(search_vnexpress("trí tuệ nhân tạo")[0])[1]))
# print(list_of_model())