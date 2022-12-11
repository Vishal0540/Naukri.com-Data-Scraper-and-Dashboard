import requests
import pandas as pd







def scrapeAndGenrateCSV(search_term , number_of_pages):
    url = "https://www.naukri.com/jobapi/v3/search"



    all_details=[]
    for page in range(1,number_of_pages+1):

        print(f"Scraping page number {page}")
        querystring = {"noOfResults":"100","urlType":"search_by_keyword","searchType":"adv","keyword":search_term,"pageNo":page,"sort":"r","k":search_term,"seoKey":search_term,"src":"jobsearchDesk","latLong":"","sid":"16616810997638740_2"}

        headers = {
            'systemid': "109",
            'appid': "109",
            'cache-control': "no-cache",
            }

        response = requests.request("GET", url,  headers=headers, params=querystring)
        jobs_data = response.json()['jobDetails']

        print(f"Number of jobs Fetched from page {page} : {len(jobs_data)}")
        for job in jobs_data:
            job_raw_data = {}
            job_id = job['jobId']
            joburl_  = f'https://www.naukri.com/jobapi/v4/job/{job_id}?src=jobsearchDesk&sid=16618577700918305_1&xp=1&px=5&microsite=y'
            job_data = requests.get(joburl_,headers=headers).json() 
            try:
        
                job_raw_data["JobId"] = job['jobId']
                job_raw_data["Description"] = job_data["jobDetails"]["description"]
                job_raw_data["Title"] = job_data["jobDetails"]["title"].strip()
                job_raw_data["MinimumSalary"] = job_data["jobDetails"]["salaryDetail"]["minimumSalary"]
                job_raw_data["MaximumSalary"] = job_data["jobDetails"]["salaryDetail"]["maximumSalary"]
                job_raw_data["staticUrl"] = job_data["jobDetails"]["staticUrl"]
                job_raw_data['keySkills']  =  []
                job_raw_data["locations"]  =  []
                job_raw_data["Job"]  =  search_term
                job_raw_data["createdDate"]  =  job_data["jobDetails"]["createdDate"]
                try:
                    for loc in job_data["jobDetails"]["locations"]:
                        job_raw_data["locations"].append(loc['label'])
                except:
                    pass
                try:
                    for skill in job_data["jobDetails"]['keySkills']['other']:
                        job_raw_data['keySkills'].append(skill['label'])
                except:
                    pass


                



                


            
                all_details.append(job_raw_data)
            except Exception as e:
                print(e)


    data_df = pd.DataFrame(all_details)
    data_df=data_df.astype(str)
    data_df.drop_duplicates(inplace=True)
    data_df.dropna(inplace=True)
    data_df.to_csv(f"{search_term}.csv",index=False)



if __name__ == '__main__':

    scrapeAndGenrateCSV(search_term = "Data Engineer" , number_of_pages = 3)