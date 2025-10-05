import requests
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from bs4 import BeautifulSoup
import json
import yaml
import os

journal_map = {"aj       " :   "Astronomical Journal                          " ,
"actaa    " :   "Acta Astronomica                                             " ,
"araa     " :   "Annual Review of Astron and Astrophys                        " ,
"apj      " :   "Astrophysical Journal                                        " ,
"apjl     " :   "Astrophysical Journal, Letters                               " ,
"apjs     " :   "Astrophysical Journal, Supplement                            " ,
"ao       " :   "Applied Optics                                               " ,
"apss     " :   "Astrophysics and Space Science                               " ,
"aap      " :   "Astronomy and Astrophysics                                   " ,
"aapr     " :   "Astronomy and Astrophysics Reviews                           " ,
"aaps     " :   "Astronomy and Astrophysics, Supplement                       " ,
"azh      " :   "Astronomicheskii Zhurnal                                     " ,
"baas     " :   "Bulletin of the AAS                                          " ,
"caa      " :   "Chinese Astronomy and Astrophysics                           " ,
"cjaa     " :   "Chinese Journal of Astronomy and Astrophysics                " ,
"icarus   " :   "Icarus                                                       " ,
"jcap     " :   "Journal of Cosmology and Astroparticle Physics               " ,
"jrasc    " :   "Journal of the RAS of Canada                                 " ,
"memras   " :   "Memoirs of the Royal Astronomical Society                    " ,
"mnras    " :   "Monthly Notices of the Royal Astronomical Society            " ,
"na       " :   "New Astronomy                                                " ,
"nar      " :   "New Astronomy Review                                         " ,
"pra      " :   "Physical Review A: General Physics                           " ,
"prb      " :   "Physical Review B: Solid State                               " ,
"prc      " :   "Physical Review C                                            " ,
"prd      " :   "Physical Review D                                            " ,
"pre      " :   "Physical Review E                                            " ,
"prl      " :   "Physical Review Letters                                      " ,
"pasa     " :   "Publications of the Astron. Soc. of Australia                " ,
"pasp     " :   "Publications of the ASP                                      " ,
"pasj     " :   "Publications of the ASJ                                      " ,
"rmxaa    " :   "Revista Mexicana de Astronomia y Astrofisica                 " ,
"qjras    " :   "Quarterly Journal of the Royal Astronomical Society          " ,
"skytel   " :   "Sky and Telescope                                            " ,
"solphys  " :   "Solar Physics                                                " ,
"sovast   " :   "Soviet Astronomy                                             " ,
"ssr      " :   "Space Science Reviews                                        " ,
"zap      " :   "Zeitschrift fuer Astrophysik                                 " ,
"nat      " :   "Nature                                                       " ,
"iaucirc  " :   "IAU Cirulars                                                 " ,
"aplett   " :   "Astrophysics Letters                                         " ,
"apspr    " :   "Astrophysics Space Physics Research                          " ,
"bain     " :   "Bulletin Astronomical Institute of the Netherlands           " ,
"fcp      " :   "Fundamental Cosmic Physics                                   " ,
"gca      " :   "Geochimica Cosmochimica Acta                                 " ,
"grl      " :   "Geophysics Research Letters                                  " ,
"jcp      " :   "Journal of Chemical Physics                                  " ,
"jgr      " :   "Journal of Geophysics Research                               " ,
"jqsrt    " :   "Journal of Quantitiative Spectroscopy and Radiative Transfer " ,
"memsai   " :   "Mem. Societa Astronomica Italiana                            " ,
"nphysa   " :   "Nuclear Physics A                                            " ,
"physrep  " :   "Physics Reports                                              " ,
"physscr  " :   "Physica Scripta                                              " ,
"planss   " :   "Planetary Space Science                                      " ,
"procspie " :   "Proceedings of the SPIE                                      "  }
journal_map = { k.rstrip():journal_map[k].rstrip() for k in journal_map.keys()}

abbrev_map = {'Astronomy and Astrophysics': 'A&A',
              'Monthly Notices of the Royal Astronomical Society': 'MNRAS',
              'Journal of Cosmology and Astroparticle Physics': 'JCAP',
              'Astrophysical Journal': 'ApJ',
              'Publications of the ASJ': 'PASJ',
              'Astrophysical Journal, Supplement': 'ApJS',
              'Astronomical Journal': 'AJ',
              'Astronomy and Computing': 'Astron. Comput.',
            #   'arXiv e-prints': 'arXiv',
              'Nature Reviews Physics': 'Nat. Rev. Phys',
              'The Open Journal of Astrophysics':'OJAp'}

