import base64 
import os

def transform(picture_name):
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), picture_name)
    open_pic = open(image_path, 'rb') 
    b64str = base64.b64encode(open_pic.read()) 
    open_pic.close()
    write_data = 'img = "%s"' % b64str.decode() 
    f = open('%s.py' % picture_name.replace('.', '_'), 'w+') 
    f.write(write_data) 
    f.close()
if __name__ == '__main__': 
    pics = ["confrim_normal.png", "confrim_secrect.png", "Anchor_point.png", "normal2.png", "secrect2.png","reset_full_size.png","reset_confrim.png"] 
    for i in pics: 
        transform(i) 
        print("ok")





