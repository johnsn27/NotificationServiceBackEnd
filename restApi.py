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
   c = conn.cursor()
   c.execute("SELECT * from BOOKINGS WHERE UserId=%s" % user)
   for item in c.fetchall():
      c.execute("SELECT Location from ROOMS WHERE id=%s" % int(item[2]))
      location = str(c.fetchone()[0])
      c.execute("SELECT Name from ROOMS WHERE id=%s" % int(item[2]))
      room_name = str(c.fetchone()[0])
      row = json.loads('{ "BookingId":%s, "UserId":%s, "RoomId":%s, "MeetingName":"%s", "StartTime":"%s", "EndTime":"%s", "Location": "%s", "RoomName": "%s"}' % (int(item[0]), int(item[1]), int(item[2]), str(item[3]), str(item[4]), str(item[5]), location, room_name))
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
      c.execute("SELECT Location from ROOMS WHERE id=%s" % int(item[2]))
      location = str(c.fetchone()[0])
      c.execute("SELECT Name from ROOMS WHERE id=%s" % int(item[2]))
      name = str(c.fetchone()[0])
      c.execute("SELECT Building from ROOMS WHERE id=%s" % int(item[2]))
      building = str(c.fetchone()[0])
      c.execute("SELECT COUNT(*) from BOOKINGS WHERE BOOKINGS.RoomId=%s AND ((BOOKINGS.StartTime >= '%s' AND BOOKINGS.StartTime < '%s') OR (BOOKINGS.EndTime > '%s' AND BOOKINGS.EndTime < '%s') OR ('%s' >= BOOKINGS.StartTime AND '%s' < BOOKINGS.EndTime))" % (int(item[2]), str(item[4]), str(item[5]), str(item[4]), str(item[5]), str(item[4]), str(item[4])))
      if int(c.fetchone()[0]) == 0:
         availability = 'Available'
      else:
         availability = 'Unavailable'
      row = json.loads('{ "WatchedId":%s, "UserId":%s, "RoomId":%s, "Capacity":%s, "StartTime":"%s", "EndTime":"%s", "Location":"%s", "RoomName":"%s", "Building":"%s", "Availability":"%s"}' % (int(item[0]), int(item[1]), int(item[2]), int(item[3]), str(item[4]), str(item[5]), location, name, building, availability))
      results.append(row)
   
   return json.dumps(results)

@app.route('/meeting-rooms',methods = ['GET', 'OPTIONS'])
def find_meeting_room():
   conn = sqlite3.connect("BOOKING.db")
   conn.row_factory = sqlite3.Row
   results = []
     
   c = conn.cursor()
   if request.args:
      content = request.args
      name = ("'%s'" % content.get('name').replace('%20', ' ')) if content.get('name') else 'Name'
      loc = ("'%s'" % content.get('location').replace('%20', ' ')) if content.get('location') else 'Building'
      floor = (content.get('floor')) if content.get('floor') else 'Floor'
      cap = ("'%s'" % content.get('capacity')) if content.get('capacity') else 0
      start = (content.get('start')) if content.get('start') else '9999-01-01 00:00:00'
      end = (content.get('end')) if content.get('end') else '9999-01-01 00:00:00'
      show_unavailable = (content.get('show_unavailable')) if content.get('show_unavailable') else 'false'
      c.execute("SELECT * from ROOMS WHERE Name=%s AND Building=%s AND Floor=%s AND Capacity>=%s" % (name, loc, floor, cap))
   else:
      c.execute("SELECT * from ROOMS")
      start = '9999-01-01 00:00:00'
      end = '9999-01-01 00:00:00'
      show_unavailable = 'false'
   try:
      for item in c.fetchall():
         c.execute("SELECT COUNT(*) from BOOKINGS WHERE BOOKINGS.RoomId=%s AND ((BOOKINGS.StartTime >= '%s' AND BOOKINGS.StartTime < '%s') OR (BOOKINGS.EndTime > '%s' AND BOOKINGS.EndTime < '%s') OR ('%s' >= BOOKINGS.StartTime AND '%s' < BOOKINGS.EndTime))" % (int(item[0]), start, end, start, end, start, start))
         if int(c.fetchone()[0]) == 0:
            availability = 'Available'
         else:
            availability = 'Unavailable'
         if not (show_unavailable == 'false' and availability == 'Unavailable'):
            row = json.loads('{ "id":%s, "Name":"%s", "Location":"%s", "Floor":"%s", "Capacity":%s, "Building":"%s", "Availability":"%s"}' % (int(item[0]), str(item[1]), str(item[2]), str(item[3]), int(item[4]), str(item[5]), availability))
            results.append(row)
   except Exception as e:
      print(e)
      return '', 500
   
   return json.dumps(results) 

@app.route('/book-room',methods = ['POST', 'GET', 'OPTIONS'])
def book_room():
   if request.method == 'POST':
      try:
         content = request.json
         conn = sqlite3.connect('BOOKING.db')
         c = conn.cursor()
         c.execute("SELECT COUNT(*) from BOOKINGS WHERE BOOKINGS.RoomId=%s AND ((BOOKINGS.StartTime >= '%s' AND BOOKINGS.StartTime < '%s') OR (BOOKINGS.EndTime > '%s' AND BOOKINGS.EndTime < '%s') OR ('%s' >= BOOKINGS.StartTime AND '%s' < BOOKINGS.EndTime))" % (content['RoomId'], content['StartTime'], content['EndTime'], content['StartTime'], content['EndTime'], content['StartTime'], content['StartTime']))
         if int(c.fetchone()[0]) == 0:
            c.execute("SELECT COUNT(*) from BOOKINGS")
            booking_id = int(c.fetchone()[0]) + 1
            c.execute("INSERT INTO BOOKINGS (BookingId,UserId,RoomId,Name,StartTime,EndTime) VALUES (%i,'%s','%s','%s','%s','%s')" % (booking_id, content['UserId'], content['RoomId'], content['Name'], content['StartTime'], content['EndTime']))
            conn.commit()
            conn.close()
            return jsonify(content), 200
         else:
            return jsonify('Room unavailable'), 500
      except Exception as e:
         print(e)
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
         c.execute("INSERT INTO WATCHED (WatchedId,UserId,RoomId,Capacity,StartTime,EndTime) VALUES (%i,%s,%s,%s,'%s','%s')" % (watched_id, content['UserId'], content['RoomId'], content['Capacity'], content['StartTime'], content['EndTime']))
         conn.commit()
         conn.close()
         return jsonify(content), 200
      except Exception as e:
         print(e)
         return 'Error', 500
   else:
      return 'Not POST'

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
