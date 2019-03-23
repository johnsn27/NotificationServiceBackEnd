import sqlite3
from flask import Flask, request, jsonify
import json
app = Flask(__name__)
from sendEmail import sendEmail

@app.after_request
def after_request(response):
   response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
   return response

@app.route('/watch-room',methods = ['POST', 'GET', 'OPTIONS'])
def watch_room():
   if request.method == 'POST':
      try:
         content = request.json
         conn = sqlite3.connect('BOOKING.db')
         c = conn.cursor()
         c.execute("SELECT COUNT(*) from WATCHED")
         watched_id = int(c.fetchone()[0]) + 1
         c.execute("INSERT INTO WATCHED (WatchedId,UserId,Capacity,StartTime,EndTime) VALUES (%i,%s,%s,'%s','%s')" % (watched_id, content['UserId'], content['Capacity'], content['StartTime'], content['EndTime']))
         conn.commit()
         conn.close()
         return jsonify(content), 200
      except:
         return 'Error', 500
   else:
      return 'Not POST'

@app.route('/delete-booking/<int:BookingId>', methods = ['DELETE', 'OPTIONS'])
def delete_booked_rooms(BookingId):
   conn = sqlite3.connect("BOOKING.db")
   conn.row_factory = sqlite3.Row
   c = conn.cursor()
   results = []
   c.execute("SELECT UserId FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
   UserIdList = [item[0] for item in c.fetchall()]
   if(UserIdList.__len__() > 0 ):
      for UserId in UserIdList:
         UserIdInt = int(UserId)
         c.execute("SELECT Email FROM USERS WHERE id='%s'" % UserIdInt)
         emailList = [item[0] for item in c.fetchall()]
         email = ''.join(emailList)
         sendEmail(email)
      else:
         print("Bookings table has no more results")

   
   try:
      c.execute("DELETE FROM BOOKINGS WHERE BookingId=%s" % BookingId)
      conn.commit()
      conn.close()
      return jsonify('')
   except:
         return 'Error', 500

@app.route('/watched-rooms')
def get_watched_rooms():
   conn = sqlite3.connect("BOOKING.db")
   conn.row_factory = sqlite3.Row
   results = []
   
   c = conn.cursor()
   c.execute("SELECT * from WATCHED")
   for item in c.fetchall():
      row = json.loads('{ "WatchedId":%s, "UserId":%s, "Capacity":%s, "StartTime":"%s", "EndTime":"%s"}' % (int(item[0]), int(item[1]), int(item[2]), str(item[3]), str(item[4])))
      results.append(row)
   
   rows = c.fetchall()
   return json.dumps(results)    

@app.route('/delete-watch/<int:WatchId>', methods = ['DELETE', 'OPTIONS'])
def delete_watched_rooms(WatchId):
   conn = sqlite3.connect("BOOKING.db")
   conn.row_factory = sqlite3.Row
   results = []
   
   c = conn.cursor()
   try:
      c.execute("DELETE FROM WATCHED WHERE WatchedId=%s" % WatchId)
      conn.commit()
      conn.close()
      return jsonify('')
   except:
         return 'Error', 500

if __name__ == '__main__':
   app.run()
