'''
PYTHON SEARCH ENGINE
BY: HRITHIK SHAH
'''

import string
import time



# 1) Create a function that will get the source code of a page given its url

def get_page(url):
    '''
    url --> string
    Description: The function will open a page given its url and convert the source code
    into a string
    Precondition: url must be a string
    '''
    try:
        import urllib.request
        with urllib.request.urlopen(url) as url:
            s = url.read()
        return str(s)
    except:
        return

# 2) Make a function that finds the next link on a page

'''def get_next_link (page):
    ''''''
    string --> string(url), int
    Description: The function takes all the text on a page, and finds the next
    first occurance of "a href=" and returns the corresponding url and its
    position.
    Precondition: page is a string from a webpage
    ''''''
    start_link = page.find("a href=")
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote+1:end_quote]

    return url, end_quote'''

# 3) Modify get_next_link to return none if no links in the page

def get_next_link(page):
    '''
    string --> string(url), int
    Description: The function takes all the text on a page, and finds the next
    first occurance of "a href=" and returns the corresponding url and its
    position.
    Precondition: page is a string from a webpage
    '''
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

# 4) Create a function that prints all urls on a page

'''def print_all_links (page):
    ''''''
    string --> string(url), int
    Description: The function takes all the text on a page, and finds the next
    the first occurance of "a href=" and prints the corresponding function
    It calls the function get_next_link repeatedly until there is no occurense of "a href"
    Precondition: page is a string from a webpage
    ''''''
    while True:
        url, endpos = get_next_link(page)
        if url:
            print (url)
            page = page[endpos:]
        else:
            break'''

# 5) Modify print_all_links to get all links and store it in a list

def get_all_links (page):
    '''
    string --> string(url), int
    Description: The function takes all the text on a page, and finds the next
    the first occurance of "a href=" and stores the corresponding function
    It calls the function get_next_link repeatedly until there is no occurense of "a href"
    Precondition: page is a string from a webpage
    '''
    urls = []
    while True:
        url, endpos = get_next_link(page)
        if url:
            urls.append (url)
            page = page[endpos:]
        else:
            break
    return urls

# 6) Union is a function that appends a value if not already in the list

def union(p,q):
    '''
    list, list --> list
    Description: return a list that combines p and q without creating duplicates
    Precondition: p and q are lists
    '''
    for e in q:
        if e not in p:
            p.append(e)

# 7) Create a function that will "crawl" through the web, or in other words
#    go through all the links of a page

def crawl_web (query, seed, seconds):
    '''
    string --> list of strings
    Description: The functions goes through all the links in the seed page, and keeps
    adding urls that it finds, while maintaining a record of the urls it has already
    crawled.
    Precondition: query is a non-empty string
    '''
    to_crawl = [seed]
    crawled = []
    index = {}
    graph = {}
    while to_crawl:
        if (seconds > 0):
            page = to_crawl.pop() # Depth-First Search
            if (not(page in crawled) and page[:8] == 'https://'):
                content = get_page(page)
                if (content == None):
                    continue
                outlinks = get_all_links(content)
                if content.find(query)!= None:
                    add_page_to_index(index, page, content)
                    graph[page] = outlinks
                union(to_crawl, outlinks)
                crawled.append(page)
            seconds -= 1
            time.sleep(1)
        else:
            break
    return index, graph

# 8) Creating an index


def add_to_index(index,keyword,url):
    """
    dict, string, string --> none
    Description: creates an index of keywords as "keys" and their urls as "elements"
    Precondition: index must be a dict, keyword and url should be strings
    """
    if keyword not in index:
        index[keyword] = []
        index[keyword].append (url)
    else:
        index[keyword].append(url)

# 9) Accessing elements in the index

def lookup(index, keyword):
    '''
    dict, string --> set
    Description: returns all the urls of the keyword
    Precondition: index must be a dict, and keyword must be a string
    '''
    '''if keyword in index:
        return index[keyword]
    else:
        return None'''
    for word in index:
        if (keyword in word):
            return index[word]
    return None
            

# 10) Adding a page to the index

def add_page_to_index(index, url, content):
    '''
    dict, string, string --> none
    Description: updates the index with keywords from the url's content
    Precondition: index must be a dict, url and content must be strings
    '''
    table = str.maketrans(dict.fromkeys(string.punctuation))
    content = content.translate(table)
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

'''def to_filter(character):
    ''''''
    string --> boolean
    Description: takes out all puncuation,
    Precondition: character must be a string
    ''''''

    if type(character) == int:
        return False
    elif character.isalpha():
        if (character in string.punctuation):
            return False
        else:
            return True
    else:
        return True'''

# WEB CRAWLER FINISHED

# 11) Creating a page ranking algorithm

def compute_ranks(graph):
    '''
    dictionary --> dictionary
    Description: uses the following formula:
    rank(page, 0) = 1/npages

    rank(page, t) = (1-d)/npages + sum (d * rank(p, t - 1) / number of outlinks from p) 
                    over all pages p that link to this page
    This formula helps determine new ranks for pages.
    Precondition: graph is a non-empty dictionary
    '''
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

# 11) Getting better results from the ranking algoritm

def best_result(index, ranks, keyword):
    '''
    dictionary, dictionary, string --> string
    Description: Finds the page with the highest rank from a given set of pages and returns it.
    Precondition: index, rank, keyword are not empty and the correct specified data types
    '''
    pages = lookup (index, keyword)
    if not pages:
        return None
    pages.sort()

    return pages[0]

# MAIN --------------------------------------------------------------------

timer = int(input("How long do you want to crawl for (in seconds)? "))

seed = input("What is your seed page? ")

query = input("What do you want to search for (one word)? ")


index, graph = crawl_web(query, seed, timer)

ranks = compute_ranks(graph)

fetched = best_result(index, ranks, query)

print (fetched)
        



    
