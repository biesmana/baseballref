
# coding: utf-8

# In[ ]:

from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment 
import pandas as pd
import html5lib
import time 
import requests
import re


# In[ ]:

# URL for team stats 
url_template_team = "http://www.baseball-reference.com/teams/tgl.cgi?team={team}&t=b&year={year}"


# In[ ]:

# teams
teams = ["LAD", "BOS", "LAA", "CHC", "TEX", 
         "OAK", "MIN", "CHW", "SEA", "KCR", 
         "MIL", "TBR", "STL", "BAL", "HOU", 
         "DET", "PIT", "NYY", "CLE", "MIN", 
         "CIN", "COL", "NYM", "SFG", "MIL", 
         "WSN", "ATL", "SDP", "ARI", "MIA", ]


# In[ ]:

# function to get column headers (pass in the url and the row at which the column headers begin)
def get_columns(url_column, row):
    
    # get the HTML from the url passed in 
    html = urlopen(url_column)
    
    # make a BS object
    soup = BeautifulSoup(html, "lxml")
    
    # find all the tr tags for the column header of interest 
    tr_tag_list = soup.findAll('tr')[row-1] 
    
    # extract table header cell elements from the tag object
    cell_el_list = tr_tag_list.findAll('th')

    # create an empty list to hold all the elements in the column header 
    column_headers = []  

    # for each cell element
    for th in cell_el_list:  
        col_element = th.getText()
        # append each cell element to the column_header list
        column_headers.append(col_element)
    return column_headers


# In[ ]:




# In[ ]:

column_teams = get_columns("http://www.baseball-reference.com/teams/tgl.cgi?team=CHC&t=b&year=2016", 1)


# In[ ]:

url_curr = url_template_team
team = teams[0]
year = 2017


# In[ ]:

url = url_curr.format(team=team, year=year)
url


# In[ ]:

html = urlopen(url)
html


# In[ ]:

soup = BeautifulSoup(html, "lxml")


# In[ ]:

first_row = soup.findAll('tr')[1]


# In[ ]:

first_row.find('th').text


# In[ ]:

for td in first_row.findAll('td'):
    print (td.text)


# In[ ]:

# function to run through multiple years and multiple teams and get the regular season game logs 
def get_game_logs(url_curr, column_headers, teams, start, end):
    
    # create an empty DataFrame to store all the game logs for all the team's seasons 
    team_stats_df = pd.DataFrame()
    
    for team in teams:
        for year in range(start, end):
            # get the url
            url = url_curr.format(team=team, year=year)
        
            # check if there are game logs for the current team and the current season
            try:
                html = urlopen(url)
            except:
                print("No data for " + team + " in the " + str(year) + " season" + " in the regular season")
                continue
                
            # get the html
            html = urlopen(url)
            # create the beautiful soup object 
            soup = BeautifulSoup(html, "lxml")
            
            ### PART 1: REGULAR SEASON DATA 
    
            # get regular season data (starts on second row)
            data_rows = soup.findAll('tr')[1:]
            
            # check if data_rows actually contains data
            if len(data_rows)<1:
                print("No data for " + team + " in the " + str(year) + " season" + " in the regular season")
                continue 

            # create an empty list to hold all the regular season stats for the current season and the current team 
            season_data= []  

            for i in range(len(data_rows)):
                # create an empty list for each game 
                game_row = []
            
                # first value. Must be handled separately since it goes by th tag instead of td tag 
                game_row.append(data_rows[i].findAll('th')[0].getText())

                # for each table data element from each table row
                for td in data_rows[i].findAll('td'):        
                    # get the text content and append to the game_row 
                    game_row.append(td.getText())        

                # then append each game to the season_data matrix
                season_data.append(game_row)
            
            # Turn season data into a DatFrame
            season_df = pd.DataFrame(season_data, columns=column_headers)
            # Add game_type column
            season_df.insert(0, 'GameType', 'RegularSeason')
            
            # create and insert the Season and Team column
            season_df.insert(1, 'Season', year)
            season_df.insert(2, 'Team', team)
        
            # Append to the big dataframe
            team_stats_df = team_stats_df.append(season_df, ignore_index=True)

    return team_stats_df


# In[ ]:

url_box = "https://www.baseball-reference.com/boxes/{team}/{team}{year}{month}{day}0.shtml"


# In[ ]:

