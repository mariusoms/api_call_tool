import streamlit as st
import base64
import pandas as pd
import requests
import json
from requests.auth import HTTPBasicAuth
import os

######  QR-Code Links in IDs umwandeln ######

def get_id_from_qr(qrcode_string):
    try:
        qr_encoded = qrcode_string.split("reference=")[1]
        qr_decoded = base64.b64decode(qr_encoded)
        qr_decoded_string = qr_decoded.decode('utf-8')

        id = qr_decoded_string.rsplit('/', 1)
        qr_id = id[-1]

        if qr_id.isdigit():
            return qr_id
        else:
            raise ValueError("The part after the last '/' is not a number.")
    except Exception as e:
        return f"An error occurred: {e}"



st.info("Scanne zuerst im Feld "'Technikkiste'" den Asset-Tag der Kiste ab, der du Technik zuordnen willst. Anschließend scannst du in die darunterliegende Tabelle alle Asset-Tags ein, die der Technikkiste zugeordnet werden soll.")

tk = st.text_input("Technikkiste")

if tk.startswith('https://permalink.atlassian.com/v1?experience=qr-code&reference') == False:
    st.error('Link-Format falsch, bitte den QR-Code eines Asset-Tags scannen!')



devices = {"QR-Codes": ["Beispiel: https://permalink.atlassian.com/v1?experience=qr-code&reference=YXJpOmNsb3VkOmNtZGI6Om9iamVjdC9iYzBjNzE0OC1mYWUxLTRlYmMtYjA1YS0wOWJlZTBhODZmNDUvMjg3Nw=="]}

df = pd.DataFrame(devices)

edited_data = st.data_editor(devices, num_rows="dynamic")

edited_df = pd.DataFrame(edited_data)




tk_id = get_id_from_qr(tk)



if 'QR-Codes' in edited_df.columns:
    edited_df['QR-IDs'] = edited_df['QR-Codes'].apply(get_id_from_qr)
    qr_ids = edited_df['QR-IDs'].tolist()
    st.write("Processed Data:")
    st.dataframe(edited_df)

else:
    st.write("Please add some input strings.")

st.write(qr_ids)


###### API Call ######

#for qr_id ind qr_ids:

ids = [{"value": ""}]

for qr_id in qr_ids:
    value_line = json.dumps({"value": qr_id}) + ','
    value_ids = st.write(value_line + '\n')

st.write(ids)


def api_call():
    
    url = "https://api.atlassian.com/jsm/assets/workspace/bc0c7148-fae1-4ebc-b05a-09bee0a86f45/v1/object/{tk_id}"
    st.secrets[JIRA_API_AUTH]

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = json.dumps({
        "attributes": [
            {
                "objectTypeAttributeId": "375",  # objectTypeAttributeId des Feldes "Technikzuordnung"
                "objectAttributeValues": [
                    ids
                ]
            }
        ],
        "objectTypeId": "27",    # objectTypeId von "Kisten"
    })

    response = requests.request(
        "PUT",
        url,
        data=payload,
        headers=headers,
        auth=auth,
    )

    st.write(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    st.info("Testinfo")


st.button("Ausführen", on_click=api_call)