# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
   # Initiate headless driver for deployment
   browser = Browser("chrome", executable_path="chromedriver", headless=True)


   news_title, news_paragraph = mars_news(browser)
# Run all scraping functions and store results in dictionary
   data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemispheres(browser),
      "last_modified": dt.datetime.now()
   }
# In[2]:
   # Stop webdriver and return data
   browser.quit()
   return data

# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': 'chromedriver'}
# browser = Browser('chrome', **executable_path)


# In[3]:


# Visit the mars nasa news site
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# In[8]:


### Featured Images


# # Visit URL
# url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
# browser.visit(url)

# In[16]:


# Visit URL
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url


# In[15]:


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


# In[18]:

def hemispheres(browser):

# 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)



# In[23]:


# 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    html = browser.html
    html_soup = soup(html, 'html.parser')

# 3. Write code to retrieve the image urls and titles for each hemisphere.


# In[24]:

    
    img_titles = []
    title_box = html_soup.find_all('div', class_="collapsible results")
    img_title = title_box[0].find_all('h3')
    for name in img_title:
        img_titles.append(name.text)


# In[25]:


    web_urls = []
    url_box = title_box[0].find_all('a')
    for image_url in url_box:
        if (image_url.img):
            url = 'https://astrogeology.usgs.gov/' + image_url["href"]
            web_urls.append(url)
    

# In[26]:

    image_urls = []
    for url in web_urls:
    
        browser.visit(url)
        html = browser.html
        image_soup = soup(html, 'html.parser')

        url = image_soup.find("img", class_="wide-image")["src"]
        img_link = 'https://astrogeology.usgs.gov/' + url
    
        image_urls.append(img_link)
    mars_hemi_zip = zip(img_titles, image_urls)

    hemisphere_image_urls = []

    # Iterate through the zipped object
    for title, img in mars_hemi_zip:
    
        mars_hemi_dict = {}
    
        # Add hemisphere title to dictionary
        mars_hemi_dict['title'] = title
    
        # Add image url to dictionary
        mars_hemi_dict['img_url'] = img
    
        # Append the list with dictionaries
        hemisphere_image_urls.append(mars_hemi_dict)
    return hemisphere_image_urls

# In[ ]:


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
