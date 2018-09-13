"""Visualizing Twitter Sentiment Across America"""

from data import word_sentiments, load_tweets
from datetime import datetime
from geo import us_states, geo_distance, make_position, longitude, latitude
try:
    import tkinter
    from maps import draw_state, draw_name, draw_dot, wait
    HAS_TKINTER = True
except ImportError as e:
    print('Could not load tkinter: ' + str(e))
    HAS_TKINTER = False
from string import ascii_letters
from ucb import main, trace, interact, log_current_line


###################################
# Phase 1: The Feelings in Tweets #
###################################

# tweet data abstraction (A), represented as a list
# -------------------------------------------------

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a Python list.

    Arguments:
    text  -- A string; the text of the tweet, all in lowercase
    time  -- A datetime object; the time that the tweet was posted
    lat   -- A number; the latitude of the tweet's location
    lon   -- A number; the longitude of the tweet's location

    >>> t = make_tweet('just ate lunch', datetime(2014, 9, 29, 13), 122, 37)
    >>> tweet_text(t)
    'just ate lunch'
    >>> tweet_time(t)
    datetime.datetime(2014, 9, 29, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    122
    >>> tweet_string(t)
    '"just ate lunch" @ (122, 37)'
    """
    return [text, time, lat, lon]

def tweet_text(tweet):
    """Return a string, the words in the text of a tweet."""
    # return the zeroth index of tweet
    return tweet[0]

def tweet_time(tweet):
    """Return the datetime representing when a tweet was posted."""
    # return the first index of tweet
    return tweet[1]

def tweet_location(tweet):
    """Return a position representing a tweet's location."""
    # return a list with indices two and three of tweet         // use make_position function
    return make_position(tweet[2], tweet[3])



# tweet data abstraction (B), represented as a function
# -----------------------------------------------------

def make_tweet_fn(text, time, lat, lon):
    """An alternate implementation of make_tweet: a tweet is a function.

    >>> t = make_tweet_fn('just ate lunch', datetime(2014, 9, 29, 13), 122, 37)
    >>> tweet_text_fn(t)
    'just ate lunch'
    >>> tweet_time_fn(t)
    datetime.datetime(2014, 9, 29, 13, 0)
    >>> latitude(tweet_location_fn(t))
    122
    """
    # Please don't call make_tweet in your solution

    # create a function that will return a value corresponding to a string t    // create tweet(t) function
    # use a series of conditionals checking t                                   // check t=='text', 'time', etc
    # return the function created earlier                                       // return tweet

    def tweet(t):
        if t=='text':
            return text
        elif t=='time':
            return time
        elif t=='lat':
            return lat
        else:
            return lon
    return tweet

def tweet_text_fn(tweet):
    """Return a string, the words in the text of a functional tweet."""
    # call tweet function
    return tweet('text')

def tweet_time_fn(tweet):
    """Return the datetime representing when a functional tweet was posted."""
    # call tweet function
    return tweet('time')

def tweet_location_fn(tweet):
    """Return a position representing a functional tweet's location."""
    # call make_position using tweet function for each parameter
    return make_position(tweet('lat'), tweet('lon'))

### === +++ ABSTRACTION BARRIER +++ === ###

def tweet_string(tweet):
    """Return a string representing a tweet."""
    location = tweet_location(tweet)
    point = (latitude(location), longitude(location))
    return '"{0}" @ {1}'.format(tweet_text(tweet), point)

def tweet_words(tweet):
    """Return the words in a tweet."""
    return extract_words(tweet_text(tweet))

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    >>> extract_words('@(cat$.on^#$my&@keyboard***@#*')
    ['cat', 'on', 'my', 'keyboard']
    """
    # check each word in the string                         // make for loop "for word in text"
    # check each letter in each word                        // place another for loop within previous for loop "for letter in word"
    # check if the word is a letter (or space)              // use an if statement "letter in (ascii_letters+" ")"
    # if yes, add the letter to an empty string             // use += operator adding letter
    # if not, add a space instead                           // use += operator adding " "
    # return the text as a list of words                    // use the built-in split function

    text_final = ""
    for word in text:
        for letter in word:
            if letter in (ascii_letters+" "):
                text_final += letter
            else:
                text_final += " "
    return text_final.split()

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> positive = make_sentiment(0.2)
    >>> neutral = make_sentiment(0)
    >>> unknown = make_sentiment(None)
    >>> has_sentiment(positive)
    True
    >>> has_sentiment(neutral)
    True
    >>> has_sentiment(unknown)
    False
    >>> sentiment_value(positive)
    0.2
    >>> sentiment_value(neutral)
    0
    """
    assert (value is None) or (-1 <= value <= 1), 'Bad sentiment value'
    # return a sentiment object which is a single-item list 
    return [value]

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    # use conditionals to check if the sentiment is none        // take index 0 of of s
    # if yes, return False; else, return True

    if s[0] == None:
        return False
    return True

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    # return the zeroth index of s
    return s[0]

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    # Learn more: http://docs.python.org/3/library/stdtypes.html#dict.get
    return make_sentiment(word_sentiments.get(word))

def analyze_tweet_sentiment(tweet):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet('berkeley golden bears!', None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    # get a list of the words in tweet                          // use the tweet_words function, set to sentiment
    # check each word in the list created                       // use a for loop "for word in sentiment"
    # check if a sentiment exists in the word                   // use the has_sentiment function 
    # if yes, add the sentiment value to some sum               // use the sentiment_value and get_word_sentiment functions
    # also, increment length                                    // length += 1
    # if length is not zero, check if sentiment value is 0      // return a sentiment with value 0
    # if sentiment value is not 0, return an average            // return a sentiment with value sum_sentiment/length
    # if length is zero, return a sentimient of value None      // return make_sentiment(None)

    sentiment = tweet_words(tweet)
    sum_sentiment = 0
    length = 0
    for word in sentiment:
        if has_sentiment(get_word_sentiment(word)):
            sum_sentiment += sentiment_value(get_word_sentiment(word))
            length += 1
    if length != 0:
        if sum_sentiment == 0:
            return make_sentiment(0)
        else:
            return make_sentiment(sum_sentiment/length)
    return make_sentiment(None)


#################################
# Phase 2: The Geometry of Maps #
#################################

def apply_to_all(map_fn, s):
    return [map_fn(x) for x in s]

def keep_if(filter_fn, s):
    return [x for x in s if filter_fn(x)]

def find_centroid(polygon):
    """Find the centroid of a polygon. If a polygon has 0 area, use the latitude
    and longitude of its first position as its centroid.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    Arguments:
    polygon -- A list of positions, in which the first and last are the same

    Returns 3 numbers: centroid latitude, centroid longitude, and polygon area.

    >>> p1 = make_position(1, 2)
    >>> p2 = make_position(3, 4)
    >>> p3 = make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1] # First vertex is also the last vertex
    >>> round_all = lambda s: [round(x, 5) for x in s]
    >>> round_all(find_centroid(triangle))
    [3.0, 2.0, 6.0]
    >>> round_all(find_centroid([p1, p3, p2, p1])) # reversed
    [3.0, 2.0, 6.0]
    >>> apply_to_all(float, find_centroid([p1, p2, p1])) # A zero-area polygon
    [1.0, 2.0, 0.0]
    """
    # get a value for n in the equation on Wikipedia            // n = len(polygon) - 1
    # compute area                                              // use a for loop "for i in range(n)", implement formula for area
    # check if area is zero; if yes, set to first position      // set x to latitude(polygon[0]) and y to longitude(polygon[0])
    # if not, compute the values of x and y                     // use a for loop "for i in range(n)", implement formulae for x and y
    # return list of x, y and area                              // make sure to take the absolute value of area

    n = len(polygon) - 1
    area = 0
    x = 0
    y = 0
    for i in range(n):
        area += (latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i]))/2
    if area==0:
        x = latitude(polygon[0])
        y = longitude(polygon[0])
    else:
        for i in range(n):
            x += ((latitude(polygon[i]) + latitude(polygon[i+1]))*(latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i])))/(6*area)
            y += ((longitude(polygon[i]) + longitude(polygon[i+1]))*(latitude(polygon[i])*longitude(polygon[i+1]) - latitude(polygon[i+1])*longitude(polygon[i])))/(6*area)
    return [x, y, abs(area)]

