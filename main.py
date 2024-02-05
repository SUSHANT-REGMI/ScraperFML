from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import glob
from bing_image_downloader import downloader
# from keras.preprocessing.image import ImageDataGenerator
import zipfile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///automationDB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Automate(db.Model):
  sno = db.Column(db.Integer, primary_key=True)
  title_name = db.Column(db.String(20), nullable=False)
  second_name = db.Column(db.String(20))
  
  third_name = db.Column(db.String(20))
  fourth_name = db.Column(db.String(20))

  

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method=='POST':
        
        global category, alternative_1, alternative_2, alternative_3
        category = request.form['category']
        alternative_1 = request.form['searchtexts1']
        alternative_2 = request.form['searchtexts2']
        alternative_3 = request.form['searchtexts3']
        
        list_of_all_the_database_categories = []
       
        connector = sqlite3.connect('automationDB.db')
        connector_cursor = connector.cursor()
        category_column_tuple = connector_cursor.execute("""select title_name from Automate""") 
        
        print(category_column_tuple)
        
        for i in category_column_tuple:
            real_list = list(i)
            for j in real_list:
                k = j.replace('(','').replace("'",'').replace(")",'')
                list_of_all_the_database_categories.append(k)
        print(list_of_all_the_database_categories)
        if category in list_of_all_the_database_categories:
            print("This one's already in the database, go to downloads inorder to download the images")
        # example = Automate(title_name="category", second_name = "alternative_1", third_name = "alternative_2", fourth_name = "alternative_3" )
       
        else:
          example = Automate(title_name=category, second_name = alternative_1, third_name = alternative_2, fourth_name = alternative_3 )
          db.session.add(example)
          db.session.commit()
  print("I am running")
  allTodo = Automate.query.all() 
 
  return render_template('index.html', allTodo=allTodo)


contents = sqlite3.connect('automationDB.db')
content = contents.cursor()

@app.route('/downloads', methods=['GET', 'POST'])
def downloads():
  return render_template('downloads.html')

@app.route('/guide', methods=['GET', 'POST'])
def guide():
  return render_template('guide.html')
# content.execute('delete from automate where sno between 1 and 84')
def read_and_exec():
  # content.execute('SELECT * FROM AUTOMATE')

    last_row_tuple = content.execute('select * from automate').fetchall()[-1]
    global last_row 
    last_row = list(last_row_tuple)

    for i in range(4,1,-1):
      if last_row[i] == "":
        last_row.pop()

# with open('content.json') as f:
#     data = json.load(f)
    try:
      os.mkdir("C:\\Users\\susha\\OneDrive\\Desktop\\Automation Project\\Content Images\\Standard Images\\"+last_row[1]+" Images\\")
    # for value in values:
      os.environ['PATH'] += r"C:/Users/susha/OneDrive/Desktop/Automation Project"
      
      for x in range(1,len(last_row)):  
          options = webdriver.ChromeOptions()
          options.add_experimental_option('excludeSwitches', ['enable-logging'])
          driver = webdriver.Chrome(options=options)

          driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')
          # *[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
          my_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
          my_element.send_keys(last_row[x])
          my_element.send_keys(Keys.ENTER)

          # xpath = '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img'
          # last_height = driver.execute_script('return document.body.scrollHeight')

          for i in range(1,25):
            sc_content = "C:\\Users\\susha\\OneDrive\\Desktop\\Automation Project\\Content Images\\Standard Images\\"+last_row[1]+" Images\\"+last_row[x]+" ("+ str(i)+ ").png"
            driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot(sc_content)
      resize_batch_images()
          # time.sleep(10)
          # driver.implicitly_wait(5)
    except Exception as e:
      
      print(f"This items' image collection already exists. i.e {e.args}")


def resize_batch_images():
    count = 1
    count1 = 1
    image_list = []
    resolution1_list = []
    resolution2_list = []
    link_address = "C:/Users/susha/OneDrive/Desktop/Automation Project/Content Images/Standard Images/"+last_row[1]+" Images/*.png"
    link_address2 = "C:/Users/susha/OneDrive/Desktop/Automation Project/Content Images/Validation Images Unresized/"+last_row[1]+"/*.jpg"
    # print(link_address)
    os.mkdir("C:\\Users\\susha\\OneDrive\\Desktop\\Automation Project\\Content Images\\Validation Images Unresized\\"+last_row[1]+"\\")
    os.mkdir("C:\\Users\\susha\\OneDrive\\Desktop\\Automation Project\\Content Images\\Resized Images\\"+last_row[1]+" Images\\")
    os.mkdir("C:\\Users\\susha\\OneDrive\\Desktop\\Automation Project\\Content Images\\Validation Images Resized\\"+last_row[1]+" Images\\")
    for filename in glob.glob(link_address):
      
      img = Image.open(filename)
      width, height = img.size
      
      resolution1_list.append(width)
      resolution2_list.append(height)
      image_list.append(img)
      
      # standard_avg_height = sum(resolution2_list)/len(resolution2_list)
      # standard_avg_width = sum(resolution1_list)/len(resolution1_list)
    
    standard_max_width = max(resolution1_list)
    standard_max_height = max(resolution2_list)

    for filename in glob.glob(link_address):
      img = Image.open(filename)
      resizedImg = img.resize((int(standard_max_width), int(standard_max_height)))
      global resized_image_folder_address 
      resized_image_folder_address = "C:/Users/susha/OneDrive/Desktop/Automation Project/Content Images/Resized Images/"+last_row[1]+" Images/"
      resized_image_address = "C:/Users/susha/OneDrive/Desktop/Automation Project/Content Images/Resized Images/"+last_row[1]+" Images/"+last_row[1]+" ("+ str(count)+ ").png"
      resizedImg.save(resized_image_address)
      count += 1
    
    downloader.download(last_row[1], limit = 6, output_dir = 'C:/Users/susha/OneDrive/Desktop/Automation Project/Content Images/Validation Images Unresized/')
    print("Nothing runs after this")
    # validation_image_resizer(standard_max_width, standard_max_height)

    for filenamez in glob.glob(link_address2):
      # print(filenamez)
      img = Image.open(filenamez)
      # print("here 1")
      resizedImg = img.resize((int(standard_max_width), int(standard_max_height)))
      # print("here 2")
      resized_image_address = "C:/Users/susha/OneDrive/Desktop/Automation Project/Content Images/Validation Images Resized/"+last_row[1]+" Images/"+last_row[1]+" ("+ str(count1)+ ").png"
      # print("here 3")
      resizedImg.save(resized_image_address)
      # print("here 4")
      count1 += 1



if __name__ == "__main__":
  app.run()
  read_and_exec()
  



