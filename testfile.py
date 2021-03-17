import requests

url = 'https://graph.microsoft.com/v1.0/me/drive/items/01CYZLFJGUJ7JHBSZDFZFL25KSZGQTVAUN/workbook/createSession'
data = {
    'authorization':'Bearer 96152e49-b641-4bb4-a81d-1677228dfce9'
    
}
header = {
    'content-type': 'Application/Json',
    'authorization':'Bearer XF6._2sDv9F_nkK-YKny3eTz4my6o8t~wj',
    'persistChanges': 'True'
    }

response = requests.post(url, headers=header)

print("The response is => \n", response.text)
