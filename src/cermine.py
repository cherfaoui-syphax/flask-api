from bs4 import BeautifulSoup

# get abstract from cermine xml output
def get_file_abstract(f):
  try :
    with open (f,'r',encoding='utf-8') as file:
        content = file.readlines()
        content = "".join(content)
        soup = BeautifulSoup(content)
        abstracts = soup.findAll("zone", {"label":"MET_ABSTRACT"})  
        abstracts_array =  [abstract.text for abstract in abstracts]
        return max(abstracts_array,key=len)
  except:
      return ""

# get keywords from cermine xml output
def get_file_keywords(f):
  try :
    with open (f,'r',encoding='utf-8') as file:
        content = file.readlines()
        content = "".join(content)
        soup = BeautifulSoup(content)
        keys = soup.findAll("zone", {"label":"MET_KEYWORDS"})  
        keys_array =  [key.text for key in keys]
        return keys_array
  except:
      return ""

def extract_cermine(path):
    return str({"abstract":get_file_abstract(path),"keywords": get_file_keywords(path)})