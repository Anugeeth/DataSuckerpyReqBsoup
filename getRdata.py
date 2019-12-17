import base64
import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
or_id = ["56795","58013"] //reg no goes here
f2 = open("info.html","w")
f1 = open("data.html","rt");
f1.close
file_wrap = BeautifulSoup(f1.read(),"lxml");
for id_ in or_id:
    ebytes = base64.b64encode(id_.encode("utf-8"))
    ec_id = str(ebytes)
    pic_page = requests.get("#/view_album.php/?"+"id="+ec_id) // # --> parent url 
    layout_data = requests.post('#', params = {'id':ec_id})
    contact_data = requests.post('#', params = {'id':id_})
    pic_parse = BeautifulSoup(pic_page.text,"lxml")
    if len(pic_parse.select("#imageBox"))!=0:
        img_tag = pic_parse.select("#imageBox")[0].img
        pic_loc = img_tag['src']
    else:
        img_tag = BeautifulSoup('<img src="photos/not_available_f.jpg"/>',"lxml")
        pic_loc = "photos/not_available_f.jpg"
    if (not os.path.isfile(pic_loc)):
        pic_link = "#" + str(pic_loc)
        pic_data = requests.get(pic_link)
        i = Image.open(BytesIO(pic_data.content))
        i.save(pic_loc)
    layout_parse = BeautifulSoup(layout_data.text,"lxml")
    contact_parse = BeautifulSoup(contact_data.text,"lxml")
    contact_table = contact_parse.body.table.contents[5]
    table = layout_parse.body.table
    table.contents[3].td.insert(0,img_tag)
    table.append(contact_table)
    file_wrap.html.body.append(table)
f2.write(str(file_wrap))
f2.close
