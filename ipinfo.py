import streamlit as st
import requests
import socket
import pandas as pd
import base64

# DOWNLOAD LINK
def download_csv(df, text, sidebar=False):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ip_info.csv">** {text} **</a>'
    st.markdown(href, unsafe_allow_html=True)



# GET IP INFO FROM API
def get_ip_info(ip):
    r = requests.get(f'https://ipinfo.io/{ip}/geo')
    if r:
        response = r.json()
        df = pd.DataFrame(response, index=[0])
        df = df.transpose()
        df.columns = ['']
        try:
            df = df.drop(['readme'])
        except:
            pass
        return df
    else:
        st.subheader("Couldn't find any info for this IP address")

# GET CLIENT IP
def client_ip():
    hostname = socket.gethostname()
    client_ip = socket.gethostbyname(hostname)
    return client_ip

################################## APP ###############################

#   STREALIT MAIN

st.title("IP Info")
ip = st.text_input("IP to check")
# Validate the IP
try:

    socket.inet_aton(ip)
    st.markdown(f"**Info for IP: {ip}**")
    response = get_ip_info(ip)
    st.table(response)
    if response is not None:
        download_csv(response, 'Download as .csv')
except socket.error:
    if ip != '':
        st.subheader("Invalid IP address")



# FOOTER
st.markdown(
    """
    ***
    **Created by [@arrantate](https://twitter.com/arrantate).** 
    You can support me by [buying me a coffee](https://www.buymeacoffee.com/arrantate).
    (I like coffee)
    """
)