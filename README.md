A safe and free way to retrieve the people names, LinkedIn URLs, and title cards of a specific search.

### Step one: Find your search URL

<p align="center">
  <img width="394" height="48" alt="Screenshot 2026-11-19 at 3 03 14 PM" src="https://github.com/user-attachments/assets/37613bb6-0727-491d-9d58-dfa4aa48c94d" />
</p>

If you're on LinkedIn Premium, you may see "I'm looking for..." in the search bar, which means your account has access to a natural language search, e.g. "All former OpenAI employees working at Anthropic," it'll return that list (accuracy not guaranteed).

<p align="center">
  <img width="825" height="584" alt="Screenshot 2026-11-19 at 3 06 40 PM" src="https://github.com/user-attachments/assets/4ead9f9c-e7c1-4415-bd1c-042e3d36a878" />
</p>


If you're on standard LinkedIn, you can just use a regular search and filter using All filters.

<p align="center">
  <img width="525" height="590" alt="Screenshot 2026-11-19 at 3 10 24 PM" src="https://github.com/user-attachments/assets/20e1d22d-b73c-45bc-9af2-e49d5ec80933" />
</p>

Copy the URL that comes up after you select Show results. It'll look butt ugly. This is GOOD! Ex: `https://www.linkedin.com/search/results/people/?keywords=Anthropic&origin=FACETED_SEARCH&currentCompany=%5B%2274126343%22%5D&pastCompany=%5B%2211130470%22%5D`

### Step two: Clone or download search_scrape.py

Yeah it's pretty straightforward. You may need to `pip install playwright && playwright install chromium` to run.

Once you have it, open the file and replace BASE with that ugly URL you just copied.

<p align="center">
  <img width="567" height="277" alt="Screenshot 2026-11-19 at 3 17 54 PM" src="https://github.com/user-attachments/assets/b2dff8a7-d46b-4b16-be96-78735b20453d" />
</p>


### Step three: Start Chrome in a debugging port

Sounds technical. Not really. Open Terminal/cmd/whatever you got and run:

Mac: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="$HOME/li_chrome"`

Windows: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\li_chrome"`

Linux: `google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/li_chrome"`

### Step four: Without closing that tab, run search_scrape.py

`python search_scrape.py` will cycle through all the pages (max 100 pages, as that's LinkedIn's max), doing the rests and pauses until it's done. It'll take a while, so I recommend running `python search_scrape.py 1 2` just to get a sample.

Start from page #n: `python search_scrape.py n`
<br>Get pages [a, b]: `python search_scrape.py a b`

Find output in `profiles.csv`, wherever you ran your scraper. Have fun!
