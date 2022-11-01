import inspect
import importlib
import numpy as np
import datajoint as dj
import plotly.graph_objects as go

from . import model

schema = dj.Schema()


def activate(schema_name, *, create_schema=True, create_tables=True):
    """Activate this schema.

    Args:
        schema_name (str): schema name on the database server
        create_schema (bool): when True (default), create schema in the database if it
                            does not yet exist.
        create_tables (bool): when True (default), create schema tables in the database
                                if they do not yet exist.
    """
    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
    )


@schema
class PoseEstimationReport(dj.Computed):
    """Computes and stores plotly figures from the body part position predictions.

    Attributes:
        PoseEstimation (foreign key): Pose estimation key.
        position_trace (longblob): Plotly figure of predictions as a function time, in json string format.
        trajectory (longblob): Plotly figure of predictions to show 2d trajectories."""

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
                go.Scatter(x=np.r_[: len(x_pos[0])] / fps_i, y=pos, name=name)
                for name, pos, fps_i in zip(
                    np.dstack([body_part + " X", body_part + " Y"]).ravel(),
                    np.dstack([x_pos, y_pos]).ravel(),
                    np.dstack([fps, fps]).ravel(),
                )
            ]
        )

        trajectory_fig = go.Figure(
            [
                go.Scatter(x=x, y=y, name=name, mode="markers", marker=dict(size=3))
                for name, x, y in zip(body_part, x_pos, y_pos)
            ]
        )
        trajectory_fig.update_yaxes(autorange="reversed")

        self.insert1(
            {
                **key,
                "position_trace": position_trace_fig.to_json(),
                "trajectory": trajectory_fig.to_json(),
            }
        )
