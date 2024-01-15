import argparse as ap
import soundfile as sf

from encode import message_encode

def main():

    parser = ap.ArgumentParser(description='Hide a secret message in an audio file')

    parser.add_argument('audio', metavar='[AUDIO_FILE]', type=str, 
                        help='path of audio file to be used (.wav only)',)
    parser.add_argument('-f', '--file', action='store_true', 
                        help='accepts [TEXT] as file path')
    parser.add_argument('text', metavar='[TEXT]', type=str, 
                        help='(default: plaintext string)/ path to .txt file')
    parser.add_argument('-p', dest='password', default=0, 
                        help='input password')

    args = parser.parse_args()

    if args.file:
        f = open(args.text, "r")
        message = f.read()
        f.close()
    else:
        message = args.text

    password = args.password
    audio_path = args.audio

    key = DSSS_embed(audio_path, message, password)
    print(f'Please remember this key: {key}')

def DSSS_embed(audio_path, message, password):
    # open and use the required audio and text files
    data, sr = sf.read(audio_path)

    # if multi-channel, use channel 1
    if data.ndim > 1:
        data = data[:, 0]

    # # process the audio and text
    out, key = message_encode(message, data, password)
    sf.write('./audio/stego_audio.wav', out, sr, subtype='PCM_24')
    return key

if __name__ == '__main__':
    main()  