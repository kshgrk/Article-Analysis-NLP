# Article-Analysis-NLP
* This is a personal project which scrapes 170 articles from [Blackcoffer](https://insights.blackcoffer.com) and does sentiment and readbility analysis on them.
* The 13 different indices calculated in this project are: - 
```
1. POSITIVE SCORE
2. NEGATIVE SCORE
3. POLARITY SCORE
4. SUBJECTIVITY SCORE
5. AVG SENTENCE LENGTH
6. PERCENTAGE OF COMPLEX WORDS
7. FOG INDEX
8. AVG NUMBER OF WORDS PER SENTENCE
9. COMPLEX WORD COUNT
10. WORD COUNT
11. SYLLABLE PER WORD
12. PERSONAL PRONOUNS
13. AVG WORD LENGTH
```
* The function for all the indices are in the `main.py` file.
* `scrape.py` is the script which is used to scrape data.

## How to use
1. Install all the important modules via the command "pip install -r requirements.txt".
2. Make sure there is a directory named "Scraped Data", if not create it. Inside it all of the scraped data will be stored.
3. Make sure "Input.xlsx", "Output.xlsx", "Loughran-McDonald_MasterDictionary_1993-2021.csv" and "StopWords_Generic.txt" files are present in the main directory.
4. Run the script "scrape.py" and wait till all the data is scraped. Check inside the "Scrape Data" directory if there are all the files starting from "1.txt" to "170.txt" present.
5. Now run the script "main.py". It will calculate all the above mentioned index values and create an excel file named "output.xlsx".

## Files Overview
1. **Input.xlsx**: - Contains links of all the 170 articles.
2. **Loughran-McDonald_MasterDictionary_1993-2021.csv**: - Master Directory with sentiment words list, can be found [here](https://sraf.nd.edu/loughranmcdonald-master-dictionary/).
3. **output.xlsx**: - Final output file.
4. **StopWords_Generic.txt**: - Lists of stopwords, can be found [here](https://sraf.nd.edu/textual-analysis/).
5. **main.py**: - Main python script to calculate all the values and creating final output file.
6. **scrape.py**: - Python script to scrape data from the given links and to store it in "Scraped Data" folder.
7. **requirements.txt**: - Text file that includes all the module requirements.
