set -e
set -x


NLTK_DATA_PATH=~/nltk_data

function download_nltk_data {
  pip install nltk~=3.1.0
  python -m nltk.downloader punkt
  python -m nltk.downloader maxent_treebank_pos_tagger
  python -m nltk.downloader averaged_perceptron_tagger
}

if [ ! -d $NLTK_DATA_PATH ]; then
  download_nltk_data
else
  echo "Using cached nltk data from $NLTK_DATA_PATH"
fi
