# Spotaya API
### The Spotaya API is a backend service for the Spotaya application, which helps friends plan their outings together by finding nearby places of interest based on the type of activity they want to do in a specific area. This API integrates with the Google Places API to provide accurate and up-to-date information about various places of interest.

# Getting Started
#### To use the Spotaya API, you will need an API key from the Google Places API. Follow these steps to get started:

1- Sign up for a Google Cloud Platform (GCP) account if you don't have one already.
2- Create a new project in the GCP Console.
3- Enable the Google Places API for your project and generate an API key.
4- Make sure to restrict your API key usage to secure it properly (e.g., limit usage to specific IP addresses, restrict API access to required services only).

# Api endpoints
  - /nearby-places
    - this endpoint take this set of arguments: 
      `{
      "lng": "30.0706",
      "lat": "31.3558",
      "types": "gym|shoe_store", 
      "from_time": "18:00:00", 
      "to_time": "22:00:00"
      }`
     - then returns a plan for the user as request:
     `[
      {
          "activity_duration": "2:00:00",
          "activity_type": "gym",
          "location": "https://www.google.com/maps/search/?api=1&query=31.3103671,30.0620059",
          "name": "Max Gym",
          "photo": "http://spotaya.pythonanywhere.com/media/uploads/ChIJGaUkEd7R9RQRF1oeRJTAhQM.jpg",
          "types": [
              "gym",
              "point_of_interest",
              "health",
              "establishment"
          ]
      },
      {
          "activity_duration": "2:00:00",
          "activity_type": "shoe_store",
          "location": "https://www.google.com/maps/search/?api=1&query=31.2971723,30.0610479",
          "name": "طارق و منصور للأحذية",
          "photo": null,
          "types": [
              "shoe_store",
              "store",
              "point_of_interest",
              "establishment"
          ]
      }
  ]`
