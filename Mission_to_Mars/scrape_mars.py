# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

executable_path = {'executable_path': 'C:\\Users\sofia\Downloads\chromedriver_win32\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():
	#executable_path = {'executable_path': 'C:\\Users\sofia\Downloads\chromedriver_win32\chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)

	# Website to scrape
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
	

	# Sleep so JavaScript has time to render needed HTML
	sleep(5)

	# Save html into BeautifulSoup
	html = browser.html 
	#html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
	soup = BeautifulSoup(html, 'html.parser')

	# Find just the first headline
	first_article = soup.find('div', class_='list_text')
	

	try:
		# scrape the article header 
		news_title = first_article.find('div', class_='content_title').text

		# scrape the article paragraph
		news_p = first_article.find('div', class_='article_teaser_body').text
	except:
		news_title = ""
		news_p = ""
		print("Data wasn't found.")

	##########################################
	# JPL Mars Space Images - Featured Image #
	##########################################

	# Website to scrape
	url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(url)

	# Save html into BeautifulSoup
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	# Get image URL
	img_data = soup.find('article', class_='carousel_item')['style']
	style_split = img_data.split("'")
	img_relative_path = style_split[1]
	featured_image_url = 'https://www.jpl.nasa.gov' + img_relative_path

	##############
	# Mars Facts #
	##############

	# Read tables from webpage
	tables = pd.read_html("https://space-facts.com/mars/")

	# Convert Mars facts to HTML table
	mars_facts = tables[0]
	mars_facts_html = mars_facts.to_html(index=False, header=False)

	####################
	# Mars Hemispheres #
	####################

	# Website to scrape
	url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(url)

	# Save html into BeautifulSoup
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')

	# Save empty list for Hemispheres, which will store our dictionary
	hemispheres = []

	# Loop through the results
	results = soup.find_all('div', class_='item')
	for result in results:
	    
	    # Store the title
	    title = result.find('h3').text
	    
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
	    
	    # Add data to dictionary
	    hem_dict = {
	        'title': title,
	        'img_url': img_url
	    }
	    
	    # Add dictionary to list
	    hemispheres.append(hem_dict)

	# Quit the browser
	browser.quit()

    # Store data in dictionary
	mars_data = {
		'news_title': news_title, 
		'news_p': news_p, 
		'featured_image_url': featured_image_url, 
		'mars_facts': mars_facts_html, 
		'hemispheres': hemispheres
	}

	return mars_data