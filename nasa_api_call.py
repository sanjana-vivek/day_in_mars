import urllib3

def get_photos(picdate:str):
    http = urllib3.PoolManager()  # helps manage multiple connections to the NASA server
    resp = http.request("GET", f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={picdate}&api_key=Ma4Z36c1x4bJfZv8shYesLICBBEdafUbyTHFpEiQ")
    if resp.status == 200:
        photo_info = {}  # request() makes a request to NASA server for the data. Data comes back in the json(Javascript Object Notation) format. Called a api call
        photos = {}
        for p in resp.json()['photos']:
            cam = p['camera']['name']
            photo_info[cam] = photo_info.get(cam,0)+1
            if cam not in photos:
                photos[cam] = []
            photos[cam].append(p['img_src'])
        
        return photo_info, photos
    else:
        return None, None

# GET request - retrieve data
# POST request - to send data
# Permission to access (send/receive) the data - api key is used
'''
[
    {
    "id": 1205049,
    "sol": 3996,
    "camera": {
    "id": 22,
    "name": "MAST",
    "rover_id": 5,
    "full_name": "Mast Camera"
    },
    "img_src": "https://mars.nasa.gov/msl-raw-images/msss/03996/mcam/3996ML1049580141206777B00_DXXX.jpg",
    "earth_date": "2023-11-02",
    "rover": {
        "id": 5,
        "name": "Curiosity",
        "landing_date": "2012-08-06",
        "launch_date": "2011-11-26",
        "status": "active",
        "max_sol": 4003,
        "max_date": "2023-11-10",
        "total_photos": 686531,
        "cameras": [
                {
                "name": "FHAZ",
                "full_name": "Front Hazard Avoidance Camera"
                },
                {
                "name": "NAVCAM",
                "full_name": "Navigation Camera"
                },
                {
                "name": "MAST",
                "full_name": "Mast Camera"
                },
                {
                "name": "CHEMCAM",
                "full_name": "Chemistry and Camera Complex"
                },
                {
                "name": "MAHLI",
                "full_name": "Mars Hand Lens Imager"
                },
                {
                "name": "MARDI",
                "full_name": "Mars Descent Imager"
                },
                {
                "name": "RHAZ",
                "full_name": "Rear Hazard Avoidance Camera"
                }
            ]
        }
    }   
'''