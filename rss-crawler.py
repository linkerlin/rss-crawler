# 6.00x Problem Set 6
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from Tkinter import *


#-----------------------------------------------------------------------
#
# Problem Set 6

#======================
# Code for retrieving and parsing RSS feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret
#======================

#======================
# Part 1
# Data structure design
#======================

class NewsStory(object):
    """Stores information about a story, i.e. guid, title, subject, summary, link."""

    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def __str__(self):
        """Returns a string representation of self"""
##storyData = {}
##storyData["guid"] = self.guid
##storyData["title"] = self.title
##storyData["subject"] = self.subject
##storyData["summary"] = self.summary
##storyData["link"] = self.link
        return "Stored information: \n GUID: " + str(self.guid) + "\n Title: " + str(self.title) + "\n Subject: " + str(self.subject) + "\n Summary: " + str(self.summary) + "\n Link: " + str(self.link)

    def getGuid(self):
        return self.guid

    def getTitle(self):
        return self.title

    def getSubject(self):
        return self.subject
    
    def getSummary(self):
        return self.summary

    def getLink(self):
        return self.link 

    



    

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger

class WordTrigger(Trigger):
    """Returns True if the whole word is found."""

    def __init__(self, triggerPhrase):
        self.triggerPhrase = triggerPhrase



    def findWord(self, searchString, triggerPhrase):
            """Matches a phrase against a string. Returns True if phrase is contained as a single word."""
            import string
            nonChars = string.punctuation + " "

            triggerPhraseLow = triggerPhrase.lower()
            searchStringLow = searchString.lower()

            if triggerPhraseLow not in searchStringLow:
                return False
            else:
                triggerPos = searchStringLow.index(triggerPhraseLow)
                triggerPhraseCount = searchStringLow.count(triggerPhraseLow)
                         
                if triggerPos == 0:
                    frontCheck = True
                else:
                    frontSearch = searchStringLow[triggerPos-1:triggerPos+len(triggerPhraseLow)]
                    if frontSearch[0] in nonChars:
                        frontCheck = True
                    else:
                        frontCheck = False
    
                if triggerPos + len(triggerPhraseLow) == len(searchStringLow):
                    endCheck = True
                else:
                    endSearch = searchStringLow[triggerPos:triggerPos+len(triggerPhraseLow)+1]
                    if endSearch[-1] in nonChars:
                        endCheck = True
                    else:
                        endCheck = False

                if frontCheck == True and endCheck == True:
                    firstCheck = True
                else:
                    firstCheck = False

                if firstCheck == True or self.extSearch(searchStringLow, triggerPhraseLow, triggerPos, triggerPhraseCount) == True:
                    return True
                else:
                    return False


    def extSearch(self, searchStringLow, triggerPhraseLow, triggerPos, triggerPhraseCount):
        """Recursive search extension."""
        if triggerPhraseCount > 1:
            searchStringCut = searchStringLow[triggerPos+len(triggerPhrase):]
            extSearch = findWord(searchStringCut, triggerPhraseLow)
            return extSearch
        else:
            return False



class TitleTrigger(WordTrigger):
    """Returns True if the trigger word is found in the title."""

    def evaluate(self, story):
        searchString = story.getTitle()
        return self.findWord(searchString, self.triggerPhrase)

class SubjectTrigger(WordTrigger):
    """Returns True if the trigger word is found in the title."""

    def evaluate(self, story):
        searchString = story.getSubject()
        return self.findWord(searchString, self.triggerPhrase)

class SummaryTrigger(WordTrigger):
    """Returns True if the trigger word is found in the title."""

    def evaluate(self, story):
        searchString = story.getSummary()
        return self.findWord(searchString, self.triggerPhrase)


# TODO: TitleTrigger
# TODO: SubjectTrigger
# TODO: SummaryTrigger


# Composite Triggers
# Problems 6-8

# TODO: NotTrigger

class NotTrigger(Trigger):
    """Returns True if a given Trigger returns False, or False otherwise."""    

    def __init__(self, otherTrigger):
        self.otherTrigger = otherTrigger

    def evaluate(self, story):
        if self.otherTrigger.evaluate(story) == False:
            return True
        else:
            return False
        

# TODO: AndTrigger


class AndTrigger(Trigger):
    """Returns the AND operation of two triggers."""    

    def __init__(self, otherTriggerOne, otherTriggerTwo):
        self.otherTriggerOne = otherTriggerOne
        self.otherTriggerTwo = otherTriggerTwo

    def evaluate(self, story):
        result = self.otherTriggerOne.evaluate(story) and self.otherTriggerTwo.evaluate(story)
        return result 

# TODO: OrTrigger

