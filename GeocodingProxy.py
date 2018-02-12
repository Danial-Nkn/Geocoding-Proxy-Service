import requests
from flask import Flask, request

GOOGLE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
HERE_URL = 'http://geocoder.cit.api.here.com/6.2/geocode.json'
HERE_APP_ID = 'Mbmdr17KU5cNuYNlYlKI'
HERE_APP_CODE = 'g_gAORxfN4j7U7SxUKGFqg'

app = Flask(__name__)


@app.route('/resolve', methods=['GET', 'POST'])
def run():
    # See if there has been a GET request first
    # Go for a POST request if that failed
    if request.method == 'GET':
        result = request.args['address']
    elif request.method == 'POST':
        result = request.form['address']

    location = request_address(result)

    print(location['lat'])
    print(location['lng'])
    result = 'Coordinates are: {0}, {1}'.format(location['lat'], location['lng'])
    return result


def request_address(address):
    
    if len(address) < 1 : print ('Address is not valid')
    
    else: 
        
        try:
            params = {'sensor': 'false', 'address': ""}
            googleReq = requests.get(GOOGLE_URL, params=params)
            g_results = googleReq.json()['results']
           
            g_latlng = g_results[0]['geometry']['location']
            g_latlng['lat'], g_latlng['lng']
            final_latlng= g_latlng
            print(g_latlng)
                
    
        except: 
            params = {'app_id': HERE_APP_ID, 'app_code': HERE_APP_CODE, 'searchtext': address}
            hereReq = requests.get(HERE_URL, params=params)
    
            # This will parse the response to get the lat, long
            h_results = hereReq.json()['Response']['View'][0]['Result']
            h_latlng = h_results[0]['Location']['NavigationPosition'][0]
    
            # Reformat the response
            final_latlng = {'lat': h_latlng['Latitude'], 'lng': h_latlng['Longitude']}
            print (final_latlng)

        return final_latlng
             
if __name__ == "__main__":
    
    app.run()
        
