import numpy as np
import datajoint as dj
from functools import partial
from plotly.io import from_json
import plotly.graph_objects as go
from ipywidgets import widgets as wg
from . import model

schema = model.schema

db_prefix = "iub-lulab_devo_"
model = dj.create_virtual_module("model", f"{db_prefix}model")

key = model.PoseEstimation.fetch("KEY", limit=1)[0]


@schema
class PoseEstimationReport(dj.Computed):
    definition = """
    -> model.PoseEstimation
    ---
    position_trace: longblob
    trajectory: longblob
    """

    def make(self, key):
        body_part, x_pos, y_pos, fps = (
            model.PoseEstimation.BodyPartPosition * model.RecordingInfo & key
        ).fetch("body_part", "x_pos", "y_pos", "fps")

        position_trace_fig = go.Figure(
            [
                go.Scatter(
                    x=np.arange(len(x_pos[0])) / fps_i,
                    y=pos,
                    name=name,
                )
                for name, pos, fps_i in zip(
                    np.hstack([body_part + " X", body_part + " Y"]),
                    np.hstack([x_pos, y_pos]),
                    np.hstack([fps, fps]),
                )
            ]
        )

        trajectory_fig = go.Figure(
            [
                go.Scatter(x=x, y=y, name=name)
                for name, x, y in zip(body_part, x_pos, y_pos)
            ]
        )

        self.insert1(
            {
                **key,
                "position_trace": position_trace_fig.to_json(),
                "trajectory": trajectory_fig.to_json(),
            }
        )


def main(db_prefix, usedb=False):
    poseestimation_dropdown = wg.Dropdown(
        options=model.PoseEstimation.fetch("KEY"),
        description="Result:",
        description_tooltip='Press "Load" to visualize the body parts.',
        disabled=False,
        layout=wg.Layout(
            width="95%",
            display="flex",
            flex_flow="row",
            justify_content="space-between",
            grid_area="poseestimation_dropdown",
        ),
        style={"description_width": "80px"},
    )

    plot_button = wg.Button(
        description="Plot",
        tooltip="Plot the trajectories and traces.",
        layout=wg.Layout(width="120px", grid_area="plot_button"),
    )

    FIG1_WIDTH = 800
    fig1 = go.Figure(
        go.Scatter(
            x=None,
            y=None,
        ),
        layout=None,
    )

    FIG2_WIDTH = 800
    fig2 = go.Figure(
        go.Scatter(
            x=None,
            y=None,
        ),
        layout=None,
    )

    fig1_widget = go.FigureWidget(fig1)
    fig2_widget = go.FigureWidget(fig2)

    def response(change):
        pass

    # fig1_widget.data[0].on_click(tooltip_click)
    plot_button.on_click(partial(response, usedb=usedb))

    return wg.VBox(
        [
            wg.HBox(
                [poseestimation_dropdown, plot_button],
                layout=wg.Layout(width=f"{FIG1_WIDTH+FIG2_WIDTH}px"),
            ),
            wg.HBox([fig1_widget, fig2_widget]),
        ]
    )
