import numpy as np
import os
import file_sizes
import player
import rate_adaptation as ra
import viewport_traces
import argparse

parser = argparse.ArgumentParser(description='Headless VRClient', prog='VRClient', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--user', default='25', help='User ID in Wu dataset')
parser.add_argument('--video', default='0', help='Video ID in Wu dataset')
# parser.add_argument('--quality', default='3', help='Quality index between 1 (low) to 5 (high)')
parser.add_argument('--prefetch', action='store_true', help='If present, times in the logs are regarded as response times with prefetching')
parser.add_argument('--perfect-prediction', action='store_true', help='If present, tells the edge cache server to use perfect prediction when prefetching')
parser.add_argument('--fold', default='1', help='For testing purposes. Number between 1 and 8 that identifies the model the traces are going to be feed to')
parser.add_argument('--k', default='-1', help='Viewport size: number of tiles per segment')
args = vars(parser.parse_args())


# Data directory
DATA_DIR = "."
K = int(args['k'])
FOLD = int(args['fold'])

# User properties
u_id = int(args['user'])        # User ID in the dataset collected by Wu et al.

# Video properties
v_id = int(args['video'])     # Video ID in the dataset collected by Wu et al.
t_hor = 4                       # Number of horizontal tiles
t_vert = 4                      # Number of vertical tiles
n_qual = 2                      # Number of quality representations
n_seg = 30                      # Number of video segments
seg_dur = 1.065                 # Segment duration [s]

# logging
LOG_PATH = f'./logs/logs_pred_model/k{K}/fold{FOLD}' if not args['perfect_prediction'] else f'./logs/logs_perfect_pred/k{K}/fold{FOLD}'
LOG_SEGMENT = f'log_seg_u{u_id}_prefetch.txt' if args['prefetch'] else f'log_seg_u{u_id}_no_prefetch.txt'
LOG_SEG_QUALITY = f'log_seg_quality_u{u_id}_prefetch.txt' if args['prefetch'] else f'log_seg_quality_u{u_id}_no_prefetch.txt'
LOG_SEG_FREEZES = f'log_seg_freezes_u{u_id}_prefetch.txt' if args['prefetch'] else f'log_seg_freezes_u{u_id}_no_prefetch.txt'
LOG_STARTUP_DELAY = f'log_startup_delay_u{u_id}_prefetch.txt' if args['prefetch'] else f'log_startup_delay_u{u_id}_no_prefetch.txt'

# Player properties
buffer_size = 2.130     # Buffer size [s]
vp_deg = 110            # Viewport size [deg]

# Server properties
host = os.getenv("CACHE_HOST") if args['prefetch'] else os.getenv("SERVER_HOST")             # Host IP
port = os.getenv("CACHE_PORT") if args['prefetch'] else os.getenv("SERVER_PORT")             # Host port
query_string = f'k={K}&fold={FOLD}&prefetch={args["prefetch"]}&perfect_prediction={args["perfect_prediction"]}&user_id={u_id}'


# Configurations
rah = 2                 # 0: UVP, 1: UVQ, 2: CTF, 3: Petrangeli, 4: Hosseini
reorder = 0             # 0: no reassignment, 1: reassignment
predict = 1             # 0: last known, 1: spherical walk, 2: perfect
n_conn = 1              # Number of parallel TCP connections

# Read file sizes for the given video and tiling scheme
file_sizes = file_sizes.read(DATA_DIR, v_id, t_hor, t_vert, n_qual, n_seg)

# Read timestamps and viewport locations for the given user and video
trace = viewport_traces.read_trace(DATA_DIR, u_id, v_id)

# Initialize rate adaptation heuristic
if rah == 0:
    vp_rad = vp_deg * np.pi / 180
    rate_adapter = ra.UVP(buffer_size, seg_dur, t_hor, t_vert, n_qual, vp_rad)
elif rah == 1:
    vp_rad = 2 * np.pi
    rate_adapter = ra.UVP(buffer_size, seg_dur, t_hor, t_vert, n_qual, vp_rad)
elif rah == 2:
    rate_adapter = ra.CTF(buffer_size, seg_dur, t_hor, t_vert, n_qual)
elif rah == 3:
    rate_adapter = ra.Petrangeli(buffer_size, seg_dur, t_hor, t_vert, n_qual)
else:
    rate_adapter = ra.Hosseini(buffer_size, seg_dur, t_hor, t_vert, n_qual)

# Initiate video player
p = player.Player(host, port, query_string, buffer_size, seg_dur, v_id, u_id, n_seg, t_hor, t_vert,
                  file_sizes, rate_adapter, reorder, predict, n_conn, trace, args['prefetch'])

# Run the video session
p.run()
with open(f'{LOG_PATH}/{v_id}/{LOG_SEGMENT}', 'w') as log_s:
    for t, bw in zip(p.download_times, p.bandwidth_log):
        log_s.write(f'{t}, {bw}\n')

with open(f'{LOG_PATH}/{v_id}/{LOG_SEG_QUALITY}', 'w') as log_s:
    for q_log in p.quality_log:
        log_s.write(f'{q_log}\n')
        
with open(f'{LOG_PATH}/{v_id}/{LOG_SEG_FREEZES}', 'w') as log_s:
    log_s.write(f'{p.freeze_freq}, {p.freeze_dur}\n')

with open(f'{LOG_PATH}/{v_id}/{LOG_STARTUP_DELAY}', 'w') as log_s:
    log_s.write(f'{p.startup_delay}\n')
