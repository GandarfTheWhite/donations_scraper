import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import os

print("\n_____Start Program_____")

def getTotal(urls):

    totalData = []
    for url in urls:

        print("\nurl: ", url)
        totalRaised = None
        giftAid = None
        target = None

        if 'justgiving' in url:
            elements = getElementsjg(url)
            #print('getTotal:',elements)    
        elif 'gofundme' in url:
            elements = getElementsgfm(url)
            #print('getTotal:',elements)
        else:
            elements = [None, None, None]

        totalRaised = elements[0]
        giftAid = elements[1]
        target = elements[2]

        print("Total raised:", totalRaised)
        print("Gift Aid:", giftAid)
        print('Target:', target)
        totalData.append([url, totalRaised, giftAid, target])

    return totalData


def getUrls(file):

    fileRead = open(file, "r")
    Lines = fileRead.readlines()
    fileRead.close()

    urls = []
    for line in Lines:  
        urls.append(line.strip())
    return urls


def processStringjg(totalString):

    if isinstance(totalString, str):
        totalString = totalString.replace(',', '')
        pattern = re.compile(r'\-?\d+\.\d+')
        totalNum = list(map(float, re.findall(pattern, totalString)))
        #print('processStringjg:',totalNum)        
        if len(totalNum)==2:
            totalNum.insert(2, None)
            #print('processStringjg:',totalNum)
            return totalNum
        elif len(totalNum)==1:
            totalNum.insert(1, None)
            totalNum.insert(2, None)
            #print('processStringjg:',totalNum)      
            return totalNum      
    else:
        return [None, None, None]


def processStringgfm(totalString):
    
    if isinstance(totalString, str):
        totalString = totalString.replace(',', '')
        #totalString = totalString.replace('.', '')
        totalNum = list(map(float, re.findall(r'\d+', totalString)))
        totalNum.insert(1, None)
        #print('processStringgfm:',totalNum)
        return totalNum
    else:
        print('Not a String')
        return [None, None, None]


def getElementsjg(url):

    resp=requests.get(url)
    if resp.status_code==200:

        # we need a parser,Python built-in HTML parser is enough
        soup=BeautifulSoup(resp.text,'html.parser')

        # l is the list which contains all the text i.e news
        l=soup.find("dd",{"class":"jg-pages-donationsummary__total jg-space-mbsm jg-text-color-branded"})
        text= l.text
        #print('getElementsjgtext:',text)
    else:
        print("Unable to reach site!!")
        text = None
        target = None

    elements = processStringjg(text)
    #print('getElementsjg:',elements)
    return elements


def writeToFile(totalList, file):
    df = pd.DataFrame(totalList, columns =['URL','Total Raised','Gift Aid', 'Target'])
    
    with pd.ExcelWriter(file) as tf:
        df.to_excel(tf, sheet_name='Sheet1')
    print('\n_____Data successfully scraped_____')


def getElementsgfm(url):

    resp=requests.get(url)
    if resp.status_code==200:

        # we need a parser,Python built-in HTML parser is enough .
        soup=BeautifulSoup(resp.text,'html.parser')

        # l is the list which contains all the text i.e news
        l=soup.find('p',{'class':"m-progress-meter-heading"})
        text = l.text
        #print('getElementsgfm:',text)
    else:
        print("Unable to reach site!!")
        text = None

    elements = processStringgfm(text)
    #print('getElementsgfm:',elements)
    return elements


def getReadFile():
    userFile = input('Please enter filename:')
    return userFile


def getWriteFile():
    path = os.path.realpath(__file__)
    return path[:-21] + '\data\donations_total.xlsx'


def runProgram():
    userFile = getReadFile()
    urls = getUrls(userFile)
    totalList = getTotal(urls)
    writeToFile(totalList, getWriteFile())

#print(getWriteFile())

runProgram()

print('\n_____End program_____')