# chess_engine

## Dataset

We use the KingBase 2019 database. It contains around 2.2 million chess games 
played since 1990 with a player ELO rating greater than 2000. We use the PGN
version.

The ```data/download_raw_dataset.sh``` script downloads the dataset.

The ```data/clean_dataset.sh``` script cleans the raw data and prepares it for
Python to parse.