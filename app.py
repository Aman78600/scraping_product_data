from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
import pandas as pd
import pickle

# Load the models and data
search_queries=pickle.load(open('/home/aman/a896/data of shop/app/models/search_queries.pkl', 'rb'))






app = Flask(__name__)






@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend_products', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    main_df=data_g(user_input)
    df = main_df[main_df['search_q'] == user_input]
    
    data = [
        list(df['img_link'].values),
        list(df['pro_titles'].values),
        list(df['pro_names'].values),
        list(df['pro_prices'].values)
    ]
    
    return render_template('index.html', data=data)

def perform_search(key):
    items = []
    t6=0
    key = key.lower()
    for i in search_queries:
        if key in i.lower():
            items.append(i)
            t6+=1
            if t6 == 10:
                break
    return items

def data_g(q):
    # try:
    #     if q not in search_queries:
    #         search_queries.append(q)
    #         pickle.dump(search_queries,open('search_queries.pkl','wb'))
    #         search_queries=pickle.load(open('search_queries.pkl','rb'))
    # except:
    #     pass
    browser = webdriver.Chrome()
    link="https://www.google.com/search?q="+'+'.join(''.join(q.split('\n')).split(' '))+'flipkart'
    try:
        browser.get(link)
        soup=BeautifulSoup(browser.page_source,'html.parser')  
        link_=soup.find('div',class_='MjjYud').find('a').get('href')
        browser.get(link_)
        soup1=BeautifulSoup(browser.page_source,'html.parser') 
        img_links=[]
        pro_titles=[]
        pro_names=[]
        pro_prices=[]
        # browser.execute_script("window.scrollTo(0, 500)")
        # time.sleep(1)
        # browser.execute_script("window.scrollTo(500, 1000)")
        #     time.sleep(1)
        # browser.execute_script("window.scrollTo(1000, 1500)")
        #     time.sleep(1)
        for i in soup1.find_all('div',class_='_1sdMkc LFEi7Z'):
            l___=str(i.find('img', class_='_53J4C-').get('src'))
            img_links.append(l___)
            pro_titles.append(i.find('div',class_='hCKiGj').find('div',class_='syl9yP').text)
            pro_names.append(i.find('div',class_='hCKiGj').find('a',class_='WKTcLC').text)
            pro_prices.append(i.find('div',class_='hCKiGj').find('div',class_='Nx9bqj').text)    

        df=pd.DataFrame(img_links,columns=['img_link'])
        df['pro_titles']=pro_titles
        df['pro_names']=pro_names
        df['pro_prices']=pro_prices
        df['search_q']=q
        # df.to_csv('data_products/'+search_queries[lll]+'.csv',index=False)
        return df
    except:
        pass
        
    



@app.route('/search')
def search():
    query = request.args.get('query', '')
    results = perform_search(query)
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
