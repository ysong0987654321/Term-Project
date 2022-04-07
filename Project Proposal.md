**Project Proposal**
1. The Big Idea:
    The main idea of the project is to take financial statements (capital IQ, Yahoo Finance...) of a company, web scrap the financial data using python (beautifulsoup) or use API, clean the data using max, min, average and other method, perform a FCFE/FCFF DCF analysis, visualize the Free Cash Flow by year, and export dataset into Excel or .csv format/create a flask website by prompting the user to enter the stock ticker of the company. There are four to five python files anticipated for now. The first one is the data extration/data cleaning file. The second one is calculation of discount rate. The third file is to perform the DCF analysis. The fourth file is to visualize the cash flow, and export the number. (There may be a fifth file to perform the flask operations and html codes)
    The topics I will explore in this project is web scraping (beautifulsoup), data cleaning (which I might have to explore a bit more by myself), data operation, export/flask.
    The main goal is to have all the components of the project to work and generate the excel/.csv file for export. A further goal if time permits is to create a min website using Flask that prompts the user to enter the stock ticker of their selected company and return the DCF result.

2. Learning Goals:
    Being able to combine what we have learned so far in OIM 3640 and apply concepts to this project.
    Being able to have problem solving skills when encountering difficulties. 
    Being able to combine materials from OIM 3640 with materials from other Babson courses and take the project beyond the scope of school.

3. Implementation Plan:
    As mentioned above, right now I picture having four to five python files.
    1. Web scrap financial data using beautifulsoup from Yahoo Finance or Capital IQ; OR use API and json files to extra financial data (will try to attempt this first as it might be a better option);
    clean any out of range/abnormal data from the file as necessary (might need to explore a bit and combine with logic from QTM 2000)
    2. Calculate discount rate (may reference python for finance book)
    3. Calculate FCFE & FCFF DCF result (may reference python for finance book)
    4. Visualize cash flow result using matplotlib, export to excel or .csv file format
    5. create a mini webpage using flask, prompt the user to enter the stock ticker and select FCFE or FCFF and return the DCF result and visualization

4. Roughly three weeks for completion of the project:
    1. 4/7 - 4/16: complete web scrap/API section; try to complete discount rate calculation and DCF calculation as well
    2. 4/17 - 4/23: complete discount rate and DCF calculation; try to complete visualization & excel/.csv export; if all completed, try flask coding and html
    3. 4/24 - project submission: complete flask sectopm; building Google Website for illustration; test functions over different stickers

    During the week, I may consult with the professor at least once a week for progress check, and ask any question/difficulties

5. Collaboration plan:
    I will be working individually for this project.

6. Risks:
    The biggest risk is time. There is only three weeks left in the semester and there are a lot to be completed
    Web scraping/API: since I have not used Yahoo Finance or Capital IQ for anything like the term project, there might be a few issues along the way for this step
    Formatting: there are a lot of formatting in this project as the DCF analysis is quite extensive. Therefore, making the formating is correct for all steps in the project is critical.

7. Additional Course Content:
    As mentioned above, the topics that will be most crucial for me are: beautifulsoup, data cleaning(may use text mining?), matplotlib, flask
    May also reference existing books for python for finance as neccessary. Will document references if used.