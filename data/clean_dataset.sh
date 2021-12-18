# If cleaned directory does not exist, create it
mkdir -p cleaned

# Concatenate all file contents into a single new file
cat ./raw/*.pgn > ./cleaned/dataset.pgn

# iconv : Convert dataset to ASCII.
# //TRANSLIT : When a character can't converted, approximate with something similar looking.
# -c : If even that doesn't work, then discard those characters
# tr -d "\r" : delete windows carriage return characters.
iconv -c -f utf-8 -t ascii//TRANSLIT < ./cleaned/dataset.pgn | tr -d "\r" > ./cleaned/clean_dataset.pgn

# clean up after yourself
rm ./cleaned/dataset.pgn