import argparse
from datetime import datetime, date
import os
import pandas as pd

NTOTAL_WEEKS = 52
NWEEK_FROM_DATE = 4


def get_prospects_calendar() -> pd.DataFrame:
    """
    Load prospects row data
    """
    df = pd.read_csv(
        os.path.dirname(os.path.abspath(__file__)) + "/../data/prospects_calendar.csv"
    )
    return df


def apply_business_opportunities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform df to add business_opp column
    Args:
        df: with prospect_name and week revenue
    Notes:
        business_opp is computed comparing week revenue with mean weekly revenue
        To detect only the start of a campaign (max 4 weeks), a filter is applied
        to remove rows for which the revenue condition is already filled during the
        last 3 weeks - ex : shift(1) use the value of the previous row
    Returns:
        df: with new columns business_opp (bool) set to True if a business opp
            is detected for a given week
    """
    for prospect_name in df.prospect_name.unique():
        prospect_df = df[df.prospect_name == prospect_name].copy()
        prospect_df["business_opp"] = (
            # week revenue > 1.5 x average revenue
            (prospect_df.revenue > prospect_df.revenue.mean() * 1.5)
            # week revenue of 3 previous weeks <= 1.5 x average revenue (to select the first start)
            & (prospect_df.revenue.shift(3) <= prospect_df.revenue.mean() * 1.5)
            & (prospect_df.revenue.shift(2) <= prospect_df.revenue.mean() * 1.5)
            & (prospect_df.revenue.shift(1) <= prospect_df.revenue.mean() * 1.5)
        )
        df.loc[df.prospect_name == prospect_name, "business_opp"] = prospect_df[
            "business_opp"
        ]
        df["business_opp"] = df["business_opp"].astype(bool)

    return df


def get_target_week(date: date) -> int:
    """
    Compute target week according to job date
    Args:
        date: job date
    Returns:
        date week incremented of NWEEK_FROM_DATE weeks
    """

    date_week = date.isocalendar().week
    if date_week < (NTOTAL_WEEKS - NWEEK_FROM_DATE):
        return date_week + NWEEK_FROM_DATE
    else:
        return NWEEK_FROM_DATE - (NTOTAL_WEEKS - date_week)


def save_outputs(df: pd.DataFrame, date: date) -> None:
    """
    Args:
        date: target date
        df: dataframe of selected prospect to save
    """
    date_str = date.strftime("%Y-%m-%d")
    filename = f"{date_str}_prospects.csv"
    df.to_csv(os.path.dirname(os.path.abspath(__file__)) + f"/../outputs/{filename}")


def get_opportunties(date: date) -> pd.DataFrame:
    """
    Load prospects data and select the ones with a campaign starting in NWEEK_FROM_DATE
    Args:
        date: target date for returning prospects opportunities
    """
    target_week = get_target_week(date)
    print(f"target_week : {target_week}")
    prospects_df = get_prospects_calendar()
    prospects_opp_df = apply_business_opportunities(prospects_df)
    df = prospects_opp_df[
        (prospects_opp_df.week == target_week) & (prospects_opp_df.business_opp == True)
    ]
    return df


def process(date: date) -> None:
    """Load weekly prospect opportunties and write output to csv

    Args:
        date (date): target date for returning prospects opportunities
    """
    print("-- Start process at : {} --".format(str(datetime.now())))
    df = get_opportunties(date)
    save_outputs(df, date)
    print("-- Eligible prospects --")
    print(df)
    print("-- Finish process at : {} --".format(str(datetime.now())))


# Allows You to Execute Code When the File Runs as a Script, but Not When It’s Imported as a Module
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    base_date = datetime.strptime(args.date, "%Y-%m-%d")
    process(date=base_date)