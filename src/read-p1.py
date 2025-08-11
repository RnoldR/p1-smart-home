import pandas as pd

def read_p1_standard(filename: str):
    df = pd.read_csv(filename, sep=';', keep_default_na=False, na_filter=False)
    
    print(df)

    return df


def read_data(filename: str):
    df = pd.read_csv(filename, sep=';', keep_default_na=False, na_filter=False)
    
    print(df)

    return df


if __name__ == "__main__":
    filename = "ini/p1-standard.csv"
    dataname = "data/ttylog.log"

    devices = read_p1_standard(filename)
    data = read_data(dataname)