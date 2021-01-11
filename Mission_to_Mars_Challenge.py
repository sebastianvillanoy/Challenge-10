#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[2]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/Users/seanvillanoy/.wdm/drivers/chromedriver/mac64/87.0.4280.88/chromedriver'}
browser = Browser('chrome', **executable_path)


# ### Visit the NASA Mars News Site

# In[4]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[5]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div", class_='content_title')


# In[7]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[9]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[11]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[14]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[15]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[16]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[17]:


df.to_html()


# ### Mars Weather

# In[63]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[19]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[20]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[5]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[6]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

# Parse the data
html = browser.html
hemi_soup = soup(html, 'html.parser')

# Find all the description sections of each image
hemi_desc = hemi_soup.find('div', class_='result-list').find_all('div', class_='description')

# From the description section, extract the img_url and title for each image
for desc in hemi_desc:
    
    # Extract title and path to next page with the full image
    title = desc.find('a').text
    path = desc.find('a')['href']
    
    # Navigate to the page with the full image
    browser.visit(f'https://astrogeology.usgs.gov{path}')
    
    # Parse the new page 
    html = browser.html
    astro_soup = soup(html,'html.parser')
    
    # Find the img_url
    img_url = astro_soup.find('div', class_='wide-image-wrapper').find('ul').find('li').find('a')['href']
    
    # Put title and img_url in a dictionary and add the dictionary to hemisphere_image_urls list
    hemisphere_image_urls.append({'img_url': img_url, 'title':title})
    
    # Navigate back to the astrogeology page
    browser.back()


# In[7]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[8]:


# 5. Quit the browser
browser.quit()


# In[ ]:




