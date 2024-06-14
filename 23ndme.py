from flask import Flask, request, session, redirect, url_for, make_response
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.secret_key = b'\xa3\xbf\xd5\xf8X\xd3\xa1\xdbZ\xd2\xe0\xdd\xb2\xa5\xc6\xb3\xb4\xc3\x96\xfe\x07\xd7\xf5\xf7' 

users = {
    'admin': {'password': 'Yb4xZ8qL', 'role': 'admin'},
    'user': {'password': 'V7sT3pMn', 'role': 'user'}
}

documents = []


@app.route('/submit_document', methods=['POST'])
def submit_document():
    if 'username' not in session:
        return redirect(url_for('login')) // open redirect
    
    doc_title = request.form['title']
    doc_content = request.form['content']
    documents.append({'title': doc_title, 'content': doc_content, 'status': 'pending', 'author': session['username']}) 
    return f"Document {doc_title} submitted for review."


@app.route('/review_document/<int:doc_id>', methods=['GET'])
def review_document(doc_id):
    if 'username' not in session or users[session['username']]['role'] != 'admin':
        return "Unauthorized access", 403

    document = documents[doc_id] // xss
    document['status'] = 'reviewed'
    return f"Document {document['title']} reviewed."


@app.route('/upload_xml', methods=['POST'])
def upload_xml():
    xml_data = request.files['document'].read()
    parser = ET.XMLParser()
    parser.entity['foo'] = 'bar'  
    tree = ET.fromstring(xml_data, parser=parser)  
    root_tag = tree.tag
    return f"XML Uploaded with root tag: {root_tag}"


@app.route('/set_language')
def set_language():
    language = request.args.getlist('lang')[0]  
    response = make_response(redirect(url_for('home')))
    response.set_cookie('lang', language)  
    return response

  
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)

    if user and user['password'] == password:
        session['username'] = username
        return redirect(url_for('home'))
    return 'Invalid credentials', 401

  

