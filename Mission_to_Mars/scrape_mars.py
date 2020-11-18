#!/usr/bin/env python
# coding: utf-8

# In[9]:


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


# In[4]:


#Setting executable path on Windows
executable_path = {'executable_path': 'C:\\Users\sofia\Downloads\chromedriver_win32\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[6]:


# URL to scrape
url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[7]:


#Define html object and parsing html by using beautiful soup
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[16]:


# Declare variable to hold the headlines in div sections
results = soup.find_all('div', class_='list_text')

# Use this line if you want to find just the first headline
#first_article = soup.find('div', class_='list_text')
#print(first_article)


# In[17]:


#Declare array to store news list
news_list = []
# for loop to loop over results
for result in results: 
    news_title = result.find('div', class_='content_title')
    news_p = result.find('div', class_='article_teaser_body')

    # Dictionary to be inserted into MongoDB
    try:
        post = {
            'title': news_title.text.strip(),
            'paragraph': news_p.text.strip(),
        }
        news_list.append(post)
    except:
        print("Skipping...................")
print(news_list)


# In[19]:


# scrape the article header 
news_title = first_article.find('div', class_='content_title').text

# scrape the article paragraph
news_p = first_article.find('div', class_='article_teaser_body').text

print(news_title)
print(news_p)


# # 👴 JPL Mars Space Images - Featured Image

# In[ ]:





# In[21]:


# Website to scrape
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

# Save html into BeautifulSoup
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[23]:


img_data = soup.find('article', class_='carousel_item')['style']
style_split = img_data.split("'")
img_relative_path = style_split[1]
featured_image_url = 'https://www.jpl.nasa.gov' + img_relative_path
print(featured_image_url)


# # Mars Facts

# In[25]:


#Getting the mars info by usung pandas
mars_tables = pd.read_html("https://space-facts.com/mars/")
mars_tables


# In[27]:


#Grabbing the first part to get a summary dataframe
mars_facts = tables[0]
mars_facts


# # Mars Hemispheres 🪐

# In[28]:


# Website to scrape
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)

# Save html into BeautifulSoup
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[29]:


# Save empty list for Hemispheres, which will store our dictionary
hemispheres = []

# Loop through the results
results = soup.find_all('div', class_='item')
for result in results:
    print('------------')
    
    # Store the title
    title = result.find('h3').text
    print(title)
    
    # Find the URL to move to, to get the large image URL
    href = result.find('a')['href']
    hemisphere_url = 'https://astrogeology.usgs.gov' + href
    
    # Visit next page
    browser.visit(hemisphere_url)

    # Save html into BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the image URL
    container = soup.find('div', class_='downloads')
    img_url = container.find('a')['href']
    print(img_url)
    
    # Add data to dictionary
    hem_dict = {
        'title': title,
        'img_url': img_url
    }
    
    # Add dictionary to list
    hemispheres.append(hem_dict)

print(hemispheres)

