import pandas as pd

def getdata(name):
    df = pd.read_excel(f"data/{name}")

    date = list(df.columns)[1]
    hindidate = list(df.columns)[2]

    session = df[date][0]

    df.columns = df.iloc[2,:]
    df = df.iloc[3:,:]

    return (date,hindidate,session,df)