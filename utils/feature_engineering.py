import numpy as np

def add_features(df):

    df["Hour"] = df["Timestamp"].dt.hour

    df["Day"] = df["Timestamp"].dt.day_name()

    df["Month"] = df["Timestamp"].dt.month_name()

    df["Year"] = df["Timestamp"].dt.year

    df["Weekday"] = df["Timestamp"].dt.weekday

    df["Weekend"] = np.where(
        df["Weekday"] >= 5,
        "Weekend",
        "Weekday"
    )

    def season(month):

        if month in [12,1,2]:
            return "Winter"

        elif month in [3,4,5]:
            return "Spring"

        elif month in [6,7,8]:
            return "Summer"

        else:
            return "Fall"

    df["Season"] = df["Timestamp"].dt.month.apply(season)

    return df