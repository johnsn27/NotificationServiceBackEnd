# NotificationServiceBackEnd

## REST API
Flask must be installed in order to start the API service:
```python
pip install flask
```
For database functionality to work within the API, the BOOKING.db database must have previously been created:
```python
python createDB.py
```
Finally, to start the API run:
```python
python restApi.py
```
The API will start on https://127.0.0.1:5000
### Endpoints
#### [/watch-room](https://127.0.0.1:5000/watch-room)
Accepts POST requests containing JSON, which is written to the database WATCHED table.
JSON format should match the following:
```
{
    WatchedId: 1,
    UserId: 1,
    Capacity: 10,
    StartTime: "2019-02-27 10:00:00",
    EndTime: "2019-02-27 11:00:00"
}
```
#### [/watched-rooms](https://127.0.0.1:5000/watched-rooms)
Accepts HTTP GET requests and returns JSON containing data from the database WATCHED table.
Can be used for testing that the /watch-room endpoint is writing to the database correctly.