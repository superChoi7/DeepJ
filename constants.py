import os

# Define the musical styles
genre = [
    'classical',
    'romantic'
]

styles = [
    [
        'data/classical/beethoven',
        'data/classical/haydn',
        'data/classical/mozart'
    ],
    [
        'data/romantic/borodin',
        'data/romantic/brahms',
        'data/romantic/tschai'
    ]
]

NUM_STYLES = sum(len(s) for s in styles)

# MIDI Resolution
DEFAULT_RES = 96
MIDI_MAX_NOTES = 128
MAX_VELOCITY = 127

# Number of octaves supported
NUM_OCTAVES = 4
OCTAVE = 12

# Min and max note (in MIDI note number)
MIN_NOTE = 36
MAX_NOTE = MIN_NOTE + NUM_OCTAVES * OCTAVE
NUM_NOTES = MAX_NOTE - MIN_NOTE

# Number of beats in a bar
BEATS_PER_BAR = 4
# Notes per quarter note
NOTES_PER_BEAT = 4
# The quickest note is a half-note
NOTES_PER_BAR = NOTES_PER_BEAT * BEATS_PER_BAR

# Training parameters
BATCH_SIZE = 16
SEQ_LEN = 8 * NOTES_PER_BAR

# Hyper Parameters
OCTAVE_UNITS = 64
STYLE_UNITS = 64
NOTE_UNITS = 3
TIME_AXIS_UNITS = 256
NOTE_AXIS_UNITS = 128

TIME_AXIS_LAYERS = 2
NOTE_AXIS_LAYERS = 2

# Move file save location
OUT_DIR = 'out'
MODEL_DIR = os.path.join(OUT_DIR, 'models')
MODEL_FILE = os.path.join(OUT_DIR, 'model.h5')
SAMPLES_DIR = os.path.join(OUT_DIR, 'samples')
CACHE_DIR = os.path.join(OUT_DIR, 'cache')
