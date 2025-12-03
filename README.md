## Setting up an environment with conda
Creating a conda environment:  
run: `conda create -n cs3435 python=3.12`  

Install the following packages:  
run: `conda install beautifulsoup4 seaborn requests`  

run: `conda install -c conda-forge selenium scrapy protego scikit-learn python-dotenv`

## Scrapy
run : `scrapy crawl allmovie` and data.jsonl will appear in data dir

## Code Dir

Go to code dir: `cd code`

### Collect Base URL's
run: `python collect_urls.py`  
Prints the base index urls

### Collect User Ratings
Note: Do after run Scrapy first  
run: `python collect_user_rating.py`  
Reads data.jsonl to load site with selenium to get user_ratings in data dir

### Combine to data.csv
Note: Do after having both data.jsonl and users.jsonl in data dir

## Visuals
Fo each file in dir just run `python {filename}.py` to make visual
## Models
Fo each file in dir just run `python {filename}.py` to make models


