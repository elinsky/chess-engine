# If raw directory does not exist, create it
mkdir -p raw

# Download zip file containing PGN files
wget https://archive.org/download/KingBase2019/KingBase2019-pgn.zip -P ./raw

# Unzip file
unzip ./raw/KingBase2019-pgn.zip -d ./raw

# remove zip file
rm ./raw/KingBase2019-pgn.zip
