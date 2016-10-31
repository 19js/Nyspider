from selenium import webdriver
import os
import time

def main():
    browser=webdriver.Firefox()
    browser.get('http://www.ncbi.nlm.nih.gov/pubmed')
    input('OK?')
    browser.implicitly_wait(10)
    count=0
    while True:
        html=browser.page_source
        f=open('html/%s.html'%count,'w')
        f.write(html)
        f.close()
        browser.find_element_by_xpath("//a[@id='EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Entrez_Pager.Page' and @sid=3]").click()
        time.sleep(5)
        count+=1
        if count==5330:
            break

main()
