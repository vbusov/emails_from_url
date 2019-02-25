# emails_from_url
A Python script for scraping URLs for email addresses

The script uses requests library to access URLs by default, which only gets static HTML and often gets poor results. To render the URL with Selenium, run the script with '-js' from the command line (requires selenium and the Chrome webdriver, links at https://seleniumhq.github.io/selenium/docs/api/py/index.html#drivers). Input file for the URL is url.txt, output is emails.csv.
