
# The expensive operation is request.get.
# It's expensive because it takes a little bit of time to go out over the Internet, to make a connection with another server. 
# It's also a little unreliable. Sometimes you don't have a good Internet connection, sometimes the server that you're connecting
# to doesn't respond in the way that it did yesterday.

import requests
import json
import os

PERMANENT_CACHE_FNAME = "permanent_cache.txt"
TEMP_CACHE_FNAME = "this_page_cache.txt"

def requestURL(baseurl, params = {}):
    # This function accepts a URL path and a params diction as inputs.
    # It calls requests.get() with those inputs,
    # and returns the full URL of the data you want to get.
    req = requests.Request(method = 'GET', url = baseurl, params = params)
    prepped = req.prepare()
    return prepped.url

def _write_to_file(cache, fname):
    with open(fname, 'w') as outfile:
        outfile.write(json.dumps(cache, indent=2))

def _read_from_file(fname):
    try:
        #  if it can't find this file or if it can't load it as JSON, then we'll just return an empty dictionary. So it'll fail gracefully
        with open(fname, 'r') as infile:
            res = infile.read()
            return json.loads(res)
    except:
        return {}

def add_to_cache(cache_file, cache_key, cache_value):
    temp_cache = _read_from_file(cache_file)
    temp_cache[cache_key] = cache_value
    _write_to_file(temp_cache, cache_file)

def clear_cache(cache_file=TEMP_CACHE_FNAME):
    _write_to_file({}, cache_file)

def make_cache_key(baseurl, params_d, private_keys=["api_key"]): # private_keys: some keys that we want to exclude. In particular, they may be private data that's used for authentication
    """Makes a long string representing the query.
    Alphabetize the keys from the params dictionary so we get the same order each time.
    Omit keys with private info."""
    alphabetized_keys = sorted(params_d.keys()) # he other thing that we want to do here is to make sure that we always get the parameters in the same order
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

def get(baseurl, params={}, private_keys_to_ignore=["api_key"], permanent_cache_file=PERMANENT_CACHE_FNAME, temp_cache_file=TEMP_CACHE_FNAME):
    full_url = requestURL(baseurl, params)
    cache_key = make_cache_key(baseurl, params, private_keys_to_ignore)
    print('cache_key: ', cache_key)
    # Load the permanent and page-specific caches from files
    permanent_cache = _read_from_file(permanent_cache_file)
    temp_cache = _read_from_file(temp_cache_file)
    if cache_key in temp_cache:
        print("found in temp_cache")
        # make a Response object containing text from the change, and the full_url that would have been fetched
        # return requests.Response(temp_cache[cache_key], full_url)
        res = json.loads(temp_cache[cache_key])
        return json.dumps(res, indent=3)
    elif cache_key in permanent_cache:
        print("found in permanent_cache")
        # make a Response object containing text from the change, and the full_url that would have been fetched
        # return requests.Response(permanent_cache[cache_key], full_url)
        res = json.loads(permanent_cache[cache_key])
        return json.dumps(res, indent=3)
    else:
        print("new; adding to cache")
        # actually request it
        resp = requests.get(baseurl, params)
        # save it
        add_to_cache(temp_cache_file, cache_key, resp.text)
        add_to_cache(permanent_cache_file, cache_key, resp.text)
        return json.dumps(resp.json(), indent=3)
