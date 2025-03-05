import pandas as pd
import streamlit as st
import mysql.connector as sql
import numpy as np
from streamlit_option_menu import option_menu
import easyocr as ocr
from PIL import Image
import io
import tempfile
import re
import easyocr

mydb=sql.connect(host="localhost",
                 user="root",
                 password="NyL@shr33",
                 database="biz_card"
                )
cur=mydb.cursor()
cur.execute("create database if not exists biz_card" )
table=cur.execute("""create table if not exists card_details1(CARDHOLDER_NAME varchar(100), DESIGNATION varchar(100),COMPANY_NAME varchar(100),CONTACT varchar(100),AREA varchar(100),CITY varchar(200),STATE text,PINCODE varchar(100),MAIL_ID varchar(100) unique,WEBSITE varchar(100) unique,IMAGE longblob)""")
mydb.commit()
#Visualization of process 

st.header(':red[BUSINESS CARD EXTRACTION WITH OCR]')

selected = option_menu(
    menu_title=None,
    options= ["ABOUT", "UPLOAD & EXTRACT", "MODIFY", "DELETE"],
    menu_icon=None,
    icons=None,
    orientation="horizontal"
    #styles={}
)
# About a project description using streamlit
if selected=="ABOUT":
    st.title("PROJECT DESCRIPTION")
    st.text('''This project leverages the EasyOCR library to recognize text on business cards and extracts the data into a SQL database and provides an intuitive interface for users to upload  extract, and modify business card data.''')
    st.caption("Streamlit")
    st.text('''A user-friendly UI built using Streamlit library, allowing users to interact with the application and perform data retrieval and analysis tasks.''')
    st.caption("Easy OCR")
    st.text('''The EasyOCR library extracts text from the uploaded image.''')
    st.caption("Python")
    st.text('''The programming language used for building the application and scripting tasks.''')
    st.caption("MySQL")
    st.text('''Migration of data from the data lake to a SQL database, allowing for efficient querying and analysis using SQL queries.''')
    st.caption("Visual Stdio Code")
    st.text('''Visual Studio Code is a code editor redefined and optimized for building and debugging modern web and cloud applications.''')
    #Extracting the image 