def get_inning_scores(url_box, column_headers, teams, y_start, y_end, m_start, m_end, d_start, d_end):

    #initiate data frames
    inning_df = pd.DataFrame()
    date_df = pd.DataFrame()
    start_time_df = pd.DataFrame()
    inning_numbers = list(range(1,50))

    for team in teams:
        for year in range(y_start, y_end):
            for month in range(m_start, m_end):
                for day in range (d_start, d_end):
                    # get the url
                    if month <= 9:
                        month = '0' + str(month)
                    if day <= 9:
                        day = '0' + str(day)
                    url = url_box.format(team=team, year=year, month=month, day=day)
            
                    # get the html
                    html = urlopen(url)

                    # create the beautiful soup object 
                    soup = BeautifulSoup(html, "lxml")

                    inning_rows = soup.findAll('tr')[2:]

                    # check if data_rows actually contains data
                    if len(data_rows)<1:
                        print("No data for " + team + " in the " + str(year) + " season" + " in the regular season")
                        continue 

                    # create an empty list to hold all the regular season stats for the current season and the current team 
                    game_data = []

                    for i in range(len(inning_rows)):
                        # create an empty list for each game 
                        game_row = []

                        # for each table data element from each table row
                        for td in data_rows[i].findAll('td')[:-3]:        
                            # get the text content and append to the game_row 
                            game_row.append(td.getText())   

                        game_data.append(game_row)
                        inning_runs_df = pd.DataFrame(game_data, columns = inning_numbers)
                        

                    #get the date data frame
                    date_df = pd.DataFrame()
                    date = soup.find("div", {"class":"scorebox_meta"}).text[0]
                    date_df = date_df.append(date, column = Date)
                    
                    #get the start time data frame
                    start_time_df = pd.DataFrame()
                    start_time = soup.find("div", {"class":"scorebox_meta"}).text[1]
                    start_time_df = start_time_df.append(start_time, column = Start Time) 
                    
                    #add a column to the start_time_df with a D for daytime or N for Nighttime
                    day_or_night = []
                    day_times = [12, 1, 2, 3, 4]
                    if start_time[0] in day_times:
                        day_or_night.append(D)
                        
                    elif day_or night.append(N)
                    start_time_df.assign(DN = day_or_night)
                        
                    #get venue and attendance. create a dataframe for each and append to the main dataframe
                    
                    venue_df = pd.Dataframe()
                    attendance_df = pd.Dataframe()
                    for strong_tag in soup.find_all('strong'):
                        venue = []
                        if strong_tag.text = 'Venue':
                            venue.append(strong_tag.next_sibling)
                            venue_df = venue_df.append(venue, column = Venue)
                    
                        attendance = []
                        elif strong_tag.text = 'Attendance':
                            attendance.append(strong_tag.next_sibling)
                            attendance_df = attendance_df.append(attendance, column = Attendance)
                            
                    # then append each game to the season_data matrix
                    inning_df = inning_df.append(inning_runs_df, date_df, start_time_df, venue_df, attendance_df)
                
                               
                    
    return inning_df

                    


# In[ ]:

start_time = time.time()
inning_numbers = list(range(1,50))


# call function for game logs 

team_game_logs_df = get_game_logs(url_template_team, column_teams, teams, 2017, 2018)
inning_game_df = get_inning_scores(url_box, inning_numbers, teams, 2016, 2017, 4, 10, 1, 31)

print("%f seconds" % (time.time() - start_time))


# In[ ]:

# look at number of rows
len(team_game_logs_df)


# In[ ]:

# look at first few rows 
team_game_logs_df.head()


# In[ ]:

# look at last few rows 
team_game_logs_df.tail()


# In[ ]:

# function to clean data
def clean_df(df):
    # Convert data to proper data types
    df = df.convert_objects(convert_numeric=True)

    # Get rid of the rows full of null values
    df = df[df.Season.notnull()]

    # Replace NaNs with 0s
    df = df.fillna(0)
    
    # Change % symbol
    df.columns = df.columns.str.replace('%', '_Perc')
    
    return df


# In[ ]:

# clean advanced player stats df
team_game_logs_df = clean_df(team_game_logs_df)
inning_game_df = clean_df(inning_game_df)


# In[ ]:

team_game_logs_df.columns
inning_game_df.columns


# In[ ]:

# Check if missing values in the DataFrame
team_game_logs_df.isnull().sum() 
inning_game_df.isnull().sum()


# In[ ]:

# write data frame to CSV
team_game_logs_df.to_csv("team_game_logs_test_4.csv")
inning_df.to_csv("team_game_logs_test_5.csv")

