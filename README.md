# Extracting-Business-card-Data-with-OCR
# Objective:
`  BizCardX is a user-friendly tool for extracting information from business cards. The tool uses OCR technology to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. Users can access the extracted information using a GUI built using streamlit. The BizCardX application is a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button. Further the data stored in database can be easily Read, updated and deleted by user as per the requirement.

## Technologies:
          1. Python
          2. Easy OCR
          3. MySQL
          4. Pandas
          5. Streamlit
# Process:
**Extracting the data**
            `Extract the particular business card data by using easyocr.`
**Transforming the data**
            `After the extraction process, the text data extracted is converted into a structured data in the form of dataframe.`
**Loading data**
            `After the transformation process, the data in the form of dataframe is stored in the MySQL database.`
**Visualizing, Updating, deleting the data**
            `The extracted data can be visualized using matlplotlib and in the form of dataframe.The data can also be updated, modified and deleted from the database.`
            
 ## User Guide:
              __step 1:__  Click the 'Browse Files' button and select an image.
              __step 2:__  Click the 'Upload to MySQL DB' button to upload the data to the Mysql database.
              __step 3:__  We can able to modify the information and delete the previous data.

# Conclusion:
          The result of the project would be a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. 

              
              
