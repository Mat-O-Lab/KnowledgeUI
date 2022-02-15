# Read metadata from each Excel-file in the folder.
# V3: This version takes the description column as index.
# V4: This version switches rows and columns
# V5: Replace german names in the dataframe with english ones

# To-Do: Edit loop over the opened excel-sheets inside the file so 
# also files with multiple Rezeptur-sheets 
# (f.e. "2014_08_04 Rezepturen_auf 85 Liter_Werner_Losert.xlsx") 
# can be included in the resulting dataframe

#----------------------------------------------------------------------------------------------------------

# Read excel with pandas, display with iPython, collect files with glob
import pandas as pd
from IPython.display import display
import glob as g

# Displaying setting
pd.set_option('display.max_rows', None)

# Collect a list of excel-Files in the current folder
excelsheets = g.glob('./*xlsx') # + g.glob('./*xls')   # atm neglect older excel-versions
datanamelist = []
for file in excelsheets:
    name = str(file[2:-5])       # use :-5 if without datatype
    datanamelist.append(name)
print("There are " + str(len(datanamelist)) + " excel-sheets to extract metadata from.")

# Translation: Read in the translation from an excel-file and prepare a function to replace german with english
translation = pd.read_excel("translation.xlsx")
translation.columns = ["german", "english"]
def translate(df):
    for deutsch, english in translation.itertuples(index=False,name=None):
        df = df.replace(deutsch,english,regex=True)
    return df
    
# Set up lists to fill inside the loop and build final dataframe from
list_of_dfs = []
list_of_excelsheets = []

# main part: extract the metadata for each excel-sheet in the folder
for excelsheet in datanamelist:

    # look for the correct worksheet, mostly named "RezepturM" + X acording to file name
    if "Rezeptur_M" in excelsheet:
        print("\n Working on: Rezeptur"+excelsheet)
        list_of_excelsheets.append(excelsheet)
        
        # load excel sheet and set proper index & column headers & translate
        exceltodf = pd.read_excel(excelsheet + ".xlsx" , sheet_name= ("Rezeptur"+excelsheet[20:]))
        exceltodf.iat[17,2] += " [kg/m^3]"
        exceltodf.iat[17,4] = "Dichte [kg/dm^3]"
        exceltodf = translate(exceltodf)
        exceltodf.rename(columns=exceltodf.iloc[17], inplace = True)
     
        # create new dataframe with only relevant data and chose Index column
        relevant_data = exceltodf.iloc[20:,[0,2,4,8]]
        relevant_data = relevant_data.set_index("Stoffart")
        
        # replace NaN
        relevant_data[relevant_data.columns[-1]] = relevant_data[relevant_data.columns[-1]].fillna("---")

        # merge df into a series and add the Zusatzstoff
        df = relevant_data
        df_out = df.stack()
        df_out.index = df_out.index.map('{0[0]}: {0[1]}'.format)
        df_out = pd.concat([df_out, pd.Series([exceltodf.iloc[24,1]],index=["Zusatzstoff"])], ignore_index=False)

        # export information out of loop through list
        list_of_dfs.append(df_out)
       

# concat the dfs from the loop into one
large_df = pd.concat(list_of_dfs, ignore_index=False, axis=1)
large_df.columns = list_of_excelsheets
large_df = large_df.T  # transpose the dataframe (swap columns and rows)

# Display or save as xlsx or csv file
large_df.to_excel("metadata.xlsx") 
#large_df.to_csv("output.csv")
display(large_df.to_string())





