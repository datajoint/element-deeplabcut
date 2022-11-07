from .. import model_report
from plotly.io import from_json
import plotly.graph_objects as go
from ipywidgets import widgets as wg


def main(model_report):
    poseestimation_dropdown = wg.Dropdown(
        options=model_report.PoseEstimationReport.fetch("KEY"),
        description="Result:",
        description_tooltip='Press "Load" to visualize the body parts predictions.',
        disabled=False,
        layout=wg.Layout(
            width="95%",
            display="flex",
            flex_flow="row",
            justify_content="space-between",
        ),
        style={"description_width": "80px"},
    )

    plot_button = wg.Button(
        description="Plot",
        tooltip="Plot the trajectories and traces.",
        layout=wg.Layout(width="120px", grid_area="plot_button"),
    )

    FIG_WIDTH = 1200

    FIG_LAYOUT = go.Layout(
        margin=dict(l=0, r=40, b=0, t=65, pad=0),
        width=FIG_WIDTH / 2,
        height=600,
        transition={"duration": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        modebar_remove=[
            "zoom",
            "pan",
            "select",
            "zoomIn",
            "zoomOut",
            "autoScale2d",
        ],
        title={
            "xanchor": "center",
            "yanchor": "top",
            "y": 0.97,
            "x": 0.5,
        },
        xaxis={
            "visible": True,
            "showticklabels": True,
            "showgrid": False,
        },
        yaxis={
            "visible": True,
            "showticklabels": True,
            "showgrid": False,
        },
        shapes=[
            go.layout.Shape(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1.0,
                line={"width": 1, "color": "black"},
            )
        ],
    )

    fig1 = go.Figure(layout=FIG_LAYOUT)
    fig1.update_layout(
        title={"text": "Position in Space"},
        xaxis={"title": "X (px)"},
        yaxis={"title": "Y (px)", "autorange": "reversed"},
    )

    fig2 = go.Figure(layout=FIG_LAYOUT)
    fig2.update_layout(
        title={"text": "Position over Time"},
        xaxis={"title": "Time (s)"},
        yaxis={"title": "Position (px)"},
    )

    fig1_widget = go.FigureWidget(fig1)
    fig2_widget = go.FigureWidget(fig2)

    def response(change):
        trajectories, traces = [
            from_json(x)
            for x in (
                model_report.PoseEstimationReport & poseestimation_dropdown.value
            ).fetch1("trajectory", "position_trace")
        ]

        with fig1_widget.batch_update():
            fig1_widget.data = []
            fig2_widget.data = []
            fig1_widget.add_traces(trajectories.data)
            fig2_widget.add_traces(traces.data)

    plot_button.on_click(response)

    return wg.VBox(
        [
            wg.HBox(
                [poseestimation_dropdown, plot_button],
                layout=wg.Layout(width=f"{FIG_WIDTH}px"),
            ),
            wg.HBox([fig1_widget, fig2_widget]),
        ]
    )
