import numpy as np
import sys

def read_frames(input_path, output_path, n_frames=None):
    '''
    Reads a specified number of frames from an input file and writes them to an output file.
    '''

    # Extracting trajectory data for first n frames
    with open(input_path, 'r') as fin, open(output_path, 'w') as fout:
        frame_count = 0
        for line in fin:
            if line.startswith('ITEM: TIMESTEP'):
                frame_count += 1
                if n_frames is not None and frame_count > n_frames:
                    break
            fout.write(line) 

    return min(frame_count, n_frames) if n_frames is not None else frame_count 

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python read_frames.py <input_file> <output_file> [n_frames]", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    n_frames = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    written = read_frames(input_file, output_file, n_frames)
    print(f"wrote: {written} frame(s) to {output_file}")