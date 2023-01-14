import mysql.connector
import os
from dotenv import load_dotenv
from flask import Flask,render_template,jsonify,make_response,request,json, redirect
import time
import requests
from communicateWithS3 import communicateWithS3
from flask_cors import CORS
import uuid

app=Flask(
			__name__,
			static_folder="static",
			static_url_path="/"
		)
CORS(app)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CLOUDFRONT_BASE_URL = "https://myawss3bucket20230110.s3.us-west-2.amazonaws.com/"


@app.route("/")
def index():
	return render_template("messageBoard.html")

@app.route('/api/user/image', methods=['POST'])
def handle_upload_image():
	textFromUser = request.form['text']
	image = request.files["image"]
	if image.content_type=="image/jpeg":
		# put image to s3, and get url of image with cloudfrond
		# put url of image and text to database
		imageName = str(uuid.uuid4()) + ".jpeg"
		s3Instance=communicateWithS3()
		s3Instance.uploadImage(imageName,image)
		urlOfImage=CLOUDFRONT_BASE_URL+imageName
		#Store data to database

		response = make_response(jsonify({"ok":True}),200 )   
		response.headers["Content-Type"] = "application/json"
		return response
	response = make_response(jsonify({"error":True,"message":"Can't store data to database."} ),400 )   
	response.headers["Content-Type"] = "application/json"
	return response

app.run(host="0.0.0.0",port=3000)