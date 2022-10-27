from workflow_deeplabcut.pipeline import train, model
from contextlib import nullcontext
import sys
import os


class QuietStdOut:
    """Context for suppressing standard output"""

    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def run(
    verbose: bool = True,
    display_progress: bool = True,
    reserve_jobs: bool = False,
    suppress_errors: bool = False,
):
    """Run all `make` methods from element-deeplabcut

    Args:
        verbose (bool, optional): Print which table is in being populated. Default True.
        display_progress (bool, optional): tqdm progress bar. Defaults to True.
        reserve_jobs (bool, optional): Reserves job to populate in asynchronous fashion.
            Defaults to False.
        suppress_errors (bool, optional): Suppress errors that would halt execution.
            Defaults to False.
    """
    populate_settings = {
        "display_progress": display_progress,
        "reserve_jobs": reserve_jobs,
        "suppress_errors": suppress_errors,
    }

    tables = [
        train.ModelTraining(),
        model.RecordingInfo(),
        model.ModelEvaluation(),
        model.PoseEstimation(),
    ]

    with nullcontext() if verbose else QuietStdOut():
        for table in tables:
            print(f"\n---- Populating {table.table_name} ----")
            table.populate(**populate_settings)


if __name__ == "__main__":
    run()
