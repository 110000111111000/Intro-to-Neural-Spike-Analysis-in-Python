"""
Utility functions for "Intro to Neural Spike Analysis
"""

from pathlib import Path
from typing import Tuple, Union, List, Literal
import pandas as pd
import numpy as np
from neo.core import SpikeTrain

data_dir = Path(__file__).parent / "data"


def get_available_sessions() -> List[str]:
    """
    Get a list of all available sessions.
    """
    return [f.name.split("-")[-1] for f in (data_dir / "allen").glob("ses-*")]


def get_brain_areas(ses_id: str) -> List[str]:
    """
    Get a list of all the brain areas recorded in a given session
    """
    spikes, _ = load_session_data(ses_id)
    return [area for area in spikes["brain_area"].unique()]


def load_session_data(
    ses_id: str, stim: str = "flash"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the data for one session.
    """
    ses = data_dir / "allen" / f"ses-{ses_id}"
    if not ses.exists():
        raise FileNotFoundError(
            "Couldn't load session. Available sessions are:", get_available_sessions()
        )
    spikes = pd.read_parquet(ses / f"{stim}_spikes.parquet")
    stimuli = pd.read_parquet(ses / f"{stim}_stimuli.parquet")
    return spikes, stimuli


def select_spikes_around_stimuli(
    spikes: pd.DataFrame,
    stimuli: pd.DataFrame,
    tmin: Union[int, float] = -0.1,
    tmax: Union[int, float] = 0.5,
) -> pd.DataFrame:
    """
    Select the spikes that happen in proximity to stimuli.
    """

    spike_times = spikes["spike_time"].values
    stim_times = stimuli["start_time"].values

    condition_matrix = (spike_times[:, None] >= stim_times + tmin) & (
        spike_times[:, None] < stim_times + tmax
    )
    selected_spikes_mask = condition_matrix.any(axis=1)
    spikes_selected = spikes[selected_spikes_mask]
    return spikes_selected


def select_brain_area(spikes: pd.DataFrame, brain_area: str) -> pd.DataFrame:
    """
    Get the brain areas recorded in a given session.
    """
    all_brain_areas = spikes["brain_area"].unique()
    brain_area = brain_area.upper()
    if not brain_area in all_brain_areas:
        raise ValueError(
            f"Brain area {brain_area} does not exist! Possible values are {all_brain_areas}"
        )
    return spikes[spikes["brain_area"] == brain_area]


def clip_spikes(spikes: pd.DataFrame, max_dur: Union[int, float]) -> pd.DataFrame:
    """
    Clip the spike trains so they don't exceed the maximum duration.
    """
    t_stop = spikes["spike_time"].min() + max_dur
    return spikes[spikes["spike_time"] <= t_stop]


def spikes_to_neo(spikes: pd.DataFrame, min_spikes: int = 0) -> List[SpikeTrain]:
    """
    Convert spikes from DataFrame to a list of SpikeTrain objects.
    """
    t_start = spikes["spike_time"].min() - 1
    t_stop = spikes["spike_time"].max() + 1
    spike_trains = []
    for unit_id in spikes["unit_id"].unique():
        brain_area = spikes[spikes["unit_id"] == unit_id]["brain_area"].iloc[0]
        spike_times = spikes[spikes["unit_id"] == unit_id]["spike_time"].to_numpy()
        spike_train = SpikeTrain(
            spike_times, units="s", t_stop=t_stop, t_start=t_start, name=brain_area
        )
        if len(spike_train.times) > min_spikes:
            spike_trains.append(spike_train)
    return spike_trains


def load_spike_trains(
    ses_id: str,
    brain_area: Union[str, None] = None,
    max_dur: Union[None, int, float] = None,
    min_spikes: int = 0,
    stim: Literal["flash", "gabor"] = "flash",
) -> List[SpikeTrain]:
    """
    Load spikes from given session and brain area.
    """
    spikes, stimuli = load_session_data(ses_id, stim)
    if brain_area is not None:
        spikes = select_brain_area(spikes, brain_area)
    spikes = select_spikes_around_stimuli(spikes, stimuli)
    if max_dur is not None:
        spikes = clip_spikes(spikes, max_dur)
    spike_trains = spikes_to_neo(spikes, min_spikes)
    return spike_trains


def find_synchronous_spikes(
    spike_trains: List[SpikeTrain],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Find the synchronous spikes in a list of spike trains.
    Arguments:
        sts (List of SpikeTrain): list of spike train objects.
    Returns:
        (np.ndarray): 1-dimensional array of the synchronous spike times (times are repeated for each synchronous spikes)
        (np.ndarray): 1-dimensional array with the indices of the spike trains containing the synchronous spikes
    """
    all_spikes = np.concatenate([spike_train.times for spike_train in spike_trains])
    all_trains = np.concatenate(
        [[i] * len(spike_train.times) for i, spike_train in enumerate(spike_trains)]
    )
    times = []
    units = []
    for s in np.unique(all_spikes):
        idx = np.where(all_spikes == s)[0]
        if len(idx) > 1:
            times.append(all_spikes[idx])
            units.append(all_trains[idx])
    if len(times) > 0:
        times = np.concatenate(times)
        units = np.concatenate(units)
    else:
        times = np.array([])
        units = np.array([])
        print("Found no synchronous spikes")
    return times, units
