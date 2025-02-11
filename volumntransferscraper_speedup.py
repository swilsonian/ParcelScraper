'''
problems i met: paging, \\n, split, replace, description to formating, import scrtname and dbf encoding,
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import concurrent.futures
from time import sleep
start = time.time()
PATH = "Documents/github/webscraper/chromedriver"
driver = webdriver.Chrome(PATH)
totalpages = 5
baseurl = "https://www.udd.gov.taipei/volumn-transfer/avdwckf"
urls = [f"{baseurl}?page={i}" for i in range(1, totalpages+1)]
data=[]
def udddata(n):
    driver.get(n)
    contents = driver.find_elements(By.CLASS_NAME, "col-md-6")
    d1 = [content.text for content in contents]
    data.append(d1)
    return
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(udddata, urls)
print(data)
driver.close()
timecut = time.time()

p = str(data).split(",")
q=[]
exception=[]
for i in range(len(p)):
    try:         
        q.append((p[i].split("\\n"))[3])
    except:
        exception.append(p[i].split("\\n"))

r = str(q).replace("、", ",").replace("及", ",").replace(" ","").replace("'","").replace("[","").replace("]","")
s = r.split(",")
s1 = [] 
for element in s:
    if "北市" in element: s1.append(element.split("北市")[1])
    else: s1.append(element)

t = []
for element in s1:
    if "地" in element:
        t.append(element.split("地")[0])
    elif "等" in element:
        t.append(element.split("等")[0])
    elif "（" in element:
        t.append(element.split("（")[0])
    elif "(" in element:
        t.append(element.split("(")[0]) 
    else: t.append(element)

print(len(p))
print(len(p[0]))
print(p)
print(p[0])
# print(len(q))
# print(len(q[0]))


u = []
for n in range(len(t)):
    if "段" not in t[n]:
        if "小段" in u[n-1]:
            u.append(str(u[n-1]).split("小段")[0]+"小段"+t[n])
        else:
            u.append(str(u[n-1]).split("段")[0]+"段"+t[n])
    else: u.append(t[n])

v = []
for n in range(len(u)):
    if "同區段" in u[n]: v.append(str(v[n-1]).split("段")[0]+"段"+str(u[n]).split("同區段")[1])
    elif "同小段" in u[n]: v.append(str(v[n-1]).split("段")[0]+"段"+str(u[n]).split("同小段")[1])
    elif "同段" in u[n]:
        if "大同段" not in u[n]: v.append(str(v[n-1]).split("段")[0]+"段"+str(u[n]).split("段")[1])
        else: v.append(u[n])
    elif "同區" in u[n]:
        if "大同區" not in u[n]: v.append(str(v[n-1]).split("區")[0]+"區"+str(u[n]).split("區")[1])
        else: v.append(u[n])
    else: v.append(u[n])

w = [(v[i].index("段")) for i in range(len(v))]
# x = [] # x 可以獲得完整 段小段地號
# for i in range(len(v)):
#     w3 = v[i].index("段")
#     if "新洲美" in v[i]: x.append(v[i][w3-3:])
#     else: x.append(v[i][w3-2:])

y = [] #y僅獲得段小段 為了統計段代碼出現次數
Z = ["金泰", "舊宗", "安康", "民生", "經貿", "向陽", "中洲", "三合", "新洲美", "軟橋"]
for i in range(len(v)):
    w2 = v[i].index("段")
    if any(z in v[i] for z in Z): y.append(v[i][w2-2:w2+1])
    elif "新洲美" in v[i]: y.append(v[i][w2-3:w2+1])
    else: y.append(v[i][w2-2:w2+4])

# 導入段代碼
import csv
import re
d = open("documents/github/Project_volumntransfer/section.csv", "r")
csvr = csv.reader(d, delimiter = ",")
sect = [row[0] for row in csvr]
# sect1 = re.split(' {9}', str(sec[0]))
# sect2 = [(re.split('\s+', str(i))) for i in sec1]
# sect1 + sect2 = sect
sect = [(re.split('\s+', str(i))) for i in (re.split(' {9}', str(sect[0])))]
sectdict = {str(sect[i][2]):sect[i][0] for i in range(len(sect))}
# print(sectdict)

n = []
for i in y:
    if i in sectdict.keys():
        n.append(sectdict.get(i))
    else: continue
from collections import Counter
print(Counter(n))

'''
'''
# if __name__ == '__main__':
#     sys.exit(main())

end = time.time()
scrapertime = timecut - start
processtime = end - timecut
timepassed = end - start
print("爬蟲計時：%f 秒鐘" %scrapertime)
print("運算計時：%f 秒鐘" %processtime)
print("總計時：%f 秒鐘" %timepassed)


