import urllib.request
import requests
import nsepython

print(nsepython.nse_get_index_list())
exit()

url = "https://www.nseindia.com/api/index-names"  # Replace with the actual URL you're accessing

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    # Process the response as needed
    print(response)
except urllib.error.HTTPError as e:
    if e.code == 301:
        redirected_url = e.headers.get("Location")
        if redirected_url:
            # Update the URL to the redirected location and retry the request
            req = urllib.request.Request(redirected_url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req)
            # Process the response as needed
            print(response.read())
    else:
        # Handle other HTTP error codes if necessary
        print("Error:", e)
except urllib.error.URLError as e:
    # Handle URL errors if necessary
    print("URL Error:", e)
