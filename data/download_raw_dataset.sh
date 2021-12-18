# If raw directory does not exist, create it
mkdir -p raw

# Download zip file containing PGN files
wget https://archive.org/download/KingBase2019/KingBase2019-pgn.zip -P ./raw

# Unzip file
unzip KingBase2019-pgn.zip

# remove zip file
rm  KingBase2019-pgn.zip

