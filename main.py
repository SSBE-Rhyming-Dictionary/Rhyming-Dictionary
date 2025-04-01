### MODULES ###
import copy as copy #Deep copy tables
import pandas as pd #Dataframe to be used with Streamlit
from streamlit_javascript import st_javascript #Dark/Light mode check
import streamlit as st #Data visualizer
import time as time #Used for the "stopwatch" or "timer", optional
import json as json #Used to write to or read from the sorted data file

### Link: https://ssbe-rhyming-dictionary.streamlit.app/

### VARIABLES ###
realDataSet = True #Whether to use RM-AZ or the shortened dataset
disableOverflow = False #Whether to disable text overflow (Show All button)
limit = 14 #Starts from the 0th index, limit+1 is the max number of results to display before pressing Show All.
maximumPenalty = 6 #Maximum number of character length difference, wrong characters, trailing characters, etc
includeResultNumber = False
useSortedData = True #False to save, True to load
syllableForm = "<h6>(x) Syllable(s) ((r) Results)</h6>\n"
commonLimit = 7 #Anything equal to or above this is considered a common word
uncommonWordThreshold = 3 #Anything equal to or below this is considered an uncommon word

filename = realDataSet and 'RM-AZ' or 'NewRMAZ' #Text files
stressedVowel = "ɛ́"[1] #The special vowel stress character
nonBreakingSpace = "\u00A0" #A space that does not carry over to the new line!
infoFileName = "infofile" #Information
sortedDataName = "SortedData"

### VOWELS ###
vowels = ["ɪ","ɛ","a","ɔ","ɵ","ə","ʌ","ɪj","ɛj",'ɑj',"oj","aw","əw","ʉw","ɪː","ɛː","ɑː","oː","ɵː","əː","ó"]

### WEB FREQUENCY ###
webFreqTable = [
  0,
  10,
  100,
  1000,
  10000,
  100000,
  1000000,
  10000000,
  100000000,
  1000000000
] #Last element has a web frequency unit of 10 (Or is it 9? I forgot)

### CODE ##

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")

isLightMode = not (st_theme == "dark")

nl = []
for i in copy.deepcopy(vowels):
  nl.append(i[0]+stressedVowel+(len(i)== 1 and " " or (i[min(1,len(i)-1)])))
for i in nl:
  vowels.append(i.rstrip())
#Duplicate vowels, append the stress, add it back
del(nl)

dict = []

print("Initializing... (0)")

def getTextFromInfoFile(num):
  with open(infoFileName+'.txt', 'r') as file:
    filecontent = file.read().split("<res>")[num-1].split("\n")
    for p in range(len(filecontent)):
      if filecontent[p].rfind("<comment>") > -.5:
        filecontent[p]=filecontent[p][:filecontent[p].rfind("<comment>")]
    return "\n".join(filecontent)
#This function retrieves a specific text section from an "infofile," based on an identifier (<res>).
#Each section is separated by <res>, and comments (marked with <comment>) are removed.

confirmButtonMarkdown = getTextFromInfoFile(1)

if isLightMode:
  confirmButtonMarkdown = confirmButtonMarkdown.replace("cyan","blue")

def listToText(ls):
  return json.dumps(ls, separators=(',', ':'))
def textToList(ls):
  return json.loads(ls)
#These functions convert lists to JSON text format (listToText) and back (textToList).
#They help with saving and loading structured data.

def getTime():
    return round(time.time() * 1000) #Get the milliseconds since Jan 1 1970

upt = getTime() #Effectively starts a stopwatch

def appendRhyme(element,value):
  newelem = copy.deepcopy(dict[element])
  newelem.append(value)
  dict[element] = newelem
#Appends a value to an entry in dict based on element.
#Used to add the rhyme as the 3nd column from 0th.

def ssbeToRhyme(str):
  return str[str.rfind(stressedVowel)-1:len(str)]

#Find stressed vowel using the variable
def removeDupesList(lr):
  fd = []
  lis = []
  pops = []
  for i in lr:
    lis.append(i)
  for i in range(len(lis)):
    for j in fd:
      if lis[i]==j:
        pops.append(i)
        break
    fd.append(i)
  for i in pops:
    lis.pop(i)
  return lis
#This removes duplicate entries from a list by comparing each element to others.
#It preserves the first occurrence while removing subsequent duplicates.
#Primarily used to update the counter.

