from pydub import AudioSegment
from yt_dlp import YoutubeDL
import librosa
from absl import app, flags
import os
import numpy as np

FLAGS = flags.FLAGS
flags.DEFINE_string('url', None, help='youtube url to download')
flags.DEFINE_string('input_path', None, help='path to input mp3 file', short_name='i')
flags.DEFINE_integer('semitones', -2, help='number of semitones to change the pitch (-5 to +5)', short_name='s')
flags.DEFINE_string('out_name', 'audio', help='output name', short_name='o')
flags.DEFINE_string('out_dir', './out', help='path to output directory')

def download(url, out_dir):
    """download audio.mp3 from specified url"""
    ydl_options = {
        'outtmpl': '_tmp.m4a',
        'format': 'm4a'}
    with YoutubeDL(ydl_options) as ydl:
        _ = ydl.download([url])

    # convert m4a to mp3
    os.makedirs(out_dir, exist_ok=True)
    audio = AudioSegment.from_file('_tmp.m4a', format='m4a')
    audio_path = os.path.join(out_dir, 'audio.mp3')
    audio.export(audio_path, format='mp3')
    os.remove('_tmp.m4a')
    return audio_path

def change_pitch(input_path, out_dir, semitones):
    sound = AudioSegment.from_file(input_path, format='mp3')
    samples = np.array(sound.get_array_of_samples()).astype(float)

    # pitch adjustment
    shifted = librosa.effects.pitch_shift(samples, sr=sound.frame_rate, n_steps=semitones)

    # np array to audiosegment
    new_sound = AudioSegment(shifted.astype('int16').tobytes(), 
                             sample_width=sound.sample_width, 
                             frame_rate=sound.frame_rate, 
                             channels=sound.channels)

    # export
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(os.path.splitext(input_path)[0]) \
                            + f'_{"#" if semitones > 0 else "b"}{abs(semitones)}'
                            + '.mp3')
    new_sound.export(out_path, format='mp3')
    print('original:', input_path)
    print('shifted :', out_path)
    return out_path

def main(argv):
    del argv
    print('Step 1: audio initialization -> ', end='')
    if FLAGS.input_path is None:
        assert FLAGS.url is not None, 'specify url or input file path'
        print('audio downloading')
        input_path = f'./out/{FLAGS.out_name}.mp3'
        download(FLAGS.url, FLAGS.out_dir)
        if FLAGS.out_name != 'audio':
            os.rename('./out/audio.mp3', input_path)
    else:
        print('audio path set')
        input_path = FLAGS.input_path

    print('Step 2: pitch adjustment -> ', end='')
    if FLAGS.semitones == 0:
        print('no pitch adjustment')
        print('output:', input_path)
    else:
        print('pitch', 'up' if FLAGS.semitones>0 else 'down', '(it may take a minute or so)')
        _ = change_pitch(input_path, FLAGS.out_dir, FLAGS.semitones)
        # leave original downloaded file alone
        # os.remove(input_path)

if __name__ == '__main__':
    app.run(main)