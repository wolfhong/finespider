.PHONY: testpage testtime testitem testerror

ERRORLOG := --logfile=./error.log --loglevel=ERROR

testpage:
	scrapy crawl -s CLOSESPIDER_PAGECOUNT=5 pedaily $(ERRORLOG)

testtime:
	scrapy crawl -s CLOSESPIDER_ITEMCOUNT=5 pedaily $(ERRORLOG)

testitem:
	scrapy crawl -s CLOSESPIDER_ITEMCOUNT=3 pedaily $(ERRORLOG)

testerror:
	scrapy crawl -s CLOSESPIDER_ERRORCOUNT=3 pedaily $(ERRORLOG)

crawl:
	scrapy crawl pedaily $(ERRORLOG)
