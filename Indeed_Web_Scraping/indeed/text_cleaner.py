from bs4 import BeautifulSoup # For HTML parsing
import urllib2 # Website connections
import re # Regular expressions
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


def text_cleaner(website):
    '''
    This function just cleans up the raw html so that I can look at it.
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    '''
    try:
        site = urllib2.urlopen(website).read()  # Connect to the job posting
    except:
        return  # Need this in case the website isn't there anymore or some other weird connection problem

    soup_obj = BeautifulSoup(site)  # Get the html from the site

    for script in soup_obj(["script", "style"]):
        script.extract()  # Remove these two elements from the BS4 object

    text = soup_obj.get_text()  # Get the text from this

    lines = (line.strip() for line in text.splitlines())  # break into lines

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  # break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' '  # Need to fix spacing issue
        return chunk_out

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode(
        'utf-8')  # Get rid of all blank lines and ends of line

    # Now clean out all of the unicode junk (this line works great!!!)

    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')  # Need this as some websites aren't formatted
    except:  # in a way that this works, can occasionally throw
        return  # an exception

    text = re.sub("[^a-zA-Z.+3]", " ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
    # Also include + for C++


    text = text.lower().split()  # Go to lower case and split them apart

    stop_words = set(stopwords.words("english"))  # Filter out any stop words
    text = [w for w in text if not w in stop_words]

    text = list(set(text))  # just get the set of these. Ignore counts

    return text


def state_extract(input, us_state_abbrev=us_state_abbrev):
    input = re.sub('[0-9]', '', input).strip()
    if ',' in input:
        state = input.split(',')[1].strip()
        city  = input.split(',')[0].strip()
    else:
        state = us_state_abbrev[input]
        city  = ''
    return city, state