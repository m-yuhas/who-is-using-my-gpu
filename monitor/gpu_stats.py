from typing import Any, Dict, List, Tuple, Union


import json
import re
import subprocess


CUDA_STATS_PATTERN = re.compile(
    r'\|\s+(\d+)\s+([\s\S]*)\s+(Off|On)\s+\|\s+(\d+:\d+:\d+\.\d+)\s+(Off|On)'
    r'\s+\|\s+(Off|On)\s+\|\s+\|\s+(\d+)\%\s+(\d+)C\s+(P\d)\s+(\d+)W\s+/\s+'
    r'(\d+)W\s+\|\s+(\d+)MiB\s+/\s+(\d+)MiB\s+\|\s+(\d+)\%\s+(\w+)\s+\|'
)
CUDA_PROCS_PATTERN = re.compile(
    r'\|\s+(\d+)\s+(\S+)\s+(\S+)\s+(\d+)\s+(C|G)\s+(\S+)\s+(\d+)MiB\s+\|'
)


def get_cuda_stats() -> Tuple[List[Dict[str, Union[int, str]]]]:
    """Get stastics on all CUDA GPUs in the system.

    Returns:
        Tuple ```(gpus, procs)```.

        ```gpus``` is a list of detected CUDA gpus on the system.  Each entry
        in the list is a dictionary with the following information: GPU ID
        (id), product name (type), current fan speed as a percentage of
        maximum (fan_speed), current temperature in Celcius (temperature),
        performance mode (mode), power usage in Watts (power_used), maximum
        possible power usage in Watts (power_available), memory usage in MiB
        (memory_used), total GPU memory in MiB (memory_available), and
        utilization as a percentage of cycles (utilization).

        ```procs``` is a list of processes currently running on the GPU.  Each
        entry is a dictionary with the following information: GPU ID (gpu),
        username of the process owner (owner), process type (type) with
        possible values 'C' for compute or 'G' for graphics, process name as
        reported by nvidia-smi (name), the command used to launch the process
        (command), and the memory used by the process in MiB (memory).
    """
    smi_out = subprocess.run(
        ['nvidia-smi'],
        capture_output=True,
        text=True,
        timeout=10
    )
    gpus = []
    for group in CUDA_STATS_PATTERN.finditer(smi_out):
        gpus.append({
            'id': int(group[0]),
            'type': group[1].strip(),
            'fan_speed': int(group[6]),
            'temperature': int(group[7]),
            'mode': int(group[8].strip('P')),
            'power_used': int(group[9]),
            'power_available': int(group[10]),
            'memory_used': int(group[11]),
            'memory_available': int(group[12]),
            'utilization': int(group[13]),
        })
    procs = []
    for group in CUDA_PROCS_PATTERN.finditer(smi_out):
        procs.append({
            'gpu': int(group[0]),
            'owner': get_proc_owner(int(group[3])),
            'type': group[4],
            'name': group[5],
            'command': get_proc_cmd(int(group[3])),
            'memory': int(group[6]),
        })
    return gpus, procs


def get_proc_owner(pid: int) -> str:
    """Get the owner of a process.

    Args:
        pid (int): POSIX process id.

    Returns:
        the username of the process owner.
    """
    ps_out = subprocess.run(
        ['ps', '-o', 'user=', '-p', str(pid)],
        capture_output=True,
        text=True,
        timeout=10
    )
    return ps_out.stdout


def get_proc_cmd(pid: int) -> str:
    """Get the command used to launch a process.

    Args:
        pid (int): POSIX process id.

    Returns:
        the command used to launch a process.
    """
    with open(os.path.join('proc', str(pid), 'cmdline'), 'r') as fp:
        return fp.read()
