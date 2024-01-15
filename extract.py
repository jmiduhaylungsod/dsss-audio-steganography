import argparse as ap
import soundfile as sf
import os

from decode import message_decode
def main():

    parser = ap.ArgumentParser(description='Extract a secret message from an audio file')

    parser.add_argument('audio', metavar='[AUDIO_FILE]', type=str, 
                        help='path of audio file to be used (.wav only)',)
    parser.add_argument('key', metavar='[KEY]', type=str, 
                        help='input provided key')
    parser.add_argument('-p', dest='password', default=0, 
                        help='input password')

    args = parser.parse_args()

    password = args.password
    stego_path = args.audio
    key = int(args.key)
    message = DSSS_extract(stego_path, password, key)
    print(f'Extracted message: {message}')
    print("Output written in 'extracted_message.txt'")

def DSSS_extract(stego_path, password, key):
# open and use the required audio and text files
    steg_data, _ = sf.read(stego_path)

    # process the audio
    msg = message_decode(steg_data, password, key*8)
    try:
        os.remove("extracted_message.txt")
    except:
        pass
    f = open("extracted_message.txt", 'w', encoding='utf-8')
    f.write(msg)
    f.close()
    return msg

if __name__ == '__main__':
    main()  