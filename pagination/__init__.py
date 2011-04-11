#!/usr/bin/env python
""" pagination """

__author__      = "Dexter Tad-y"
__credits__     = ["Leon Brocard", "Leo Lapworth"]
__license__     = "GPL"
__version__     = 0.2

class Page:
    _total_entries      = None
    _entries_per_page   = None
    _current_page       = None

    def __init__(self, total_entries=0, entries_per_page=10, current_page=1):
        self.total_entries(total_entries)
        self.entries_per_page(entries_per_page)
        self.current_page(current_page)

    def total_entries(self, value=None):
        if value is not None:
            self._total_entries = value
        return self._total_entries

    def entries_per_page(self, value=None): 
        if value is not None:
            if value < 1:
                raise ValueError("fewer than one entry per page")
            self._entries_per_page = value
        return self._entries_per_page

    def current_page(self, value=None):
        # try set
        if value is not None:
            self._current_page = value
            return self._current_page
        # get
        if self._current_page == None:
            return self.first_page()
        elif self._current_page < self.first_page():
            return self.first_page()
        elif self._current_page > self.last_page():
            return self.last_page()
        else:
            return self._current_page

    def first_page(self):
        return 1

    def last_page(self):
        pagesf = self.total_entries() / (self.entries_per_page() * 1.0)
        pages = int(pagesf)
        last_page = None
        if pagesf == pages:
            last_page = pages
        else:
            last_page = pages + 1
        if last_page < 1:
            last_page = 1
        return last_page

    def first_entry(self):
        if self.total_entries() == 0:
            return 0
        else:
            return ((self.current_page() - 1) * self.entries_per_page()) + 1

    def last_entry(self):
        if self.current_page() == self.last_page():
            return self.total_entries()
        else:
            return (self.current_page() * self.entries_per_page())

    def previous_page(self):
        if (self.current_page() > 1):
            return self.current_page() - 1
        else:
            return None

    def next_page(self):
        if self.current_page() < self.last_page():
            return self.current_page() + 1

    def skipped(self):
        skipped = self.first_entry() - 1
        if skipped < 0:
            return 0
        return skipped
        


class Pageset(Page):

    _pages_per_set          = None
    _page_set_previous      = None
    _page_set_pages         = None
    _page_set_next          = None

    def __init__(self, total_entries=0, entries_per_page=10, current_page=1, pages_per_set=9):
        Page.__init__(self, total_entries, entries_per_page, current_page)
        if pages_per_set is not None:
            self.pages_per_set(pages_per_set)

    def current_page(self, value=None):
        if value is not None:
            Page.current_page(self, value) 
            # Redo calculations, using current pages_per_set value
            self.pages_per_set( self.pages_per_set() )
        return Page.current_page(self)
        

    def pages_per_set(self, value=None):
        # try get first
        if value is None:
            return self._pages_per_set
        self._pages_per_set = value
        if not self._pages_per_set > 1:
            # only have one page in the set, must be page 1
            cp = self.current_page()
            if cp != 1:
                self._page_set_previous = cp - 1
            self._page_set_pages = [ 1 ]
            if cp < self.last_page():
                self._page_set_next = cp + 1
        else:
            # slide mode for now
            if self._pages_per_set >= self.last_page():
                # No sliding, no next/prev pageset
                self._page_set_pages = range( 1, self.last_page() + 1 )
            else:
                # Find the middle rounding down - we want more pages after, than before
                middle = int( self._pages_per_set / 2 )

                # offset for extra value right of center on even numbered sets
                offset = 1

                if self._pages_per_set % 2 != 0:
                    # must have been an odd number, add one
                    middle = middle+1
                    offset = 0

                starting_page = self.current_page() - middle + 1
                if starting_page < 1:
                    starting_page = 1

                end_page = starting_page + self._pages_per_set - 1
                if self.last_page() < end_page:
                    end_page = self.last_page()

                if self.current_page() <= middle:

                    # near the start of the page numbers
                    self._page_set_next = self._pages_per_set + middle - offset
                    self._page_set_pages = range( 1, self._pages_per_set + 1 )

                elif self.current_page() > ( self.last_page() - middle - offset ):

                    # near the end of the page numbers
                    self._page_set_previous = self.last_page() - self._pages_per_set - middle + 1
                    self._page_set_pages = range(   self.last_page() - self._pages_per_set + 1,
                                                    self.last_page() + 1,
                                                    )
                else:

                    # Start scrolling baby!
                    self._page_set_pages = range( starting_page, end_page+1 )
                    self._page_set_previous = starting_page - middle - offset
                    if self._page_set_previous < 1:
                        self._page_set_previous = 1
                    self._page_set_next = end_page + middle


    def previous_set(self):
        return self._page_set_previous
    
    def next_set(self):
        return self._page_set_next
    
    def pages_in_set(self):
        return self._page_set_pages
    
        


