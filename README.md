# Climate Tech Jobs Scraper

#### This project scrapes the Climate Tech Jobs webpage and saves the HTML content to a file.

## Prerequisites

- Python 3.x
- Google Chrome browser

## Setup Instructions

### 1. Clone the Repository

First, clone this repository to your local machine:

`https://github.com/Jagadisg/smartify_scrapper.git`

`cd smartify_scrapper`

### 2. Create a Virtual Environment
Create a virtual environment to isolate your dependencies:

`python -m venv venv`

Activate the virtual environment:

**On Windows:**
`.\venv\Scripts\activate`

**On macOS and Linux:**
`source venv/bin/activate`

### 3. Install the Requirements
Install the required packages from requirements.txt:

`pip install -r requirements.txt`

### 4. To run in local environment. 
comment out the lambda handler function and add `asyncio.run(main)` at last line.

Run this command in terminal or cmd `python main.py`
