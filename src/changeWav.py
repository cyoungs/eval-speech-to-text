import os
import sys
import subprocess

def main():

    # hardcoded in directory names
    #directory = '/Users/catharineyoungs/Documents/GradSchool/spring18/575/common-voice/cv-valid-test/'
    #output_dir = '/Users/catharineyoungs/Documents/GradSchool/spring18/575/speech-to-text/parts/'

    # pass in the full directory names for [1] the directory of the speech files and [2] the directory of the output wav
    directory = sys.argv[1]
    output_dir = sys.argv[2]

    for filename in os.listdir(directory):
        file = os.path.splitext(filename)[0]

        #print(file)
        #print(output_dir+file)

        subprocess.call(['ffmpeg', '-i', directory + filename, output_dir + file + '.wav'])

if __name__ == "__main__":
    main()