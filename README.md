This program is designed to work in a similar manner to audio identification apps, where the user records and uploads a short segment of audio, and the software attempts to find the closest matching track on its database - if the segment of track is from a track on the database, this should be the track the software returns. This works even with a reasonable level of background noise and/or lossy audio quality, although the success rate drops off as background noise and quality loss increase, just like the commercially available apps. Track with prominent percussion tends to have higher success rates than, for example, stringed-instrument-based classical music, as note onsets are more easily detected in the frequency domain for percussive instruments than bowed stringed instruments. This is adapted from a project I created as part of my university coursework. As per the project brief, the software works by running two functions, and creates the "fingerprints" and output results as text files:

Function 1 - create "fingerprints":
1. Function arguments are the path to the directory containing a database of audio files, and the name of a text document where "fingerprints" will be saved.
2. Create a text document containing filenames of all the tracks in this directory
3. For each track in the directory -
   a. Upload the track and convert to 22050 Hz, and remove silence at at start and end of track
   b. Obtain spectrogram values by taking STFT
   c. Find local peaks - using a pre-determined matrix size, take each point of the spectrogram as the centre of a matrix. If the given point at the centre is the highest value in the matrix, this is a local piece - record the coordinates
   d. For each coordinate, find its relation to some of the other coordinates. Create a "target zone" a small amount of time ahead of a given coordinate and within a small frequency window either side.
   e. Create "hashes" from the relationship between each initial coordinate and the coordinates in its target zone - for each relationship, record the initial frequency, the subsequent frequency, and the time difference between them.
   f. The list of all the hashes for a track is what creates the fingerprint - it is a very large list for each track, thousands of characters long (depending on the matrix size). Add this line of text to the text file containing the fingerprints.

Function 2 - audio identification:
1. Run function 1 again, but with the new function arguments containing the directory of the query files, the text file containing fingerprints of the query files, and the output text file.
2. From the query fingerprints text file, go through it track by track and hash by hash - compare with each hash in each line in the database file. If a match is found, record the line number as a "hash counter". The hash counter list is incremented is the appropriate index position each time a match is found.
3. The three most likely matches are identified.
4. A line is added to the output file with the query's filename, and (most to least likely, from left to right) the three best matches are listed.
