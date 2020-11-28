from selenium import webdriver
from bs4 import BeautifulSoup

import re
import sys
import time


wb = webdriver.Firefox()
url = "http://quote.eastmoney.com/f1.html?code=" + sys.argv[1] + "&market=2"
wb.get(url)

soup = BeautifulSoup(wb.page_source, "lxml")

pageNav_fl = soup.find_all("div", attrs={'class':'pageNav fl'})
all_page = pageNav_fl[0].find("ul").find_all("li")[4].find_all("span")[1].string

file = open(sys.argv[1], 'a+')

while 1:
    soup = BeautifulSoup(wb.page_source, "lxml")

    pageNav_fl = soup.find_all("div", attrs={'class':'pageNav fl'})
    current_page = pageNav_fl[0].find("ul").find_all("li")[4].find_all("span")[0].string

    commidtabs = soup.find_all("div", class_="listDiv")
    for commidtab in commidtabs:
        tables = commidtab.find_all("table")
        for table in tables:
            tbody = table.find("tbody")
            trs = tbody.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                time = tds[0].string
                price = tds[1].string
                pattern = re.compile(r'>(.*)<b')
                count = pattern.findall(str(tds[2]))
                jtTd = tds[2].attrs['class']
                updown = '-'
                if len(jtTd) == 2:
                    updown = jtTd[1]
                line = time + "\t" + price + "\t" + count[0] + "\t" + updown + "\n"
                file.write(line)
    if current_page == all_page:
        break
    wb.find_element_by_class_name('nextPage').click()
    #time.sleep(3)

wb.close()
wb.quit()



