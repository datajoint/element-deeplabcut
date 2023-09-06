import matplotlib.pyplot as plt
import plotly.graph_objects as go

from .. import model


def plot_xy(imaging, df, model_name) -> go.Figure:
    """Prepare plotly trajectory figure.

    Args:
        imaging (dj.Table): imaging table.
        df (dataframe): Pose Estimation coordinates in a panda's dataframe
        model_name(str): name of the model used



    """

    df_xy = df.iloc[:, df.columns.get_level_values(2).isin(["x", "y"])][model_name]
    df_xy.plot().legend(loc="right")
