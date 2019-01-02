import flask
from flask import request, jsonify
import requests
from tika import parser

import nltk, os, subprocess, code, glob, re, traceback, sys, inspect
from time import clock, sleep
from pprint import pprint
import json
import zipfile
import urllib

import textract

import PyPDF2

import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def convertRtfToText(path):
        return textract.process(path).decode("utf-8")


def convertDocxToText(path):
        return textract.process(path).decode("utf-8")


def convertOdtToText(path):
        return textract.process(path).decode("utf-8")

def convertPDFToText(path):
    print('called')
    text = ''
    file = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(file)
    pages = pdfReader.numPage

    for page in range(0,pages):
        pageObj = pdfReader.getPage(page)
        text = text + pageObj.extractText()

    return text

def convert_pdf_to_txt(path):
    print('called')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,password=password,caching=caching,check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

@app.route('/api/get', methods=['GET'])
def getText():


    if 'path' in request.args:
       path = request.args['path']

    # Parse data from file
    file_data = parser.from_file(path)
    # Get files text content
    text = file_data['content']

    return text

@app.route('/api/get-text', methods=['GET'])
def readFile():

        print(os.getcwd())

        if 'path' in request.args:
             fileName = request.args['path']
        print(fileName)
        extension = fileName.split(".")[-1]
        print(extension)
        if extension == "txt":
            f = open(fileName, 'r')
            string = f.read()
            f.close()
            return string
        elif extension == "doc":
                print('call doc')
                text = textract.process(fileName,extension='doc')
                text = text.decode('utf-8')
                print(text)
                return jsonify(text)
            #return subprocess.Popen(['antiword', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        elif extension == "docx":
            try:
                print('call docx')
                text = textract.process(fileName,extension='docx')
                text = text.decode('utf-8')
                print(text)
                return jsonify(text)
                #return convertDocxToText(fileName)
            except:
                return ''
                pass
        elif extension == "rtf":
           try:
               print('call rtf')
               text = convertRtfToText(fileName)
               text = {'text':text}
               print(text)
               return jsonify(text)
               #return convertRtfToText(fileName)
           except:
               return ''
               pass
        elif extension == "pdf":
            try:
                print('call pdf')
                text = textract.process(fileName, method='pdfminer')
                #print(text)
                text = text.decode('utf-8')                
                text = {'text':text}
                print(text)
                return jsonify(text)
            except:
               return ''
               pass
        elif extension == "odt":
            try:
                print('call odt')
                text = convertOdtToText(fileName)
                text = {'text':text}
                print(text)
                return jsonify(text)
                #return convertOdtToText(fileName)
            except:
                return ''
                pass
        else:
            print('Unsupported format')
            return ''


@app.route('/try', methods=['GET'])
def home():
    return "it's working"


app.run(host='0.0.0.0',port=3434,debug=True)