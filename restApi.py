import sqlite3
from flask import Flask, request, jsonify
import json
import datetime
app = Flask(__name__)
from sendEmail import sendEmail

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

@app.route('/delete-booking/<int:BookingId>', methods = ['DELETE', 'OPTIONS'])
def delete_booked_rooms(BookingId):
   conn = sqlite3.connect("BOOKING.db")
   conn.row_factory = sqlite3.Row
   c = conn.cursor()
   BookingUserIdList = []
   WatchedUserIdList = []

   c.execute("SELECT StartTime FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
   BookingStartTimeDateList = [item[0] for item in c.fetchall()]
   BookingStartTimeDateString =""
   BookingEndTimeDateString =""
   for BookingStartTimeDateString in BookingStartTimeDateList:
      f = '%Y-%m-%d %H:%M:%S'
      BookingStartTimeDate = datetime.datetime.strptime(BookingStartTimeDateString, f)
      BookingStartTime = BookingStartTimeDate.strftime('%H:%M:%S')
      BookingDate = BookingStartTimeDate.strftime('%Y-%m-%d')

   c.execute("SELECT EndTime FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
   BookingEndTimeDateList = [item[0] for item in c.fetchall()]
   for BookingEndTimeDateString in BookingEndTimeDateList:
      f = '%Y-%m-%d %H:%M:%S'
      BookingEndTimeDate = datetime.datetime.strptime(BookingEndTimeDateString, f)
      BookingEndTime = BookingEndTimeDate.strftime('%H:%M:%S')

   c.execute("SELECT RoomId FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
   RoomIdList = [item[0] for item in c.fetchall()]
   if(RoomIdList.__len__() > 0 ):
      for RoomId in RoomIdList:
         RoomIdInt = int(RoomId)

         c.execute("SELECT Name FROM ROOMS WHERE id='%s'" % RoomIdInt)
         roomNameList = [item[0] for item in c.fetchall()]
         roomName = ''.join(roomNameList)

         c.execute("SELECT UserId FROM WATCHED WHERE RoomId='%s'" % RoomIdInt)
         WatchedUserIdList = [item[0] for item in c.fetchall()]
         for WatchedUserId in WatchedUserIdList:
            WatchedUserIdInt = int(WatchedUserId)

            c.execute("SELECT StartTime FROM WATCHED WHERE RoomId='%s' AND UserId='%s'" % (RoomIdInt, WatchedUserIdInt))
            WatchedStartTimeDateList = [item[0] for item in c.fetchall()]
            for WatchedStartTimeDateString in WatchedStartTimeDateList:
               dateTimeFormat = '%Y-%m-%d %H:%M:%S'
               WatchedStartTimeDate = datetime.datetime.strptime(WatchedStartTimeDateString, dateTimeFormat)
               WatchedStartTime = WatchedStartTimeDate.strftime('%H:%M:%S')
               WatchedDate = WatchedStartTimeDate.strftime('%Y-%m-%d')
               
            c.execute("SELECT EndTime FROM WATCHED WHERE RoomId='%s' AND UserId='%s'" % (RoomIdInt, WatchedUserIdInt))
            WatchedEndTimeDateList = [item[0] for item in c.fetchall()]
            for WatchedEndTimeDateString in WatchedEndTimeDateList:
               f = '%Y-%m-%d %H:%M:%S'
               WatchedEndTimeDate = datetime.datetime.strptime(WatchedEndTimeDateString, f)
               WatchedEndTime = WatchedEndTimeDate.strftime('%H:%M:%S')
            c.execute("SELECT UserId FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
            BookingUserIdList = [item[0] for item in c.fetchall()]

   if(BookingUserIdList.__len__() > 0 ):
      for BookingUserId in BookingUserIdList:
         BookingUserIdInt = int(BookingUserId)
         c.execute("SELECT Email FROM USERS WHERE id='%s'" % BookingUserIdInt)
         emailList = [item[0] for item in c.fetchall()]
         email = ''.join(emailList)
         sendEmail(email, roomName, 'booking',  BookingStartTime, BookingEndTime, BookingDate)
      else:
         print("Bookings table has no more results")
   if(WatchedUserIdList.__len__() > 0 ):
      for WatchedUserId in WatchedUserIdList:
         WatchedUserIdInt = int(WatchedUserId)
         c.execute("SELECT Email FROM USERS WHERE id='%s'" % WatchedUserIdInt)
         emailList = [item[0] for item in c.fetchall()]
         email = ''.join(emailList)
         if WatchedStartTimeDate >= BookingStartTimeDate and WatchedEndTimeDate <= BookingEndTimeDate and WatchedStartTimeDate < BookingEndTimeDate and WatchedEndTimeDate > BookingStartTimeDate:
            sendEmail(email, roomName, 'watched', WatchedStartTime , WatchedEndTime, WatchedDate)
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
