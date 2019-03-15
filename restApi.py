import sqlite3
from flask import Flask, request, jsonify
import json
app = Flask(__name__)

@app.after_request
def after_request(response):
   response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
   return response

@app.route('/user-bookings/<int:user>')
def get_bookings_by_user(user):
   conn = sqlite3.connect("BOOKING.db")
   conn.row_factory = sqlite3.Row
   results = []
   # Need to return room name, maybe change roomId? Also add meeting name?
   c = conn.cursor()
   c.execute("SELECT * from BOOKINGS WHERE UserId=%s" % user)
   for item in c.fetchall():
      c.execute("SELECT Location from ROOMS WHERE id=%s" % int(item[2]))
      location = str(c.fetchone()[0])
      c.execute("SELECT Name from ROOMS WHERE id=%s" % int(item[2]))
      name = str(c.fetchone()[0])
      row = json.loads('{ "BookingId":%s, "UserId":%s, "RoomId":%s, "StartTime":"%s", "EndTime":"%s", "Location": "%s", "RoomName": "%s"}' % (int(item[0]), int(item[1]), int(item[2]), str(item[3]), str(item[4]), location, name))
      results.append(row)
   
   return json.dumps(results)

@app.route('/user-watch-list/<int:user>')
def get_rooms_watched_by_user(user):
   conn = sqlite3.connect("BOOKING.db")
   conn.row_factory = sqlite3.Row
   results = []
   
   c = conn.cursor()
   c.execute("SELECT * from WATCHED WHERE UserId=%s" % user)
   for item in c.fetchall():
      row = json.loads('{ "WatchedId":%s, "UserId":%s, "Capacity":%s, "StartTime":"%s", "EndTime":"%s", "Location":"LOCATION PLACEHOLDER", "RoomName":"ROOM NAME PLACEHOLDER"}' % (int(item[0]), int(item[1]), int(item[2]), str(item[3]), str(item[4])))
      results.append(row)
   
   rows = c.fetchall()
   return json.dumps(results)

# Needs '' when using the params, the defaults can't have ''. Maybe use like for the name so it's a search but not 100% match
# This is messy, not sure how it would be in the front end if I did this so maybe need to do some ifs, or just make the default on the front end be the table names
@app.route('/meeting-rooms', defaults={'loc': 'Location', 'floor': 'Floor', 'cap': 0})
@app.route('/meeting-rooms/location/<loc>', defaults={'floor': 'Floor', 'cap': 0})
@app.route('/meeting-rooms/location/<loc>/floor/<floor>', defaults={'cap': 0})
@app.route('/meeting-rooms/location/<loc>/capacity/<int:cap>', defaults={'floor': 'Floor'})
@app.route('/meeting-rooms/location/<loc>/floor/<floor>/capacity/<int:cap>')
def find_meeting_room(loc, floor, cap):
   conn = sqlite3.connect("BOOKING.db")
   conn.row_factory = sqlite3.Row
   results = []
   
   c = conn.cursor()
   c.execute("SELECT * from ROOMS WHERE Location=%s AND Floor=%s AND Capacity>=%s" % (loc, floor, cap))
   for item in c.fetchall():
      row = json.loads('{ "id":%s, "Name":"%s", "Location":"%s", "Floor":"%s", "Capacity":%s}' % (int(item[0]), str(item[1]), str(item[2]), str(item[3]), int(item[4])))
      results.append(row)
   
   rows = c.fetchall()
   return json.dumps(results) 

# get rid of this - or keep it to make system look more complete as book room button will work
@app.route('/book-room',methods = ['POST', 'GET', 'OPTIONS'])
def book_room():
   if request.method == 'POST':
      try:
         content = request.json
         conn = sqlite3.connect('BOOKING.db')
         c = conn.cursor()
         c.execute("SELECT COUNT(*) from BOOKINGS")
         watched_id = int(c.fetchone()[0]) + 1
         c.execute("INSERT INTO BOOKINGS (BookingId,UserId,RoomId,StartTime,EndTime) VALUES (%i,%s,%s,'%s','%s')" % (watched_id, content['UserId'], content['RoomId'], content['StartTime'], content['EndTime']))
         conn.commit()
         conn.close()
         return jsonify(content), 200
      except:
         return 'Error', 500
   else:
      return 'Not POST'

# get rid of this
@app.route('/add-room',methods = ['POST', 'GET', 'OPTIONS'])
def watch_room():
   if request.method == 'POST':
      try:
         content = request.json
         conn = sqlite3.connect('BOOKING.db')
         c = conn.cursor()
         c.execute("SELECT COUNT(*) from ROOMS")
         watched_id = int(c.fetchone()[0]) + 1
         c.execute("INSERT INTO ROOMS (id,Name,Location,Floor,Capacity) VALUES (%i,'%s','%s','%s','%s')" % (watched_id, content['Name'], content['Location'], content['Floor'], content['Capacity']))
         conn.commit()
         conn.close()
         return jsonify(content), 200
      except:
         return 'Error', 500
   else:
      return 'Not POST'

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