def squeezeInPosition(value,position):
  for i in range(len(dict)-1,position-1,-1):
    dict[i+1] = dict[i]
  dict[position] = value
#Shifts all elements at position+1 up, then inserts a value into position. Same as pop.

def stressedAndUnstress(ipa):
  parse = ipa.split(" ")
  stri = ""
  for p in parse:
    if p in vowels:
     stri += (stressedVowel in p and "S" or "u")
  return stri
#This identifies stressed and unstressed vowel patterns in an IPA string.
#Marks stressed vowels with "S" and unstressed with "u.".
#Also used to determine the number of syllables.

def narrowList(key):
  #newlist = copy.deepcopy(narrowList(enter))
  newl = {}
  retri = []
  for i in dict:
    if i[2] == key.lower():
      retri.append(i[3])
  if len(retri) != 0:
    for j in range(len(retri)):
      for i in dict:
        if i[3] == retri[j]:
            if newl.get(j,False)==False:
              newl[j] = []
            newl[j].append(copy.deepcopy(i))
  return newl 
#Filters dict based on a key and returns matched entries.

def rowToColumnRow(lis,number):
  rs = []
  for i in lis:
    rs.append(i[number])
  return rs
#Create an array from the numberth column of the result of a 2d array.

def removeCharacter(str,pos):
  return (pos == 0 and "" or str[:max(pos-1,0)])+(pos == len(str)-1 and "" or str[min(pos,len(str)-1):])
#Removes character from string with constraints in mind.

def autoComplete(trm):
  if len(trm) == 0:
    return
    
  prv = ""
  trm = copy.deepcopy(trm.lower()) #Prevent modifying the original
  savedtrm = trm
  lowpenal = min(maximumPenalty,len(trm))
  #Attempt with deduction for extra letters

  for i in dict:
    stringToCompare = copy.deepcopy(i[2]).lower()
    if stringToCompare[0] == trm[0]:
      penalty = 0

      for j in range(max(len(stringToCompare),len(trm))):
        if j >= len(trm) or j >= len(stringToCompare):
          penalty = penalty + 1
        elif not (stringToCompare[j] == trm[j]):
          penalty = penalty + 1

      if penalty < lowpenal:
        lowpenal = penalty
        prv = copy.deepcopy(i[2].lower()).title()

  for i in dict:
    stringToCompare = copy.deepcopy(i[2]).lower()
    if stringToCompare[0] == trm[0]:
      penalty = 0
      trm = savedtrm

      for j in range(max(len(stringToCompare),len(trm))):
        if j >= len(trm) or j >= len(stringToCompare):
          penalty = penalty + 1
        elif not (stringToCompare[j] == trm[j]):
          penalty = penalty + 1

          if j+2 < len(trm) and j+1 < len(stringToCompare):
            if stringToCompare[j] == trm[j+1] and stringToCompare[j+1] == trm[j+2]: 
              trm = removeCharacter(trm,j)
          elif j+1 < len(trm) and j+2 < len(stringToCompare):
            if stringToCompare[j+1] == trm[j] and stringToCompare[j+2] == trm[j+1]:
              stringToCompare = removeCharacter(stringToCompare,j)

      if penalty < lowpenal:
        lowpenal = penalty
        prv = copy.deepcopy(i[2].lower()).title()
  #Attempt without deduction for wrong letters
  if prv:
    return ", did you mean \""+prv+"\"? (No exact matches found)"
  else:
    return " (No matches found)"
#Attempts to match an input term (trm) to the closest word based on a "penalty" system for incorrect characters
#and length differences. It suggests the closest match if no exact match is found. Basically autocomplete.

def enclose(k,impt):
    sub = k.replace(" ", "-") #Format the text into link style
    ff = '<sup><a style="color:Tomato;" href="https://www.dictionary.com/browse/' + sub + '">D</a>&nbsp;'
    af = '<a style="color:DodgerBlue;" href="https://www.thesaurus.com/browse/' + sub + '">T</a></sup>&nbsp;'
    formattedStr = '<b style="color:'+(isLightMode and "DimGray" or "Azure")+';"><u>' + k + "</u></b>"
    originalStr = '<span style="color:'+(isLightMode and "Black" or "LightGrey")+';">' + k.replace(" ","&nbsp;") + "</span>"
    #Use &nbsp; aka non breaking space to prevent the text from carrying over to the next line
    return "".join([formattedStr if impt else originalStr, ff, af])
