# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from newmexico.items import AssessorItem
from bs4 import BeautifulSoup
from scrapy import Selector
import pandas as pd
import logging
logging.basicConfig(filename='ASSESSOR.log', level=logging.INFO)

class AssessorSpider(Spider):
    name = 'assessor'
    allowed_domains = ['liveweb.leacounty-nm.org']
    
    def __init__(self):
        self.BASE_URL = 'http://liveweb.leacounty-nm.org/'
        self.start_urls = ['http://liveweb.leacounty-nm.org/assessor.aspx?source=assessor&page=optOwner&searchterm=1']
        self.df = pd.DataFrame(columns=list(AssessorItem().fields.keys()))
        self.csv = False
        
    def parse(self, response):
                
        table = Selector(response).xpath('//table[@border="1"]').extract_first()

        soup = BeautifulSoup(table, 'lxml')

        rows = soup.findAll('tr')[1:]

        for row in rows:
            try:
                item = AssessorItem()
                entries = row.findAll('td')
                item['PropertyUrl'] = self.BASE_URL + entries[4].a['href'].strip()
                item['Owner'] = entries[0].a.text.strip()
                item['Name'] = entries[1].text.strip()
                item['InCareOf'] = entries[2].text.strip()
                item['District'] = entries[3].text.strip()
                item['PropertyCode'] = entries[4].a.text.strip()
                yield Request(item['PropertyUrl'], callback=self.parse_property, meta={'item': item})
                
            except Exception as e:
                logging.exception(e)
            
        next_page = Selector(response).xpath('//a[contains(text(), "Next>")]/@href').extract_first()
#        
        yield Request(self.BASE_URL+next_page, callback=self.parse)
    
    def parse_property(self, response):
        item = response.meta['item']
        
        page = BeautifulSoup(Selector(response).xpath('//div[@id="pagecontent"]').extract_first(), 'lxml')
        
        topinfo = page.find('fieldset').findAll('label')
        
        NAME_INDICATORS = ['LLC', 'LIABILITY', 'COMPANY', ',', 'INC', 'UNITED', 'GROUP', 
                           'LP', 'COOPERATIVE', 'LTD', 'LLP', 'LLLP', 'ASSEMBLY',
                           'FELLOWSHIP', 'GROUP', 'CITY OF HOBBS', 'CHURCH', 'AGENCY', 
                           'SERVICING', 'ASSOCIATION']

        for i in range(4, len(topinfo)):
            if not any(name_indicator in topinfo[i].text.strip() for name_indicator in NAME_INDICATORS):
                if topinfo[i].text.strip() != '':
                    if 'MailingAddress' not in item:
                        item['MailingAddress'] = (topinfo[i].text.strip())
                    else:
                        item['MailingAddress'] += (' ' + topinfo[i].text.strip())
                        
        midinfo = [label.text.strip().replace('#','') for label in page.findAll('fieldset')[1].findAll('label')]
        
               
        for j in range(0, len(midinfo)):
            field = midinfo[j].replace(' ','')
            if field == 'Subdivision':
                item['Subdivision'] = ''
                subdivisionIndex = j
                break
            if field == 'PhysicalAddress':
                if midinfo[j+1] != '':
                    item[field] = midinfo[j+1]
                    get_address = True
                else:
                    get_address = False
            
                further = 2
                while get_address:
                    if midinfo[j+further] not in ('', 'Bldg', 'Apt'):
                        item[field] += (' ' + midinfo[j+further])
                        further += 1
                    else:
                        get_address = False
                
            elif field == 'Range':
                item['Subdivision'] = ''
                subdivisionIndex = j+2
                
            elif field in list(AssessorItem().fields.keys()):
                item[field] = midinfo[j+1]
                
        if subdivisionIndex:
            for k in range(subdivisionIndex+1, len(midinfo)):
                item['Subdivision'] += midinfo[k] + ' '
            
            item['Subdivision'] = ' '.join(item['Subdivision'].split())
        
        infoTables = page.findAll('table', {'cellpadding':'2'})
        
        for table in infoTables:
            for count, row in enumerate(table.findAll('tr')):
                entries = row.findAll('td')
                if len(entries) == 4:
                    for i in range(0, len(entries), 2):
                        if entries[i].text.strip() not in ('\xa0', '', ' '):
                            item[entries[i].text.strip().replace(' ','')] = entries[i+1].text.strip()
                elif len(entries) == 8:
                    item['BasementSqFt'] = entries[1].text.strip()
                    item['FirstFloorSqFt'] = entries[3].text.strip()
                    item['SecondFloorSqFt'] = entries[5].text.strip()
                    item['YearBuilt'] = entries[7].text.strip()  
                else:
                    item['PropertyValueInfo'+str(count)] = ''
                    for i in entries:
                        if i.text.strip() not in ('', ' '):
                            if i.text.strip() != '\xa0':
                                item['PropertyValueInfo'+str(count)] += (i.text.strip() + ' ')
                
        print(item)
        
        if self.csv:
            for col in self.df.columns:
                if col not in item:
                    try:
                        item[col] = ''
                    except:
                        logging.info(col)
                
            self.df = self.df.append(pd.DataFrame(dict(item), index=[0]))
            self.df.to_csv('assessor.csv', index=False)
        
        yield item
        

  

                
    
                      
        

            

    
    
            
        
    
                






