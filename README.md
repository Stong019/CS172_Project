# CS172_Project: Reddit Post Collector

Crawled Data - [https://drive.google.com/drive/folders/1RXtagArfV1uIKl7C-WqpscmX4jXI1YMi?usp=sharing](https://drive.google.com/drive/folders/1RXtagArfV1uIKl7C-WqpscmX4jXI1YMi?usp=sharing)

## Installing Reddit API
Setting up Reddit Scraper: https://www.youtube.com/watch?v=nssOuD9EcVk

## Prequisite Installation and Setup

1. Install Python
   
   Download and install Python


2. Install necessary Python packages: PRAW and TQDM
   ```bash
   pip install praw tqdm

## Running the Script
1. **Open your terminal** and navigate to your project directory:
   ```bash
   cd path/to/your/project

2. Setup and activate virtual environment
   ```bash
   python -m venv env
   
3. Windows
   ```bash
   env\Scripts\activate
   ```
   Linux/macOS
   ```bash
   source env/bin/activate
4. Run the script
   ```bash
   python scraper.py

## Using the Script

1. Follow the prompts to enter the number of subreddits to scrape
2. Enter subreddits to scrape
3. Enter Number of Posts to Scrape for each subreddit

5. When done using scraper deactivate the virtual environment using command:
   ```bash
   deactivate
