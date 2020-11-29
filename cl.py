import os
import requests
#from flask import Flask, session, redirect, request, url_for
from requests_oauthlib import OAuth2Session
import pandas as pd
from typing import Tuple
from datetime import date
import json
from pathlib import Path

TYPE_SLEEP = "sleep"
TYPE_ACTIVITY = "activity"
TYPE_READINESS = "readiness"


# def json_to_csv(json_obj, out_path : str)-> None:
    
#     if out_path != None:
#         folder = Path(out_path).parent
#         if not folder.exists():
#             folder.mkdir(parents=True,exist_ok=True)
#         df.to_csv(out_path)

def create_url(token: str, start: str, end: str, datatype: str) -> str:
    """token is personal access token.
        start and end should be in YYYY-MM-DD format.
        datatype should be "sleep", "activity", or "readiness"""

    if start ==None:
        start = '2013-01-01' #founding of Oura company
    
    if end==None:
        end = date.today().strftime("%Y-%m-%d") #today
    
    head = "https://api.ouraring.com/v1/"
    data_type=f"{datatype}?"
    time = f"start={start}&end={end}"
    auth = f"&access_token={token}"

    url = head + data_type + time + auth
    return url

def get_oura_personal_token() -> str:

    token = os.getenv("OURA_PERSONAL_TOKEN")
    if token ==None:
        token = input("Enter your oura personal token\n(see https://cloud.ouraring.com/personal-access-tokens):\n").strip()
    else:
        print("Token retrieved from OURA_PERSONAL_TOKEN environmental variable:\n", token)

    return token


# def get_sleep_data(token, start = None, end = None, out_path: str = None ):
#     """start, end should be in 'YYYY-MM-DD' format"""

#     url = create_url(
#         token=token,
#         start=start,
#         end=end,
#         datatype="sleep"
#     )
#     response = requests.get(url).json()
   
#     if out_path!=None:
#         json_to_csv(response['sleep'], out_path)

def get_oura_data(token :str, data_type: str, start = None, end = None, out_path : str = None) -> pd.DataFrame:
    
    url = create_url(
        token=token,
        start=start,
        end=end,
        datatype=data_type
    )

    response = requests.get(url).json()

    df = pd.DataFrame(response[data_type])

    if out_path!=None:
        folder = Path(out_path).parent
        if not folder.exists():
            folder.mkdir(parents=True,exist_ok=True)
        df.to_csv(out_path)

    return df
    




def main():

    token = get_oura_personal_token()

    # get_sleep_data(
    #     token = token,
    #     out_path= "C:/data/oura/oura_sleep.csv")

    readiness = get_oura_data(
        token=token,
        data_type = TYPE_READINESS,
        out_path="C:/data/oura/readiness.csv"
    )
   
    

if __name__== "__main__":
    main()