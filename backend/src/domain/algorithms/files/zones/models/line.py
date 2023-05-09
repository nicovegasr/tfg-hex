import pandas as pd

from .dataset_od import DatasetOD


class Line:
    """
    ## Line Object.
    Store a list of pairs origin-destiny, and his accumulated time.
    """

    def __init__(self, dataset: DatasetOD) -> None:
        """
        ### Parameters:
        * dataset `DatasetOD`: The dataset.
        """
        self.stop_pars: list[tuple[int, int]] = []
        self.time = 0
        self.dataset = dataset

    def add_stop_par(self, stop_par: tuple[int, int], time: int, first: bool = False):
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The stop par to add
        * time `int`: The time to go from the left stop to the right stop of the stop_par
        * first `bool` (defaults False): Boolean to control if you want to go from right to left.
        """
        if not first:
            self.stop_pars.append(stop_par)
            self._invalid_stop_pars()
        else:
            self.stop_pars.insert(0, stop_par)
            self._invalid_stop_pars(reverse=True)
        self.time += time
        return self

    def stops(self) -> set:
        """
        ### Returns the stops this line has visited.
        """
        return set(
            [stop[0] for stop in self.stop_pars] + [stop[1] for stop in self.stop_pars]
        )

    def _invalid_stop_pars(self, reverse: bool = False):
        """
        ### Parameters:
        * reverse `bool` (defauls False): To determine if invalid the stop pars reversely.
        """
        last_stop = self.last_stop()
        stops = list(self.stops())
        if reverse:
            stops.reverse()
        for stop in stops:
            if last_stop == stop:
                continue
            self.dataset.invalid_stop_par((stop, last_stop))
            self.dataset.invalid_stop_par((last_stop, stop))
        return self

    def first_stop(self) -> int:
        """
        ### Returns the first stop of the line.
        """
        return self.stop_pars[0][0]

    def last_stop(self) -> int:
        """
        ### Returns the last stop of the line.
        """
        return self.stop_pars[-1][-1]

    def to_df(self) -> pd.DataFrame:
        """
        ### Returns the DataFrame of the line with columns [ORIGEN, DESTINO, DEMANDA, TIEMPO]
        """
        df = pd.DataFrame({}, columns=["ORIGEN", "DESTINO", "DEMANDA", "TIEMPO"])
        for stop_par in self.stop_pars:
            row = [
                stop_par[0],
                stop_par[1],
                self.dataset.demand(stop_par),
                self.dataset.time(stop_par),
            ]
            df.loc[len(df), :] = row  # type: ignore
        return df
