# https://docs.python.org/2/library/robotparser.html
import urllib
import urllib.parse
from bs4 import BeautifulSoup
from urllib import robotparser
from queue import Queue
import logging
"""
Crawing web links from seed.
"""

logging.getLogger("LinkCrawler").setLevel(logging.DEBUG)


class LinkCrawler:
    
    def __init__(self):
        self.robot_parser = robotparser.RobotFileParser()
        self.n_limit_pages = 5
    
    def is_crawlable(self, url):
        """
        Check policy from target website
        return True is the link is able to crawl otherwise return False. 
        """
        is_link_outside_page = self.is_correct_format_url(url)
        
        if is_link_outside_page == False:
            # Do not process this link in following steps
            # Continue with other links in queue
            return False
        else:
            robot_url = self.get_host_name(url) + "robots.txt"
                
            print("bot url: ", robot_url, "---------", url)
            self.robot_parser.set_url(robot_url)
            try:
                self.robot_parser.read()
            except urllib.error.URLError as e: 
                logging.error("URLError: %s", str(e))
                print("Error on_data: ", str(e))
                return False
                
            is_able_to_fetch = self.robot_parser.can_fetch("*", url)
            return is_able_to_fetch

    def is_correct_format_url(self, url):
        """
        Process URL if it comes with http
        """
        if not url.startswith("https"):
            return False
        
    def get_host_name(self, url):
        parsed_uri = urllib.parse.urlparse(url)
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return result

    def start_crawling(self, seed_url):
        """
        Crawl links from seed page 
        """
       
        # Get tag <a href..></a> for links
        q_links = Queue()
        # TODO need to check if we need to put seed in queue
        q_links.put(seed_url)
        q_discovered_link = Queue()
        counter = 0
        while not q_links.empty():
            link = q_links.get()
            print("================ seed ", link, "================")
            page = ""

            with urllib.request.urlopen(seed_url) as url:
                page = url.read()
                
            soup = BeautifulSoup(page, features="lxml")
            soup.prettify()
            # crawling href tag
            for anchor in soup.findAll('a', href=True):
                href = anchor['href']
                # check if the link is able to be crawled or not.
                is_crawlable = self.is_crawlable(href)
                print("Crawable", is_crawlable, " Link: ", href)
                if is_crawlable == True:
                    if counter < self.n_limit_pages:
                        q_links.put(href)
                        counter += 1
                    else:
                        break
        
            q_discovered_link.put(link)
        
        # print result of discovered page
        while not q_discovered_link.empty():
            print(q_discovered_link.get())


if __name__ == "__main__":
    crawler = LinkCrawler()
    seed_url = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
    crawler.start_crawling(seed_url)
