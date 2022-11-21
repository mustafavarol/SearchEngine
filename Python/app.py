from flask import Flask, render_template,request


def Quick_sort(pages,ranks):   #ranklara gore sayfa siralar
 if len(pages)>1:
  var=ranks[pages[0]]
  x=0
  y=0
  for y in range(1,len(pages)):
   if ranks[pages[y]]>var:
    pages[x],pages[y]=pages[y],pages[x]
    x+=1
  pages[x-1],pages[0]=pages[0],pages[x-1]
  Quick_sort(pages[1:x],ranks)
  Quick_sort(pages[x+1:len(pages)],ranks)




def get_page(url):  #kutuphaneyi cagirir
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""




def compute_ranks(graph):   #sayfa sayisina gore rank cikartir
    d = 0.8 
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages    
            newranks[page] = newrank
        ranks = newranks
    return ranks

 



def crawl_web(seed):    #aramayi yapiyor
    tocrawl = [seed]
    crawled = []
    graph = {}  
    index = {}
    limit = 0
    while tocrawl and limit<=20:
        limit+=1
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    print (crawled)
    return index, graph





def get_next_target(page):  #linkleri cikartiyor
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote    




def get_all_links(page):    #butun linkleri cikariyor
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links



 
def union(a, b):    #ayni sayfalari cikarmasini engeller
    for e in b:
        if e not in a:
            a.append(e)




def add_page_to_index(index, url, content):   #sayfayi index e ekliyor
    words = content.split()
    for word in words:
        add_to_index(index, word, url)




def add_to_index(index, keyword, url):  #keywordu index e ekliyor
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]




def lookup(index, keyword):   #sayfa ici kelime aramasi
    if keyword in index:
        return index[keyword]
    else:
        return []




def lookup_2(index,ranks,keyword):   #lookup ve quick sortu birlestirir
	pages=lookup(index,keyword)
	urls = []
	Quick_sort(pages,ranks)
	for a in pages: 
		urls.append(a)
	return urls



app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")




@app.route('/toplam',methods=['POST'])
def sum():
    x=request.form.get('seed')
    y=request.form.get('lookup')
    index, graph = crawl_web(x)
    ranks = compute_ranks(graph)
    c = lookup_2(index, ranks, y)
    return render_template('number.html', c = c)
if __name__=="__main__":
    app.run(debug=True)