import pandas as pd
from .greedy import Greedy


def solve(
    dataset: pd.DataFrame,
    max_passengers_by_stop_dataframe: pd.DataFrame,
    passenger_threshold: float = 10.0,
    max_km_h: int = 17,
    ratio_time_pass_thres: int = 200,
    tmax: int = 45 * 60,
    segs_parada: int = 30,
) -> pd.DataFrame:
    """
    ## Main Function that runs the algorithm.
    ### Parameters:
    * dataset `pd.DataFrame`: The dataframe to solve.
    * passenger_threshold `float` (defaults 10.0): The minimum number of people to attend.
    * max_km_h `int` (defaults 17): The max speed.
    * ratio_time_pass_thres `int` (defaults 200): The max time will each person wait.
    * tmax `int` (defaults 45*60): The max time of a line.
    * segs_parada `int` (defaults 30): The seconds a line will wait in a stop.
    ### Returns: `pd.DataFrame`
    """
    alg = Greedy(
        dataset=dataset,
        passenger_threshold=passenger_threshold,
        max_km_h=max_km_h,
        ratio_time_pass_thres=ratio_time_pass_thres,
    )
    lines = alg.solve(max_passengers_by_stop_dataframe, tmax=tmax, segs_parada=segs_parada)
    return lines.to_df()
