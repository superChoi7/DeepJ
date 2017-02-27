import numpy as np
import tensorflow as tf
from collections import deque
from util import *
from midi_util import *
from music import NUM_CLASSES, NOTES_PER_BAR
from dataset import load_melodies, process_melody, compute_beat, build_history_buffer
from constants import *
import math
import argparse

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Generates music.')
    parser.add_argument('model', metavar='M', type=str,
                        help='Path to the model file')
    parser.add_argument('--style', metavar='S', default=None, type=float, nargs='+',
                        help='A list that defines the weights of style')
    parser.add_argument('--bars', default=8, type=int, dest='bars',
                        help='How many bars of music to generate.')

    args = parser.parse_args()

    style = args.style
    samples = 5
    time_steps = 4
    bars = args.bars

    if style is None:
        style = np.random.rand(NUM_STYLES)

    assert len(style) == NUM_STYLES

    # Normalize style
    style /= np.linalg.norm(style)

    # Inspiration melodies
    inspirations = list(map(process_melody, load_melodies(styles, limit=samples * 10)))

    with tf.device('/cpu:0'):
        model = load_supervised_model(time_steps, args.model)

    for sample_count in range(samples):
        # A priming melody
        inspiration = None

        while inspiration is None or len(inspiration) < time_steps:
            inspiration = np.random.choice(inspirations)

        composition = generate(model, inspiration, time_steps, style, bars)
        mf = midi_encode_melody(composition)
        midi.write_midifile('out/melody_{}.mid'.format(sample_count), mf)

def generate(model, inspiration, time_steps, style, bars):
    """
    Generates a sequence
    """
    print('Generating music with style {} for {} bars:'.format(style, bars))
    # TODO: Mask the model output for Wavenet
    # out = Lambda(lambda x: x[:, -1, :], output_shape=(out._keras_shape[-1],))(out)
    # Prime the time steps
    history = build_history_buffer(time_steps, NUM_CLASSES, NOTES_PER_BAR, style, prime_beats=False)

    # Prime the RNN for one bar
    for i in range(NOTES_PER_BAR):
        model.predict([np.array([x]) for x in zip(*history)])
        note_hot = one_hot(inspiration[i], NUM_CLASSES)
        beat_input = compute_beat(i, NOTES_PER_BAR)
        completion_input = np.array([i / (len(inspiration) - 1)])
        # TODO: This completion may not be good, since it resets to 0 later.
        history.append([note_hot, beat_input, completion_input, style])

    # Compose
    composition = []

    N = NOTES_PER_BAR * bars
    for i in range(N):
        results = model.predict([np.array([x]) for x in zip(*history)])
        prob_dist = results[0]#[-1] # TODO: Used for old model architecture
        note = np.random.choice(len(prob_dist), p=prob_dist)

        note_hot = one_hot(note, NUM_CLASSES)
        beat_input = compute_beat(i, NOTES_PER_BAR)
        completion_input = np.array([i / (N - 1)])
        history.append([note_hot, beat_input, completion_input, style])

        composition.append(note)

    model.reset_states()
    print(composition)
    return composition

if __name__ == '__main__':
    main()
