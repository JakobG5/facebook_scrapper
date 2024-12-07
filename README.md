Here's a corrected and polished version of your README file for your **Facebook Page Scraper** project:

---

# Facebook Page Scraper

A Python-based tool for scraping Ethiopian media Facebook pages and analyzing their follower counts.

---

## Features

- **Automated Facebook login** using Selenium.  
- **Search for specific Ethiopian media pages** by customizable search terms.  
- Extracts page information, including:  
  - Page name  
  - URL  
  - Follower count  
  - Page category  
- Filters pages based on a **minimum follower count threshold**.  
- **Exports results to a CSV file** for easy analysis.

---

## Prerequisites

- **Python 3.x**  
- **Google Chrome** browser installed.  
- **Facebook account credentials**.  

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/JakobG5/facebook_scrapper.git
   cd facebook_scrapper
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Facebook credentials:

   ```
   FACEBOOK_EMAIL=your_email@example.com
   FACEBOOK_PASSWORD=your_password
   ```

---

## Usage

1. **Configure your search terms** in the `scrape.py` file:

   ```python
   search_terms = [
       "EBC Ethiopia",
       "Ethiopian News Channel",
       "Ethiopian Broadcasting Corporation",
       "Ethiopian Media Official",
       # Add more search terms as needed
   ]
   ```

2. Run the scraper:

   ```bash
   python scrape.py
   ```

3. The results will be saved as `ethiopian_pages.csv` in the project directory.

---

## Configuration

- **Default minimum follower count**: 10,000  
- **Default scroll count**: 5 times per search term (adjustable in the code).  
- Results are **automatically saved** after analyzing each qualifying page.  

---

## Output Format

The output CSV file (`ethiopian_pages.csv`) includes:  

- **Page Name**: The name of the Facebook page.  
- **URL**: Direct link to the Facebook page.  
- **Follower Count**: Total number of followers.  
- **Category**: Page category (if available).  

---

## Notes

- The scraper uses **Selenium** with the **Chrome WebDriver**.  
- **Rate limiting and careful usage are recommended** to avoid Facebook restrictions.  
- Dynamic loading on some pages may require additional processing time.  

---

## Contributing

Contributions are welcome! Please follow these steps:  

1. Fork the repository.  
2. Create a new branch (`git checkout -b feature-name`).  
3. Commit your changes (`git commit -m "Add feature description"`).  
4. Push to the branch (`git push origin feature-name`).  
5. Create a Pull Request.  

For major changes, open an issue first to discuss your ideas.  

---

## License

This project is licensed under the MIT License.  

---

If you'd like further edits or customization, let me know!
