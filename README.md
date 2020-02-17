# pythonthreading
<sub>Dan Grecoe - A Microsoft Employee</sub>


Python examples using:
- Threading
- TKinter
- html.parser.HTMLParser

This repo is an example on how to use threading and TKinter UI components. The example it's used for is contrived simply for me to learn how to do a few things. So, what does it do?

1. Parses out text, links, and images from a given set of news sources. This is done by launching a thread for each source that:
    - Reads the current content of the URL provided.
    - Uses HTMLParser derived class to strip out relevant information.
    - Stores the results on disk in a provided local directory in the structure:
        - [base_directory]/[site_name]/[year]/[month]/[day]
            - data : Text file in JSON format that has the text that was pulled as a key and a list of date/time stamps it was recieved. 
            - images : Text file in JSON format that has the image link as the key and a JSON object as the value holding the image ID and a list of date/time stamps it was seen.
            - links : Text file in JSON format that has the link as the key and a JSON object as the value holding the image ID and a list of date/time stamps it was seen.
            - run_history : A list of date/time stamps data was collected on the given day.
2. Enables the user to search the news sources for specific terms. The terms are search in a case insensitive manner and cane be done using:
    - command line: Takes the search term and returns stories from all sources only if they contain all of the search terms.
    - tkinter ui: Allows the user to do more refined searches.
        - Choose only the sources the user wants to look at with checkbox selections.
        - Enter in new search terms.
        - Search in three different ways:
            1. Exact : The user entered text must match exactly
            2. Any : Return all stories that have any of the search terms.
            3. All : Return stories that have all of the search terms. 

## Supporting Scripts

|Script|Description|
|-----|------|
|siteParser.py|Python file that collects the information from the website and stores it on the local disk.|
|siteSearch.py|Command line utility for searching the collected site information.|
|siteSearchUI.py|TKinter UI for searching the collected site information.|
