## Step 2 - MongoDB and Flask Application
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above. 
# - Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute 
#   all of your scraping code from above and return one Python dictionary containing all of the scraped data. 

def scrape():
    data_dict = {}

    # Dependencies
    from bs4 import BeautifulSoup as bs
    from splinter import Browser
    from splinter.exceptions import ElementDoesNotExist
    import pandas as pd
    import requests
    import os
    import time

    # # Step 1 - Scraping

    # URLs of pages to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    mars_facts_url = 'https://space-facts.com/mars/'
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # start browser for splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    

    # ### NASA Mars News
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

    # Visit the NASA Website
    browser.visit(nasa_url)
    browser.is_element_present_by_css("div.article_teaser_body", wait_time=1)
    html = browser.html
    soup_nasa = bs(html, 'html.parser')
    news_title = soup_nasa.find("div", class_="content_title").text
    news_p = soup_nasa.find('div', class_='article_teaser_body').text

    data_dict['news_title'] = news_title
    data_dict['news_p'] = news_p

    # ### Mars Space Images - Featured Image

    # Visit the url for JPL Featured Space Image
    browser.visit(jpl_url)
    url1 = 'https://www.jpl.nasa.gov'

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    # and assign the url string to a variable called featured_image_url.
    html_jpl = browser.html
    soup_jpl = bs(html_jpl, 'html.parser')
    url2 = soup_jpl.find('article', class_="carousel_item")['style'].split("'")[1]
    featured_image_url = url1 + url2

    data_dict['featured_image_url'] = featured_image_url


    # ### Mars Weather
    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

    browser.visit(mars_weather_url)
    html_mw = browser.html
    soup_mw = bs(html_mw, 'html.parser')
    mars_weather = soup_mw.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    data_dict['mars_weather'] = mars_weather
    
    # ### Mars Facts

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet 
    # including Diameter, Mass, etc.
    browser.visit(mars_facts_url)
    table_df = pd.read_html(browser.url)[0]
    table_df = table_df.rename(columns={0:'Fact', 1:'Value'})
    
    # Use Pandas to convert the data to a HTML table string.
    html_table = table_df.to_html()
    
    data_dict['html_table'] = html_table

    # ### Mars Hemispheres

    # - Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    # - You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # - Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # - Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    browser.visit(usgs_url)
    html_hemi = browser.html
    soup_hemi = bs(html_hemi, 'html.parser')

    links = []
    hemi_dict = []
    url = 'https://astrogeology.usgs.gov'

    description = soup_hemi.find_all("div", class_="description")

    for a in description:
        links.append(a.find('a')['href'])
        

    for link in links:
        # browser.find_link_by_href(link).last.click()
        browser.visit(url+link)
        soup = bs(browser.html, 'html.parser')
        title = soup.find("h2", class_="title").text
        img_url = url + soup.find("img", class_="wide-image")['src']
        hemi_dict.append({'title':title, 'img_url':img_url}) 
    
    data_dict['hemi_dict'] = hemi_dict

    return data_dict
