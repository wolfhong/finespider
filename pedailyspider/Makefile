.PHONY: testpage testtime testitem testerror

testpage:
	scrapy crawl -s CLOSESPIDER_PAGECOUNT=3 pedaily

testtime:
	scrapy crawl -s CLOSESPIDER_ITEMCOUNT=5 pedaily

testitem:
	scrapy crawl -s CLOSESPIDER_ITEMCOUNT=3 pedaily

testerror:
	scrapy crawl -s CLOSESPIDER_ERRORCOUNT=3 pedaily
