from flask import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# from textblob import TextBlob

from tensorflow.keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os


model = load_model('model_cat_dog.h5')
UPLOAD_FOLDER = './static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  

  
@app.route('/')  
def customer():  
   return render_template('page1.html')  
  
@app.route('/success',methods = ['POST', 'GET'])  
def print_data():
	f = request.files['img']
	path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
	f.save(path)
	#f.save(secure_filename(f.filename))
	#return 'file uploaded successfully'
	fn=path

	test_image = image.load_img(fn, target_size = (64,64))
	test_image = image.img_to_array(test_image)
	test_image = np.expand_dims(test_image, axis = 0)
	result = model.predict(test_image)
	# training_set.class_indices
	if result[0][0] == 1:
		prediction = 'DOG'
	else:
		prediction = 'CAT'
	#return prediction
	return render_template('page2.html', result = f.filename, pred=prediction)

if __name__ == '__main__':  
   app.run(debug = True)