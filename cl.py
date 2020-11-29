import os
import requests
#from flask import Flask, session, redirect, request, url_for
from requests_oauthlib import OAuth2Session
import pandas as pd
from typing import Tuple
from datetime import date
import json
from pathlib import Path
from dataclasses import dataclass

TYPE_SLEEP = "sleep"
TYPE_ACTIVITY = "activity"
TYPE_READINESS = "readiness"
ALL_TYPES = [TYPE_SLEEP, TYPE_ACTIVITY, TYPE_READINESS]

@dataclass
class OuraData:
    sleep: pd.DataFrame
    activity: pd.DataFrame
    readiness: pd.DataFrame


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

def get_all_oura_data(token: str, start = None, end = None, out_folder : str = None) -> OuraData:
    
    if start ==None:
        start = '2013-01-01' #founding of Oura company
    
    if end==None:
        end = date.today().strftime("%Y-%m-%d") #today
    
    if out_folder!= None:
        folder = Path(out_folder)
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
        sleep_path = out_folder + '/' + f"sleep ({start}-{end}).csv"
        readiness_path = out_folder + '/' + f"readiness ({start}-{end}).csv"
        activity_path = out_folder + '/' + f"activity ({start}-{end}).csv"
    else:
        sleep_path = None
        readiness_path=None
        activity_path=None

    sleep = get_oura_data(
        token = token,
        data_type= TYPE_SLEEP,
        start=start,end=end,
        out_path=sleep_path
    )

    readiness=get_oura_data(
        token = token,
        data_type= TYPE_READINESS,
        start=start,end=end,
        out_path=readiness_path
    )

    activity=get_oura_data(
        token = token,
        data_type= TYPE_ACTIVITY,
        start=start,end=end,
        out_path=activity_path
    )

    return OuraData(sleep, activity,readiness)

    
def main():

    token = get_oura_personal_token()

  
    data = get_all_oura_data(
        token=token,
        out_folder="C:/data/oura"
    )
   
    sleep_data = data.sleep
    print(sleep_data.head(15))

if __name__== "__main__":
    main()