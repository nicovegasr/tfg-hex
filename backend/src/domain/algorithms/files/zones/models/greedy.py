import pandas as pd

from .dataset_od import DatasetOD
from .lines import Lines


class Greedy:
    """
    ## Greedy Algorithm.
    Selects the maximum demand of the pairs origin-destiny and try to append it to a line.
    Builds all the lines simultaneously.
    """

    def __init__(
        self,
        dataset: pd.DataFrame,
        passenger_threshold: float = 10.0,
        max_km_h: int = 17,
        ratio_time_pass_thres: int = 200,
    ) -> None:
        """
        ### Parameters:
        * dataset `pd.DataFrame`: The dataframe to solve.
        * passenger_threshold `float` (defaults 10.0): The minimum number of people to attend.
        * max_km_h `int` (defaults 17): The max speed.
        * ratio_time_pass_thres `int` (defaults 200): The max time will each person wait.
        """
        self.dataset = DatasetOD(dataset, passenger_threshold, ratio_time_pass_thres)
        self.max_km_h = max_km_h

    def solve(self, max_passengers_by_stop_dataframe: pd.DataFrame, tmax: int = 45 * 60, segs_parada: int = 30) -> Lines:
        """
        ### Parameters:
        * tmax `int` (defaults 45*60): The max time of a line.
        * segs_parada `int` (defaults 30): The seconds a line will wait in a stop.
        ### Returns: `Lines`
        """

        lines = Lines(self.dataset, max_passengers_by_stop_dataframe, tmax)
        for stop_par, row in self.dataset.iterrows():
            if not self._valid_stop_par(stop_par):
                continue
            lines.add_stop(stop_par, row.TIEMPO_GUAGUA + segs_parada)
        return lines

    def _valid_stop_par(self, stop_par: tuple[int, int]) -> bool:
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The origin-destiny the check if is valid.
        ### Returns: `bool`
        """
        return (
            self.dataset.is_valid(stop_par)
            and self.dataset.have_demand(stop_par)
            and self.dataset.speed(stop_par) < self.max_km_h
        )
