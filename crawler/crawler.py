# https://docs.python.org/2/library/robotparser.html
import urllib
from urllib.parse import urlparse
from urllib import robotparser
from bs4 import BeautifulSoup
from queue import Queue
import logging

"""
Crawing web links from seed.
"""

logging.getLogger("LinkCrawler").setLevel(logging.DEBUG)


class LinkCrawler:
    
    def __init__(self):
        self.robot_parser = robotparser.RobotFileParser()
        self.n_limit_pages = 50
    
    def is_crawlable(self, url):
        """
        Check policy from target website
        return True is the link is able to crawl otherwise return False. 
        """
        # is_link_outside_page = self.is_correct_format_url(url)
        
#         if is_link_outside_page == False:
            # Do not process this link in following steps
            # Continue with other links in queue
#             return False
        
        robot_url = self.get_host_name(url) + "robots.txt"
        self.robot_parser.set_url(robot_url)
        try:
            self.robot_parser.read()
        except urllib.error.URLError as e: 
            logging.error("URLError: %s", str(e))
            print("Error on_data: ", str(e))
            return False
        # test disallow 
        # url = "https://edition.cnn.com/ads/"
        is_able_to_fetch = self.robot_parser.can_fetch("*", url)
        print("able to fetch: ", is_able_to_fetch, ", bot url: ", robot_url, ", crawl url: ", url)
        return is_able_to_fetch

    def is_correct_format_url(self, url):
        """
        Process URL if it comes with http
        """
        if not url.startswith("https"):
            return False
        
    def get_host_name(self, url):
        parsed_uri = urlparse(url)
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
            # Set limited number of crawling
            if q_discovered_link.qsize() > self.n_limit_pages:
                break
            
                        # 4.a Check if it has not been already crawled
            if link in q_discovered_link.queue:
                print("================ Link was discover then skip ", link, "================")
                continue

            if not self.is_crawlable(link):
                continue
            
            print("================ current seed ", link, "================")
            page = ""
            
            # 1. Pick a URL
            with urllib.request.urlopen(link) as url:
                data = urlparse(link)
                scheme = data[0]
                domain = ""
                if scheme != "" and scheme.startswith("http"):
                    domain = scheme + "://" + data[1]
                page = url.read()
                print("domain ==== ", domain)
            
            # 2. Parse the HTML to extract links to other URLs (jsoup or Beautiful Soup)
            soup = BeautifulSoup(page, features="lxml")
            soup.prettify()
        
            # 3. Add the links to a repository following breadth-first approach.
            # crawling href tag
            for anchor in soup.findAll('a', href=True):
                href = anchor['href']
                
                if href.startswith("#"):
                    continue
                elif href.startswith("//"):
                    href = scheme + ":" + href
                elif href.startswith("/"):
                    href = domain + href
                    
                if not href in q_links.queue:
                    print("add link for internal domain: ", href)
                    q_links.put(href)
        
            q_discovered_link.put(link)
        
        # print result of discovered page
        while not q_discovered_link.empty():
            print("Discovered links: ", q_discovered_link.get())


if __name__ == "__main__":
    crawler = LinkCrawler()
    seed_url = 'https://edition.cnn.com/'
    crawler.start_crawling(seed_url)
