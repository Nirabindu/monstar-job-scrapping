from rest_framework.decorators import api_view
import requests
import random
import pandas as pd
from bs4 import BeautifulSoup as soup
from datetime import datetime
import lxml
from rest_framework.response import Response
import os 
from django.http import FileResponse
from django.http import HttpResponse


# creating fake user agents
user_agents_list = {
    "agent1": {
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
    "agent2": {
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


def job_title(containers):
    '''
    function for getting/scrapping only jobs-title from containers
    and return list of job-title 
    '''
    job_title = []
    
    for container in containers:
        # getting job titles from containers
        title = container.xpath('./div[@class="job-tittle"]/h3[@class="medium"]/a')[0].text
        job_title.append(title.strip())
    return job_title


def job_company(containers):
    '''
    function for getting company name from containers 
    '''
    company_name = []
    for container in containers:
        company = container.xpath('./div[@class="job-tittle"]/span[@class="company-name"]/a')
        # some of company name is not provided
        if company != []:
            company_name.append(company[0].text.strip())
        else:
            company = container.xpath('./div[@class="job-tittle"]/span[@class="company-name"]')
            company_name.append(company[0].text.strip())
    return company_name
        
        
        
def job_locations(containers):
    '''
    function for getting job-location from containers
    return list of 
    '''
    locations = []
    for container in containers:
        job_locations = container.xpath(
        './div[@class="job-tittle"]/div[@class="searctag row"]/div[@class="col-xxs-12 col-sm-5 text-ellipsis"]/span[@class="loc"]/small[descendant-or-self::text()]')

        # multiple job location are there
        if len(job_locations) > 1:
            new_location = ""
            for i in job_locations:
                new_location += i.text.strip()
                new_location += " "
            locations.append(new_location.strip())
        else:
            locations.append(job_locations[0].text.strip())
    return locations


# def job_experience(containers):
#     experience = []
#     pass


def job_package_offer(containers):
    
    '''
    function for getting job package offer 
    '''
    package_offer = []
    for container in containers:
        package = container.xpath(
        './div[@class="job-tittle"]/div[@class="searctag row"]/div[@class="package col-xxs-12 col-sm-4 text-ellipsis hidden-sm"]/span[@class="loc"]/small')
        package_offer.append(package[0].text.strip())
    
    return package_offer
    
    

def job_description(containers):
    '''
    function for getting job descriptions
    '''
    job_desc = []
    for container in containers:
        job_des = container.xpath('./p[@class="job-descrip"]')
        job_desc.append(job_des[0].text.strip())
    return job_desc



def job_required_skills(containers):
    '''
    function for getting job required skills
    '''
    skills = []
    for container in containers:
        skill = container.xpath("./p[2]/label[descendant-or-self::text()]/span")
        if len(skill) > 1:
            new_skills = ""
            for i in skill:
                new_skills += i.text.strip()
                new_skills += ","
        skills.append(new_skills.strip())
    return skills



# apis for creating csv
@api_view(["GET"])
def get_jobs(request):
    
    
    # scraping url
    URL = "https://www.monsterindia.com/search/work-from-home-jobs"

    # getting list of keys
    agents_keys = list((user_agents_list.keys()))
    HEADERS = user_agents_list[random.choice(agents_keys)]

    webpage = requests.get(URL, headers=HEADERS)
    web_obj = soup(webpage.content, "html.parser")
    dom = lxml.etree.HTML(str(web_obj))

    # find jobs exact container for loop through
    containers = dom.xpath('//div[@class="card-apply-content"]')
    
    # call respective function
    title = job_title(containers)
    company = job_company(containers)
    locations = job_locations(containers)
    # experience = job_experience(containers)
    package_offer = job_package_offer(containers)
    job_desc = job_description(containers)
    skills = job_required_skills(containers)
    
    data_dict = {
    "job_title": title,
    "company_name": company,
    "locations": locations,
    "package_offer": package_offer,
    "job_description": job_desc,
    "skills": skills,
    }

    data_frame = pd.DataFrame(data_dict)
    file_name = "monster-jobs.csv"
    os.makedirs('csv', exist_ok=True) 
    data_frame.to_csv(f'csv/{file_name}')

    
    # now send the file to response
    file = open('csv\monster-jobs.csv', 'rb')
    response = HttpResponse(file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'monster-jobs.csv'
    return response
    
    
    


  
  
  
  