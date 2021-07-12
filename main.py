import requests
import sys


# Itunes API documentation https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

search_media = ""           # ex. movie, podcast, music, musicVideo, audiobook, shortFilm, tvShow, software, ebook, all
search_query = ""           # Any URL-encoded text string, all spaces replaced with +
search_limit = ""           # 1 to 200
limit_number = ""           # the actual limit number
concatenate_symbol = "&"    # symbol used to concatenate each key and value pair ex. key1=value1&key2=value2&key3=value3
results = []                # list where all results are stored


def get_required_inputs():
    choose_query_type()
    choose_query_content()
    choose_query_limit()


def choose_query_type():
    global search_media

    query_type = input("Movie or Music: ").lower()

    if "music" in query_type:
        search_media = "media=music" + concatenate_symbol
    elif "movie" in query_type:
        search_media = "media=movie" + concatenate_symbol
    else:
        print("Please enter either movie or music.")
        sys.exit()


def choose_query_content():
    global search_query

    query = input("Search Query: ").lower()

    if len(query) == 0:
        print("Please input search query.")
        sys.exit()
    else:
        search_query = "term=" + query.replace(" ", "+") + concatenate_symbol


def choose_query_limit():
    global search_limit
    global limit_number

    limit_number = input("Limit: ")

    if len(limit_number) == 0 or int(limit_number) > 200:
        print("Please enter a limit from 1-200.")
        sys.exit()
    else:
        search_limit = "limit=" + limit_number


def prepare_url():

    global results
    global limit_number

    url = "https://itunes.apple.com/search?" + search_query + search_media + search_limit

    errorCheck(url)    # make sure URL is good

    request = requests.get(url).json()
    ctr = 0

    try:

        for i in range(int(limit_number)):

            results.append("{track_Name} by {artist_Name}, {type} - {genre}".format(track_Name=request["results"][ctr]["trackName"],
                                                                           artist_Name=request["results"][ctr]["artistName"],
                                                                           type=request["results"][ctr]["kind"], genre=request["results"][ctr]["primaryGenreName"]))
            ctr += 1
    except IndexError:
        print("The limit you have entered is too high for this search query, I will show you all I found for your search query!")




def errorCheck(url):
    try:  # see if user is connected to internet
        requests.get(url)
    except requests.ConnectionError:
        print("You are not connected to internet! This program needs internet to function properly. Exiting now...")
        sys.exit()

    check = requests.get(url)

    if check.ok:  # status lookup that returns a boolean (if true = everything is good)
        return
    elif not check.ok:
        print("There is an error with status lookup, please try again later.")
        sys.exit()


def print_results():
    global results

    print("\n")

    for i in range(len(results)):
        print(results[i])

    print("\n")

def continue_question():
    answer = input("Would you like to keep searching? (Yes/No)").lower()

    if answer == "yes":
        pass
    else:
        print("Exiting program.")
        sys.exit()


if __name__ == '__main__':
    while True:
        get_required_inputs()
        prepare_url()
        print_results()
        continue_question()
