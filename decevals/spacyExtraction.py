from bs4 import BeautifulSoupimport requestsimport reimport spacyfrom spacy import displacyfrom collections import Counterimport en_core_web_smnlp = en_core_web_sm.load()def url_to_string(url):    res = requests.get(url)    html = res.text    soup = BeautifulSoup(html, 'html5lib')    for script in soup(["script", "style", 'aside']):        script.extract()    return " ".join(re.split(r'[\n\t]+', soup.get_text()))ny_bb = url_to_string("https://pdf.usaid.gov/pdf_docs/PA00WPHQ.pdf")article = nlp(ny_bb)labels = [(X.text, X.label_) for X in article.ents]open('spact.txt', 'wt').write(str(labels))#get rid of duplicates#match name with org#note duplicate names from different missions