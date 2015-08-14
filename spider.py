
import aiohttp, asyncio
import io, sys,os,time
import bs4
import re
import logging;logging.basicConfig(level = logging.INFO)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

@asyncio.coroutine
def save(title, imgs):
	path = r'%s\%s\%s'%(os.path.split(os.path.realpath(__file__))[0], 'tuigirl8', title)
	#logging.info('saveing:%s' % title)
	if not os.path.exists(path):
		os.makedirs(path)
	for img in imgs:
		name = img.split('/')[3:]
		file_path = r'%s\%s' % (path, '_'.join(name))
		#logging.info(file_path)
		if os.path.exists(file_path):
			continue
		logging.info('downloading: %s_%s [%s]'%(title, '_'.join(name), img))
		content = yield from aiohttp.get(img)
		content = yield from content.read()
		#time.sleep(1)
		logging.info('saving: %s_%s'%(title, '_'.join(name)))
		with open(file_path, 'wb') as f:
			f.write(content)
		logging.info('saved: %s_%s'%(title, '_'.join(name)))



@asyncio.coroutine
def parse_url(url):
	page = yield from aiohttp.get(url)
	page = yield from page.text()
	soup = bs4.BeautifulSoup(page,"html.parser")
	imgs = soup.find_all('img', src=re.compile('jpg'))
	title = soup.title.string.split('-')[0].strip()
	
	urls = []
	for img in imgs:
		urls.append(img.get('src'))
		#print(img.get('src'))
	if urls:
		#print(title)
		yield from save(title, urls)

@asyncio.coroutine
def parse_page(url):
	page = yield from aiohttp.get(url)
	page = yield from page.text()
	soup = bs4.BeautifulSoup(page,"html.parser")
	a = soup.find_all('a', href=re.compile('reply'))
	#print(url)
	for link in a:
		print(link)
		yield from parse_url(link.get('href'))


loop = asyncio.get_event_loop()
urls = [('http://www.tuigirl8.com/home/getmore/'+str(page)) for page in range(1,10,1)]
loop.run_until_complete(asyncio.wait([parse_page(url) for url in urls] ))
#loop.run_until_complete(parse_page('http://www.tuigirl8.com/home/getmore/1'))
#loop.run_until_complete(parse_url('http://www.tuigirl8.com/forum/view/1763'))
loop.close()