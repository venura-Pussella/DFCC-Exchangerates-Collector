import pandas as pd
from io import StringIO
from datetime import datetime

def process_html_content(html_content):

    html_file_like = StringIO(html_content)

    df = pd.read_html(html_file_like)[0]

    df.replace('-', 0, inplace=True)
    
    df.fillna(0, inplace=True)
    
    df.reset_index(drop=True, inplace=True)

    df.drop(columns=['Currency Type'], inplace=True)

    df.rename(columns={'Currency Type.1': 'Currency Type'}, inplace=True)

    df['Date'] = datetime.now().strftime('%Y-%m-%d')  
    df['Time'] = datetime.now().strftime('%H:%M:%S')
    df['Bank'] = 'DFCC'
    df['ST BANK CODE'] = '7454'

    df.replace('-', 0, inplace=True)

    df.fillna(0, inplace=True)

    return df

