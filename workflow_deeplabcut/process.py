from workflow_deeplabcut.pipeline import train, model


def run(verbose=True, display_progress=True, reserve_jobs=False, suppress_errors=False):
    """ Run all `make` methods from element-deeplabcut
    :param verbose: when True (default), display table names before populating
    :param display_progress: when True (default) Show progress bar
    :param reserve_jobs: when True, reserves job to populate in asynchronous fashion
    :param suppress_errors:  when True, do not terminate execution.

    """
    populate_settings = {'display_progress': display_progress,
                         'reserve_jobs': reserve_jobs,
                         'suppress_errors': suppress_errors}

    tables = [train.ModelTraining(),
              model.RecordingInfo(), model.ModelEvaluation(), model.PoseEstimation()]

    for table in tables:
        if verbose:
            print(f'\n---- Populating {table.table_name} ----')
            table.populate(**populate_settings)
        else:
            with QuietStdOut():
                table.populate(**populate_settings)


class QuietStdOut:
    """If verbose set to false, used to quiet tear_down table.delete prints"""
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


if __name__ == '__main__':
    run()
