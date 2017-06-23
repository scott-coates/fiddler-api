import dryscrape
import sys

if 'linux' in sys.platform:
  # start xvfb in case no X is running. Make sure xvfb
  # is installed, otherwise this won't work!
  dryscrape.start_xvfb()

scraper = dryscrape
