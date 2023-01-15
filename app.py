import mysql.connector
import os
from dotenv import load_dotenv
from flask import Flask,render_template,jsonify,make_response,request,json, redirect
import time
import requests
from model.communicateWithS3 import communicateWithS3
from model.communicateWithRDS import communicateWithRDS
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

load_dotenv()
databaseName=os.getenv("databaseName")
pool_name=os.getenv("pool_name")

@app.route("/")
def index():
	return render_template("messageBoard.html")

@app.route('/api/messageBoard/content', methods=['POST'])
def handle_upload_content():
	textFromUser = request.form['text']
	image = request.files["image"]
	if image.content_type=="image/jpeg":
		# put image to s3, and get url of image with cloudfrond
		# put url of image and text to database
		imageName = str(uuid.uuid4()) + ".jpeg"
		try:
			s3Instance=communicateWithS3()
			s3Instance.uploadImage(imageName,image)
		except Exception as e:
			response = make_response(jsonify({"error":True,"message":"Can't upload to database."} ),500 )   
			response.headers["Content-Type"] = "application/json"
			return response
		urlOfImage=CLOUDFRONT_BASE_URL+imageName
		#Store data to database
		databasePoolInstance=communicateWithRDS(databaseName,pool_name)
		databasePoolInstance.InsertToTabel_messageBoard(textFromUser,urlOfImage)
		
		response = make_response(jsonify({"ok":True}),200 )   
		response.headers["Content-Type"] = "application/json"
		return response
	response = make_response(jsonify({"error":True,"message":"Can't store data to database."} ),400 )   
	response.headers["Content-Type"] = "application/json"
	return response

@app.route('/api/messageBoard/content', methods=['GET'])
def handle_get_contentFromRDS():
	#Get data from database
	try:
		databasePoolInstance=communicateWithRDS(databaseName,pool_name)
		contentFromRDS=databasePoolInstance.GetAllData_messageBoard()
	except Exception as e:
		response = make_response(jsonify({"error":True,"message":"communicate to database failed."} ),500 )   
		response.headers["Content-Type"] = "application/json"
		return response
	if contentFromRDS==-1:
		response = make_response(jsonify({"error":True,"message":"communicate to database failed."} ),500 )   
		response.headers["Content-Type"] = "application/json"
		return response
	response = make_response(jsonify({"data":contentFromRDS} ),200 )   
	response.headers["Content-Type"] = "application/json"
	return response
app.run(host="0.0.0.0",port=2000)