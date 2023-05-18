from serpapi import GoogleSearch
import os, json,csv
import pandas as pd


def get_jobs(job_type,count):
    params = {
        'api_key': 'c64770297de3c659e4281cfc836a81f0cc2e36da88fca95a3391117dc12e9939',  #https://serpapi.com/manage-api-key
        # https://site-analyzer.pro/services-seo/uule/
        'uule': 'w+CAIQICIFSW5kaWE',  # encoded location (INDIA)
        'q': job_type,
        'hl': 'en',  # language of the search
        'gl': 'us',  # country of the search
        'engine': 'google_jobs',  # SerpApi search engine
        'start': 0  # pagination
    }


    google_jobs_results = []

    while count != 0:
        search = GoogleSearch(params)  # where data extraction happens on the SerpApi backend
        result_dict = search.get_dict()  # JSON -> Python dict

        if 'error' in result_dict:
            break

        for result in result_dict['jobs_results']:
            google_jobs_results.append(result)

        params['start'] += 20
        if result :
            count -= 1

    # employee_data = json.loads(google_jobs_results, indent=2, ensure_ascii=False)
    # print(employee_data)

    # headers to the CSV file
    col = list(google_jobs_results[0].keys())
    # print(col)
    data_file = pd.DataFrame(google_jobs_results,columns = col)

    return data_file
    # if choice == 2:
    #     job_data = pd.read_csv("Job_Data.csv")
    #     print(job_data.head(10))

