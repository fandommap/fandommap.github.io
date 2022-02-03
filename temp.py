import sys
import os
from flask import Flask, render_template,request, jsonify,redirect,url_for,jsonify,flash
import mysql.connector as mysql
from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime
import glob, os

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = open("password.txt", "r").read(),
    database = "fandommap"
)