def find_state_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in
    polygons, weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_state_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_state_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    # check each polygon in the list of polygons                // use a for loop "for polygon in polygons"
    # use an assignment statement to compute x, y, and area     // use find_centroid function
    # implement the formulae for average x and y                // be sure to sum each area (part of formula)
    # return a position                                         // use make_position function

    original_area = 0
    ave_x = 0
    ave_y = 0
    length = len(polygons)
    for polygon in polygons:
        x, y, area = find_centroid(polygon)
        original_area += area
        ave_x += x * area
        ave_y += y * area
    return make_position(ave_x/original_area, ave_y/original_area)


###################################
# Phase 3: The Mood of the Nation #
###################################

def group_by_key(pairs):
    """Return a dictionary that relates each unique key in [key, value] pairs
    to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_key(example)
    {1: [2, 3, 2], 2: [4], 3: [2, 1]}
    """
    # Optional: This implementation is slow because it traverses the list of
    #           pairs one time for each key. Can you improve it?
    keys = [key for key, _ in pairs]
    return {key: [y for x, y in pairs if x == key] for key in keys}

def group_tweets_by_state(tweets):
    """Return a dictionary that groups tweets by their nearest state center.

    The keys of the returned dictionary are state names and the values are
    lists of tweets that appear closer to that state center than any other.

    Arguments:
    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> two_tweets_by_state = group_tweets_by_state([sf, ny])
    >>> len(two_tweets_by_state)
    2
    >>> california_tweets = two_tweets_by_state['CA']
    >>> len(california_tweets)
    1
    >>> tweet_string(california_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    # create a function that returns the state with min distance    // create find_closest function
    # get location of each tweet in tweets                          // use for loop "for tweet in tweets"
    # list out every distance between tweet and every state         // create dictionary
    # take out the state that corresponds to minimum distance       // use if condition with min function
    # create a list of pairs                                        // use a list comprehenshion to create state_key
    # use function created a beginning                              // return group_by_key(state_key)

    def find_closest(tweet):
        distance = {state: abs(geo_distance(tweet_location(tweet), find_state_center(us_states[state]))) for state in us_states}
        for state in distance:
            if distance[state] == min(distance.values()):
                return state
    state_key = [[find_closest(tweet), tweet] for tweet in tweets]
    return group_by_key(state_key)


def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely. Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0. 0 represents neutral sentiment, not unknown
    sentiment.

    Arguments:
    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    # create a helper function that returns an average for each state       // create helper(state_tweets) function
    # check each tweet by state                                             // use a for loop "for tweet in state_tweets"
    # create a sentiment for each tweet                                     // use analyze_tweet_sentiment function
    # check if a sentiment exists; if so, sum sentiment values              // use the sentiment_value function to get the value
    # also, increment length                                                // length += 1
    # outside of loop check if length is zero; if so, return None           // if length == 0
    # otherwise, return the average value                                   // return sum_sentiment/length
    # outside of helper, use a list comprehension for dictionary            // for each state assign the average value given by helper
    # return the dictionary                                                 // return the variable set to the list comprehension

    def helper(state_tweets):
        length = 0
        sum_sentiment = 0
        for tweet in state_tweets:
            sentiment = analyze_tweet_sentiment(tweet)
            if has_sentiment(sentiment):
                sum_sentiment += sentiment_value(sentiment)
                length += 1
        if length == 0: 
            return None
        return sum_sentiment/length 
    state_ave = {state: helper(tweets_by_state[state]) for state in tweets_by_state.keys() if helper(tweets_by_state[state]) != None}
    return state_ave

##########################
# Command Line Interface #
##########################

def uses_tkinter(func):
    """A decorator that designates a function as one that uses tkinter.
    If tkinter is not supported, will not allow these functions to run.
    """
    def tkinter_checked(*args, **kwargs):
        if HAS_TKINTER:
            return func(*args, **kwargs)
        print('tkinter not supported, cannot call {0}'.format(func.__name__))
    return tkinter_checked

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

@uses_tkinter
def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    centers = {name: find_state_center(us_states[name]) for name in us_states}
    center = centers[center_state.upper()]
    distance = lambda name: geo_distance(center, centers[name])
    for name in sorted(centers, key=distance)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

@uses_tkinter
def draw_state_sentiments(state_sentiments):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    Arguments:
    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        draw_state(shapes, state_sentiments.get(name))
    for name, shapes in us_states.items():
        center = find_state_center(shapes)
        if center is not None:
            draw_name(name, center)

@uses_tkinter
def draw_map_for_query(term='my job', file_name='tweets2014.txt'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term, file_name)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()

def swap_tweet_representation(other=[make_tweet_fn, tweet_text_fn,
                                     tweet_time_fn, tweet_location_fn]):
    """Swap to another representation of tweets. Call again to swap back."""
    global make_tweet, tweet_text, tweet_time, tweet_location
    swap_to = tuple(other)
    other[:] = [make_tweet, tweet_text, tweet_time, tweet_location]
    make_tweet, tweet_text, tweet_time, tweet_location = swap_to




@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_query', '-m', type=str)
    parser.add_argument('--tweets_file', '-t', type=str, default='tweets2014.txt')
    parser.add_argument('--use_functional_tweets', '-f', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    if args.use_functional_tweets:
        swap_tweet_representation()
        print("Now using a functional representation of tweets!")
        args.use_functional_tweets = False
    if args.draw_map_for_query:
        print("Using", args.tweets_file)
        draw_map_for_query(args.draw_map_for_query, args.tweets_file)
        return
    for name, execute in args.__dict__.items():
        if name != 'text' and name != 'tweets_file' and execute:
            globals()[name](' '.join(args.text))
