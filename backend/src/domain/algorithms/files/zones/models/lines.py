import pandas as pd

from .dataset_od import DatasetOD
from .line import Line


class Lines:
    """
    ## Lines Object.
    Store a list of Lines.
    """

    def __init__(self, dataset: DatasetOD, max_passengers_by_stop_dataframe: pd.DataFrame, tmax: int) -> None:
        """
        ### Parameters:
        * dataset `DatasetOD`: The dataset of the problem.
        * tmax `int`: Max time each line can have.
        """
        self.dataset = dataset
        self.max_passengers_by_stop_dataframe = max_passengers_by_stop_dataframe
        self.lines: list[Line] = []
        self.stops = set()
        self.tmax = tmax

    def add_line(self, stop_par: tuple[int, int], time: int):
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The par of stops to add to the new Line.
        * time `int`: The time it takes to go with the stop par.
        """
        line = Line(self.dataset)
        line.add_stop_par(stop_par, time)
        self.lines.append(line)
        self.stops = self.stops.union(line.stops())
        return self

    def add_stop(self, stop_par: tuple[int, int], time: int):
        """
        ### Parameters:
        * stop_par `tuple[int, int]`: The par of stops to add.
        * time `int`: The time it takes to go with the stop par.
        """
        if stop_par[0] not in self.stops and stop_par[1] not in self.stops:
            return self.add_line(stop_par, time)
        added = False
        for line in self.lines:
            if (line.time + time) > self.tmax:
                continue
            if line.last_stop() == stop_par[0]:
                line.add_stop_par(stop_par, time)
                added = True
                break
            if line.first_stop() == stop_par[1]:
                line.add_stop_par(stop_par, time, first=True)
                added = True
                break
            if line.last_stop() == stop_par[1]:
                line.add_stop_par((stop_par[1], stop_par[0]), time)
                added = True
                break
            if line.first_stop() == stop_par[0]:
                line.add_stop_par((stop_par[1], stop_par[0]), time, first=True)
                added = True
                break
        if not added:
            return self.add_line(stop_par, time)
        self.stops.add(stop_par[0])
        self.stops.add(stop_par[1])
        return self

    def to_df(self):
        """
        ### Returns the DataFrame of the lines with the stops and the coords.
        """
        df = pd.DataFrame(
            {}, columns=["LINEA", "ORIGEN", "DESTINO", "DEMANDA", "TIEMPO"]
        )
        for i, line in enumerate(self.lines):
            df_linea = line.to_df()
            df_linea["LINEA"] = i
            df = pd.concat([df, df_linea])
        df_coords = self.max_passengers_by_stop_dataframe
        #df_coords = pd.read_csv("csv/paradas_max_pasajeros.csv")
        cols = df_coords.columns
        df_coords.columns = ["ORIGEN_" + col for col in cols]
        df = df.merge(
            df_coords, how="left", left_on="ORIGEN", right_on="ORIGEN_destino"
        ).drop("ORIGEN_destino", axis=1)
        df_coords.columns = ["DESTINO_" + col for col in cols]
        df = df.merge(
            df_coords, how="left", left_on="DESTINO", right_on="DESTINO_destino"
        ).drop("DESTINO_destino", axis=1)
        return df