#Add hyperlinks (to the dictionary and thesarus) to k (The word).

def HTMLed(dataf):
  return dataf
  #for index, row in dataf.iterrows():
    #row['Name']=enclose(row['Name'])
    #st.markdown(row['Name'], unsafe_allow_html=True)
#Initially used to use HTML in tables, unsafe

def returnMainDataFrame(newlist,showUncommonWords):
    names = rowToColumnRow(newlist,0)
    ipaform = rowToColumnRow(newlist,1)
    syllables = rowToColumnRow(newlist,4)
    stressedp = rowToColumnRow(newlist,5)
    commonused = rowToColumnRow(newlist,6)
    compactModeWords = []
    ct = 0
    for index in range(len(names)):
      try:
        k=names[index]
        commonlyUsed=(int(commonused[index].lower())>=commonLimit)
        if int(commonused[index]) > uncommonWordThreshold or showUncommonWords:
          compactModeWords.append([ipaform[index],enclose(k,commonlyUsed)])
        ct += 1
      except IndexError:
        print("No results or out of range")
    sma = []
    over = max(len(compactModeWords)-limit,0)
    for p in range(min(limit,len(compactModeWords))):
      sma.append(compactModeWords[p])
    maindataframe = {
      #"Result No.":lm,
      "Name":names,
      "IPA format":ipaform,
      "Syllables":syllables,
      "Un/Stressed Vowel Pattern": stressedp,
      "Web Frequency":commonused
    }
    smalldataframe = {}
    for key in maindataframe:
      smalldataframe[key] = maindataframe[key][:limit]
    if includeResultNumber:
      smalldataframe["Result No."] = ",   ".join(compactModeWords)
    def res(lis):
      primaryVowelContainer = []
      vowelMatches = {}
      for p in lis:
        rrm = len(stressedAndUnstress(p[0]))
        if str(rrm) in vowelMatches:
          vowelMatches[str(rrm)].append(p[1])
        else:
          vowelMatches[str(rrm)]=[p[1]]
      vowelMatchKeys = []
      for p in vowelMatches:
        vowelMatchKeys.append(int(p))
      vowelMatchKeys.sort()
      for p in vowelMatchKeys:
        primaryVowelContainer.append(syllableForm
        .replace("(x)",(int(p)<1 and "Unidentified Number Of" or str(p)))
        .replace("(s)",(str(int(p)//1)=="1" and" "or"s"))
        .replace("(r)",str(len(vowelMatches[str(p)])))
        +"\n"+(",   ".join(vowelMatches[str(p)]))) #Format the syllable text
      return ("\n\n".join(primaryVowelContainer))
    bigwl = res(compactModeWords)
    smallwl = res(sma)

    return maindataframe, smalldataframe, len(names), newlist[0], bigwl, smallwl, over
#This function organizes data into two DataFrames: maindataframe for the full dataset and smalldataframe for a limited set. 
#It prepares this data for display in the Streamlit app.

#This system basically stores the already sorted dictionary in a text file.
#This shortens the runtime from 12-13s to a measly 0.2s.
if useSortedData:
  print("Retrieving data...")
  with open(sortedDataName+".txt") as fli:
    dict = textToList(fli.read())
else:
  print("Preparing list...")
  stressImportance = {}
  #We cannot use the original method of directly adding to dict to avoid confusion
  #Because Stress Importance was added near the end of our project.

  with open(filename+'.txt', 'r') as file:
    for i in file:
      plaintxt = i.split("▶") #Splits word and SSBE
      if len(plaintxt) < 2:
        continue #Cannot split
      
      rawmatch = str(plaintxt[0]).rstrip().replace("\t","") #Removes tab for word
      for j in range(10):
        rawmatch = rawmatch.replace(str(j),"") #Removes numbers from word
      
      key = str(plaintxt[1]).rstrip().replace("\t","") #Removes tab for SSBE
      key = key.replace("\u2009"," ") #Removes \u2009 (Probably a whitespace?)
      ipa = key
      num = ""
      for j in range(len(ipa)):
        index = (len(ipa)-j)-1
        if ipa[index].isdigit() and int(ipa[index]) in range(10):
          num+=ipa[index]
        elif ipa[index] != "," and ipa[index]!="":
          break
      num=num[::-1]
      for j in range(10):
        ipa = ipa.replace(str(j),"")
      ipa = ipa.replace(",","")
      stressImportance[rawmatch+ipa]=num
      dict.append([rawmatch,ipa,rawmatch.lower()])

  #print("Removing duplicates...")
  #removeDuplicates()

  print(f"Adding rhymes... ({(round((getTime()-upt)//100))*0.1})s")
  
  for i in range(len(dict)):
    appendRhyme(i,ssbeToRhyme(dict[i][1]))
    vowelStr = stressedAndUnstress(copy.deepcopy(dict[i][1]))
    dict[i].append(len(vowelStr))
    dict[i].append(vowelStr)
    isM = int(((dict[i][0]+dict[i][1]) in stressImportance) and stressImportance[dict[i][0]+dict[i][1]] or "-1")
    freq = -1
    for p in range(len(webFreqTable)):
      if webFreqTable[p] <= isM:
        freq = p
    dict[i].append(str(freq))
    #Appends the stressed or unstressed vowel pattern and the syllables
  #printdict()
  with open(sortedDataName+".txt","w") as fli:
    fli.write(listToText(dict))

  print(f"Ready ({(round((getTime()-upt)//100))*0.1}s)")

if not realDataSet:
  kuru = st.warning("You are using the testing dataset!",icon="⚠️")

def home_page():
  st.header("SSBE RHYMING DICTIONARY")
  st.markdown("""
    <h3 style='text-align: left; font-size: 20px; margin-top: -10px;'>Made by 
    <a href="https://sites.google.com/view/gavrielchia/" target="_blank" style="color: #4A90E2;">Gavriel Chia</a> and 
    <a href="https://sites.google.com/view/test/" target="_blank" style="color: #4A90E2;">Mak Mun Zhong</a> and  
    <a href="https://sites.google.com/view/test/" target="_blank" style="color: #4A90E2;">Jayden Tan Yi Zhe</a></h3>
    <h4 style='text-align: left; font-size: 18px; margin-top: -5px;'>Development guided by 
    <a href="https://www.instagram.com/szetodl/" target="_blank" style="color: #F1C40F;">Mr. Szeto Dillion</a></h4>
    <h4 style='text-align: left; font-size: 18px; margin-top: -5px;'>Database from the 
    <a href="http://seas.elte.hu/cube/" target="_blank" style="color: #E74C3C;">CUBE Dictionary</a></h4>
    """, unsafe_allow_html=True)
  
  # Buttons to navigate to other pages
  col1, col2 = st.columns(2)
  with col1:
    if st.button("Go to Rhyming Search"):
      st.session_state.page = "search"
      st.rerun()  # Force a rerun to load the new page
  with col2:
    if st.button("About the Dictionary"):
      st.session_state.page = "about"
      st.rerun()  # Force a rerun to load the new page

def about_page():
  st.title("About the Rhyming Dictionary")
  st.markdown("""
      <p>This tool is a rhyming dictionary tool based on Standard Southern British English (SSBE) that helps you find rhymes for any word. This project is open sourced, and the code may be found <a href="https://github.com/SSBE-Rhyming-Dictionary/Rhyming-Dictionary" target="_blank" style="color: #4A90E2;">here</a>.</p>
      """, unsafe_allow_html=True)
  st.markdown("""
      <h2 style='text-align: left; font-size: 20px; margin-top: 1px;'>Common Questions:</h2>
      """, unsafe_allow_html=True)
  st.markdown("""
      <h4 style='text-align: left; font-size: 18px; margin-top: -5px;'>What is a rhyming dictionary?</h4>
      """, unsafe_allow_html=True)
  st.markdown("""
      <p>A rhyming dictionary is a specialised dictionary where words that rhyme with each other are categorised together, often used when writing song lyrics and poetry.</p>
      """, unsafe_allow_html=True)
  st.markdown("""
      <h4 style='text-align: left; font-size: 18px; margin-top: -5px;'>What is Standard Southern British English (SSBE)?</h4>
      """, unsafe_allow_html=True)
  st.markdown("""
      <p>In the 20th century, Received Pronunciation (RP) was considered the standard educated pronunciation and the prestige variety of British English. 
      However, Dr. Geoff Lindsey argues that from the late 20th century to the early 21st century, the pronunciation of the de-facto standard variety of British English in the southeast of England has shifted so significantly, 
      such that several characteristics of RP sound outdated today. Therefore, this new "accent" of British English was transcripted into the International Phonetic Alphabet by him, resulting in the Current British English (CUBE) Dictionary. 
      This transcription is known as SSBE.</p>
      """, unsafe_allow_html=True)
  st.markdown("""
      <h4 style='text-align: left; font-size: 18px; margin-top: -5px;'>Why do we require a rhyming dictionary, particularly one for SSBE?</h4>
      """, unsafe_allow_html=True)
  st.markdown("""
      <p>Due to the discrepancy between the phonologies of General American English (GenAm), Received Pronunciation (RP) and Standard Southern British English (SSBE), 
      different sets of words rhyme with one another in each accent. Thus, different rhyming dictionaries are required for each accent.</p>
      """, unsafe_allow_html=True)
  st.markdown("""
      <h4 style='text-align: left; font-size: 18px; margin-top: -5px;'>Where is the database from?:</h4>
      """, unsafe_allow_html=True)
  st.markdown("""
      <p>The original database is the <a href="http://seas.elte.hu/cube/" target="_blank" style="color: #4A90E2;">Current British English (CUBE) Dictionary</a>, designed and compiled by Péter Szigetvári and Geoff Lindsey. Their database was drawn from a transcription dictionary by 
      Ádám Nádasdy and Szigetvári (Huron’s English Pronouncing Dictionary/Huron angol kiejtési kézikönyv). What this application has done is reformatted and implemented an alorithm to find rhyming pairs of words. </p>
      """, unsafe_allow_html=True)
  st.markdown("""
      <h2 style='text-align: left; font-size: 20px; margin-top: -10px;'>Queries and Contact Information:</h2>
      """, unsafe_allow_html=True)
  st.markdown("""
      <p>This project was made by <a href="https://sites.google.com/view/gavrielchia/" target="_blank" style="color: #4A90E2;">Gavriel Chia</a> and 
    <a href="https://github.com/Discwebhook" target="_blank" style="color: #4A90E2;">Mak Mun Zhong</a> and  
    <a href="https://sites.google.com/view/test/" target="_blank" style="color: #4A90E2;">Jayden Tan Yi Zhe</a></h3>. 
    The developmental process was guided by <a href="https://www.instagram.com/szetodl/" target="_blank" style="color: #4A90E2;">Mr. Szeto Dillion</a>. If you have any queries, do email us at: gavriel_chia_kai_ze@s2022.ssts.edu.sg or mak_mun_zhong@s2022.ssts.edu.sg</p>
      """, unsafe_allow_html=True)
  
  # Back button to return to the main page
  if st.button("Back to Home", type="primary"):
    st.session_state.page = "home"
    st.rerun()  # Force a rerun to load the new page

def rhyme_search_page():
  st.header("SSBE RHYMING DICTIONARY")
  textinput = st.text_input("Your search term",key="w",max_chars=100,placeholder="...")
  enter= textinput.replace("'","’").rstrip()

  mainlist = copy.deepcopy(narrowList(enter))
  totalLength = 0 #Number of pronunciation results from narrowList
  for i in removeDupesList(mainlist):
    totalLength += len(mainlist[i])

  if len(enter) == 0:
      'Enter a term to get started!' #Term is empty
  else:
    noResults = totalLength==0
    'Your term: ', enter.title() , (noResults and autoComplete(enter) or (" ("+str(totalLength))+" matches found)")
    isSummary, showUncommonWords = False, True
    if not noResults:
      isSummary = st.toggle("Summary",False,"Sumry","Displays rhyming words as plain text only.")
    #if isSummary:
      #showUncommonWords = st.toggle("Show rarely used words",True,"Sruw")
    print("\nNEW RESULT")
    print("Search term:\""+enter+"\"")
    print("Results: "+str(len(mainlist)))

    if disableOverflow:
      overflow = 0
    
    rhymeArray = [] #Store duplicate rhymes

    storedResult = False #Initialize to nothing
    if "LastSearchedTerm" in st.session_state:
      storedResult = st.session_state["LastSearchedTerm"]
    st.session_state["LastSearchedTerm"] = enter
    
    override = False

    for j in range(len(mainlist)):
      data,smalldata,resultNum,rm,compactWordsList,smallerWordsList,overflow = returnMainDataFrame(mainlist[j],showUncommonWords)
      rhyme = rm[3]
      ipa = rm[2]
      enter = enter.rstrip()
      matchr = False

      for i in rhymeArray:
        if i.lower() == rhyme.lower():
          matchr = True
      if matchr:
        continue #Does the same word have the same rhyme?

      rhymeArray.append(rhyme)

      if "Override" in st.session_state:
        override = (override or st.session_state["Override"] and (not storedResult or storedResult == enter))
      if j == len(mainlist):
        st.session_state["Override"] = (overflow > 0)
      #This section of the code decides whether to automatically "Show All"

      if len(data["Name"]) != 0:
        st.text('Rhyme: "'+rhyme+'" ('+str(resultNum)+" Results)") #Label for each rhyme a word has
        
        if isSummary:
          if overflow > 0 and not override: #Has "Show All" not been clicked, and are there too many results?
            containerTextResults = st.empty() 
            containerShowAllButton = st.empty() #Create two containers to store the two components.

            with containerTextResults:
              compacter = st.write(smallerWordsList,unsafe_allow_html=True)
            with containerShowAllButton:
              compactButton = st.button(str(overflow)+" Results Hidden, Show All",'kna'+rhyme)

            #st.markdown(confirmButtonMarkdown, unsafe_allow_html=True)
            
            if compactButton:
              containerTextResults.empty() #Deletes the previously compacted word list.
              containerShowAllButton.empty() #Deletes the "Show All" button.
              compacter = st.write(compactWordsList,unsafe_allow_html=True) #Shows the full word list instead.
          else:
            compacter = st.write(compactWordsList,unsafe_allow_html=True) 
            #Nothing special done, just shows the original words list
        else:
          if overflow > 0 and not override: #Has "Show All" not been clicked, and are there too many results?
            containerDataframe = st.empty() #Create a containers to store the compacted table of results to (possibly) delete later.
            
            with containerDataframe:
              dataframe = HTMLed(pd.DataFrame(smalldata).rename_axis('Result Num', axis=1))
              row_height2=int(len(data["Name"])==0 and 0 or 37*(resultNum-overflow+1)/(resultNum-overflow+1))
              dataTM = st.dataframe(dataframe, 1000,len(data["Name"])==0 and 0 or 37*(resultNum-overflow+1),row_height=row_height2)
            
            containerButton = st.empty() #Create a containers to store the "Show All" button to (possibly) delete later.
            with containerButton:
              showAllDataframe = st.button(str(overflow)+" Results Hidden, Show All",'kar'+rhyme)
            #st.markdown(confirmButtonMarkdown, unsafe_allow_html=True)
            
            if showAllDataframe:
              containerButton.empty() #Deletes the previously compacted table of results.
              containerDataframe.empty() #Deletes the "Show All" button.
              dataframe = HTMLed(pd.DataFrame(data).rename_axis('Result Num', axis=1)) #Shows the full table instead.
              row_height2=int(len(data["Name"])==0 and 0 or 37*(resultNum+1)/(resultNum+1))
              dataTM = st.dataframe(dataframe,1000,len(data["Name"])==0 and 0 or 37*(resultNum+1),row_height=row_height2)
          else:
            #Nothing special done, just shows the original table
            dataframe = HTMLed(pd.DataFrame(data).rename_axis('Result Num', axis=1))
            row_height2=int(len(data["Name"])==0 and 0 or 37*(resultNum+1)/(resultNum+1))
            dataTM = st.dataframe(dataframe,1000,len(data["Name"])==0 and 0 or 37*(resultNum+1),row_height=row_height2)
        #Generate dataframe (table) for each response
  
  # Back button to return to the main page
  if st.button("Back to Home", type="primary"):
    st.session_state.page = "home"
    st.rerun()  # Force a rerun to load the new page        
        
# Main function to display the page based on the session state
def main():
    # Initialize session state for navigation if not already done
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "search":
        rhyme_search_page()
    elif st.session_state.page == "about":
        about_page()

if __name__ == "__main__":
    main()
