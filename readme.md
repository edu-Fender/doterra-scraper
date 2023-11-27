Easily the hardest scraper I've ever built. The dynamic nature of the target website makes the scrape very tricky. On top of that, the HTML pages are not 100% standardized (althought that's to be expected). At least, the website didn't show any sorts countermeasures.

The scraper heavily relies on recursion in order to navigate through website dynamic menus na pages. It's inneficient in fact, but it was the obvious solution that came to my mind. No multi-threading/async was used, but it would be a great improvement. 

__IMPORTANT:__
1. The scraper was built and tested with Python 3.9.6.
2. Edge browser was chosen. _Edge v119.0.2151.44_ was used together with _msgedgedriver.exe v119.0.2151.44_. The driver can (gladly) be found at __/components/msgedgedriver.exe__.
3. The scraper will only work properly when connected to Portugal's website. A VPN is advised.