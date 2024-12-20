# imports
import pandas as pd
import numpy as np
import plotly as pl

import matplotlib.pyplot as plt
import os
import xarray as xr

import streamlit as st 
import matplotlib
import mpld3
import streamlit.components.v1 as components
import matplotlib as mpl
from matplotlib import cm
from matplotlib import colors
import datetime
import plotly.graph_objects as go
import statistics
import plotly.express as px
from plotly.subplots import make_subplots
import re
from io import BytesIO





engagementMapping = {
    'Appointment':  'Appointment',
    'Group Appointment':  'Appointment',
    'Career Fair':  'Career Fair',
    'Drop-In/Chat':  'Drop-In/Chat',
    'Employer On-Site':  'Employer Activity ',
    'Employer Partner Event':  'Employer Activity ',
    'Employer Site Visit':  'Employer Activity ',
    'Trek':  'Employer Activity ',
    'OCI':  'Employer Activity ',
    'Info Session':  'Employer Activity ',
    'Career Course':  'Career Course ',
    'Hiration':  'Hiration ',
    'Networking':  'Networking Event',
    'Mentor Meetup':  'Networking Event',
    'Speaker/Panel':  'Networking Event',
    'Type Focus':  'Type Focus ',
    'Hiatt Funding':  'Hiatt Funding',
    'Virtual Session':  'Workshop/Event',
    'Classroom Presentation':  'Workshop/Event',
    'Club Presentation':  'Workshop/Event',
    'Orientation':  'Workshop/Event',
    'Workshop':  'Workshop/Event',
    'Employment Toolkit':  'Online Resource ',
    'Forage':  'Online Resource ',
    'Rise Together':  'Rise Together',
    'WOW':  'Do not Include',
    'Completed Handshake Profile':  'Do not Include',
    'Alumni Interview Coaching':  'Do not Include',
    'BIX Review':  'Do not Include',
    'Career Closet':  'Do not Include',
    'CIC Career Fair':  'Do not Include',
    'Club Support':  'Do not Include',
    'HS Employer Review':  'Do not Include',
    'HS Interview Review':  'Do not Include',
    'Library Book':  'Do not Include',
    'LinkedIn Photobooth':  'Do not Include',
    'Mentor Program':  'Do not Include',
    'Micro-internships':  'Do not Include',
    'Other':  'Do not Include',
    'Wisdom Wanted Ad':  'Do not Include',
    'appointment':  'Appointment',
    'Employer On-site':  'Employer Activity ',
    'HS Job Review':  'Do not Include',
}


def clean_semesters(row):
    string = row['Semester']
    if "Winter" in string:
        string = "Winter 20" + str((int(string[-3:-1]) - 1))
    if "(FY" in string:
        string = string[:string.rfind('(')-1]
    if "FAll" in string:
        string = "Fall" + string[4:]
    return string
def create_semester_value(str, map):
        date = int(str[-4:])
        num = (date - 2017) * 4 + 1
        if "Fall" in str:
            num += 1
        if "Winter"in str:
            num += 2
        if "Spring" in str:
            num += -1
        if "Summer" in str:
            num += 0
        map[num] = str
        return num
def create_aggregated_semester_value(str, graduationSemester):
        if graduationSemester in [0, 'nan', 'None', np.nan]:
            return -9999
        date = int(str[-4:])
        gradYear = (int(graduationSemester[-4:]) - 2021)
        if "Fall" in graduationSemester:
            gradYear += 1
        num = (date - 2017) * 4 + 1
        if "Fall" in str:
            num += 1
        if "Winter"in str:
            num += 2
        if "Spring" in str:
            num += -1
        if "Summer" in str:
            num += 0
        num -= (gradYear *4)
        return num
def create_semester_value_from_number(num, map):
        year = str(int(num/4) + 2017)
        if num%4 == 1:
            year = "Summer " + year
        if num%4 == 2:
            year = "Fall " + year
        if num%4 == 3:
            year = "Winter " + year
        if num%4 == 0:
            year = "Spring " + year
        
        map[num] = year
        return num
def addChartToPage(fig):
    if fig not in st.session_state['currentGraphs']:
        st.session_state['currentGraphs'].append(fig)
    chart = st.plotly_chart(fig, on_select="rerun", selection_mode=["points"])


    if chart['selection']['points']:
        for point in chart['selection']['points']:
            figureLength = len(fig.data)
            printout = fig.data[figureLength-1].hovertemplate
            #print(fig.data)
            with st.container():
                #print(printout)
                #print("Printout frewibgfuierwbgureiwobgueriwbgoiurbwug")
                printout = printout.replace("%{", "{")
                printout = printout.replace("<extra></extra>", "")
                printout = printout.replace("<br>", " ")
                
                listOfVariables = re.findall("{(?:[^{}])*}", printout)
                for initialVar in listOfVariables:
                    var = initialVar[1:-1]
                    
                    try:
                        index = var.index(":")
                        qualifier = var[index:]
                        var = var[:index]
                    except:
                        qualifier = ""
                        var = var
                    
                    if var == "marker.size":
                        var = "marker_size"
                    if "customdata" in var:
                        data = point["customdata"][int(var[-2:-1])]
                    else:
                        data = point[var]
                    
                    formatting = ("{" + qualifier + "}")
                    final = formatting.format(data)

                    printout = printout.replace(initialVar, final)
                    
                st.write(printout)
                

    if fig not in st.session_state['workbookGraphs']:
        if st.button("Add this graph to the workbook", key = fig):
            st.session_state['workbookGraphs'].append(fig)
            st.write("Graph added!")
    else:
        st.write("This graph is in the workbook!")

import streamlit as st
import pandas as pd
from io import StringIO

pl.io.templates.default = 'plotly'

aaa = datetime.datetime.now()

