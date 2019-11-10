# Web-crawler
It is for learning how to retrieve links from the seed URL.
It starts from checking the permission if the website or links allow to be crawled. The robotparser library is used for this task.

Once the website allows for crawling, the links will be retrieved and added to Queue until number of links have reached to defined limit.


#### Instruction for running source code
Python Version: 3

Required Library: bs4==0.0.1, urllib3==1.23

Main file: 	Source code has been implemented in a single file. 

Therefore, it can be executed by running below command line after accessing to its directory (crawler folder).
 $ python crawler.py
 
Function named “start_crawling” will be invoked and start crawling process. In order to change the URL of seed, please change value of below variable before running.

seed_url = 'seed URL here'

#### Crawler Description implemented in this lab

2 queues objects are used for storing links from crawled pages and discovered pages.

Number of discovered page is set to 50 to limit amount of crawling as for experiment.

The seed page is crawled first to get all links on the page.

To get link from href tag, BeautifulSoup library is used.

There is the case that link written in “href” tag is not a full URI such as “/link1”, “//link2”. Therefore, pre-processing to get correct URL is performed.

The links obtained on the page have been added to repository (Queue) object to support Breadth First Search data structure.

Once all links have been added to the repository, crawling process from link in repository starts.

Before crawling the URL, the URL domain has been used for concatenating with “robots.txt” and robotparser library is used to check whether the crawling URL is able to be crawled or not, if not, skip crawling this URL and process next URL.

In case that the crawling URL has been discovered, the program skips this URL and starts crawling next URL in repository.

Example result from crawling seed “https://edition.cnn.com” with limited 50 pages.
