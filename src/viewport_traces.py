import help_functions as hf
import pandas as pd
import numpy as np

def read_trace(DATA_DIR, u_id, v_id):
    """Reads the viewport locations for a given user and video

    Parameters
    ----------
    u_id : int
        The user's ID in Wu's dataset (1-49)
    v_id : int
        The video's ID in Wu's dataset (0-8)

    Returns
    -------
    list
        A list of tuples, containing a timestamp, phi and theta
    """
    trace_df = pd.read_csv(f"{DATA_DIR}/traces/{u_id}/video_{v_id}.csv").drop_duplicates(subset=['PlaybackTime']).sort_values(by='PlaybackTime')
    trace_df['phi'], trace_df['theta'] = zip(*trace_df.apply(lambda r: hf.cart_to_spher(*hf.quat_to_cart(r['UnitQuaternion.x'], r['UnitQuaternion.y'], r['UnitQuaternion.z'], r['UnitQuaternion.w'])), axis=1))
    return trace_df[['PlaybackTime', 'phi', 'theta']].to_numpy()