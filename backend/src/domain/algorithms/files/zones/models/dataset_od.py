import pandas as pd
from typing import Iterable, Union, Hashable, cast


class DatasetOD:
    """
    ## DatasetOD Object.
    Store a list of pairs origin-destiny, and his accumulated time.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        passenger_threshold: float = 10.0,
        ratio_time_pass_thres: float = 200,
    ):
        """
        ### Parameters:
        * df `pd.DataFrame`: The dataframe to solve.
        * passenger_threshold `float` (defaults 10.0): The minimum number of people to attend.
        * ratio_time_pass_thres `int` (defaults 200): The max time will each person wait.
        """
        self.df = df.set_index(["ORIGEN", "DESTINO"])
        self.passenger_threshold = passenger_threshold
        self.ratio_time_pass_thres = ratio_time_pass_thres
        self.df["VALID"] = True

    def iterrows(self) -> Iterable[tuple[tuple[int, int], pd.Series]]:
        """
        ### Returns the iterable of the dataset.
        """
        iter_rows: Union[
            Iterable[tuple[tuple[int, int], pd.Series]],
            Iterable[tuple[Hashable, pd.Series]],
        ]
        iter_rows = self.df.iterrows()
        iter_rows = cast(Iterable[tuple[tuple[int, int], pd.Series]], iter_rows)
        return iter_rows

    def invalid_stop_par(self, stop_par: tuple[int, int]) -> None:
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The stop par to invalidate.
        """
        self.df.loc[stop_par, "VALID"] = False

    def is_valid(self, stop_par: tuple[int, int]) -> bool:
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The stop par to check if is valid.
        """
        return bool(self.df.loc[stop_par, "VALID"])

    def demand(self, stop_par: tuple[int, int]) -> float:
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The stop par to check the demand.
        """
        return cast(float, self.df.loc[stop_par, "PASAJEROS"])

    def time(self, stop_par: tuple[int, int]) -> float:
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The stop par to check what time takes.
        """
        return cast(float, self.df.loc[stop_par, "TIEMPO_GUAGUA"])

    def have_demand(self, stop_par: tuple[int, int]) -> bool:
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The stop par to check if have demand.
        """
        return (
            cast(float, self.df.loc[stop_par, "PASAJEROS"]) > self.passenger_threshold
            and cast(float, self.df.loc[stop_par, "TIEMPO/PASAJERO_GUAGUA"])
            < self.ratio_time_pass_thres
        )

    def ratio_time_pass(self, stop_par: tuple[int, int]) -> float:
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The stop par to check the ratio time per passenger.
        """
        return cast(float, self.df.loc[stop_par, "TIEMPO/PASAJERO_GUAGUA"])

    def speed(self, stop_par: tuple[int, int]) -> float:
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The stop par to check the speed.
        """
        return cast(float, self.df.loc[stop_par, "KM/H_GUAGUA"])
