#Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import requests
import pymongo
import pandas as pd

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #create a python dictionary for all scraped data
    mars_dict = {}

    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = bs(response.text,'html.parser')
    #print(soup.prettify())
    
    #scrape title from latest news
    latest_title = soup.find("div", class_="content_title").text.strip()
    mars_dict['latest_title'] = latest_title
    #scrape teaser from latest news
    latest_teaser = soup.find("div", class_="rollover_description").text.strip()
    mars_dict['latest_teaser'] = latest_teaser

    #JPL Mars Space Images - Featured Image

    #Visit the url for JPL Featured Space Image here.  Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url. Make sure to find the image url to the full size .jpg image. Make sure to save a complete url string for this image.

    JPL_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPL_url)
    html = browser.html
    JPL_soup = bs(html, "html.parser")

    img = JPL_soup.find("div", class_="image_and_description_container").find("div", class_="img").find("img", class_="thumb")
    mars_img = img.attrs['src']
    mars_dict['mars_img'] = mars_img
    #img_url = print(str(mars_img))

    mars_img_url = "https://www.jpl.nasa.gov" + mars_img
    

    mars_dict['img_url'] = mars_img_url

    #Visit the Mars Weather twitter account here and #scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

    tweet_url = "https://twitter.com/marswxreport?lang=en"
    tweet_resp = requests.get(tweet_url)
    tweet_soup = bs(tweet_resp.text, "lxml")
    tweet_weather = tweet_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_dict['tweet_weather'] = tweet_weather

    #Mars Facts

    #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    facts_url = "https://space-facts.com/mars/"
    mars_tables = pd.read_html(facts_url)
    mars_df = mars_tables[0]
    mars_df.columns = ["Description", "Value"]
    mars_df.set_index("Description",inplace=True)
    #mars_df

    #Use Pandas to convert the data to a HTML table string.
    mars_df_html = mars_df.to_html()
    mars_df_html = mars_df_html.replace('\n','')
    mars_dict['mars_df_html'] = mars_df_html
    

    #Mars Hemispheres

    #Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    USGS_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(USGS_url)
    html = browser.html
    USGS_soup = bs(html, "html.parser")
    #print(USGS_soup.prettify())

    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image. Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title. Append the dictionary with the image url string and the hemisphere title to a list.  This list will contain one dictionary for each hemisphere.

    products = USGS_soup.find("div", class_="collapsible results")
    hemispheres = products.find_all("h3")
    #hemispheres

    #make list for dictionaries to be appened to:
    dict_list = []

    #for loop - add info to lists
    for hemisphere in hemispheres:
        hemisphere_dict = {}
        try:
            title = (hemisphere.text)
            hemisphere_dict['title'] = title
            #click the link, pull in the href for the image
            browser.click_link_by_partial_text("Enhanced")
            samples = browser.find_link_by_text("Sample").first
            link=samples["href"]
            hemisphere_dict["img_url"] = link
            dict_list.append(hemisphere_dict)
        except ElementDoesNotExist:
            print("Out of appendable junk")
    
    mars_dict['hemispheres_dict'] = dict_list

    # Close the browser after scraping
    browser.quit()

    return mars_dict

#scrape()