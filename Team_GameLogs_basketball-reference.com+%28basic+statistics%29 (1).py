
# coding: utf-8

# In[114]:

from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment 
import pandas as pd
import html5lib
import time 
import requests
import re


# In[115]:

# URL for team stats 
url_template_team = "http://www.baseball-reference.com/teams/tgl.cgi?team={team}&t=b&year={year}"


# In[116]:

# teams
teams = ["LAD", "BOS", "LAA", "CHC", "TEX", 
         "OAK", "MIN", "CHW", "SEA", "KCR", 
         "MIL", "TBR", "STL", "BAL", "HOU", 
         "DET", "PIT", "NYY", "CLE", "MIN", 
         "CIN", "COL", "NYM", "SFG", "MIL", 
         "WSN", "ATL", "SDP", "ARI", "MIA", ]


# In[117]:

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


# In[118]:

column_teams = get_columns("http://www.baseball-reference.com/teams/tgl.cgi?team=CHC&t=b&year=2016", 1)


# In[119]:

url_curr = url_template_team
team = teams[0]
year = 2017


# In[120]:

url = url_curr.format(team=team, year=year)
url


# In[121]:

html = urlopen(url)
html


# In[122]:

soup = BeautifulSoup(html, "lxml")


# In[123]:

first_row = soup.findAll('tr')[1]


# In[124]:

first_row.find('th').text


# In[125]:

for td in first_row.findAll('td'):
    print (td.text)


# In[126]:

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


# In[127]:

url_template_box = "https://www.baseball-reference.com/boxes/{team}/{team}{year}{month}{day}0.shtml"


# In[4]:

def get_inning_columns(url_template_box, row):

    inning_numbers = [] 
    for x in range (1, 50):
        inning_numbers.append(x)
    return inning_numbers


# In[6]:

def get_inning_scores(url_box, column_headers, teams, y_start, y_end, m_start, m_end, d_start, d_end):
    
     inning_df = pd.Dataframe()
    
     for team in teams:
        for year in range(start, end):
            for month in range(start, end):
                for day in range (start, end):
                    # get the url
                    url = url_box.format(team=team, year=year, month=month, day=day)
            
            # get the html
            html = urlopen(url)
            
            # create the beautiful soup object 
            soup = BeautifulSoup(html, "lxml")
            
            inning_rows = soup.findAll('tr')[3:]
            
            # check if data_rows actually contains data
            if len(data_rows)<1:
                print("No data for " + team + " in the " + str(year) + " season" + " in the regular season")
                continue 

            # create an empty list to hold all the regular season stats for the current season and the current team 
            game_data= []  

            for i in range(len(inning_rows)):
                # create an empty list for each game 
                game_row = []

                # for each table data element from each table row
                for td in data_rows[i].findAll('td'):        
                    # get the text content and append to the game_row 
                    game_row.append(td.getText())   
                
                game_data.append(game_row)
                    
                #I want to delete the last 3 columns from each team, append the bottom row to the first, and create a column for the opponent
                

                # then append each game to the season_data matrix
                inning_df.append(game_data)
            


# In[128]:

def get_extra_stats(url_box, column_headers, teams, y_start, y_end, m_start, m_end, d_start, d_end):
    for team in teams:
        for year in range(start, end):
            for month in range(start, end):
                for day in range (start, end):
                    # get the url
                    url = url_box.format(team=team, year=year, month=month, day=day)
            
            # get the html
            html = urlopen(url)
            
            # create the beautiful soup object 
            soup = BeautifulSoup(html, "lxml")
            
            #Pull in the runs scored in each inning
            innings = tr_tag_list.findAll('th')[0].getText()

            # create an empty list to hold all the elements in the column header 
            inning_numbers = soup.findAll('th')[2:]
            #create an empty list to hold all the regular season runs by inning for the current season and the current team
            inning_data = []
            
            for i in range(len(inning_numbers)):
                #create an empty list for each game
                game_innings = []
                game_innings.append(inning_numbers[i].findAll('th')[0].getText())
                for td in data_rows[i].findAll('td'):        
                    # get the text content and append to the game_row 
                    game_innings.append(td.getText()) 
                #find a way to delete the last 3, 
                inning_data.append(game_innings)
                

            ###########################################################
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
            ###########################################################
            
            innings = []
            # for each cell element
            for i in range(len(inning_numbers)):  
                innings.append(inning_numbers[i])
               
            
            game_length = soup.findAll('td')[2:]
            
            # check if data_rows actually contains data
            if len(game_length)<1:
                print("No data for " + team + " in the " + str(year) + " season" + " in the regular season")
                continue 

            # create an empty list to hold all the regular season stats for the current season and the current team 
            season_data_extra = []  
            game_row = []
            for i in range(len(game_length)):
                # create an empty list for each inning 
                          
                # for each table data element from each table row
                for td in game_length[i].findAll('td'):        
                    # get the text content and append to the game_row 
                    game_row.append(td.getText())        

                # then append each game to the season_data_extra matrix
                season_data_extra.append(game_row)
            
                    


# In[ ]:




# In[129]:

start_time = time.time()

# call function for game logs 
team_game_logs_df = get_game_logs(url_template_team, column_teams, teams, 2017, 2018)

print("%f seconds" % (time.time() - start_time))


# In[130]:

# look at number of rows
len(team_game_logs_df)


# In[131]:

# look at first few rows 
team_game_logs_df.head()


# In[132]:

# look at last few rows 
team_game_logs_df.tail()


# In[133]:

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


# In[134]:

# clean advanced player stats df
team_game_logs_df = clean_df(team_game_logs_df)


# In[135]:

team_game_logs_df.columns


# In[136]:

# Check if missing values in the DataFrame
team_game_logs_df.isnull().sum() 


# In[137]:

# write data frame to CSV
team_game_logs_df.to_csv("team_game_logs_test_2.csv")


# In[ ]:



