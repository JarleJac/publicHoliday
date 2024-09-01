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
    runRequestAndProintResult(userCountryCode, year, params)            

    print("\n\n")

def runRequestAndProintResult(userCountryCode, year, params):
    try:
        reqResult = requests.get('https://kayaposoft.com/enrico/json/v3.0/getHolidaysForYear', params)

        if (reqResult.status_code != 200):
            _printErrorResult(reqResult)
        else:
            holidays = getHolidays(reqResult.json())
            _printResult(userCountryCode, year, holidays)
    except Exception as e:
        print("En ukjent feil har opstått ved kall til underliggende web-tjeneste.")            
        print("Tekningske deltaljer:\n " + str(e) )


def getHolidays(holidaysDict) -> list:
    holidays = list()
    for entry in holidaysDict:
        dateDict = entry["date"]
        holiday = Holiday(datetime.datetime(dateDict["year"], dateDict["month"], dateDict["day"]), _getDescriptionText(entry))
        holidays.append(holiday)
        
    return holidays
    
    
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

class Holiday:
    def __init__(self, date, description = "") -> None:
        self.date = date
        self.description = description
        
    def getInfo(self):
        return f"{self.date.strftime('%d.%m.%Y')} {self.description}"
    
    
def _printResult(userCountryCode, year, holidays):
    print(f"\nHer er helligdagene for land {userCountryCode} og år {year}\n")
    print("Dato       Beskrivelse")
    print("---------- ---------------------------------------------------------------")
    for holiday in holidays:
        print(holiday.getInfo())

    print(f"Det er mange! Dvs: {len(holidays)}")


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
    