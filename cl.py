import os
import requests
#from flask import Flask, session, redirect, request, url_for
from requests_oauthlib import OAuth2Session
import pandas as pd
from typing import Tuple
from datetime import date
import json
from pathlib import Path

def get_oura_personal_token() -> str:

    token = os.getenv("OURA_PERSONAL_TOKEN")
    if token ==None:
        token = input("Enter your oura personal token\n(see https://cloud.ouraring.com/personal-access-tokens):\n").strip()
    else:
        print("Token retrieved from OURA_PERSONAL_TOKEN environmental variable:\n", token)

    return token


def get_sleep_data(token, start = None, end = None, out_path: str = None ):
    """start, end should be in 'YYYY-MM-DD' format"""

    if start ==None:
        start = '2013-01-01' #founding of Oura company
        print("Start = ", start)

    if end==None:
        end = date.today().strftime("%Y-%m-%d") #today
        print("end = ", end)
   
    
    head = "https://api.ouraring.com/v1/"
    data_type="sleep?"
    time = f"start={start}&end={end}"
    auth = f"&access_token={token}"

    url = head + data_type + time + auth
    # print(url)
    
    sleep_data = requests.get(url)
    json_sleep = sleep_data.json()
    #print(json_sleep)
    #print(type(json_sleep))
    #print(sleep_data)
    # json_formatted = json.dumps(json_sleep, indent=4)
    # print(json_formatted)

    df = pd.DataFrame(json_sleep['sleep'])
    if out_path != None:
        folder = Path(out_path).parent
        if not folder.exists():
            folder.mkdir(parents=True,exist_ok=True)
        df.to_csv(out_path)

def main():

    token = get_oura_personal_token()
    # get_sleep_data( 
    #     start="2020-10-01",
    #     end="2020-11-30",
    #     token=token)

    get_sleep_data(
        token = token,
        out_path= "C:/data/oura/oura_sleep.csv")
   
    

if __name__== "__main__":
    main()