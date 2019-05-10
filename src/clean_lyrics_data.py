import csv
i = 0
with open('../data/raw_lyrics.csv') as csvfile:
    with open('../data/lyrics.txt', 'w') as fout:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fout.write(row['lyrics'])
            i += 1
            if i > 12500:
                break