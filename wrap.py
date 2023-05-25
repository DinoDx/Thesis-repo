import requests
import pandas as pd
from bs4 import BeautifulSoup

def smell_detection(path):

    df = pd.read_csv(path)
    url_upload = 'http://localhost:5005' 
    files = {'upload': open(path, 'rb')}
    context = {}

    response = requests.post(url_upload, files=files)
    # Verifica lo stato della risposta
    if response.status_code == 200:
        print("Upload completato con successo.")
    else:
        print("Si è verificato un errore durante l'upload.")


    url_customize = 'http://localhost:5005/customize.html' 
    context = {"smells":[
                        "DataSmellType.DUPLICATED_VALUE_SMELL",
                        "DataSmellType.EXTREME_VALUE_SMELL",
                        "DataSmellType.SUSPECT_SIGN_SMELL",
                        "DataSmellType.CASING_SMELL",
                        "DataSmellType.LONG_DATA_VALUE_SMELL",
                        "DataSmellType.MISSING_VALUE_SMELL",
                        "DataSmellType.FLOATING_POINT_NUMBER_AS_STRING_SMELL",
                        "DataSmellType.INTEGER_AS_FLOATING_POINT_NUMBER_SMELL",
                        "DataSmellType.INTEGER_AS_STRING_SMELL"
                    ], 
                "columns": df.columns
        }

    response = requests.post(url_customize, context)
    # Verifica lo stato della risposta
    if response.status_code == 200:
        print("Customizzazione effettuata.")
    else:
        print("Si è verificato un errore durante la customizzazione.")


    url_results = 'http://localhost:5005/results.html'

    response = requests.post(url_results)
    # Verifica lo stato della risposta
    if response.status_code == 200:
        print("Detection effettuata.")
    else:
        print("Si è verificato un errore durante la detection.")


    result_page = response.text
    soup = BeautifulSoup(result_page, 'html.parser')
    results = soup.find(id="myTabContent")
    tables = results.find_all('table')
    df = pd.DataFrame()

    # Iterate through each table and extract data into the DataFrame
    for table in tables:
        # Extract table header
        header = [th.get_text(strip=True) for th in table.find_all('th')]
        
        # Extract table rows
        rows = []
        for row in table.find_all('tr'):
            rows.append([td.get_text(strip=True) for td in row.find_all('td')])
        
        # Create a temporary DataFrame for the current table
        temp_df = pd.DataFrame(rows, columns=header)
        
        # Append the temporary DataFrame to the main DataFrame
        df = pd.concat([df, temp_df])

    # Print the resulting DataFrame
    df = df.dropna()

    return df
