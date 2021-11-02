# DS3002-Project-1

## Pipeline Goal:
Spotify gives user's the option to download their listening data as JSON files; however, these files only contain the song's end time, artist name, track name, and the duration fo the play. For user's to access more interesting information on a song such as the song's audio features, they need to have the song's "track ID". Since this information was not readily available in the JSON download from Spotify, I decided to supplement this file with the track ID using the Spotify API. Using the artist and track names I was able to use the search endpoint of the API to find the associated track ID to create a new, more robust dataset. 

## How it works:
1. The code uses my stored client ID and client secret in the client credentials flow to create an access token that will be used for all API queries. The client credential flow is managed through the "SpotifyAPI" class. The code will raise exceptions if it is unable to authenticate the client.
2. Next the code loads my Spotify streaming history which is stored in this GitHub repository. It accesses the JSON file via a URL.
3. After downloading the JSON file it is converted to a Pandas dataframe. The columns are then reduced from 4 to 2: "artistName" and "trackName". These were kept since they are required to find the track ID. The number of records is reduced from 10,000 to 51 to reduce the number of API calls required.
4. The program then iterates through the rows of the dataframe and uses the column values in the API query for the track data. The track data is then subsetted to isolate the track ID. The track ID is then added to a list called "id_list".
5. id_list is then concatenated with the subsetted dataframe, making the new dimensions of the dataframe 3 columns and 51 rows. This new dataframe is then converted to a CSV file and written to disk using a file path. NOTE: this file path is specific to my computer and will need to be changed when the program is run on a different device. The program will warn the user if the file path specified does not exist. 
6. The program prints a summary of the original dataframe (number of records and columns) as well as a summary of the transformed dataframe.

## Meeting benchmarks:
i:
  1. The program fetches a JSON file by URL 
  2. The program takes a JSON file as input but outputs a CSV file
  3. The program removes two extraneous columns and adds an additional column of Track IDs, the program also reduces the number of records from 10,000 to 51
  4. The program writes the new file to disk 
  5. The program prints the number of columns and records for both the original and the transformed dataset
ii:
  1. The program raises exceptions when it is unable to authenticate the client, to perform the API call, when it cannot use the default file path provided, and when it is unable to write the new dataframe to CSV
 Extra: it uses the Spotify API to pull track ID data to supplement the downloaded streaming history data
