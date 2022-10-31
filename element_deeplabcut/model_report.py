import numpy as np
import datajoint as dj
import plotly.graph_objects as go

from . import model

schema = dj.Schema()


def activate(schema_name, *, create_schema=True, create_tables=True):
    """
    activate(schema_name, *, create_schema=True, create_tables=True)
        :param schema_name: schema name on the database server to activate the `dlc_report` schema
        :param create_schema: when True (default), create schema in the database if it does not yet exist.
        :param create_tables: when True (default), create tables in the database if they do not yet exist.
    (The "activation" of this imaging_report module should be evoked by one of the imaging modules only)
    """

    schema.activate(
        schema_name,
        create_schema=create_schema,
        create_tables=create_tables,
    )


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
