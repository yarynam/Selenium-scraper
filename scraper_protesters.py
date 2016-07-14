# -*- coding: utf-8 -*-
import codecs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

# uncomment if using Firefox web browser
driver = webdriver.Firefox()

url = 'https://elephrame.com/textbook/BLM'
driver.get(url)

# set initial page count
pages = 1
with codecs.open('protests.csv', 'w', encoding='utf-8') as f:
    while True:
        try:
            # sleep here to allow time for page load
            sleep(5)

            pagination = driver.find_element_by_class_name('pagination')
            btn_next = pagination.find_element_by_xpath(".//ul/li[4]")
            btn_next_number = btn_next.get_attribute("p")
            btn_next_value = float(btn_next_number)
            protests = driver.find_elements_by_class_name('protest')
            for protest in protests:

                name = protest.find_element_by_xpath(".//div[@class='item-header']").text
                name_clean = name.replace(","," ")
                participants = protest.find_element_by_xpath(".//div[@class='item-body']")
                information = protest.find_element_by_xpath(".//div[@class='item-info']").text
                information_clean = information.replace(",",";")
                details = protest.find_element_by_xpath(".//div[@class='item-details']").text
                details_clean = details.replace(",",";")
                footer =  protest.find_element_by_tag_name("a")
                link_value = footer.get_attribute("href")
                f.write(name_clean + "," + participants.text  + ","  + information_clean  + "," + details_clean + "," + link_value + '\n')

            # Exit if no more Next button is found, ie. last page
            if btn_next_value > 46:
                print "crawling completed."
                exit(-1)
            # otherwise click the Next button and repeat crawling the urls
            pages += 1
            btn_next.click()

        # you should specify the exception here
        except:
            print "Error found, crawling stopped"
            exit(-1)