if selected=="UPLOAD & EXTRACT":
    st.subheader("upload a Image")
    
    #initialize ocr reader
    #with tempfile.TemporaryDirectory() as temp_dir:
    # Streamlit file uploader to upload an image
    image_file=st.file_uploader("upload Images",type=["png","jpg","jpeg","gif"])
    if image_file is not None:
    #display the image
        try:
            st.image(image_file,width=350,caption="uploaded Images")
            def IMG_to_TXT(path):
                Inp_Img= Image.open(path)
                Img_arr= np.array(Inp_Img)# converting image into array
                lang= easyocr.Reader(["en"]) #define reader language 
                text= lang.readtext(Img_arr, detail=0)
                return text, Inp_Img
            text,img=IMG_to_TXT(image_file)
    
      # If you want to save the image into a BytesIO stream (for example to manipulate it in memory)
            image_bytes=io.BytesIO()
            img.save(image_bytes,format='PNG')# Save the image to the BytesIO stream
            image_bytes.seek(0)# Go to the beginning of the stream after saving
            image_data=image_bytes.getvalue()
            
        except Exception as e:
            st.error(f"Error processing the image: {e}")

        def extract_text(resu,Img):
                    col={'CARDHOLDER_NAME':[],
                    'DESIGNATION':[],
                    'COMPANY_NAME':[],
                    'CONTACT':[],
                    'AREA':[],
                    'CITY':[],
                    'STATE':[],
                    'PINCODE':[],
                    'MAIL_ID':[],
                    'WEBSITE':[],"IMAGE": []}
                    print("extracted text:",resu)
                    data=[]
                    data = [i.strip() for i in resu if i.strip()]
                #To get image
                    image_bytes = io.BytesIO()
                    Img.save(image_bytes, format='PNG')  # Save the image to the BytesIO stream
                    col['IMAGE'].append(image_bytes.getvalue())
                    #col['IMAGE'].append(Img)
                #Extract cardholder name
                    col['CARDHOLDER_NAME'].append(data[0] if len(data)>0 else  col['CARDHOLDER_NAME'].append(None))
                #To get designation
                    col['DESIGNATION'].append(data[1] if len(data)> 1 else col['DESIGNATION'].append(None))
                #To get company_name
                    try:
                        if re.findall("^d.",data[-1]):
                            co1=data[7]+' '+data[9]
                            col['COMPANY_NAME'].append(co1)
                        elif re.findall("^A.",data[-1]):
                            co2=data[7]+' '+data[8]
                            col['COMPANY_NAME'].append(co2)
                        elif re.findall("^R.",data[-1]):
                            co3=data[6]+' '+data[8]
                            col['COMPANY_NAME'].append(co3)
                        elif re.findall("^I.",data[-2]):
                            co4=data[8]+' '+data[10]+' '+data[11]
                            col['COMPANY_NAME'].append(re.sub(r'[^a-zA-Z\s]', '',co4))
                        else:
                            col['COMPANY_NAME'].append(data[-1])
                    except Indexerror:
                        col['COMPANY_NAME'].append(None)
                    # To get contact
                    for item in range(len(data)):
                    #To get Contact
                        if '+' in data[item] or '-' in data[item]:
                            col['CONTACT'].append(data[item].strip())
                            if (len(col['CONTACT'])==2):
                                col['CONTACT']=col['CONTACT'][0]+","+col['CONTACT'][1]
                            elif not col['CONTACT']:
                                col['CONTACT'].append(None)
                    # To get AREA
                        try:
                            if re.findall(r"^[0-9].+[a-zA-Z]+",data[item]):
                                col['AREA'].append(data[item].split(',')[0].strip())
                                
                    # To get city
                            if re.findall(r'.+St , ([a-zA-z]).+',data[item]):
                                col['CITY'].append(re.sub(r'[^a-zA-Z\s]', '',data[item].split(',')[1].strip()))
                            elif 'St,,' in data[item]:
                                city_part = data[item].split('St,,')[1].strip()
                                city_name = city_part.split(',')[0].strip()
                                col['CITY'].append(re.sub(r'[^a-zA-Z\s]', '',city_name))
                            elif re.findall(r'^[E].*',data[item]):
                                col['CITY'].append(re.sub(r'[^a-zA-Z\s]', '',data[item].strip())) 
                    # To get state 
                            if re.findall(r'.+St,, .+, ([a-zA-z\s]+);',data[item]):
                                col['STATE'].append(re.sub(r'[^a-zA-Z\s]', '',data[item].split(',,')[1].split(',')[1].strip()))
                            elif re.findall(r'.+St , .+, ([a-zA-z\s]+);',data[item]):
                                col['STATE'].append(re.sub(r'[^a-zA-Z\s]', '',data[item].split(' ,')[1].split(',')[1].strip()))
                    # To get pincode
                            if data[item].isdigit():
                                col['PINCODE'].append(data[item].strip())
                            elif re.findall(r'[a-zA-Z]{9} +[0-9]',data[item]):
                                col['PINCODE'].append(data[item].split()[1].strip())
                                col['STATE'].append(re.sub(r'[^a-zA-Z\s]', '',data[item].split()[0].strip()))
                             
                   
                    # To get mail id
                            elif '@' in data[item]:
                                col['MAIL_ID'].append(data[item])
                    # To get website
                            elif 'www' in data[item] or 'wwW' in data[item] or 'Www' in data[item] or 'WWW' in data[item]:
                                col["WEBSITE"].append(data[item].lower())
                                if col['WEBSITE'][0]=='www':
                                    col['WEBSITE']=col['WEBSITE'][0]+ '.' + data[5]
                                #col['WEBSITE'].append(co) 

                        except Exception as e:
                            print(f"Error extracting fields: {e}")
                            print(f"Problematic data: {item}")    
                        
                    return col
    #Extracted the data in a corresponding column name
        table=extract_text(text,img)
        print(table)
    # Extracted data saved in a dataframe
        df=pd.DataFrame(table)
        st.write(df)
        if st.button("Upload to Datbase(SQL)"):
            values=df.values.tolist() # converted dataframe to list of values
            for row in values:
                email=row[8]
                check_query=("select 1 from card_details1 where MAIL_ID=%s")
                cur.execute(check_query,(email,))
                result=cur.fetchone()
                if result:
                    st.error("Data already saved")
                else:
                    insert_query='''insert ignore into card_details1(CARDHOLDER_NAME,DESIGNATION,COMPANY_NAME,CONTACT,AREA,CITY,STATE,PINCODE,MAIL_ID,WEBSITE,IMAGE)
                            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                
                    cur.executemany(insert_query,values)
                    mydb.commit()
                    st.success("New entry added successfully")
CARDHOLDER_NAME = ""
if selected=="MODIFY": 
    cur.execute("select CARDHOLDER_NAME from card_details1")
    re=cur.fetchall()
    names=[row[0] for row in re]
    selected_card=st.selectbox("select the card",names)
    if selected_card:
        cur.execute("select CARDHOLDER_NAME,DESIGNATION,COMPANY_NAME,CONTACT,AREA,CITY,STATE,PINCODE,MAIL_ID,WEBSITE from card_details1 where CARDHOLDER_NAME=%s" ,(selected_card,))
        result=cur.fetchone()
        if result:
            try:
                CARDHOLDER_NAME = st.text_input("CARDHOLDER_NAME", result[0])
                DESIGNATION = st.text_input("DESIGNATION", result[1])
                COMPANY_NAME=st.text_input("COMPANY_NAME",result[2])
                CONTACT=st.text_input("CONTACT",result[3])
                AREA=st.text_input("AREA",result[4])
                CITY=st.text_input("CITY",result[5])
                STATE=st.text_input("STATE",result[6])
                PINCODE=st.text_input('PINCODE',result[7])
                MAIL_ID=st.text_input("MAIL_ID",result[8])
                WEBSITE=st.text_input("WEBSITE",result[9])
            except:
                pass
            
            if st.button("UPDATE CHANGES"):
                try:
                    cur.execute(f"UPDATE card_details1 SET CARDHOLDER_NAME=%s, DESIGNATION=%s, COMPANY_NAME=%s, CONTACT=%s, AREA=%s, CITY=%s, STATE=%s, PINCODE=%s, MAIL_ID=%s, WEBSITE=%s WHERE CARDHOLDER_NAME=%s", 
                            (CARDHOLDER_NAME, DESIGNATION, COMPANY_NAME, CONTACT, AREA, CITY, STATE, PINCODE, MAIL_ID, WEBSITE, selected_card))
                    mydb.commit()
                    st.success("Updated successfully")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                
        else:

            st.error("No details found for the selected card.")
    else:
        st.warning("Please select a card.")
    if st.button("View the updated data"):
                        new=cur.execute("select * from card_details1")
                        fetch=cur.fetchall()
                        updated_df=pd.DataFrame(fetch,columns=["CARDHOLDER_NAME","DESIGNATION","COMPANY_NAME","CONTACT","AREA","CITY","STATE","PINCODE","MAIL_ID","WEBSITE","IMAGE"])
                        st.dataframe(updated_df)

if selected=="DELETE":
    cur.execute("select CARDHOLDER_NAME from card_details1")
    res=cur.fetchall()
    business_cards = {}
    for row in res:
                business_cards[row[0]] = row[0]
    select_card=st.selectbox("select the card",list(business_cards.keys()))
    
    if select_card:
        if st.button("DELETE"):
            try:
                cur.execute("delete from card_details1 where CARDHOLDER_NAME=%s", (select_card,))
                mydb.commit()
                st.success("DELETED SUCCESSFULLY")
            except Exception as e:
                    st.error(f"An error occurred: {e}")
    if st.button("View the deleted data"):
        new=cur.execute("select * from card_details1")
        fetch=cur.fetchall()
        updated_df=pd.DataFrame(fetch,columns=["CARDHOLDER_NAME","DESIGNATION","COMPANY_NAME","CONTACT","AREA","CITY","STATE","PINCODE","MAIL_ID","WEBSITE","IMAGE"])
        st.dataframe(updated_df)
        
