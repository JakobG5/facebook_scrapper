# Facebook Page Scraper

A Python-based tool for scraping Ethiopian media Facebook pages and analyzing their follower counts.

## Features

- Automated Facebook login
- Search for specific Ethiopian media pages
- Extract page information including:
  - Page name
  - URL
  - Follower count
  - Page category
- Minimum follower threshold filtering
- CSV export of results

## Prerequisites

- Python 3.x
- Chrome browser installed
- Facebook account credentials

## Installation

1. Clone the repository:
bash
git clone https://github.com/JakobG5/facebook_scrapper.git
cd facebook_scrapper

2. Install required packages:
bash
pip install -r requirements.txt

3. Create a `.env` file in the project root and add your Facebook credentials:
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password

## Usage

1. Configure your search terms in `scrape.py`:

    python
   search_items = [
    "EBC Ethiopia",
    "Ethiopian News Channel",
    "Ethiopian Broadcasting Corporation",
    "Ethiopian Media Official",
    # Add more search terms as needed
   ]

2. Run the scraper:
bash
python scrape.py


The results will be saved to `ethiopian_pages.csv`.

## Configuration

- Default minimum follower count: 10,000
- Default scroll count: 5 times per search term
- Results are automatically saved after each qualifying page is found

## Output Format

The CSV output includes:
- Page Name
- URL
- Follower Count
- Category

## Notes

- The scraper uses Selenium with Chrome WebDriver
- Rate limiting and careful usage is recommended to avoid Facebook restrictions
- Some pages may require additional processing time due to dynamic loading

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
