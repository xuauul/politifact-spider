# LINE Spider

This is a simple project for crawling COVID-19 news from [PolitiFact](https://www.politifact.com).

## Requirements

* python 3.X
* beautifulsoup4
* selenium

## Data Format

```
{
    "date": "July 20, 2021"
    "label": "...",
    "source": "...",
    "text": "...",
    "verify_date": "...",
    "verify_url": "..."
}
...
```

## Usage

```
python crawler.py
```