class OrTrigger(Trigger):
    """Returns the OR operation of two triggers."""    

    def __init__(self, otherTriggerOne, otherTriggerTwo):
        self.otherTriggerOne = otherTriggerOne
        self.otherTriggerTwo = otherTriggerTwo

    def evaluate(self, story):
        result = self.otherTriggerOne.evaluate(story) or self.otherTriggerTwo.evaluate(story)
        return result 

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    """Matches a phrase against a string. Returns True if phrase is contained entirely."""

    def __init__(self, triggerPhrase):
        self.triggerPhrase = triggerPhrase

    def evaluate(self, story):
        InTitle = self.triggerPhrase in story.getTitle()
        InSubject = self.triggerPhrase in story.getSubject()
        InSummary = self.triggerPhrase in story.getSummary()
        InTitleOrInSubject = InTitle or InSubject
        result = InTitleOrInSubject or InSummary
        return result

 

#======================
# Part 3
# Filtering
#======================

def filterStories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering)
    allStories = stories[:]
    passedStories = []

    for story in allStories:
        for trigger in triggerlist:
            fire =  trigger.evaluate(story)
            if fire == True:
                passedStories.append(story)
            else:
                pass

    return passedStories

#======================
# Part 4
# User-Specified Triggers
#======================

def makeTrigger(triggerMap, triggerType, params, name):
    """
    Takes in a map of names to trigger instance, the type of trigger to make,
    and the list of parameters to the constructor, and adds a new trigger
    to the trigger map dictionary.

    triggerMap: dictionary with names as keys (strings) and triggers as values
    triggerType: string indicating the type of trigger to make (ex: "TITLE")
    params: list of strings with the inputs to the trigger constructor (ex: ["world"])
    name: a string representing the name of the new trigger (ex: "t1")

    Modifies triggerMap, adding a new key-value pair for this trigger.

    Returns: None
    """
    # TODO: Problem 11

    if triggerType == "PHRASE":
        parameter = ""
        for item in params:
            parameter += item
        trigger = TitleTrigger(parameter)
        triggerMap[name] = trigger
        return triggerMap
    
    if triggerType == "TITLE":
        trigger = TitleTrigger(params[0])
        triggerMap[name] = trigger
        return triggerMap

    if triggerType == "SUBJECT":
        trigger = SubjectTrigger(params[0])
        triggerMap[name] = trigger
        return triggerMap

    if triggerType == "SUMMARY":
        trigger = SummaryTrigger(params[0])
        triggerMap[name] = trigger
        return triggerMap
    
    if triggerType == "AND":
        trigger = AndTrigger(triggerMap[params[0]], triggerMap[params[1]])
        triggerMap[name] = trigger
        return triggerMap
    
    if triggerType == "OR":
        trigger = OrTrigger(triggerMap[params[0]], triggerMap[params[1]])
        triggerMap[name] = trigger
        return triggerMap
    
    if triggerType == "NOT":
        trigger = NotTrigger(triggerMap[params[0]])
        triggerMap[name] = trigger
        return triggerMap

    else:
        raise ValueError(str(triggerType) + ": is an undefined trigger type in trigger.txt -- allowed tiggers are: TITLE, SUBJECT, SUMMARY, PHRASE, AND, OR, NOT" )




def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """

    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    triggers = []
    triggerMap = {}

    # Be sure you understand this code - we've written it for you,
    # but it's code you should be able to write yourself
    for line in lines:

        linesplit = line.split(" ")

        # Making a new trigger
        if linesplit[0] != "ADD":
            trigger = makeTrigger(triggerMap, linesplit[1],
                                  linesplit[2:], linesplit[0])

        # Add the triggers to the list
        else:
            for name in linesplit[1:]:
                triggers.append(triggerMap[name])

    return triggers
    
import thread

SLEEPTIME = 60 #seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    try:
        # These will probably generate a few hits...
        t1 = TitleTrigger("Occupy")
        t2 = SubjectTrigger("Israel")
        t3 = PhraseTrigger("Gaza conflict")
        t4 = OrTrigger(t2, t3)
        triggerlist = [t1, t4]
        
        # TODO: Problem 11
        # After implementing makeTrigger, uncomment the line below:  --> sometimes working, sometimes not :(
        #triggerlist = readTriggerConfig("triggers.txt")

        # from here is about drawing
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.getGuid() not in guidShown:
                cont.insert(END, newstory.getTitle()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.getSummary())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.getGuid())

        while True:

            print "Polling . . .",
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

            stories = filterStories(stories, triggerlist)

            map(get_cont, stories)
            scrollbar.config(command=cont.yview)


            print "Sleeping..."
            time.sleep(SLEEPTIME)

    except Exception as e:
        print e


if __name__ == '__main__':

    root = Tk()
    root.title("Some RSS parser")
    thread.start_new_thread(main_thread, (root,))
    root.mainloop()

