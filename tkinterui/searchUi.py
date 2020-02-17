from tkinter import * 
import tkinter.scrolledtext as tkst


class SearchWindow(Frame):
    search_type_exact = "Exact Search"
    search_type_all = "Contains All"
    search_type_any = "Contains Any"

    def __init__(self, site_data, master=None):
        Frame.__init__(self, master)

        self.master_win = master
        self.site_data = site_data

        '''
            Set up sub frames for each of the groups we need.
        '''
        self.optFrame = Frame(self.master_win)
        self.optFrame.grid(row=0, column=0, columnspan=1, sticky='nwse')

        self.srchFrame = Frame(self.master_win)
        self.srchFrame.grid(row=1, column=0, columnspan=1, sticky='nwse')

        self.srchResult = Frame(self.master_win)
        self.srchResult.grid(row=0, column=1, rowspan=2,  sticky='nwse')

        self.master_win.grid_rowconfigure(0, weight=1)
        self.master_win.grid_rowconfigure(1, weight=1)
        self.master_win.grid_columnconfigure(1, weight=3)

        '''
            Set up the options we want
        '''
        self.sources = {}
        for key in self.site_data.keys():
            self.sources[key] = IntVar()

        self.search_selection = IntVar()
        self.search_options = [
            (SearchWindow.search_type_exact , 1),
            (SearchWindow.search_type_all, 2),
            (SearchWindow.search_type_any, 3),
        ]

        self._createSourceOptions(self.optFrame)
        self._createSearchOptions(self.srchFrame)
        self.results_pane = tkst.ScrolledText(self.srchResult, wrap=WORD)
        self.results_pane.pack(fill=BOTH, expand=1)



    '''
        Callbacks 
    '''
    def _printSelection(self):
        print("Got source selection")
        for k in self.sources.keys():
            print(k, self.sources[k].get())

    def _printSearchSelection(self):
        print("Got search selection")
        print(self.search_selection.get())


    '''
        Sources
    '''
    def _createSourceOptions(self, frame):
        Label(frame, text="Source Options:").pack(anchor=NW)
        for k in self.sources.keys():
            c1 = Checkbutton(
                    frame, 
                    text=k,
                    variable=self.sources[k], 
                    onvalue=1, 
                    offvalue=0, 
                    command=self._printSelection).pack(anchor=NW, padx=5, pady=5)

    '''
        Search Options
    '''
    def _createSearchOptions(self, frame):
        Label(frame, text="Search Options:").pack(anchor=NW)

        Label(frame, text="Search Term").pack(anchor=NW)
        self.SearchTerm = Text(frame, height=2, width=30)
        self.SearchTerm.pack(anchor=NW)

        for option, val in enumerate(self.search_options):
            Radiobutton(
                  frame, 
                  text=val[0],
                  padx = 20, 
                  variable=self.search_selection, 
                  command=self._printSearchSelection,
                  value=val[1]).pack(anchor=NW, padx=5, pady=5)    

        self.SearchButton = Button(frame, text="Search", command=self._performSearch)
        self.SearchButton.pack(fill=BOTH)

    '''
        Search 
    '''
    def _performSearch(self):
        self.results_pane.delete(1.0, END)

        search_selection = self.search_selection.get()
        search_term = self.SearchTerm.get("1.0",END)
        search_terms = []
        search_sources = []
        search_type = ""

        '''
            Clean up term
        '''
        search_term = search_term.strip()
        search_terms = search_term.split(' ')
        
        '''
            Get search option
        '''
        for selection in self.search_options:
            if selection[1] == search_selection:
                search_type = selection[0]

        '''
            Get search sources
        '''
        for k in self.sources.keys():
            source_selected = self.sources[k].get()
            print(k, source_selected)
            if source_selected == 1:
                search_sources.append(k)

        if not search_type or len(search_sources) == 0 or len(search_terms) == 0:
            self.results_pane.insert(END, "Search type, term, or sources is empty\n")
        else:
            self.results_pane.insert(END, "Search Type : {}\n".format(search_type))
            self.results_pane.insert(END, "Search Term : {}\n".format(search_terms))
            self.results_pane.insert(END, "Sources : \n")
            for source in search_sources:
                self.results_pane.insert(END, "    {}\n".format(source))

            search_data = self._doSearch(search_sources, search_terms, search_type)

            if len(search_data) > 0:
                for site in search_data.keys():
                    self.results_pane.insert(END, "\n*********************\n")
                    self.results_pane.insert(END, "\nSource : {} \n".format(site))
                    self.results_pane.insert(END, "\n*********************\n")
                    for date in search_data[site].keys():
                        self.results_pane.insert(END, "\nDate : {} - {} stories \n\n".format(date, len(search_data[site][date])))
                        story_index = 1
                        for story in search_data[site][date]:
                            self.results_pane.insert(END, "{} : {} \n".format(story_index, story))
                            story_index += 1




    def _doSearch(self, sources, terms, srch_type):
        '''
            Loaded site data in this format, return will be the same

            {
                "SiteName": {"date", [data]}
            }

        '''
        return_results = {}

        sorted_keys = list(self.site_data.keys())
        sorted_keys.sort()
        for site_key in sorted_keys:
            if site_key in sources:
                return_results[site_key] = {}
                print("Searching ", site_key, srch_type)
                
                for date_key in self.site_data[site_key]:
                    if srch_type == SearchWindow.search_type_exact:
                        '''
                            Has to have exact input
                        '''
                        search_term = " ".join(terms)
                        dated_mentions = [entry for entry in self.site_data[site_key][date_key] if search_term.lower() in entry.lower()]
                        if len(dated_mentions) > 0:
                            return_results[site_key][date_key] = dated_mentions
                            print("Found" , len(return_results[site_key][date_key]))

                    elif srch_type == SearchWindow.search_type_all:
                        '''
                            Has to have all search terms. Clean them up 
                        '''
                        terms = list(set(terms))
                        dated_mentions = [entry for entry in self.site_data[site_key][date_key] if terms[0].lower() in entry.lower()]
                        if len(dated_mentions) > 0:
                            for term in terms[1:len(terms)]:
                                dated_mentions = [entry for entry in dated_mentions if term.lower() in entry.lower()]

                            if len(dated_mentions) > 0:
                                return_results[site_key][date_key] = dated_mentions
                                print("Found" , len(return_results[site_key][date_key]))

                    elif srch_type == SearchWindow.search_type_any:
                        '''
                            Has to have any search terms. Clean them up
                        '''
                        terms = list(set(terms))
                        dated_mentions = []
                        for term in terms:
                            current_mentions = [entry for entry in self.site_data[site_key][date_key] if term.lower() in entry.lower()]
                            for cur in current_mentions:
                                if cur not in dated_mentions:
                                    dated_mentions.append(cur)

                        if len(dated_mentions) > 0:
                            return_results[site_key][date_key] = dated_mentions
                            print("Found" , len(return_results[site_key][date_key]))
                        pass
        
        return return_results
