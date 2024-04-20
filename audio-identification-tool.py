# Audio identification tool for assignment 2 - 221063228 - ECS7006

import librosa
import numpy as np
import scipy
import os
from pathlib import Path


def fingerprintBuilder(path_to_database, path_to_fingerprints):
    for filename in os.listdir(path_to_database):
        with open ("database_filenames.txt", "a") as db_filenames:
            db_filenames.write(str(filename) + "\n")
    for filename in os.listdir(path_to_database):
        track, Fs = librosa.load(path_to_database + filename)
        track = np.trim_zeros(track)
        f, t, Zxx = scipy.signal.stft(track, nperseg = 2048)
        track_stft = np.transpose(abs(Zxx))
        tau = 5 # x-axis parameter
        kappa = 17 # y-axis parameter
        x_coords = []
        y_coords = []
        for segment in range(tau, len(track_stft) - tau):
            for frequency in range(kappa, len(track_stft[0]) - kappa):
                matrix = track_stft[segment - tau : segment + tau + 1 , frequency - kappa : frequency + kappa +1]
                if track_stft[segment, frequency] == matrix.max() and track_stft[segment, frequency] > 0:
                    x_coords.append(segment)
                    y_coords.append(frequency)
        x_coords = np.array(x_coords)
        y_coords = np.array(y_coords)
        for index in range (0, len(x_coords)):
            tzone_x_coords = []
            tzone_y_coords = []
            x_tzone_min = x_coords[index] + 20
            x_tzone_max = x_coords[index] + 30
            y_tzone_min = y_coords[index] - 25
            y_tzone_max = y_coords[index] + 25
            x_zero = x_coords[index]
            y_zero = y_coords[index]
            for x_number in range(0, len(x_coords)):
                if x_coords[x_number] >= x_tzone_min and x_coords[x_number] <= x_tzone_max:
                    if y_coords[x_number] >= y_tzone_min and y_coords[x_number] <= y_tzone_max:
                        tzone_x_coords.append(x_coords[x_number])
                        tzone_y_coords.append(y_coords[x_number])
            hashes = [0] * len(tzone_x_coords)
            for timestamp in range (0, len(tzone_x_coords)):
                hashes[timestamp] = f"{y_zero}:{tzone_y_coords[timestamp]}:{tzone_x_coords[timestamp] - x_zero}"
            hashes_str = str(hashes).replace("[","").replace("]","").replace(" ","").replace("'","")
            with open(path_to_fingerprints, "a") as fingerprints:
                fingerprints.write(hashes_str + ",")
        with open(path_to_fingerprints, "a") as fingerprints:
            fingerprints.write("\n")
    return


def audioIdentification(path_to_queryset, path_to_query_fingerprints, path_to_output_txt):
    fingerprintBuilder(path_to_queryset, path_to_query_fingerprints)
    with open("database_fingerprints.txt", "r") as db_fp:
        db_hashes = db_fp.readlines()
    with open("query_fingerprints.txt", "r") as q_fp:
        q_hashes = q_fp.readlines()
    with open ("database_filenames.txt", "r") as db_f_txt:
        db_filenames = db_f_txt.readlines()
    for line in range(0, len(q_hashes)):
        q_hashes[line] = q_hashes[line].split(',')
    query_audio_filenames = []
    for filename in os.listdir(path_to_queryset):
        query_audio_filenames.append(filename)
    for query in range (0, len(q_hashes)):
        hash_counter = [0] * len(db_hashes)
        for hash in range(0, len(q_hashes[query])):
            for song in range(0, len(db_hashes)):
                if q_hashes[query][hash] in db_hashes[song]:
                    hash_counter[song] += 1
        most_common = 0
        second_most_common = 0
        third_most_common = 0        
        for i in range(0, len(hash_counter)):
            if hash_counter[i] >= most_common:
                third_most_common = second_most_common
                second_most_common = most_common
                most_common = hash_counter[i]
            elif hash_counter[i] >= second_most_common and hash_counter[i] <= most_common:
                third_most_common = second_most_common
                second_most_common = hash_counter[i]
            elif hash_counter[i] >= third_most_common and hash_counter[i] <= second_most_common:
                third_most_common = hash_counter[i]
        most_common_index = hash_counter.index(most_common)
        second_most_common_index = hash_counter.index(second_most_common)
        third_most_common_index = hash_counter.index(third_most_common)
        output_string = f"{query_audio_filenames[query]}\t\t{db_filenames[most_common_index]}\t\t{db_filenames[second_most_common_index]}\t\t{db_filenames[third_most_common_index]}\n".replace("\n","")
        with open (path_to_output_txt, "a") as output_txt:
            output_txt.write(str(output_string) + "\n")
    return