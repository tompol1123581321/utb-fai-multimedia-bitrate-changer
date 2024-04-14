import os
import ffmpeg
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def change_video_bitrate(input_file, output_file, video_bitrate):
    ffmpeg.input(input_file).output(output_file, video_bitrate=video_bitrate, format="mp4").run(overwrite_output=True)
    print(f"Video saved as {output_file} with bitrate {video_bitrate}")

def change_audio_bitrate(mp3_path, output_path, new_bitrate):
    audio = AudioSegment.from_file(mp3_path)
    audio.export(output_path, format="mp3", bitrate=new_bitrate)
        
        
            
def get_file_size(output_file):
    """Get the file size in megabytes."""
    try:
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
        return file_size
    except OSError:
        print(f"Error: Could not read file {output_file}")
        return 0
    
def convert_mp4_to_mp3(mp4_path, mp3_path):
    video_clip = VideoFileClip(mp4_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(mp3_path)
    audio_clip.close()
    video_clip.close()

def handle_video():
    bitrates = [500,1500,2000,3000,4000,5000]
    qualities = [95, 90, 85, 70, 50, 30]
    qualities.reverse()
    sizes = []
    input_video = 'inputs/input.mp4'  # Change 'path/to/input.mp4' to your input file path
    for bitRateValue in bitrates:
        output_video = 'outputs/bitrate_video_' + bitRateValue.__str__() + '_output.mp4' 
        change_video_bitrate(input_video, output_video, f'{bitRateValue.__str__()}k')
        sizes.append(get_file_size(output_video))
    print(sizes)
    return bitrates,sizes,qualities

def handle_audio():
    bitrates = [320,256,192,160,128,96,64]
    qualities = [95, 95, 85, 80, 60, 30,20]
    sizes = []
    input_video = 'inputs/input.mp4'  # Change 'path/to/input.mp4' to your input file path
    input_audio = "inputs/input.mp3"
    convert_mp4_to_mp3(input_video,input_audio)
    for bitRateValue in bitrates:
        output_video = 'outputs/bitrate_audio_' + bitRateValue.__str__() + '_output.mp3' 
        change_audio_bitrate(input_audio, output_video, f'{bitRateValue.__str__()}k')
        sizes.append(get_file_size(output_video))
    print(sizes)
    return bitrates,sizes,qualities




def generate_charts(bitrates,sizes,qualities,is_audio):
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(bitrates, sizes, marker='o')
    plt.title("File Size vs Bitrate")
    plt.xlabel("Bitrate (kbps)")
    plt.ylabel("File Size (MB)")
    plt.grid(True)

    # Plot subjective quality vs bitrate
    plt.subplot(1, 2, 2)
    plt.plot(bitrates, qualities, marker='o', color='red')
    plt.title("Subjective Video Quality vs Bitrate")
    plt.xlabel("Bitrate (kbps)")
    plt.ylabel("Subjective Quality (%)")
    plt.grid(True)

    # Save as PDF
    plt.tight_layout()
    if is_audio:
        plt.savefig("audio_quality_analysis.pdf")
    else:
        plt.savefig("video_quality_analysis.pdf")

    plt.show()


def main():
    video_bitrates,video_sizes,video_qualities = handle_video()
    generate_charts(video_bitrates,video_sizes,video_qualities,False)

    audio_bitrates,audio_sizes,audio_qualities = handle_audio()
    generate_charts(audio_bitrates,audio_sizes,audio_qualities,True)

if __name__ == '__main__':
    main()
