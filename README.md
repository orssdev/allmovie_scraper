# AllMovie Scraper

A web scraping project for collecting and analyzing movie data from AllMovie using Scrapy and Selenium.

## Table of Contents
- [Setup](#setup)
- [Usage](#usage)
  - [Scraping Data](#scraping-data)
  - [Collecting URLs](#collecting-urls)
  - [Collecting User Ratings](#collecting-user-ratings)
  - [Combining Data](#combining-data)
- [Visualization](#visualization)
- [Models](#models)

## Setup

### Create Conda Environment

1. Create a new conda environment with Python 3.12:
   ```bash
   conda create -n cs3435 python=3.12
   ```

2. Activate the environment:
   ```bash
   conda activate cs3435
   ```

3. Install required packages:
   ```bash
   conda install beautifulsoup4 seaborn requests
   conda install -c conda-forge selenium scrapy protego scikit-learn python-dotenv
   ```

## Usage

### Scraping Data

Run the Scrapy spider to collect movie data:
```bash
scrapy crawl allmovie
```

This will generate `data.jsonl` in the `data/` directory containing the scraped movie information.

### Collecting URLs

Navigate to the code directory and run:
```bash
cd code
python collect_urls.py
```

This prints the base index URLs for scraping.

### Collecting User Ratings

**Note:** Run the Scrapy spider first before executing this step.

```bash
python collect_user_rating.py
```

This script reads `data.jsonl` and uses Selenium to collect user ratings, saving them to `users.jsonl` in the `data/` directory.

### Combining Data

**Note:** Ensure both `data.jsonl` and `users.jsonl` exist in the `data/` directory.

```bash
python combine.py
```

This combines the scraped data and user ratings into a single `data.csv` file.

## Visualization

Navigate to the `visuals/` directory and run any visualization script:
```bash
cd visuals
python genre_vs_rating.py
python rating.py
python runtime_vs_rating.py
```

Each script generates visualizations analyzing different aspects of the movie data.

## Models

Navigate to the `models/` directory and run the modeling script:
```bash
cd models
python rating_pred.py
```

This trains machine learning models to predict movie ratings based on the collected data.


