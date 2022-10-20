import requests
import random
import pandas as pd
from bs4 import BeautifulSoup as soup
from datetime import datetime
import lxml



'''
fake user agent list
'''


user_agents_list = {
    
    "agent1" : {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    },
    "agent2" : {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    },
}

# getting list of keys
agents_keys = list((user_agents_list.keys()))
HEADERS =   user_agents_list[random.choice(agents_keys)]



# getting random fake user agents from above list
# HEADERS = {'User-Agent': random.choice(user_agents_list)}


URL = 'https://www.monsterindia.com/search/work-from-home-jobs'

webpage = requests.get(URL,headers=HEADERS)
web_obj = soup(webpage.content, "html.parser")
dom = lxml.etree.HTML(str(web_obj))


# find jobs exact container for loop through
containers = dom.xpath('//div[@class="card-apply-content"]')
job_title  = []
company_name = []
locations = []
experience = []
package_offer = []
job_description = []
skills=[]

for container in containers:
    # job title
    # title = container.xpath('./div[@class="job-tittle"]/h3[@class="medium"]/a')[0].text
    # job_title.append(title.strip())
    
    # # company-name
    # company = container.xpath('./div[@class="job-tittle"]/span[@class="company-name"]/a')
    # # some of company name is not provided
    # if company != []:
    #     company_name.append(company[0].text.strip())
    #     # print(company[0].text)
    # else:
    #     company = container.xpath('./div[@class="job-tittle"]/span[@class="company-name"]')
    #     company_name.append(company[0].text.strip())
    
    # locations
    
    # job_locations = container.xpath('./div[@class="job-tittle"]/div[@class="searctag row"]/div[@class="col-xxs-12 col-sm-5 text-ellipsis"]/span[@class="loc"]/small[descendant-or-self::text()]')
    
    # if len(job_locations) > 1:
    #     new_location = ''
    #     for i in job_locations:
    #         new_location += i.text.strip()
    #         new_location += " "
    #     locations.append(new_location.strip())
    # else:
    #     # print(job_locations[0].text)
    #     locations.append(job_locations[0].text.strip())
            
    
    #Experience 
    
    # /html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/div/div/div/div[2]/div/span/small
    
    job_experience = container.xpath('./div[@class="job-tittle"]/div[@class="searctag row"]/div/div[@class="exp col-xxs-12 col-sm-3 text-ellipsis"]/span[@class="loc"]/small')
    experience.append(job_experience[0].text.strip())
    print(experience)

    
    
#     # package
#     package = container.xpath('./div[@class="job-tittle"]/div[@class="searctag row"]/div[@class="package col-xxs-12 col-sm-4 text-ellipsis hidden-sm"]/span[@class="loc"]/small')
#     package_offer.append(package[0].text.strip())
    
#     # job description
#     job_des =  container.xpath('./p[@class="job-descrip"]')
#     job_description.append(job_des[0].text.strip())
    
#     # skills set
#     skill = container.xpath('./p[2]/label[descendant-or-self::text()]/span')
#     if len(skill) > 1:
#         new_skills = ''
#         for i in skill:
#             new_skills += i.text.strip()
#             new_skills +=","
#     skills.append(new_skills.strip())




# data_dict = {'job_title':job_title,'company_name':company_name,'locations':locations,'package_offer':package_offer,'job_description':job_description,'skills':skills}   



# # we have created csv file every day so we have distinguish the every day data by date
# now = datetime.now()

# # # creating format as MMDDYYYY
# month_date_year =  now.strftime("%m%d%Y")

# data_frame = pd.DataFrame(data_dict)
# file_name = f'monster-jobs-{month_date_year}.csv'
# data_frame.to_csv( file_name)







