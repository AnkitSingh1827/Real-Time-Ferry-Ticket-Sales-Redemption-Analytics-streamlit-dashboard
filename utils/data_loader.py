import pandas as pd

def load_data():

    df = pd.read_csv("data/Toronto Island Ferry Tickets.csv")

    return df