import streamlit as st

START_COLOR = '"#4DCAFF"'
END_COLOR = '"#4DCAFF"'
DIAMOND_SHAPE_COLOR = '"#3CBD96"'
RECTANGLE_SHAPE_COLOR = '"#886EE6"'
NEON_GREEN = '"#FFFFFF"'
NEON_BLUE = '"#EAE9ED"'
BACKGROUND_COLOR = '"#2A174E"'
TEXT_COLOR = '"white"'
DARKER_TEXT_COLOR = '"black"'

flowchart_code = f"""
digraph RhymingDictionaryFlow {{
    // Set background and text colors
    graph [bgcolor={BACKGROUND_COLOR}];
    node [style=filled, fontcolor={TEXT_COLOR}, fontsize=10, splines=true, rankdir=LR]; 

    // Define color schemes for nodes with neon colors
    Start [shape=ellipse, label="Start", fillcolor={START_COLOR},fontcolor = {DARKER_TEXT_COLOR}];
    End [shape=ellipse, label="End", fillcolor={END_COLOR}, fontcolor = {DARKER_TEXT_COLOR}];
    
    UseSortedData [label="Use Sorted Data?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    ReadSortedData [label="Read Data from File", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    InitializeStressImportance [label="Initialize stressImportance", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    ReadDataFromFile [label="Read Data from File", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    ValidSplit [label="Valid Split?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    CleanWord [label="Clean and Process Word", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    CleanSSBE [label="Clean and Process SSBE", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    ProcessIPA [label="Process IPA", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    StoreStressImportance [label="Store Stress Importance", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    AddToDataDict [label="Add to Data Dictionary", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    AddRhymeAndVowel [label="Add Rhyme and Vowel Data?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    AddRhyme [label="Add Rhyme", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    AddVowelInfo [label="Add Vowel Information", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    AssignFrequency [label="Assign Frequency", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    WriteSortedData [label="Write Sorted Data?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    
    UsingRealDataset [label="Is Using Real Dataset?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    DisplayWarning [label="Display warning: Using testing dataset", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    DisplayHeader [label="Display Header", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    GetSearchTerm [label="Get Search Term", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    IsSearchTermEmpty [label="Is Search Term Empty?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    ProcessMainList [label="Process Main List", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    NoResultsFound [label="No Results Found?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    ToggleSummary [label="Toggle Summary?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    StoreLastSearchedTerm [label="Store Last Searched Term", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    LoopThroughMainList [label="Loop Through Main List", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    ShowAllResults [label="Show All Results?", shape=diamond, fillcolor={DIAMOND_SHAPE_COLOR}];
    DisplayResults [label="Display Results", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    GenerateDataFrame [label="Generate Dataframe", shape=rect, fillcolor={RECTANGLE_SHAPE_COLOR}];
    

    // Define node edges with neon colors for transitions
    Start -> UseSortedData [label="Start", color={NEON_GREEN}];
    UseSortedData -> ReadSortedData [label="Yes", color={NEON_BLUE}];
    UseSortedData -> ReadDataFromFile [label="No", color={START_COLOR}];
    ReadSortedData -> InitializeStressImportance [color={NEON_GREEN}];
    ReadDataFromFile -> InitializeStressImportance [color={NEON_GREEN}];
    InitializeStressImportance -> ValidSplit [color={NEON_GREEN}];
    ValidSplit -> CleanWord [label="Yes", color={NEON_BLUE}];
    ValidSplit -> ReadDataFromFile [label="No", color={START_COLOR}];
    CleanWord -> CleanSSBE [color={NEON_GREEN}];
    CleanSSBE -> ProcessIPA [color={NEON_GREEN}];
    ProcessIPA -> StoreStressImportance [color={NEON_GREEN}];
    StoreStressImportance -> AddToDataDict [color={NEON_GREEN}];
    AddToDataDict -> AddRhymeAndVowel [color={NEON_GREEN}];
    AddRhymeAndVowel -> AddRhyme [label="Yes", color={NEON_BLUE}];
    AddRhymeAndVowel -> AddVowelInfo [label="Yes", color={NEON_BLUE}];
    AddRhyme -> AddVowelInfo [color={NEON_GREEN}];
    AddVowelInfo -> AssignFrequency [color={NEON_GREEN}];
    AssignFrequency -> WriteSortedData [color={NEON_GREEN}];
    WriteSortedData -> End [label="Yes", color={NEON_BLUE}];
    
    UsingRealDataset -> DisplayWarning [label="No", color={START_COLOR}];
    UsingRealDataset -> DisplayHeader [label="Yes", color={NEON_BLUE}];
    DisplayWarning -> DisplayHeader [color={NEON_GREEN}];
    DisplayHeader -> GetSearchTerm [color={NEON_GREEN}];
    GetSearchTerm -> IsSearchTermEmpty [color={NEON_GREEN}];
    IsSearchTermEmpty -> ProcessMainList [label="No", color={NEON_BLUE}];
    IsSearchTermEmpty -> End [label="Yes", color={NEON_BLUE}];
    ProcessMainList -> NoResultsFound [color={NEON_GREEN}];
    NoResultsFound -> DisplayResults [label="No", color={START_COLOR}];
    NoResultsFound -> DisplayWarning [label="Yes", color={NEON_BLUE}];
    DisplayResults -> ToggleSummary [color={NEON_GREEN}];
    ToggleSummary -> StoreLastSearchedTerm [color={NEON_GREEN}];
    StoreLastSearchedTerm -> LoopThroughMainList [color={NEON_GREEN}];
    LoopThroughMainList -> ShowAllResults [color={NEON_GREEN}];
    ShowAllResults -> DisplayResults [label="Yes", color={NEON_BLUE}];
    ShowAllResults -> DisplayResults [label="No", color={START_COLOR}];
    DisplayResults -> GenerateDataFrame [color={NEON_GREEN}];
    GenerateDataFrame -> End [color={NEON_GREEN}];
}}
"""

st.title('🔄 Flowchart Visualizations for Rhyming Dictionary')

st.markdown("""
## Rhyming Dictionary Function Flowchart

This flowchart provides an overview of the processes involved in the Rhyming Dictionary functionality.
It covers everything from reading sorted data, processing IPA (International Phonetic Alphabet), 
to displaying search results and generating data frames.
""")

st.graphviz_chart(flowchart_code)

st.markdown("""
### Key Functions:
- **Lorem ipsum**: dolor sit amet.
""")