api_key = os.environ['ADS_API_KEY']

# Loading the customizations
with open('_data/custom_bib.yml', 'r') as f:
  customization = yaml.load(f, Loader=yaml.FullLoader)

# Getting all bibcodes
encoded_query='q=author:Guerrini,Sacha&fq=database:astronomy&fl=bibcode&rows=1000&sort=date+desc'
r = requests.get('https://api.adsabs.harvard.edu/v1/search/query?'+encoded_query,
                 headers={"Authorization":"Bearer "+api_key,})

# Check if the request was successful
if r.status_code != 200:
    print(f"❌ ADS API search request failed with status code: {r.status_code}")
    print(f"Response: {r.text}")
    exit(1)

soup = BeautifulSoup(r.content, 'html.parser')
response_text = soup.contents[0] if soup.contents else ""

# Debug: print the raw response
print(f"📝 Raw ADS API response: {response_text[:200]}...")

try:
    response_data = json.loads(response_text)
    if 'response' not in response_data or 'docs' not in response_data['response']:
        print(f"❌ Unexpected API response structure: {response_data}")
        exit(1)
    bibcodes = response_data['response']['docs']
    print(f"✅ Found {len(bibcodes)} publications")
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse JSON response: {e}")
    print(f"Raw response: {response_text}")
    exit(1)
bibtex_query = ""
for entry in bibcodes:
  bibtex_query += '"%s",'%entry['bibcode']
bibtex_query = bibtex_query[:-1]

# Retrieving the full bibtex entries
r = requests.post('https://api.adsabs.harvard.edu/v1/export/bibtexabs', 
                 data='{"bibcode":[%s]}'%bibtex_query,
                 headers={"Authorization":"Bearer "+api_key,
                          "Content-Type": "application/json"})

# Check if the export request was successful
if r.status_code != 200:
    print(f"❌ ADS API export request failed with status code: {r.status_code}")
    print(f"Response: {r.text}")
    exit(1)

try:
    export_data = r.json()
    if 'export' not in export_data:
        print(f"❌ Unexpected export response structure: {export_data}")
        exit(1)
    result = export_data['export']
    print(f"✅ Successfully retrieved bibtex data")
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse export JSON response: {e}")
    print(f"Raw response: {r.text}")
    exit(1)
# Parse it with bibtexparser
bibtex_database = bibtexparser.loads(result)

entries = []
# Now, doing a little bit of magic 
for entry in bibtex_database.entries:
  # We ignore ascl citations 
  if 'Erratum' in entry['title']:
    continue
  
  if 'archiveprefix' in entry.keys():
    if entry['archiveprefix'] == 'ascl':
      continue
  
  if 'journal' in entry.keys():
    if entry['journal'][1:] in journal_map.keys():
      entry['journal'] = journal_map[entry['journal'][1:]]

    if entry['journal'] in abbrev_map.keys():
      entry['abbr'] = abbrev_map[entry['journal']]

  # Display bibtex entry
  entry['bibtex_show']='true'

  # Adding link to arxiv
  if 'eprint' in entry.keys():
    arxiv_id = entry['eprint']
    entry['arxiv']= arxiv_id
  
  # Getting the altmetric info
  if 'doi' in entry.keys():
    r = requests.get('https://api.altmetric.com/v1/doi/'+entry['doi'])
    if r.ok and 'altmetric_id' in r.json().keys():
      entry['altmetric'] = str(r.json()['altmetric_id'])

  # If the entry has some customization, apply it
  if entry['ID'] in customization.keys():
    for k in customization[entry['ID']]:
      entry[k] = customization[entry['ID']][k]

  entries.append(entry)
# Updating entries
bibtex_database.entries = entries

# Exporting bibtex file
writer = BibTexWriter()
writer.order_entries_by = None
with open('_bibliography/papers.bib', 'w') as bibfile:
  bibfile.write(writer.write(bibtex_database))

print(f"✅ Wrote {len(bibtex_database.entries)} entries to _bibliography/papers.bib")