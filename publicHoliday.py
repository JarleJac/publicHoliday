import requests
import json
import datetime

def _getIntInput(prompt) -> int: 
    while (True):
        answer = input(prompt)
        if(answer.isdigit()):
            return int(answer)
        print(f"{answer} er ikke gyldig input")

    
def getPublicHolyDays():
    userCountryCode = input("Angi landkode iso 3166-1 2 eller 3 tegn (blank for å avslutte): ")
    if (userCountryCode == ""):
        return ""
    
    year = _getIntInput("Angi årstall:  ")

    params = dict(year=year, country=userCountryCode, holidayType="public_holiday")
    reqResult = requests.get('https://kayaposoft.com/enrico/json/v3.0/getHolidaysForYear', params)

    if (reqResult.status_code != 200):
        _printErrorResult(reqResult)
    else:
        _printResult(userCountryCode, year, reqResult.text)

    print("\n\n")


def _printErrorResult(reqResult):
    print(f"Kall til underliggende system feilet. Mottok status {reqResult.status_code}" )
    try:
        resultDict = json.loads(reqResult.text)
        if ("error" in resultDict):
            print("Mottok følgende feilmelding: " + resultDict["error"])
            return
    except ValueError as e:
        pass
    print("Ukjent returverdi: " + reqResult.text)

    
def _printResult(userCountryCode, year, jsonText):
    holiDays = json.loads(jsonText)
    print(f"\nHer er helligdagene for land {userCountryCode} og år {year}\n")
    print("Dato       Beskrivelse")
    print("---------- ---------------------------------------------------------------")
    for entry in holiDays:
        date = datetime.datetime(entry["date"]["year"], entry["date"]["month"], entry["date"]["day"])
        text = _getDescriptionText(entry)
        print(f"{date.strftime('%d.%m.%Y')} {text}")
    

def _getDescriptionText(entry):
    noText = ""
    enText = ""
    for descrItem in entry["name"]:
        if (descrItem["lang"] == "no"):
           noText = descrItem["text"]
        elif (descrItem["lang"] == "en"):
           enText = descrItem["text"]
        else:
           text = descrItem["text"]
               
    if (noText != ""):
        text = noText
    elif (enText != ""):
        text = enText
    return text
    