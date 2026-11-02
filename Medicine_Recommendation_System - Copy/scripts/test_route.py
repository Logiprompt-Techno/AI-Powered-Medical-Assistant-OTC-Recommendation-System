from flask import Flask, jsonify, session, send_file
import app as myapp
from datetime import datetime
from bson.objectid import ObjectId
import json
import traceback

with myapp.app.test_request_context('/user/history/download/123456789012345678901234'):
    try:
        from user.routes import download_pdf
        # Mock session
        session['user_id'] = '123456789012345678901234'
        download_pdf('123456789012345678901234')
        print('Route execution finished without 500.')
    except Exception as e:
        traceback.print_exc()