st.markdown("<p style='text-align: center; font-size: 3em; font-weight: bold; color: #003478; margin-bottom: 0.5em; line-height: 1.2;'>Hiatt Career Center -- Advanced Visualization Creator<p>", unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.5em; font-weight: bold; color: #003478; margin-bottom: 1.5em; line-height: 1.1; font-style: italic;">Created By: Rowan Scassellati and Jon Schlesinger</p>', unsafe_allow_html=True)
st.html(
    '''
    <style>
    hr {
        border: none;
        height: 2px;
        /* Set the hr color */
        color: #003478;  /* old IE */
        background-color: #003478;  /* Modern Browsers */
        margin-bottom: 0px;
        margin-top: 0px;
    }
    </style>
    '''
)
st.divider()

tabs_font_css = """
<style>
div[class*="stCheckbox"] label p {
  font-size: 20px;
}

div[class*="stMultiSelect"] label p {
  font-size: 20px;
}

div[class*="stNumberInput"] label p {
  font-size: 20px;
}

div[class*="stRadio"] label p {
  font-size: 20px;

}

div[class*="stSelectbox"] label p {
  font-size: 20px;
}

div[data-testid="stExpander"] details summary p{
    font-size: 20px;
    font-weight: bold;
}
</style>
"""
st.write(tabs_font_css, unsafe_allow_html=True)


st.markdown("""
    <style>
        .stMultiSelect [data-baseweb=select] span{
            max-width: 500px;
        }
    </style>
    """, unsafe_allow_html=True)

if 'dataFile' not in st.session_state:
    st.markdown('<p style="font-size: 20px; ">In order to get started, please add the excel file that contains the correctly formatted Hiatt data</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("In order to get started, please add the excel file that contains the correctly formatted Hiatt data", label_visibility="collapsed")
else:
    uploaded_file = st.session_state['dataFile']

if uploaded_file is None:
    st.session_state['checkFile'] = True



if uploaded_file is not None and st.session_state['checkFile'] == True:
    st.session_state['dataFile'] = uploaded_file
    print("Hello!")

    xls = pd.read_excel(uploaded_file, engine = 'calamine', sheet_name=['Data', 'Demographics', 'Event Groupings', 'Event Rankings', 'Majors and Minors', 'Majors and Minors Groupings', 'Graduate Emails'])

    # Access individual sheets using sheet names
    data_df = xls['Data']
    demographics = xls['Demographics']
    groupings = xls['Event Groupings']
    rankings = xls['Event Rankings']
    majors = xls['Majors and Minors']
    majorsGroupings = xls['Majors and Minors Groupings']
    graduateEmails = xls['Graduate Emails']

    
    


    data_df['Semester'] = data_df['Semester'].str.strip()


    originalEngagementMapping = {}
    groupings['Event Type Name'] = groupings['Event Type Name'].str.lower()
    data_df['Event Type Name'] = data_df['Event Type Name'].str.lower()


    for ind in groupings.index:
        originalEngagementMapping[groupings['Event Type Name'][ind]] = groupings['Event Type Summarized\r\nIn order to ignore this event, use "Do not Include"'][ind]


    def engagement_categories(row):
        return originalEngagementMapping[row['Event Type Name']]
    data_df['Engagement Type'] = data_df.apply(engagement_categories, axis=1)


    data_df = data_df.drop(data_df[data_df['Engagement Type'] == 'Do not Include'].index)

    eventRankings = {}

    for ind in rankings.index:
        #print(rankings["Types of Event Groupings\r\nDO NOT MODIFY -- PULLS FROM EVENT GROUPINGS TAB!"][ind])
        eventRankings[rankings['Types of Event Groupings\r\nDO NOT MODIFY -- PULLS FROM EVENT GROUPINGS TAB!'][ind]] = rankings['Ranked Importance of Events'][ind]
    def ranking_events(row):
        return eventRankings[row['Engagement Type']]
     

    data_df['Event Ranking from User'] = data_df.apply(ranking_events, axis=1)

    rankings = rankings.sort_values(['Ranked Importance of Events'], ascending=[True])
    rankedEngagementList = list(rankings['Types of Event Groupings\r\nDO NOT MODIFY -- PULLS FROM EVENT GROUPINGS TAB!'])
    
    st.session_state['RankedEngagementList'] = [x for x in rankedEngagementList if "Do not Include" not in x]

    demographics['Email'] = demographics['Email'].str.lower()
    data_df['Email'] = data_df['Email'].str.lower()

    gradMapping = {np.nan: None}
    for ind in demographics.index:
        gradMapping[demographics['Email'][ind]] = demographics['Expected Completion Period'][ind]

    
    def gMap(email):
        if email in gradMapping:
           return gradMapping[email]
        else:
            return np.nan

    data_df['Graduation_Semester'] = data_df.apply(lambda x: gMap(x.Email), axis = 1)

    graduationYears = set(gradMapping.values())
    graduationYears = [s.strip()[-4:] for s in graduationYears if str(s) not in ['0', 'nan', 'None']]
    graduationYears = list(set(graduationYears))
    graduationYears.sort(reverse = True)
    graduationYears.insert(0, "Do not restrict by graduation year")
    st.session_state['Graduation List'] = graduationYears


    majorsGroupingsMapping = {}
    for ind in majorsGroupings.index:
        majorsGroupingsMapping[majorsGroupings['Types of Majors'][ind]] = majorsGroupings['Majors (Restricted List)'][ind]
    
    def majorsGroupingsMap(major):
        return majorsGroupingsMapping[major]
    
    majors['Majors'] = majors['Majors Name']
    majors['Majors Name'] = majors.apply(lambda x: majorsGroupingsMap(x.Majors), axis = 1)

    majors['Email'] = majors['Students Email - Institution'].str.lower()



    majorsMapping = {np.nan: []}
    for ind in majors.index:
        email = majors['Email'][ind]
        if (email not in majorsMapping):
            majorsMapping[email] = [majors['Majors Name'][ind]]
        else:
            majorsMapping[email].extend([majors['Majors Name'][ind]])
    st.session_state['Majors Mapping'] = majorsMapping
    
    def majorsMap(email):
        if email not in majorsMapping:
            return "No Major Found"
        else:
            return majorsMapping[email]

    data_df['Majors'] = data_df.apply(lambda x: majorsMap(x.Email), axis = 1)

    majorsList = sorted(set(majorsGroupings['Majors (Restricted List)']))
    #print(majorsList)
    st.session_state['Majors List'] = majorsList

    #data_df.to_excel("OutputSecond.xlsx")

    st.session_state['graphsGenerated'] = False
    st.session_state['df'] = data_df
    st.session_state['graduateEmails'] = graduateEmails
    st.session_state['checkFile'] = False
    st.session_state['sankeyColumns'] = 3
    st.session_state['sankeyLineWeight'] = 3
    st.session_state['neverEngagedBefore'] = False
    st.session_state['neverEngagedAgain'] = False
    st.session_state['scatterMinimumSize'] = 3
    st.session_state['majorsToInclude'] = []
    st.session_state['aggregatedScatter'] = "Do not aggregate (default)"
    st.session_state['scatterMaxPercentile'] = float(100.0)
    st.session_state['numbervspercent'] = False
    st.session_state['restrictByKnownGraduates'] = False
    st.session_state['downloadFile'] = False
    st.session_state['steppedColorbars'] = False
    st.session_state['numberOfColorDivisions'] = 5
    st.session_state['graduationYearToRestrictBy'] = "Do not restrict by graduation year"
    st.session_state['graphTypes'] = []
    st.session_state['advancedOptions'] = False

    st.session_state['restrictingDataOptions'] = False
    st.session_state['sankeyGraphOptions'] = False
    st.session_state['scatterPlotOptions'] = False
    st.session_state['otherOptions'] = False
    st.session_state['lineGraphEngagementOptions'] = ['Any Engagement']

    st.rerun()
    

if uploaded_file is not None and st.session_state['checkFile'] == False:
    def store_value(key):
        st.session_state[key] = st.session_state["_"+key]
    def load_value(key):
        st.session_state["_"+key] = st.session_state[key]


    load_value("graphTypes")
    st.session_state['graphTypes'] = st.multiselect(
        "What type of visualizations should be generated?",
        ["Sequential Pathways of Student Engagements", "Engagement Relationships (Unique)", "Engagement Relationships (Total)", "First Engagements Data (Unique)", "First Engagements Data (Total)", "Return Rates Based on All Engagements", "Return Rates Based on First Engagements", "Rates of Unique Engagements", "Students with only 1 Engagement", "Total Engagement Percentages", "When Students Engaged with Hiatt"],
        key="_graphTypes", on_change=store_value, args=["graphTypes"]
    )

    # st.session_state['graphTypes'] = st.multiselect(
    #     "What type of visualizations should be generated?",
    #     ["Sequential Pathways of Student Engagements", "Engagement Relationships (Unique)", "Engagement Relationships (Total)", "First Engagements Data (Unique)", "First Engagements Data (Total)", "Return Rates Based on All Engagements", "Return Rates Based on First Engagements", "Rates of Unique Engagements", "Students with only 1 Engagement", "Total Engagement Percentages", "Engagement Percentages by Grade"],
    #     default=st.session_state['graphTypes']
    # )
    
    
    #st.session_state['graduationYearToRestrictBy'] = st.selectbox("What graduating class should the data be from?", st.session_state['Graduation List'], index = st.session_state['Graduation List'].index(st.session_state['graduationYearToRestrictBy']))
    
    bbb = datetime.datetime.now()
    print((bbb-aaa).total_seconds())

    def downloadExcelFile(df):
        graduationYearToRestrictBy = st.session_state['graduationYearToRestrictBy']
        graphTypes = st.session_state['graphTypes']

        
        df = st.session_state['df'].copy()
        
        df['Unique ID'] = df.groupby(['Email']).ngroup()
        df['Semester'] = df.apply(clean_semesters, axis=1)

        def updatedRestrictByCohort(df, graduationYear):
            df.drop(df[
                (df['Graduation_Semester'] != 'Spring Semester ' + str(graduationYear)) &
                (df['Graduation_Semester'] != 'Summer Semester ' + str(graduationYear)) &
                (df['Graduation_Semester'] != 'GPS Spring Semester ' + str(graduationYear)) &
                (df['Graduation_Semester'] != 'GPS Fall Semester ' + str(graduationYear-1)) &
                (df['Graduation_Semester'] != 'Fall Semester ' + str(graduationYear-1))].index, inplace=True)
            return df
        def restrictByCohort(df, graduationYear):
            df.drop(df[
                ((df['Class Level'] != 'Senior') &
                (df['Class Level'] != 'Junior')  &
                (df['Class Level'] != 'Sophomore') &
                (df['Class Level'] != 'Freshman'))
                ].index, inplace=True)
            df.drop(df[((df['Semester'] == (str(graduationYear-1) + 'Fall')))].index, inplace=True)
            df.drop(df[((df['Class Level'] == 'Senior') & 
                    ((df['Semester'] != ('Summer ' + str(graduationYear-1))) & 
                    (df['Semester'] != ('Fall ' + str(graduationYear-1))) &
                    (df['Semester'] != ('Winter ' + str(graduationYear-1))) & 
                    (df['Semester'] != ('Spring ' + str(graduationYear)))))].index, inplace=True)
            df.drop(df[((df['Class Level'] == 'Junior') & 
                    ((df['Semester'] != ('Summer ' + str(graduationYear-2))) & 
                    (df['Semester'] != ('Fall ' + str(graduationYear-2))) &
                    (df['Semester'] != ('Winter ' + str(graduationYear-2))) & 
                    (df['Semester'] != ('Spring ' + str(graduationYear-1)))))].index, inplace=True)
            df.drop(df[((df['Class Level'] == 'Sophomore') & 
                    ((df['Semester'] != ('Summer ' + str(graduationYear-3))) & 
                    (df['Semester'] != ('Fall ' + str(graduationYear-3))) &
                    (df['Semester'] != ('Winter ' + str(graduationYear-3))) & 
                    (df['Semester'] != ('Spring ' + str(graduationYear-2)))))].index, inplace=True)
            df.drop(df[((df['Class Level'] == 'Freshman') & 
                ((df['Semester'] != ('Summer ' + str(graduationYear-4))) & 
                (df['Semester'] != ('Fall ' + str(graduationYear-4))) &
                (df['Semester'] != ('Winter ' + str(graduationYear-4))) & 
                (df['Semester'] != ('Spring ' + str(graduationYear-3)))))].index, inplace=True)
            return(df)


        #graduationYearToRestrictBy = 2021
        if(graduationYearToRestrictBy != 'Do not restrict by graduation year'):
            #df = restrictByCohort(df, int(graduationYearToRestrictBy))
            df = updatedRestrictByCohort(df, int(graduationYearToRestrictBy))
            subtitle = "Graduating class of " + graduationYearToRestrictBy
        else:
            subtitle = "Data not restricted by graduating class"
        ###
        #df.to_excel('OutputSource.xlsx', sheet_name="source")
        ###
        def event_sizes(row):
            return eventSize[row['Engagement Type']]


        eventSize = df.groupby('Engagement Type').count().to_dict(orient='dict')['Semester']
        df['Event Size'] = df.apply(event_sizes, axis=1)

        ##This is used to drop the smaller events as desired, and the number is the minimum number of engagements
        ####THIS SHOULD BE DELETED LATER!!!! IT CAN BE HANDLED LOWER DOWN, THIS WILL LEAD TO INACCURATE RESULTS!!!!
        #df = df.drop(df[df['Event Size'] < 1000].index)
        #####


        mapping = {}
        events = df.groupby('Engagement Type').count().to_dict(orient='dict')['Unique ID']
        sorted_events = sorted(events.items(), key=lambda x:x[1], reverse=True)
        sorted_events_dictionary = dict(sorted_events)
        
        x=0
        while x < len(sorted_events):
            mapping[sorted_events[x][0]] = x+1
            x +=1

        def ranked_events(row):
            return mapping[row['Engagement Type']]
        df['Ranked Events'] = df.apply(ranked_events, axis=1)
        ######

        #Not used for line graphs, but used for other graphing types
        #originalEngagementList = list(sorted_events_dictionary.keys())
        originalEngagementList = st.session_state['RankedEngagementList']

        total = pd.DataFrame(index = originalEngagementList, columns=originalEngagementList)
        for col in total.columns:
            total[col].values[:] = 0

        #success = total.copy()
        #percent = total.copy()

        majorsToInclude = set(st.session_state['majorsToInclude'])
        if len(majorsToInclude) > 0:
            to_delete = list()
            for id, row in df.iterrows():
                if not set(row.Majors).intersection(majorsToInclude):
                    to_delete.append(id)
            df.drop(to_delete, inplace=True)

            subtitle += ", only including students with majors in the following categories: " + ', '.join(majorsToInclude)
        else:
            if subtitle == "Data not restricted by graduating class":
                subtitle += " or students major"
            else:
                subtitle += ", data not restricted by students major"

        
        if st.session_state['restrictByKnownGraduates']:
            if subtitle != "Data not restricted by graduating class or students major":
                subtitle += "<br>Data also restricted to only include students known to have graduated"
            else:
                subtitle = "Data restricted to only include students known to have graduated, but not by students major or graduating class"
            
            graduateEmailsDF = st.session_state['graduateEmails']
            graduateEmailsList = graduateEmailsDF.values.flatten()
            df = df[df['Email'].isin(graduateEmailsList)]



        df = df.sort_values(['Unique ID', 'Events Start Date Date'], ascending=[True, True])
        df.reset_index(drop=True, inplace=True)
        
        
        graduateEmailsDF = st.session_state['graduateEmails']
        graduateEmailsList = graduateEmailsDF.values.flatten()
        df['First Engagement?'] = df['Unique ID'].duplicated().map({True: "No", False: "Yes"})
        df['Last Engagement?'] = df['Unique ID'].duplicated(keep='last').map({True: "No", False: "Yes"})
        df["Student's Number of Engagements"] = df.groupby('Unique ID')['Unique ID'].transform('count')
        df["Known Graduate?"] = np.where(df['Email'].isin(graduateEmailsList), 'Graduate', 'Not Graduate')
        
        df.drop(['Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19', 'Email.1', 'Self-Reported Graduation Date', "Event Type Name", 'Medium', 'Event Originator', "Event Medium", "Host", "Event Ranking from User", "Event Size", "Ranked Events"], axis=1, inplace=True)
        df.insert(0, subtitle, None) 

        def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, index=False, sheet_name='Sheet1', engine = 'xlsxwriter')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            format1 = workbook.add_format({'num_format': '0.00'}) 
            worksheet.set_column('A:A', None, format1)  
            writer._save()
            processed_data = output.getvalue()
            return processed_data
        df_xlsx = to_excel(df)
        
        return df_xlsx
        
        

    #st.session_state['advancedOptions'] = st.checkbox("Show advanced options", value = st.session_state['advancedOptions'])
    st.divider()
    with st.expander("Show ways to restrict the data, which applies to all graphs"):
        st.divider()
        load_value("graduationYearToRestrictBy")
        st.selectbox("What graduating class should the data be from?", st.session_state['Graduation List'], key = "_graduationYearToRestrictBy", on_change=store_value, args=["graduationYearToRestrictBy"])
        load_value("majorsToInclude")
        st.multiselect("What majors should be included? Pulls from the graduation records, so it does not matter when a student declared", st.session_state['Majors List'], placeholder = "If left blank, will include all data", key = "_majorsToInclude", on_change=store_value, args=["majorsToInclude"])
        load_value("restrictByKnownGraduates")
        st.checkbox("Restrict data to only include students who are known to have graduated (data starts in 2021)", key = "_restrictByKnownGraduates", on_change=store_value, args=["restrictByKnownGraduates"])

    st.divider()
    with st.expander("Show fine tuning options for the scatter plots"):
        st.divider()
        load_value("scatterMinimumSize")
        st.number_input(label = "Minimum engagement size in all scatter Plots (based on number of engagements)", min_value=1, key = "_scatterMinimumSize", on_change=store_value, args=['scatterMinimumSize'],  format = "%d")
        load_value("scatterMaxPercentile")
        st.number_input(label = "Restrict maximum percentile for the color bar in scatter plots -- useful if one or two outliers are disrupting the full picture. Recommended to keep this number between 95-100.", min_value=1.0, max_value=100.0, format = "%f", key = "_scatterMaxPercentile", on_change=store_value, args=['scatterMaxPercentile'])
        load_value("numbervspercent")
        st.checkbox("Use total number for scatter plots (where appropriate) instead of percentage", key = "_numbervspercent", on_change=store_value, args=["numbervspercent"])
    st.divider()
    with st.expander("Show fine tuning options for the sankey diagram"):
        st.divider()
        load_value("sankeyColumns")
        st.number_input(label = "Number of columns in the Sankey Diagram", min_value=2, format = "%d", key = "_sankeyColumns", on_change=store_value, args=['sankeyColumns'])
        load_value("sankeyLineWeight")
        st.number_input(label = "Minimum line weight in the Sankey Diagram (number of engagements per line)", min_value=0, format = "%d", key = "_sankeyLineWeight", on_change=store_value, args=['sankeyLineWeight'])
        load_value("neverEngagedBefore")
        st.checkbox("Show Never Engaged Before in the Sankey Diagrams", key = "_neverEngagedBefore", on_change=store_value, args=['neverEngagedBefore'])
        load_value("neverEngagedAgain")
        st.checkbox("Show Never Engaged Again in the Sankey Diagrams", key = "_neverEngagedAgain", on_change=store_value, args=["neverEngagedAgain"])
    st.divider()
    with st.expander("Other options, including fine tuning options for multiple graph types and download features"):
        st.divider()
        load_value('aggregatedScatter')
        st.radio("Should the the x-axis for all scatter plots and the *When Students Engaged With Hiatt* graph be aggregated?", options = ["Do not aggregate (default)", "Aggregate by class year (Freshman Fall, Freshman Spring, ...)", "Aggregate by class year and semester (Freshman Year, Sophomore Year, ...)"], key = "_aggregatedScatter", on_change=store_value, args=["aggregatedScatter"])
        load_value('lineGraphEngagementOptions')
        st.multiselect("What engagements should be displayed on the 'When Students Engaged with Hiatt' line graph?", ['Any Engagement'] + st.session_state['RankedEngagementList'], key="_lineGraphEngagementOptions", on_change=store_value, args=['lineGraphEngagementOptions'])
        load_value('steppedColorbars')
        st.checkbox("Should colorbars be stepped (rather than a continuous color gradient) for all scatter plots and heat maps?", key="_steppedColorbars", on_change=store_value, args=['steppedColorbars'])
        load_value("numberOfColorDivisions")
        st.number_input(label = "If the colorbars are stepped, how many steps should there be?", min_value=1, format = "%d", key="_numberOfColorDivisions", on_change=store_value, args=['numberOfColorDivisions'])
        load_value("downloadFile")
        if st.checkbox("Enable the option to download the data file created by this code (useful for further exploration of data)", key = "_downloadFile", on_change=store_value, args = ['downloadFile']):
            graduationYearToRestrictBy = st.session_state['graduationYearToRestrictBy']
            if(graduationYearToRestrictBy != 'Do not restrict by graduation year'):
                #df = restrictByCohort(df, int(graduationYearToRestrictBy))
                subtitle = "Graduating class of " + graduationYearToRestrictBy
            else:
                subtitle = "Data not restricted by graduating class"
            majorsToInclude = set(st.session_state['majorsToInclude'])
            if len(majorsToInclude) > 0:
                subtitle += ", only including students with majors in the following categories: " + ', '.join(majorsToInclude)
            else:
                if subtitle == "Data not restricted by graduating class":
                    subtitle += " or students major"
                else:
                    subtitle += ", data not restricted by students major"

            
            if st.session_state['restrictByKnownGraduates']:
                if subtitle != "Data not restricted by graduating class or students major":
                    subtitle += "<br>Data also restricted to only include students known to have graduated"
                else:
                    subtitle = "Data restricted to only include students known to have graduated, but not by students major or graduating class"
                
            st.write("For the Export File, " + subtitle)
            st.download_button(label='Download Cleaned Data',
                                        data=downloadExcelFile(st.session_state['df']),
                                        file_name= 'OUTPUT_DATA.xlsx')
    st.divider()    

    if st.button("Generate!") and uploaded_file is not None and len(st.session_state['graphTypes']) != 0:
        st.session_state['currentGraphs'] = []
        st.session_state['graphsGenerated'] = True
        graduationYearToRestrictBy = st.session_state['graduationYearToRestrictBy']
        graphTypes = st.session_state['graphTypes']

        def steppedColorscale(colorsList):
                from plotly.express.colors import sample_colorscale
                from sklearn.preprocessing import minmax_scale
                colorsRGB = [colors.to_rgb(c) for c in colorsList]
                #for c in colorsList:
                #    colorsRGB.append(colorsList.to_rgb(c))
            
                colors_range = range(0, st.session_state['numberOfColorDivisions'])
                discrete_colors = sample_colorscale(colorsRGB, minmax_scale(colors_range))

                steppedColorscale = []

                for i in range (0, st.session_state['numberOfColorDivisions']):
                    for notUsed in range (0, 100):
                        steppedColorscale.append(discrete_colors[i])
                return steppedColorscale



        def createHeatMap(countTotal):
            df = originalDf.copy()
            mapping = originalMapping.copy()
            total = originalTotal.copy()
            success = originalSuccess.copy()
            percent = originalPercent.copy()
            engagementList = originalEngagementList.copy()

            ###This is unique for the heatmap
            #df = df.drop(df[df['Engagement Type'] == 'WOW'].index)
            
            
            df = df.sort_values(['Unique ID', 'Events Start Date Date'], ascending=[True, True])
            df.reset_index(drop=True, inplace=True)
            #df.to_excel('OutputSource.xlsx', sheet_name="source")
            def heatMapCountingTotalEngagements(df, total, success):
                for ind in df.index:
                    tempInd = ind + 1
                    total.loc[df['Engagement Type'][ind]] += 1
                    alreadyCounted = []
                    while (tempInd + 1< len(df) and df['Unique ID'][tempInd] == df['Unique ID'][tempInd + 1]):
                            if not df['Engagement Type'][tempInd] in alreadyCounted:
                                success.loc[df['Engagement Type'][ind], df['Engagement Type'][tempInd]] += 1
                                alreadyCounted.append(df['Engagement Type'][tempInd])
                            tempInd +=1
            def heatMapCountingUniqueEngagements(df, total, success):
                countedPerson = []
                for ind in df.index:
                    if (ind + 1< len(df) and (df['Unique ID'][ind] != df['Unique ID'][ind + 1])):
                        if not df['Engagement Type'][ind] in countedPerson:
                            total.loc[df['Engagement Type'][ind]] += 1
                        countedPerson = []
                        #print(df['Unique ID'][ind], " ", df['Unique ID'][ind + 1])
                        continue
                    tempInd = ind + 1 
                    if not df['Engagement Type'][ind] in countedPerson:
                        countedPerson.append(df['Engagement Type'][ind])
                        #if 'Employer Activity' in df['Engagement Type'][ind]:
                            #print(ind, " ", tempInd, " ", df['Engagement Type'][tempInd])
                        total.loc[df['Engagement Type'][ind]] += 1
                        alreadyCounted = []
                        #print(ind, tempInd)
                        while (tempInd < len(df) and tempInd - 1 > -1 and (df['Unique ID'][tempInd] == df['Unique ID'][tempInd - 1])):
                            if not df['Engagement Type'][tempInd] in alreadyCounted:
                                success.loc[df['Engagement Type'][ind], df['Engagement Type'][tempInd]] += 1
                                alreadyCounted.append(df['Engagement Type'][tempInd])
                                #print(df['Engagement Type'][tempInd])
                                #if 'Employer Activity' in df['Engagement Type'][ind]:
                                #    print(ind, " ", tempInd, " ", df['Engagement Type'][tempInd])
                                #    print(df['Unique ID'][tempInd], " ", df['Unique ID'][tempInd + 1])
                            tempInd +=1
                    #if (ind + 1< len(df) and df['Unique ID'][ind] != df['Unique ID'][ind + 1]):
                        

            #countTotal = True

            if countTotal:
                heatMapCountingTotalEngagements(df, total, success)
            else:
                heatMapCountingUniqueEngagements(df, total, success)


            a = np.array(success.values)
            b = np.array(total.values)

            totalCount = [str(f'{int(item):,}') for item in total[total.columns[0]]]
            percent = pd.DataFrame(np.divide(a, b, out=np.zeros_like(a), where=b!=0), index = total.index.values + " (" + totalCount + ")", columns=engagementList)
            percent = percent.astype(float).round(decimals=4)

            name = "HM - "
            longName = "Engagement Relationships -- "
            if countTotal:
                name += "Total"
                longName += "Total"
            else:
                name += "Unique"
                longName += "Unique"

            if graduationYearToRestrictBy != 'Do not restrict by graduation year':
                name += " - " + graduationYearToRestrictBy
                longName += " -- Class of " + graduationYearToRestrictBy
                

            name += ".xlsx"

            percent.rename_axis('Heat Map', inplace = True)


            #percent.sort_values(by=percent.index.name, inplace = True)
            percent.columns.name = "Second Events"
            #percent.sort_values(by=percent.columns.name, axis=1, inplace = True)


            (max_row, max_col) = percent.shape
            # Add a percent number format.

            

            hoverText = percent.copy().astype(str)
            percentStrings = percent.copy().astype(str)
            sortedEngagementList = (list(engagementList))
            #print(sortedEngagementList)
            for col in range(0, max_col):
                #worksheet.conditional_format(1, col+1, max_row, col+1, {"type": "3_color_scale"})
                for row in range(0, max_row):
                    rowEvent = percent.index[row]
                    colEvent = sortedEngagementList[col]
                    cell = format(percent[colEvent][rowEvent], ".0%")
                    event1 = sortedEngagementList[row].strip()
                    event2 = colEvent.strip()
                    if countTotal:
                        string = cell + " of the time " + event1 + " led to " + event2 + " (at any point)."
                    else:
                        string = cell + " of people who went to " + event1 + ", later went to " +event2 + " (at any point)."
                    #worksheet.write_comment(row + 1, col + 1, string)



                    percentStrings.loc[rowEvent, colEvent] = cell
                    if countTotal:
                        hoverText.loc[rowEvent, colEvent] = cell + " of the time " + event1 + " led to " + event2 + " (at any point)."
                    else:
                        hoverText.loc[rowEvent, colEvent] = cell + " of people who went to " + event1 + ", later went to " +event2 + " (at any point)."



            #worksheet.freeze_panes(1, 1)
            #writer.close()




            percent.rename_axis('First Events', inplace = True)
            normalized_df=(percent-percent.min())/(percent.max()-percent.min())

            #fig = px.imshow(percent, text_auto=True, aspect="auto")
            colorscale = ["red","lemonchiffon", "green"]
            if st.session_state['steppedColorbars']:
                colorscale = steppedColorscale(colorscale)
            #colorscale = "inferno"
            fig = go.Figure(data=go.Heatmap(x = percent.columns,
                                            y = percent.index,
                                            z = normalized_df,
                                            colorscale = colorscale,
                                            hoverinfo='none',
                                            texttemplate="%{text}", 
                                            text = percentStrings,
                                            #hovertext=hoverText,
                                            ))

            
            fig.update_xaxes(title_text="Second Event")
            fig.update_yaxes(title_text="First Event")
            if countTotal:
                fig.update_layout(title = longName + "<br><sub>Depicts the percentage of total engagements where the first engagement was followed by the second, at any point</sub>")
            else:
                fig.update_layout(title = longName + "<br><sub>Depicts the percentage of students who went to the second engagement at any point after the first</sub>")
            fig.update_traces(showscale=False)

            fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Second Event<br><i><sub>" + subtitle + "</sub></i>")
            #fig.show()
            if countTotal:
                chartType = "Engagement Relationships (Total)"
            else:
                chartType = "Engagement Relationships (Unique)"


            xlist = []
            ylist = []
            value = []

            
            for col in percent.columns:
                for row in percent.index:
                    xlist.append(col)
                    ylist.append(row)
                    value.append(100*percent[col][row]) 
             

            fig.add_trace(go.Scatter(x=xlist, y=ylist, opacity=1, marker_size = value, hoverinfo = None, mode = "markers", name="Scatter Plot"))
            if countTotal:
                fig.update_traces(hovertemplate="%{marker.size:.0%} of the time %{x} led to %{y} (at any point).<extra></extra>", selector = ({'name':'Scatter Plot'}))
            else:  
                fig.update_traces(hovertemplate="%{marker.size:.0%} of people who went to %{x}, later went to %{y} (at any point).<extra></extra>", selector = ({'name':'Scatter Plot'}))
            #fig.add_trace(px.line(x=xlist, y =ylist))
            addChartToPage(fig)
        def createSankeyDiagram():
            df = originalDf.copy()
            mapping = originalMapping.copy()
            total = originalTotal.copy()
            success = originalSuccess.copy()
            percent = originalPercent.copy()
            engagementList = originalEngagementList.copy()
            

            df = df.sort_values(['Unique ID', 'Events Start Date Date'], ascending=[True, True])
            df.reset_index(drop=True, inplace=True)
            #df.to_excel('OutputSource.xlsx', sheet_name="source")

            maxStep = df['Unique ID'].value_counts().iat[0] + 4


            engagementList = list(engagementList)
            engagementList.insert(0, "Never Engaged Before")
            engagementList.append("Never Engaged Again")


            mapping["Never Engaged Before"] = 0
            mapping["Never Engaged Again"] = len(engagementList) - 1


            grid = np.zeros((maxStep, len(engagementList), len(engagementList)))

            stepCounter = 0
            for ind in df.index:
                currentEvent = df['Event Ranking from User'][ind]

                if st.session_state['neverEngagedBefore']:
                    if (ind-1 > 0 and df['Unique ID'][ind] != df['Unique ID'][ind - 1]):
                        ###WE MIGHT STILL WANT THIS LINE! I DON'T KNOW IF WE DO!
                        grid[0][0][currentEvent] += 1
                if (ind+1<len(df)):
                    stepCounter += 1
                    if (df['Unique ID'][ind] == df['Unique ID'][ind + 1]):
                        grid[stepCounter][currentEvent][df['Event Ranking from User'][ind + 1]] += 1
                    else:
                        
                        #if st.session_state['neverEngagedAgain']:
                        ###WE MIGHT STILL WANT THIS LINE! I DON'T KNOW IF WE DO!
                        grid[stepCounter][currentEvent][len(engagementList) - 1] += 1
                        stepCounter = 0
                
            #    tempInd = ind + 1
            #    total.loc[df['Engagement Type'][ind]] += 1
            #    alreadyCounted = []
            #    while (tempInd + 1< len(df) and df['Unique ID'][tempInd] == df['Unique ID'][tempInd + 1]):
            #            if not df['Engagement Type'][tempInd] in alreadyCounted:
            #                success.loc[df['Engagement Type'][ind], df['Engagement Type'][tempInd]] += 1
            #                alreadyCounted.append(df['Engagement Type'][tempInd])
            #            tempInd +=1



            #sourceLabel = list(success.index)
            #targetLabel = []
            #for item in sourceLabel:

            #    targetLabel.append(item + " ")










            np.random.seed(1)
            TD = xr.Dataset(
                #{"product_A": (("year", "quarter"), np.random.randn(2, 4))},
                {
                    "Count": (["Step", "First Event", "Second Event"], grid),
                    #"1": (["First Event", "Second Event"], np.round(100 * np.random.rand(len(list(engagementList)), len(list(engagementList))))),
                },
                coords={
                    "First Event": list(engagementList),
                    "Second Event": list(engagementList),
                    "Step": range(maxStep),
                    #"First": np.round(100 * np.random.rand(len(list(engagementList)))),
            #        "2": 0,
            #        "3": 0,
            #        "4": 0,
            #        "5": 0,
            #        "6": 0,
            #        "7": 0,
            #        "8": 0,
            #        "9": 0,
            #        "10": 0,
                },
            )

            new = TD.to_dataframe()
            #print(new)
            #for series_name in new.items():
            #    new[series_name] = new[series_name].astype('int64')



            source = []
            target = []
            value = []
            nodeTotals = {}
            minimumLineWeight = st.session_state['sankeyLineWeight'] - 1 ##This is restricting so only larger lines are displayed
            maximumAllowedStep = st.session_state['sankeyColumns'] ##This is restricting so only the first few steps are displayed
            for ind in new.index:
                for series_name, series in new.items():
                    if (series[ind] > minimumLineWeight and ind[0] < maximumAllowedStep):
                        if st.session_state['neverEngagedAgain'] or ind[2] != "Never Engaged Again":
                            source.append(ind[1] + " " + str(ind[0]))
                            target.append(ind[2] + " " + str(ind[0] + 1))
                            value.append(int(series[ind]))
                    if (ind[0] <= maximumAllowedStep):
                        e = ind[1] + " " + str(ind[0])
                        if e in nodeTotals:
                            nodeTotals[e] += int(series[ind])
                        else:
                            nodeTotals[e] = int(series[ind])


            

            shortenedLists = list(set(source + target))
            dictionaryConverter = dict(zip(shortenedLists, range(len(shortenedLists))))

            sourceConverted = [dictionaryConverter[key] for key in source]
            targetConverted = [dictionaryConverter[key] for key in target]
            
            colorLinkList = [x[:x.rfind(" ")] for x in source]




            #print(shortenedLists)
            ####
            #sourceDict = dict(zip(shortSource, range(len(source))))
            #sourceConverted = [sourceDict[key] for key in source]
            #print(source)
            #print(sourceConverted)


            #shortTarget = list(set(target))
            #targetDict = dict(zip(shortTarget, range(len(shortSource), len(source) + len(target))))
            #targetConverted = [targetDict[key] for key in target]
            #print(target)
            #print(targetConverted)
            ####

            locationList = []
            eventNameList = []
            for event in shortenedLists:
                locationList.append((float(event.split()[-1])))
                eventNameList.append(event[:event.rfind(" ")])
            while (min(locationList) != 0):
                locationList = [loc - 1 for loc in locationList]
            #print(locationList)
            locationList = [x/max(locationList) if x != 0 else 1e-9 for x in locationList]
            locationList = [x if x != 1 else 1-1e-9 for x in locationList]

            import plotly.graph_objects as go
            colorSet = ["firebrick", "orangered", "forestgreen",  "blueviolet", "grey", "darkcyan", "cornflowerblue",  "mediumvioletred", "turquoise", "saddlebrown"]

            colorMapping = {}
            colorTracker = 0
            for event in set(eventNameList):
                colorMapping[event] = colorSet[colorTracker]
                colorTracker += 1
                if colorTracker == len(colorSet):
                    colorTracker = 0
            #print(colorMapping)

            #from matplotlib import colors
            colorsList = [colorMapping[x] for x in eventNameList]
            colorLinkList = ["rgba" + str(colors.to_rgba(colorMapping[x], alpha = 0.3)) for x in colorLinkList]
            

            nodeValues = [nodeTotals[item] for item in shortenedLists]

            linkPercentage = [value[index] / nodeValues[sourceConverted[index]] for index in range(len(sourceConverted))]

            fig = go.Figure(go.Sankey(
                arrangement = "snap",
                node = dict(
                pad = 15,       
                thickness = 20,
                line = dict(color = "black", width = 0.5),
                label = shortenedLists, 
                customdata = nodeValues,
                x = locationList,
                y = [0.1]*len(locationList),
                color = colorsList,
                hovertemplate='%{customdata:,} students went to %{label}<extra></extra>',
                ),
                link = dict(
                source = sourceConverted, # indices correspond to labels, eg A1, A2, A1, B1, ...
                target = targetConverted,
                value = value,
                color = colorLinkList,
                customdata = linkPercentage,
                hovertemplate='%{customdata:.1%} of the students who went to %{source.label}<br>went next to %{target.label} (%{value:,} students)<extra></extra>',
                )))

            #fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
            #fig.update_yaxes(automargin=True)
            #fig.update_xaxes(automargin=True)
            fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=100),
                #paper_bgcolor="LightSteelBlue",
            )

            fig.update_layout(
                hoverlabel=dict(
                    bgcolor="black",
                    font_color = "white",
                    font_size = 14,
                )
            )

            fig.update_layout(
                title_text="Sequential Pathways of Student Engagements<br><sup>Shows the order of events that students engaged in, and the pathways in between to represent students transition</sup>",
                #font_family="Times New Roman",
                font_color="black",
                font_size=14,
                #title_font_family="Times New Roman",
                #title_font_color="red",
            )

            fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Semester<br><i><sub>" + subtitle + "</sub></i>")
            fig.add_annotation(
                x=0.5, 
                y=-0.1, 
                xref='paper', 
                yref='paper',
                text="<br><i><sub>" + subtitle + "</sub></i>",
                showarrow=False,
            )
            addChartToPage(fig)

            reshapedDataFrame = new.loc[0, :, :]
            #print(type(reshapedDataFrame))
            #print(type(new))
            #print(reshapedDataFrame)


            for step in set(new.index.get_level_values('Step')):
                #print("here is the step", step)
                #print(new.loc[step, :, :])
                #reshapedDataFrame["Count"] = reshapedDataFrame["Count"] + new.loc[step, :, :]
                reshapedDataFrame = reshapedDataFrame.join(new.loc[step, :, :], lsuffix='', rsuffix=' ' + str(step))
                #reshapedDataFrame = pd.concat(reshapedDataFrame, new.loc[step, :, :])
            reshapedDataFrame = reshapedDataFrame.drop('Count', axis=1)
            #print(reshapedDataFrame)
            #reshapedDataFrame.to_excel('SankeyData.xlsx', sheet_name="Source Data")
            #print(shortenedLists)  
        def createLineGraph():
            df = originalDf.copy()
            mapping = originalMapping.copy()
            engagementList = originalEngagementList.copy()



            semesterValueMappings = {}

            df = df.drop(df[df['Semester'].str.contains('Summer')].index)
            df = df.drop(df[df['Semester'].str.contains('Winter')].index)
            
            df['Unique ID'] = df.groupby(['Full Name','Email']).ngroup()

            ##THIS IS STILL USEFUL! THIS APPLIES A MANUAL SORTING BASED ON sort_engagement
            ##df['Event Number'] = df.apply(sort_engagement, axis = 1)
            ##THIS IS STILL USEFUL! THIS SORTS IF I HAVEN'T MANUALLY DONE IT
            df['Event Number'] = df.groupby(['Engagement Type']).ngroup()+1

            def graphWithDates(df):
                df = df.drop_duplicates(subset=['Events Start Date Date', 'Unique ID'])
                df = df.pivot(index='Events Start Date Date', columns='Unique ID', values='Ranked Events')
                return df

            def graphWithSemesters(df):
                df['Semester Number'] = df.apply(lambda x: create_semester_value(x.Semester, semesterValueMappings), axis=1)
                global secondDataframe 
                secondDataframe = df.value_counts(['Semester Number', 'Ranked Events']).reset_index().rename(columns={0:'count'})
                df = df.drop_duplicates(subset=['Semester Number', 'Unique ID'])
                #print(len(df.index))
                df = df.pivot(index='Semester Number', columns='Unique ID', values='Ranked Events')
                return df




            df = graphWithSemesters(df)

            #print("HERE'S THE SECOND ONE")
            #print(secondDataframe)

            #print("Pivot Table:")
            #df = df.astype(str)
            #print(df.dtypes)
            #print(df)


            dfGraph = df.interpolate(method = 'linear')
            ax = dfGraph.plot.line(alpha = 100/len(df.columns), ms=1, color='black')
            #print(type(ax))

            items = list(mapping.keys())
            items[:] = [item+" (" + str(events[item]) + ")" for item in items]

            firstDate = df.apply(pd.Series.first_valid_index)
            pd.concat([pd.Series([1]), firstDate])
            counter = 0
            firstEvent = []
            #print(firstDate)
            #print(len(df.columns))
            #print(firstDate[3])
            while counter < len(df.columns)-1:
                #print(counter)
                #print(firstDate[counter])
                firstEvent.append(df.at[firstDate[counter], counter])
                counter += 1
            firstEvent.insert(0, 1)


            #print("HERE IT IS!!")
            #print(firstDate)
            #print(firstEvent)
            #ax.scatter(firstDate, firstEvent, color='limegreen', alpha = 35/len(df.columns), s=25)

            dataframe = pd.DataFrame(list(zip(firstDate, firstEvent)), columns =['Date', 'Event'])
            #dataframe = pd.DataFrame(lst, columns= ["Date", "Event"])
            #print(dataframe)
            #print(dataframe.duplicated(keep=False).value_counts())

            dataframe = dataframe.value_counts(['Date', 'Event']).reset_index().rename(columns={0:'count'})
            #print(dataframe)
            #print(dataframe[['Date', 'Event']].apply(pd.Series.value_counts()))
            #df[['a', 'b']].apply(pd.Series.value_counts)
            lastDate = df.apply(pd.Series.last_valid_index)
            pd.concat([pd.Series([1]), lastDate])
            lastCounter = 0
            lastEvent = []
            #print(lastDate)
            #print(len(df.columns))
            while lastCounter < len(df.columns)-1:
                #print(lastCounter)
                #print(lastDate[lastCounter])
                lastEvent.append(df.at[lastDate[lastCounter], lastCounter])
                lastCounter += 1
            lastEvent.insert(0, 1)


            #ax.scatter(lastDate, lastEvent, color='red', alpha = 25/len(df.columns), s=25)




            #plt.show()

            #df.plot.scatter(x="Events Start Date Date", y="Event Type Name", alpha = 0.1)
            #plt.show()

            #df.to_excel('2023Seniors.xlsx', sheet_name="Cleaned Data", index=False)

            #fig = Figure
            
            #print(dfGraph)
            #fig1 = fig.add_subplot(111)
            #print(firstDatePLOT)
            #fig1.scatter(firstDatePLOT, firstEventPLOT)
            #fig = plt.figure()
            YlGn = mpl.colormaps['Blues']
            Reds = mpl.colormaps['Reds']
            maxCount = dataframe['count'].max()
            secondMaxCount = secondDataframe['count'].max()
            secondTheScatter = plt.scatter(secondDataframe['Semester Number'], secondDataframe['Ranked Events'], c = secondDataframe['count'], cmap = Reds, alpha = 1, s = secondDataframe['count']/secondMaxCount * 200)
            theScatter = plt.scatter(dataframe['Date'], dataframe['Event'], c = dataframe['count'], cmap = YlGn, alpha = 1, s = dataframe['count']/secondMaxCount * 200)
            #plt.plot(dfGraph, alpha = 100/len(df.columns), ms=1, color='black')
            #secondLegend1 = fig1.legend(*secondTheScatter.legend_elements(num=10), title="Color Key", bbox_to_anchor=(1.21, 1), loc='upper left', draggable = True)
            #fig1.add_artist(secondLegend1)
            plt.colorbar(cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=dataframe['count'].min(), vmax=maxCount), cmap=YlGn), ax=ax)
            plt.colorbar(cm.ScalarMappable(norm = mpl.colors.Normalize(vmin=secondDataframe['count'].min(), vmax=secondMaxCount), cmap=Reds), ax=ax)



            ax.set_yticks(list(mapping.values()), items)
            ax.set_xticks(list(semesterValueMappings.keys()), list(semesterValueMappings.values()))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=75, ha='right')
            ax.set(xlabel="Semester", ylabel="Event Type")
            ax.get_legend().remove()
            if graduationYearToRestrictBy != "Do not restrict by graduation year":
                plt.title("The Graduating Class of " + str(graduationYearToRestrictBy) + "'s Engagement Graph") # type: ignore
            else:
                plt.title("Engagement Graph")
            plt.subplots_adjust(left = 0.285, bottom = 0.28, right = 0.99, top = 0.92)


            st.pyplot(plt)
        def createScatterPlot():
            aa = datetime.datetime.now()
            df = originalDf.copy()
            mapping = originalMapping.copy()
            engagementList = originalEngagementList.copy()

            print("Length of the Dataframe: ", len(df.index))
            df.dropna(subset=['Unique ID'], inplace=True)
            print("Length of the Dataframe: ", len(df.index))

            semesterValueMappings = {}
            df['Semester Number'] = df.apply(lambda x: create_semester_value(x.Semester, semesterValueMappings), axis=1)
            aggregatedSemesterValueMappings = {16: "Senior Spring", 15: "Senior Winter", 14: "Senior Fall", 13: "Senior Summer", 12: "Junior Spring", 11: "Junior Winter", 10: "Junior Fall", 9: "Junior Summer", 8: "Sophomore Spring", 7: "Sophomore Winter", 6: "Sophomore Fall", 5: "Sophomore Summer", 4: "Freshman Spring", 3: "Freshman Winter", 2: "Freshman Fall", 1: "Freshman Summer"}
            df['Aggregated Semester Number'] = df.apply(lambda x: create_aggregated_semester_value(x.Semester, x.Graduation_Semester), axis=1)
            df['Double Aggregated Semester Number'] = (np.ceil(df['Aggregated Semester Number'] / 4)).astype(int)
            doubleAggregatedSemesterValueMappings = {4: "Senior Year", 3: "Junior Year", 2:"Sophomore Year", 1:"Freshman Year"}
            

            def aggregated_semester_name(row):
                num = row['Aggregated Semester Number']
                if num in aggregatedSemesterValueMappings:
                    return aggregatedSemesterValueMappings[num]
                else:
                    return "Do Not Include"
                
            def double_aggregated_semester_name(row):
                num = row['Double Aggregated Semester Number']
                if num in doubleAggregatedSemesterValueMappings:
                    return doubleAggregatedSemesterValueMappings[num]
                else:
                    return "Do Not Include"
            
            df['Aggregated Semester Name'] = df.apply(aggregated_semester_name, axis = 1)
            df['Double Aggregated Semester Name'] = df.apply(double_aggregated_semester_name, axis = 1)
            #df.to_excel("FileOutpit.xlsx")
            global secondDataframe 

            

            if st.session_state['aggregatedScatter'] == "Do not aggregate (default)":
                semesterNumberedColumn = 'Semester Number'
                semesterMapping = semesterValueMappings
            elif st.session_state['aggregatedScatter'] == "Aggregate by class year (Freshman Fall, Freshman Spring, ...)":
                semesterNumberedColumn = 'Aggregated Semester Number'
                semesterMapping = aggregatedSemesterValueMappings
            elif st.session_state['aggregatedScatter'] == "Aggregate by class year and semester (Freshman Year, Sophomore Year, ...)":
                semesterNumberedColumn = 'Double Aggregated Semester Number'
                semesterMapping = doubleAggregatedSemesterValueMappings

            averages = pd.DataFrame(index = range(df[semesterNumberedColumn].min(), df[semesterNumberedColumn].max()+1), columns = engagementList, data = [])
            combined = averages.copy()
            
            for col in averages.columns:
                for row in averages.index:
                    averages.loc[row, col] = []
                    combined.loc[row, col] = []
            #averages.loc["Appointment", "Hiatt Funding"].append(1)

            #print(averages)
            df = df.sort_values(['Unique ID', 'Events Start Date Date'], ascending=[True, True])
            df.reset_index(drop=True, inplace=True)

            #print(df)
            #df.to_excel('OutputSourceFromNEW.xlsx', sheet_name="source")
            #print(df["Semester Number"])
            firstEngagements = pd.DataFrame(index = range(df[semesterNumberedColumn].min(), df[semesterNumberedColumn].max()+1), columns = engagementList, data = 0)
            oneAndDone = firstEngagements.copy()


            numberOfUniqueEngagements = pd.DataFrame(index = range(df[semesterNumberedColumn].min(), df[semesterNumberedColumn].max()+1), columns = engagementList, data = {})

            for col in numberOfUniqueEngagements.columns:
                for row in numberOfUniqueEngagements.index:
                    numberOfUniqueEngagements.loc[row, col] = set()
            

            bb = datetime.datetime.now()
            firstIndexMapping = {}
            lastIndexMapping = {}

            for ind in df.index:
                #print(ind)
                #print(df["Unique ID"][ind])
                ID = df['Unique ID'][ind]
                if ID not in firstIndexMapping:
                    firstIndexMapping[ID] = ind
                if ID not in lastIndexMapping:
                    tempInd = ind
                    while tempInd + 1 in df.index and ID == df['Unique ID'][tempInd + 1]:
                        tempInd += 1
                    lastIndexMapping[ID] = tempInd
                #lastIndex = df["Unique ID"].where(df["Unique ID"]==df['Unique ID'][ind]).last_valid_index()
                #firstIndex = df["Unique ID"].where(df["Unique ID"]==df['Unique ID'][ind]).first_valid_index()
                #print(ind, " ", lastIndexMapping[ID], " ", firstIndexMapping[ID])
                semesterNumber = df[semesterNumberedColumn][ind]
                engagementType = df['Engagement Type'][ind]
                #print(semesterNumber)
                averages.loc[semesterNumber, engagementType].append(lastIndexMapping[ID]-ind)

                #print(ID not in numberOfUniqueEngagements.loc[semesterNumber, engagementType])
                

                numberOfUniqueEngagements.loc[semesterNumber, engagementType].add(int(ID))
                
                if firstIndexMapping[ID] == ind:
                    firstEngagements.loc[semesterNumber, engagementType] += 1
                    combined.loc[semesterNumber, engagementType].append(lastIndexMapping[ID]-ind)
                if firstIndexMapping[ID] == ind and lastIndexMapping[ID] ==ind:
                    oneAndDone.loc[semesterNumber, engagementType] += 1
            cc = datetime.datetime.now()  

            
            
            #averages.to_excel('Averages.xlsx')
            #combined.to_excel('Combined.xlsx')

            
            scatterDataFrame = pd.DataFrame(columns=["Engagement Type", "Semester", "Average", "Number of Engagements", "First Engagements", "Percent First Engagement", "Unique Number of Engagements", "Unique Percent First Engagement", "Percentage of Unique Engagements", "One and Done", "Percentage of One and Done"])  
            
            for row in averages.index:
                skip = True
                for col in averages.columns:
                    if len(averages.loc[row, col]) >= st.session_state['scatterMinimumSize']:
                        skip = False
                        break
                if skip == False:
                    for col in averages.columns:
                        if st.session_state['aggregatedScatter'] == "Do not aggregate (default)":
                            if row not in semesterValueMappings:
                                create_semester_value_from_number(row, semesterValueMappings)
                        elif st.session_state['aggregatedScatter'] == "Aggregate by class year (Freshman Fall, Freshman Spring, ...)":
                            if row not in aggregatedSemesterValueMappings:
                                continue
                        elif st.session_state['aggregatedScatter'] == "Aggregate by class year and semester (Freshman Year, Sophomore Year, ...)":
                            if row not in doubleAggregatedSemesterValueMappings:
                                continue
                        
                        firstEngageData = firstEngagements.loc[row][col]
                        oneAndDoneData = oneAndDone.loc[row][col]

                        avgUniqueList = numberOfUniqueEngagements.loc[row, col]
                        if len(avgUniqueList) >= st.session_state['scatterMinimumSize']:
                            uniqueLength = len(avgUniqueList)
                            uniquePercentage =  firstEngageData/uniqueLength
                        else:
                            uniqueLength = 0
                            uniquePercentage = 0
                        
                        
                        avgList = averages.loc[row, col]
                        if len(avgList) >= st.session_state['scatterMinimumSize']:
                            avg = statistics.fmean(avgList)
                            length = len(avgList)
                            percent = firstEngageData/length
                            percentageOfUniqueVsTotal = uniqueLength/length
                            percentOfOneAndDone = oneAndDoneData/uniqueLength
                        else:
                            avg = 0
                            length = 0
                            percent = 0
                            percentageOfUniqueVsTotal = 0
                            percentOfOneAndDone = 0
                        
                        #print(length, " : ", uniqueLength)
                        scatterDataFrame.loc[len(scatterDataFrame.index)] = [col, semesterMapping[row], avg, length, firstEngageData, percent, uniqueLength, uniquePercentage, percentageOfUniqueVsTotal, oneAndDoneData, percentOfOneAndDone]
            #print(scatterDataFrame)
            #averages = pd.DataFrame(averages.to_records())
            dd = datetime.datetime.now()
            

            combinedScatterDataFrame = pd.DataFrame(columns=["Engagement Type", "Semester", "Average", "Number of First Engagements", "First Engagements", "Percent First Engagement", "One and Done", "Percentage of One and Done"])  
            #THIS COULD POSSIBLY GET CONDENSED IN THE FUTURE TO BE MORE EFFICIENT, BUT NOT CONCERNED WITH IT RIGHT NOW
            for row in combined.index:
                skip = True
                for col in combined.columns:
                    if len(combined.loc[row, col]) >= st.session_state['scatterMinimumSize']:
                        skip = False
                        break
                if skip == False:
                    for col in combined.columns:
                        if st.session_state['aggregatedScatter'] == "Do not aggregate (default)":
                            if row not in semesterValueMappings:
                                create_semester_value_from_number(row, semesterValueMappings)
                        elif st.session_state['aggregatedScatter'] == "Aggregate by class year (Freshman Fall, Freshman Spring, ...)":
                            if row not in aggregatedSemesterValueMappings:
                                continue
                        elif st.session_state['aggregatedScatter'] == "Aggregate by class year and semester (Freshman Year, Sophomore Year, ...)":
                            if row not in doubleAggregatedSemesterValueMappings:
                                continue

                        avgList = combined.loc[row, col]
                        oneAndDoneData = oneAndDone.loc[row][col]

                        if len(avgList) >= st.session_state['scatterMinimumSize']:
                            avg = statistics.fmean(avgList)
                            length = len(avgList)
                            percentOfOneAndDone = oneAndDoneData/length
                            percentFirstEngagement = firstEngageData/length
                        else:
                            avg = 0
                            length = 0
                            percentOfOneAndDone = 0
                            percentFirstEngagement = 0
                        firstEngageData = firstEngagements.loc[row][col]
                        
                        combinedScatterDataFrame.loc[len(combinedScatterDataFrame.index)] = [col, semesterMapping[row], avg, length, firstEngageData, percentFirstEngagement, oneAndDoneData, percentOfOneAndDone]
                        
            #print(combinedScatterDataFrame)

            #print(averages)
            #listofthings = averages.columns 
            #print(listofthings)

            #print(scatterDataFrame)
            #scatterDataFrame.sort_values(['Semester Sorting', 'Engagement Type'], ascending=[True, True], inplace=True)
            #print(scatterDataFrame)
            
            

            


            colorscale = ["red","yellow", "green"]
            if st.session_state['steppedColorbars']:
                colorscale = steppedColorscale(colorscale)
            if "Return Rates Based on All Engagements" in graphTypes:
                maximum = np.percentile(scatterDataFrame['Average'], st.session_state['scatterMaxPercentile'])
                minimum = min([x if x!=0 else max(scatterDataFrame['Average']) for x in scatterDataFrame['Average']])
                
                fig = px.scatter(scatterDataFrame, x="Semester", y="Engagement Type", color = 'Average', range_color = (minimum, maximum), size="Number of Engagements", color_continuous_scale= colorscale, 
                                    title = "Return Rates Based on All Engagements<br><sup>Shows how students engaged over time</sup><br><i><sub>Color: the average number of engagements attended after</sub><br><sup> Size: the number of engagements</sup></i>", 
                                    labels={"Average": ""}, hover_data={"Average": False, "Average Number of Events Attended Afterwards": (':.1f', scatterDataFrame['Average'])})

                fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Semester<br><i><sub>" + subtitle + "</sub></i>")
                fig.update_traces(marker=dict(
                              line=dict(width=0.25,
                                        color='Black')),
                  selector=dict(mode='markers'))

                fig.update_traces(hovertemplate="There were %{marker.size:,} %{y} engagements in %{x},<br>with an average number of %{customdata[1]:.1f} subsequent engagements<extra></extra>")
                #fig.update_traces(hovertemplate='%{x}, %{y}:<br>%{marker.size:,} total engagements<br>Average number of subsequent engagements: %{customdata[1]:.1f}<extra></extra>')
                addChartToPage(fig)

            if "Return Rates Based on First Engagements" in graphTypes:
                maximum = np.percentile(combinedScatterDataFrame['Average'], st.session_state['scatterMaxPercentile'])
                minimum = min([x if x!=0 else max(scatterDataFrame['Average']) for x in scatterDataFrame['Average']])
                fig = px.scatter(combinedScatterDataFrame, x="Semester", y="Engagement Type", color = "Average", range_color = (minimum, maximum), size="Number of First Engagements", color_continuous_scale=colorscale, 
                                    title = "Return Rates Based on First Engagements<br><sup>Shows how students engaged after their first engagement point</sup><br><i><sub>Color: the average number of engagements attended after</sub><br><sup> Size: the number of first engagements</sup></i>", labels={"Average": ""}, hover_data={"Average": False, "Average Number of Events Attended Afterwards": (':.1f', combinedScatterDataFrame['Average'])})
                #fig.update_coloraxes(showscale=False)
                fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Semester<br><i><sub>" + subtitle + "</sub></i>")
                fig.update_traces(marker=dict(
                              line=dict(width=0.25,color='Black')),
                  selector=dict(mode='markers'))

                fig.update_traces(hovertemplate="There were %{marker.size:,} %{y} first engagements in %{x},<br>with an average number of %{customdata[1]:.1f} subsequent engagements<extra></extra>")
                #fig.update_traces(hovertemplate='%{x}, %{y}:<br>%{marker.size:,} first engagements<br>Average number of subsequent engagements: %{customdata[1]:.1f}<extra></extra>')
                addChartToPage(fig)

            

            

            #with col2:
            colorscale2 = ["sandybrown", "gold", "green"]
            if st.session_state['steppedColorbars']:
                colorscale2 = steppedColorscale(colorscale2)

            if "First Engagements Data (Total)" in graphTypes:
                if st.session_state['numbervspercent'] == False:
                    colorData = 'Percent First Engagement'
                    titleSubstring = "Color: the percent of first engagements"
                else:
                    colorData = "First Engagements"
                    titleSubstring = "Color: the number of first engagements"
                maximum = np.percentile(scatterDataFrame[colorData], st.session_state['scatterMaxPercentile'])
                minimum = min([x if x!=0 else max(scatterDataFrame[colorData]) for x in scatterDataFrame[colorData]])
                fig = px.scatter(scatterDataFrame, x="Semester", y="Engagement Type", color = colorData, range_color=(minimum,maximum), size="Number of Engagements", color_continuous_scale=colorscale2, 
                                title = "First Engagements Data (Total)<br><sup>Data shows total and first engagements across activity and semester</sup><br><i><sub>" + titleSubstring + "</sub><br><sup> Size: the number of total engagements</sup></i>", 
                                labels={"First Engagements": "", colorData : ""}, hover_data={"First Engagements": False, "Number of First Engagements": (':d', scatterDataFrame['First Engagements']), "Percentage of First Engagements": (':.0%', scatterDataFrame['Percent First Engagement'])})
                #print(scatterDataFrame)
                #fig.update_coloraxes(showscale=False)
                fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Semester<br><i><sub>" + subtitle + "</sub></i>")
                fig.update_traces(marker=dict(
                            line=dict(width=0.25,
                                        color='Black')),
                selector=dict(mode='markers'))
                #fig.update_traces(hovertemplate='%{x}, %{y}:<br>%{marker.size:,} total engagements, %{customdata[1]:,d} first engagements<br>Percentage of first engagements %{customdata[2]:.0%}' + 
                #                    '<br>Of the %{marker.size:,} %{y} engagements in %{x}, %{customdata[2]:.0%} of them (%{customdata[1]:,d}) were first time engagements<extra></extra>')
                fig.update_traces(hovertemplate='Of the %{marker.size:,} %{y} engagements in %{x},<br>%{customdata[2]:.0%} of them (%{customdata[1]:,d}) were first time engagements<extra></extra>')
                addChartToPage(fig)


            if "First Engagements Data (Unique)" in graphTypes:
                if st.session_state['numbervspercent'] == False:
                    colorData = 'Unique Percent First Engagement'
                    titleSubstring = "Color: the percent of first engagements"
                else:
                    colorData = "First Engagements"
                    titleSubstring = "Color: the number of first engagements"
                maximum = np.percentile(scatterDataFrame[colorData], st.session_state['scatterMaxPercentile'])
                minimum = min([x if x!=0 else max(scatterDataFrame[colorData]) for x in scatterDataFrame[colorData]])
                fig = px.scatter(scatterDataFrame, x="Semester", y="Engagement Type", color = colorData, range_color=(minimum, maximum), size="Unique Number of Engagements", color_continuous_scale=colorscale2, 
                                title = "First Engagements Data (Unique)<br><sup>Data shows unique and first engagements across activity and semester</sup><br><i><sub>" + titleSubstring + "</sub><br><sup> Size: the number of unique engagements</sup></i>", 
                                labels={"First Engagements": "", colorData : ""}, hover_data={"First Engagements": False, "Number of First Engagements": (':d', scatterDataFrame['First Engagements']), "Unique Percentage of First Engagements": (':.0%', scatterDataFrame['Unique Percent First Engagement'])})
                #print(scatterDataFrame)
                #fig.update_coloraxes(showscale=False)
                fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Semester<br><i><sub>" + subtitle + "</sub></i>")
                fig.update_traces(marker=dict(
                            line=dict(width=0.25,
                                        color='Black')),
                selector=dict(mode='markers'))
                # fig.update_traces(hovertemplate='%{x}, %{y}:<br>%{marker.size:,} unique engagements, %{customdata[1]:,d} first engagements<br>Percentage of first engagements %{customdata[2]:.0%}' + 
                #                     '<br>%{marker.size:,} students went to %{y} in %{x}, %{customdata[2]:.0%} of them (%{customdata[1]:,d}) were students who were engaging for the first time<extra></extra>')
                fig.update_traces(hovertemplate='%{marker.size:,} students went to %{y} in %{x},<br>%{customdata[2]:.0%} of them (%{customdata[1]:,d}) were students who were engaging for the first time<extra></extra>')
                addChartToPage(fig)

            colorscale3 = ["gold", "darkorange", "crimson"]
            if st.session_state['steppedColorbars']:
                colorscale3 = steppedColorscale(colorscale3)
            if "Rates of Unique Engagements" in graphTypes:
                if st.session_state['numbervspercent'] == False:
                    colorData = 'Percentage of Unique Engagements'
                    titleSubstring = "Color: the percentage of unique engagements"
                else:
                    colorData = "Unique Number of Engagements"
                    titleSubstring = "Color: the number of unique engagements"
                maximum = np.percentile(scatterDataFrame[colorData], st.session_state['scatterMaxPercentile'])
                minimum = min([x if x!=0 else max(scatterDataFrame[colorData]) for x in scatterDataFrame[colorData]])
                fig = px.scatter(scatterDataFrame, x="Semester", y="Engagement Type", color = colorData, range_color=(minimum,maximum), size="Number of Engagements", color_continuous_scale=colorscale3, 
                                title = "Rates of Unique Engagements<br><sup>Data shows unique and total engagements across activity and semester</sup><br><i><sub>" + titleSubstring + "</sub><br><sup> Size: the number of total engagements</sup></i>", 
                                labels={"Number of Engagements": "", colorData : ""}, hover_data={colorData: False, "Number of Unique Engagements": (':,d', scatterDataFrame['Unique Number of Engagements']), "Number of Total Engagements": (':,d', scatterDataFrame['Number of Engagements']), "Percent of Unique Engagements": (':.0%', scatterDataFrame['Percentage of Unique Engagements'])})
                #print(scatterDataFrame)
                #fig.update_coloraxes(showscale=False)
                fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Semester<br><i><sub>" + subtitle + "</sub></i>")
                fig.update_traces(marker=dict(
                              line=dict(width=0.25,
                                        color='Black')),
                  selector=dict(mode='markers'))
                #fig.update_traces(hovertemplate='%{x}, %{y}:<br>%{customdata[1]:,d} unique engagements, %{marker.size:,} total engagements<br>Percentage of unique engagements %{customdata[3]:.0%}' + 
                #                    '<br>There were %{marker.size:,} %{y} engagements in %{x}, %{customdata[3]:.0%} of them (%{customdata[1]:,d} students) were unique engagements<extra></extra>')
                fig.update_traces(hovertemplate='There were %{marker.size:,} %{y} engagements in %{x},<br>%{customdata[3]:.0%} of them (%{customdata[1]:,d} students) were unique engagements<extra></extra>')
                addChartToPage(fig)
            
            colorscale4 = ["green", "gold", "orangered"]
            if st.session_state['steppedColorbars']:
                colorscale4 = steppedColorscale(colorscale4)
            if "Students with only 1 Engagement" in graphTypes:
                if st.session_state['numbervspercent'] == False:
                    colorData = 'Percentage of One and Done'
                    titleSubstring = "Color: the percentage of first engagements which never engaged again"
                else:
                    colorData = "One and Done"
                    titleSubstring = "Color: the number of students who engaged for the first and last time"
                maximum = np.percentile(combinedScatterDataFrame[colorData], st.session_state['scatterMaxPercentile'])
                minimum = min([x if x!=0 else max(combinedScatterDataFrame[colorData]) for x in combinedScatterDataFrame[colorData]])
                fig = px.scatter(combinedScatterDataFrame, x="Semester", y="Engagement Type", color = colorData, range_color=(minimum,maximum), size="Number of First Engagements", color_continuous_scale=colorscale4, 
                                title = "Students with only 1 Engagement<br><sup>Data shows the students who went to an event once and never again engaged with Hiatt</sup><br><i><sub>" + titleSubstring + "</sub><br><sup> Size: the number of first engagements</sup></i>", 
                                labels={"Number of First Engagements": "", colorData : ""}, hover_data={colorData: False, "Students who only engaged once": (':,d', combinedScatterDataFrame['One and Done']), "Percent of all students how many only engaged once": (':.0%', combinedScatterDataFrame['Percentage of One and Done'])})
                fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Semester<br><i><sub>" + subtitle + "</sub></i>")
                fig.update_traces(marker=dict(
                              line=dict(width=0.25,
                                        color='Black')),
                  selector=dict(mode='markers'))
                fig.update_traces(hovertemplate='There were %{marker.size:,} %{y} first engagements in %{x},<br>%{customdata[2]:.0%} of them (%{customdata[1]:,d}) were students who engaged for the first and last time<extra></extra>')
                addChartToPage(fig)

            
            #with col3:
            #    fig = px.scatter(scatterDataFrame, x="Semester", y="Engagement Type", color = colorData, size="Number of Engagements", color_continuous_scale=px.colors.sequential.Greens, 
            #                    title = "First Engagement Percentages", labels={colorData: ""}, )
                #fig.update_coloraxes(showscale=False)
                #fig.update_layout(title_x=0.5, xanchor = 'center')
            #    fig.update_layout(
            #        title={
            #        'x':0.5,
            #        'xanchor': 'center'
            #        })
            #    st.plotly_chart(fig)
            ee = datetime.datetime.now()

            #print("Scatter Plot: ", (bb-aa).total_seconds())
            #print("Scatter Plot: ", (cc-bb).total_seconds())
            #print("Scatter Plot: ", (dd-cc).total_seconds())
            #print("Scatter Plot: ", (ee-dd).total_seconds())
            #print("Total Scatter Plot: ", (ee-aa).total_seconds())
        def createGraduateGraph():
            graduateEmailsDF = st.session_state['graduateEmails']
            df = originalDf.copy()
            engagementList = originalEngagementList.copy()

            emailSet = set(df['Email'])
            graduateYears = graduateEmailsDF.columns
            
            percentagesDF = pd.DataFrame(columns = ["Class Year", "Category", "Percentages"])
            
            for year in graduateYears:
                currentSet = set(graduateEmailsDF[year])
                currentSet.discard(np.nan)
                
                majorsToInclude = set(st.session_state['majorsToInclude'])
                majMap = st.session_state['Majors Mapping']
                if len(majorsToInclude) > 0:
                    to_discard = list()
                    for gradEmail in currentSet:
                        if gradEmail not in majMap:
                            to_discard.append(gradEmail)
                        elif not set(majMap[gradEmail]).intersection(majorsToInclude):
                            to_discard.append(gradEmail)
                    for d in to_discard:
                        currentSet.discard(d)

                percent = len(emailSet & currentSet) / len(currentSet)
                percentagesDF.loc[len(percentagesDF)] = [year, "Any Engagement", percent]

                for category in engagementList:
                    df_subset = df[df['Engagement Type'] == category]
                    tempBaseSet = set(df_subset['Email'])

                    percent = len(tempBaseSet & currentSet) / len(currentSet)
                    percentagesDF.loc[len(percentagesDF)] = [year, category, percent]
                

            fig = px.line(percentagesDF, x="Class Year", y="Percentages", color = "Category", title='Percentage of Each Class Year that Engaged with Hiatt', markers=True, hover_data={"Type of Engagement": percentagesDF['Category']})
            fig.update_layout(yaxis_tickformat = '.0%', yaxis_range = [0, 1])
            fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Class Year<br><i><sub>" + subtitle + "</sub></i>")
            fig.update_traces(hovertemplate="For the %{x}, %{y:.0%} of students engaged with %{customdata[0]}<extra></extra>")
            addChartToPage(fig)
        def createGradesEngagementsGraph():
            df = originalDf.copy()
            df.dropna(subset=['Unique ID'], inplace=True)
            percentagesDF = pd.DataFrame(columns = ["Semester", "Category", "Percentages", "Total Number of Graduates", "Semester Name", "Graduating Year", "Engagement"])


            
            semesterValueMappings = {}
            df['Semester Number'] = df.apply(lambda x: create_semester_value(x.Semester, semesterValueMappings), axis=1)
            aggregatedSemesterValueMappings = {16: "Senior Spring", 15: "Senior Winter", 14: "Senior Fall", 13: "Senior Summer", 12: "Junior Spring", 11: "Junior Winter", 10: "Junior Fall", 9: "Junior Summer", 8: "Sophomore Spring", 7: "Sophomore Winter", 6: "Sophomore Fall", 5: "Sophomore Summer", 4: "Freshman Spring", 3: "Freshman Winter", 2: "Freshman Fall", 1: "Freshman Summer"}
            df['Aggregated Semester Number'] = df.apply(lambda x: create_aggregated_semester_value(x.Semester, x.Graduation_Semester), axis=1)
            df['Double Aggregated Semester Number'] = (np.ceil(df['Aggregated Semester Number'] / 4)).astype(int)
            doubleAggregatedSemesterValueMappings = {4: "Senior Year", 3: "Junior Year", 2:"Sophomore Year", 1:"Freshman Year"}
            

            def aggregated_semester_name(row):
                num = row['Aggregated Semester Number']
                if num in aggregatedSemesterValueMappings:
                    return aggregatedSemesterValueMappings[num]
                else:
                    return "Do Not Include"
                
            def double_aggregated_semester_name(row):
                num = row['Double Aggregated Semester Number']
                if num in doubleAggregatedSemesterValueMappings:
                    return doubleAggregatedSemesterValueMappings[num]
                else:
                    return "Do Not Include"
            
            df['Aggregated Semester Name'] = df.apply(aggregated_semester_name, axis = 1)
            df['Double Aggregated Semester Name'] = df.apply(double_aggregated_semester_name, axis = 1)
            #df.to_excel("FileOutpit.xlsx")


            df = df.sort_values(['Unique ID', 'Events Start Date Date'], ascending=[True, True])
            df.reset_index(drop=True, inplace=True)

            if st.session_state['aggregatedScatter'] == "Do not aggregate (default)":
                semesterNumberedColumn = 'Semester Number'
                correctMapping = semesterValueMappings
            elif st.session_state['aggregatedScatter'] == "Aggregate by class year (Freshman Fall, Freshman Spring, ...)":
                semesterNumberedColumn = 'Aggregated Semester Number'
                correctMapping = aggregatedSemesterValueMappings
            elif st.session_state['aggregatedScatter'] == "Aggregate by class year and semester (Freshman Year, Sophomore Year, ...)":
                semesterNumberedColumn = 'Double Aggregated Semester Number'
                correctMapping = doubleAggregatedSemesterValueMappings



            def agg_to_set(series):
                return set(series)
            # Create the pivot table

            # graduateYears = graduateEmailsDF.columns

            # pivot_table = df.pivot_table(index='Unique ID', columns=semesterNumberedColumn, values='Engagement Type', aggfunc=agg_to_set)
            # pivot_table = pivot_table.ffill(axis=1)
            # pivot_table = pivot_table.rename(columns=(correctMapping))
            # pivot_table = pivot_table.drop(columns=[col for col in pivot_table.columns if col not in correctMapping.values()])
            # pivot_table.dropna(axis = 0, how = "all", inplace = True)


            # for col in pivot_table.columns:
            #     percentagesDF.loc[len(percentagesDF)] = [col, "Any Engagement", pivot_table[col].count()/len(pivot_table.index)]
            graduateEmailsDF = st.session_state['graduateEmails']
            graduateYears = graduateEmailsDF.columns
            
            engagementsToUse = st.session_state['lineGraphEngagementOptions']
            for category in engagementsToUse:
                if category != "Any Engagement":
                    first_df_subset = df[df['Engagement Type'] == category]
                else:
                    first_df_subset = df
                
                for year in graduateYears:
                    df_subset = first_df_subset[first_df_subset['Email'].isin(graduateEmailsDF[year])] 
                    pivot_table = df_subset.pivot_table(index='Unique ID', columns=semesterNumberedColumn, values='Engagement Type', aggfunc=agg_to_set)
                    pivot_table = pivot_table.ffill(axis=1)
                    #pivot_table = pivot_table.rename(columns=(correctMapping))
                    pivot_table = pivot_table.drop(columns=[col for col in pivot_table.columns if col not in correctMapping.keys()])
                    pivot_table.dropna(axis = 0, how = "all", inplace = True)

                    
                    currentSet = set(graduateEmailsDF[year])
                    currentSet.discard(np.nan)

                    majorsToInclude = set(st.session_state['majorsToInclude'])
                    majMap = st.session_state['Majors Mapping']
                    if len(majorsToInclude) > 0:
                        to_discard = list()
                        for gradEmail in currentSet:
                            if gradEmail not in majMap:
                                to_discard.append(gradEmail)
                            elif not set(majMap[gradEmail]).intersection(majorsToInclude):
                                to_discard.append(gradEmail)
                        for d in to_discard:
                            currentSet.discard(d)

                    numOfGrads = len(currentSet)
                    print(year)
                    print(numOfGrads)
                    for col in pivot_table.columns:
                        percentagesDF.loc[len(percentagesDF)] = [col, year + " " + category, pivot_table[col].count()/numOfGrads, numOfGrads, correctMapping[col], year, category]

            percentagesDF.sort_values(by=["Category", "Semester"], ascending = [True, True], inplace=True)
            
            #percentagesDF['Semester'] = percentagesDF['Semester'].map(correctMapping)
            print(percentagesDF)
            fig = px.line(percentagesDF, x="Semester", y="Percentages", color = "Category", title='When Students Engaged with Hiatt', markers=True, hover_data={"Type of Engagement": percentagesDF['Category'], "Real Semester": percentagesDF['Semester Name'], "Year": percentagesDF['Graduating Year'], "Engagement Name": percentagesDF['Engagement']})
            fig.update_layout(yaxis_tickformat = '.0%')
            fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Semester<br><i><sub>" + subtitle + "</sub></i>")
            fig.update_traces(hovertemplate="%{y:.0%} of the graduating class of %{customdata[2]} engaged with %{customdata[3]} by %{customdata[1]}<extra></extra>")
            fig.update_xaxes(ticktext=list(correctMapping.values()), tickvals=list(correctMapping.keys())) 
            addChartToPage(fig)

            return
            print("Hello", len(pivot_table.index))

            graduateEmailsDF = st.session_state['graduateEmails']
            df = originalDf.copy()
            engagementList = originalEngagementList.copy()

            emailSet = set(df['Email'])
            graduateYears = graduateEmailsDF.columns
            
            percentagesDF = pd.DataFrame(columns = ["Class Year", "Category", "Percentages"])
            
            for year in graduateYears:
                currentSet = set(graduateEmailsDF[year])
                currentSet.discard(np.nan)
                
                majorsToInclude = set(st.session_state['majorsToInclude'])
                majMap = st.session_state['Majors Mapping']
                if len(majorsToInclude) > 0:
                    to_discard = list()
                    for gradEmail in currentSet:
                        if gradEmail not in majMap:
                            to_discard.append(gradEmail)
                        elif not set(majMap[gradEmail]).intersection(majorsToInclude):
                            to_discard.append(gradEmail)
                    for d in to_discard:
                        currentSet.discard(d)
                print(len(currentSet))

                percent = len(emailSet & currentSet) / len(currentSet)
                percentagesDF.loc[len(percentagesDF)] = [year, "Any Engagement", percent]

                for category in engagementList:
                    df_subset = df[df['Engagement Type'] == category]
                    tempBaseSet = set(df_subset['Email'])

                    percent = len(tempBaseSet & currentSet) / len(currentSet)
                    percentagesDF.loc[len(percentagesDF)] = [year, category, percent]
                

            fig = px.line(percentagesDF, x="Class Year", y="Percentages", color = "Category", title='Percentage of Each Class Year that Engaged with Hiatt', markers=True, hover_data={"Type of Engagement": percentagesDF['Category']})
            fig.update_layout(yaxis_tickformat = '.0%', yaxis_range = [0, 1])
            fig.update_layout(
                    title={'x':0.5, 'xanchor': 'center'}, 
                    xaxis_title = "Class Year<br><i><sub>" + subtitle + "</sub></i>")
            fig.update_traces(hovertemplate="For the %{x}, %{y:.0%} of students engaged with %{customdata[0]}<extra></extra>")
            addChartToPage(fig)
        
            



        
        
























        aa = datetime.datetime.now()
        
        # Can be used wherever a "file-like" object is accepted:
        
        df = st.session_state['df'].copy()
        #database = st.session_state['database'].copy()
        #print(dict(df['Graduation_Semester'].value_counts()))

        ######
        
        #df.insert(2, 'Full Name', df["First Name"] + (' ' + df["Last Name"]).fillna(''))
        df['Unique ID'] = df.groupby(['Email']).ngroup()
        ######
        #df['Engagement Type'] = df.apply(engagement_categories, axis=1)
        df['Semester'] = df.apply(clean_semesters, axis=1)
        #df = df.drop(df[df['Engagement Type'] == 'Do not Include'].index)
        ######
        def updatedRestrictByCohort(df, graduationYear):
            df.drop(df[
                (df['Graduation_Semester'] != 'Spring Semester ' + str(graduationYear)) &
                (df['Graduation_Semester'] != 'Summer Semester ' + str(graduationYear)) &
                (df['Graduation_Semester'] != 'GPS Spring Semester ' + str(graduationYear)) &
                (df['Graduation_Semester'] != 'GPS Fall Semester ' + str(graduationYear-1)) &
                (df['Graduation_Semester'] != 'Fall Semester ' + str(graduationYear-1))].index, inplace=True)
            return df
        def restrictByCohort(df, graduationYear):
            df.drop(df[
                ((df['Class Level'] != 'Senior') &
                (df['Class Level'] != 'Junior')  &
                (df['Class Level'] != 'Sophomore') &
                (df['Class Level'] != 'Freshman'))
                ].index, inplace=True)
            df.drop(df[((df['Semester'] == (str(graduationYear-1) + 'Fall')))].index, inplace=True)
            df.drop(df[((df['Class Level'] == 'Senior') & 
                    ((df['Semester'] != ('Summer ' + str(graduationYear-1))) & 
                    (df['Semester'] != ('Fall ' + str(graduationYear-1))) &
                    (df['Semester'] != ('Winter ' + str(graduationYear-1))) & 
                    (df['Semester'] != ('Spring ' + str(graduationYear)))))].index, inplace=True)
            df.drop(df[((df['Class Level'] == 'Junior') & 
                    ((df['Semester'] != ('Summer ' + str(graduationYear-2))) & 
                    (df['Semester'] != ('Fall ' + str(graduationYear-2))) &
                    (df['Semester'] != ('Winter ' + str(graduationYear-2))) & 
                    (df['Semester'] != ('Spring ' + str(graduationYear-1)))))].index, inplace=True)
            df.drop(df[((df['Class Level'] == 'Sophomore') & 
                    ((df['Semester'] != ('Summer ' + str(graduationYear-3))) & 
                    (df['Semester'] != ('Fall ' + str(graduationYear-3))) &
                    (df['Semester'] != ('Winter ' + str(graduationYear-3))) & 
                    (df['Semester'] != ('Spring ' + str(graduationYear-2)))))].index, inplace=True)
            df.drop(df[((df['Class Level'] == 'Freshman') & 
                ((df['Semester'] != ('Summer ' + str(graduationYear-4))) & 
                (df['Semester'] != ('Fall ' + str(graduationYear-4))) &
                (df['Semester'] != ('Winter ' + str(graduationYear-4))) & 
                (df['Semester'] != ('Spring ' + str(graduationYear-3)))))].index, inplace=True)
            return(df)


        #graduationYearToRestrictBy = 2021
        if(graduationYearToRestrictBy != 'Do not restrict by graduation year'):
            #df = restrictByCohort(df, int(graduationYearToRestrictBy))
            df = updatedRestrictByCohort(df, int(graduationYearToRestrictBy))
            subtitle = "Graduating class of " + graduationYearToRestrictBy
        else:
            subtitle = "Data not restricted by graduating class"
        ###
        #df.to_excel('OutputSource.xlsx', sheet_name="source")
        ###
        def event_sizes(row):
            return eventSize[row['Engagement Type']]

        eventSize = df.groupby('Engagement Type').count().to_dict(orient='dict')['Semester']
        df['Event Size'] = df.apply(event_sizes, axis=1)



        ##This is used to drop the smaller events as desired, and the number is the minimum number of engagements
        ####THIS SHOULD BE DELETED LATER!!!! IT CAN BE HANDLED LOWER DOWN, THIS WILL LEAD TO INACCURATE RESULTS!!!!
        #df = df.drop(df[df['Event Size'] < 1000].index)
        #####


        mapping = {}
        events = df.groupby('Engagement Type').count().to_dict(orient='dict')['Unique ID']
        sorted_events = sorted(events.items(), key=lambda x:x[1], reverse=True)
        sorted_events_dictionary = dict(sorted_events)
        
        x=0
        while x < len(sorted_events):
            mapping[sorted_events[x][0]] = x+1
            x +=1

        def ranked_events(row):
            return mapping[row['Engagement Type']]
        df['Ranked Events'] = df.apply(ranked_events, axis=1)
        ######

        #Not used for line graphs, but used for other graphing types
        #originalEngagementList = list(sorted_events_dictionary.keys())
        originalEngagementList = st.session_state['RankedEngagementList']

        total = pd.DataFrame(index = originalEngagementList, columns=originalEngagementList)

        for col in total.columns:
            total[col].values[:] = 0

        #success = total.copy()
        #percent = total.copy()

        majorsToInclude = set(st.session_state['majorsToInclude'])
        if len(majorsToInclude) > 0:
            to_delete = list()
            for id, row in df.iterrows():
                if not set(row.Majors).intersection(majorsToInclude):
                    to_delete.append(id)
            df.drop(to_delete, inplace=True)

            subtitle += ", only including students with majors in the following categories: " + ', '.join(majorsToInclude)
        else:
            if subtitle == "Data not restricted by graduating class":
                subtitle += " or students major"
            else:
                subtitle += ", data not restricted by students major"

        
        if st.session_state['restrictByKnownGraduates']:
            if subtitle != "Data not restricted by graduating class or students major":
                subtitle += "<br>Data also restricted to only include students known to have graduated"
            else:
                subtitle = "Data restricted to only include students known to have graduated, but not by students major or graduating class"
            
            graduateEmailsDF = st.session_state['graduateEmails']
            graduateEmailsList = graduateEmailsDF.values.flatten()
            df = df[df['Email'].isin(graduateEmailsList)]




        originalDf = df
        originalMapping = mapping
        originalTotal = total
        originalSuccess = total
        originalPercent = total
        
        bb = datetime.datetime.now()
        #print((bb-aa).total_seconds(), ": THis is the one we care about!")

        if "Engagement Relationships (Unique)" in graphTypes:
            createHeatMap(False)
        if "Engagement Relationships (Total)" in graphTypes:
            createHeatMap(True)
        if "Sequential Pathways of Student Engagements" in graphTypes:
            createSankeyDiagram()
        #All code for the line graphs are still present, but they have been removed from the options for now
        #if "Line Graph" in graphTypes:
        #    createLineGraph()
        if bool({"First Engagements Data (Total)", "First Engagements Data (Unique)", "Return Rates Based on All Engagements", "Return Rates Based on First Engagements", "Rates of Unique Engagements", "Students with only 1 Engagement"} & set(graphTypes)):
            createScatterPlot()
        if "Total Engagement Percentages" in graphTypes:
            createGraduateGraph()
        if "When Students Engaged with Hiatt" in graphTypes:
            createGradesEngagementsGraph()


        
    elif st.session_state['graphsGenerated']:
        for fig in st.session_state['currentGraphs']:
            addChartToPage(fig)
