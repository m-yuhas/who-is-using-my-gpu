import json


from flask import Flask


from gpu_stats import get_cuda_gpus, get_cuda_procs


app = Flask(__name__)


@app.route('/')
def get_gpu_stats():
    """Main and only route for this application.  Return the GPU stats for
    the current machine.

    Returns:
        JSON string with three properties: ```gpus```, list of detectable GPUs
        on the system and their status; ```procs```, list of processes
        using GPU memory currently running on the system and their status; and
        ```errors```, list of errors that occurred while attempting to
        retrieve GPU stats.
    """
    stats = {'gpus': [], 'procs': [], 'errors': []}
    try:
        stats['gpus'].extend(get_cuda_gpus())
    except Exception as err:
        stats['errors'].append(f'{type(err).__name__}: {err}')
    try:
        stats['procs'].extend(get_cuda_procs())
    except Exception as err:
        stats['errors'].append(f'{type(err).__name__}: {err}')
    return json.dumps(stats)
