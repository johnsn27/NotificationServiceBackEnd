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
      c.execute("SELECT COUNT(*) from BOOKINGS WHERE BOOKINGS.RoomId=%s AND ((BOOKINGS.StartTime BETWEEN '%s' AND '%s') OR (BOOKINGS.EndTime BETWEEN '%s' AND '%s') OR ('%s' BETWEEN BOOKINGS.StartTime AND BOOKINGS.EndTime))" % (int(item[2]), str(item[4]), str(item[5]), str(item[4]), str(item[5]), str(item[4])))
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
         c.execute("SELECT COUNT(*) from BOOKINGS WHERE BOOKINGS.RoomId=%s AND ((BOOKINGS.StartTime BETWEEN '%s' AND '%s') OR (BOOKINGS.EndTime BETWEEN '%s' AND '%s') OR ('%s' BETWEEN BOOKINGS.StartTime AND BOOKINGS.EndTime))" % (int(item[0]), start, end, start, end, start))
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
         c.execute("SELECT COUNT(*) from BOOKINGS, WATCHED WHERE BOOKINGS.RoomId=%s AND ((BOOKINGS.StartTime BETWEEN '%s' AND '%s') OR (BOOKINGS.EndTime BETWEEN '%s' AND '%s') OR ('%s' BETWEEN BOOKINGS.StartTime AND BOOKINGS.EndTime))" % (content['RoomId'], content['StartTime'], content['EndTime'], content['StartTime'], content['EndTime'], content['StartTime']))
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
   bookingStartTimeList = [item[0] for item in c.fetchall()]
   for bookingStartTimeString in bookingStartTimeList:
      print(bookingStartTimeString)
      f = '%Y-%m-%d %H:%M:%S'
      BookingStartTime = datetime.datetime.strptime(bookingStartTimeString, f)

   c.execute("SELECT EndTime FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
   bookingEndTimeList = [item[0] for item in c.fetchall()]
   for bookingEndTimeString in bookingEndTimeList:
      print(bookingEndTimeString)
      f = '%Y-%m-%d %H:%M:%S'
      BookingEndTime = datetime.datetime.strptime(bookingEndTimeString, f)


   c.execute("SELECT RoomId FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
   RoomIdList = [item[0] for item in c.fetchall()]
   if(RoomIdList.__len__() > 0 ):
      for RoomId in RoomIdList:
         RoomIdInt = int(RoomId)
         print('RoomIdInt:')
         print(RoomIdInt)
         c.execute("SELECT Name FROM ROOMS WHERE id='%s'" % RoomIdInt)
         roomNameList = [item[0] for item in c.fetchall()]
         roomName = ''.join(roomNameList)
         print(roomName)
         c.execute("SELECT UserId FROM WATCHED WHERE RoomId='%s'" % RoomIdInt)
         WatchedUserIdList = [item[0] for item in c.fetchall()]
         for WatchedUserId in WatchedUserIdList:
            WatchedUserIdInt = int(WatchedUserId)
            print('WatchedUserIdInt:')
            print(WatchedUserIdInt)
            c.execute("SELECT StartTime FROM WATCHED WHERE RoomId='%s' AND UserId='%s'" % (RoomIdInt, WatchedUserIdInt))
            WatchedStartTimeList = [item[0] for item in c.fetchall()]
            for WatchedStartTimeString in WatchedStartTimeList:
               print(WatchedStartTimeString)
               f = '%Y-%m-%d %H:%M:%S'
               WatchedStartTime = datetime.datetime.strptime(WatchedStartTimeString, f)
            c.execute("SELECT EndTime FROM WATCHED WHERE RoomId='%s' AND UserId='%s'" % (RoomIdInt, WatchedUserIdInt))
            WatchedEndTimeList = [item[0] for item in c.fetchall()]
            for WatchedEndTimeString in WatchedEndTimeList:
               print(WatchedEndTimeString)
               f = '%Y-%m-%d %H:%M:%S'
               WatchedEndTime = datetime.datetime.strptime(WatchedEndTimeString, f)
            c.execute("SELECT UserId FROM BOOKINGS WHERE BookingId='%s'" % BookingId)
            BookingUserIdList = [item[0] for item in c.fetchall()]

   if(BookingUserIdList.__len__() > 0 ):
      for BookingUserId in BookingUserIdList:
         BookingUserIdInt = int(BookingUserId)
         c.execute("SELECT Email FROM USERS WHERE id='%s'" % BookingUserIdInt)
         emailList = [item[0] for item in c.fetchall()]
         email = ''.join(emailList)
         sendEmail(email, roomName, 'booking')
      else:
         print("Bookings table has no more results")
   if(WatchedUserIdList.__len__() > 0 ):
      for WatchedUserId in WatchedUserIdList:
         WatchedUserIdInt = int(WatchedUserId)
         c.execute("SELECT Email FROM USERS WHERE id='%s'" % WatchedUserIdInt)
         emailList = [item[0] for item in c.fetchall()]
         email = ''.join(emailList)
         if BookingStartTime == WatchedStartTime and BookingEndTime == WatchedEndTime:
            sendEmail(email, roomName, 'watched')
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
