An unofficial REST API wrapper for the [Irish Rail Realtime API](http://api.irishrail.ie/realtime/). The current API returns XML across a series of inconsistently named SOAP endpoints and it's not very user-friendly. I used Flask to make a self-documenting OpenAPI REST API around it, making it easier to interact with and get a view of how the different endpoints relate to each other

Made using [APIFlask](https://apiflask.com/)

# How does it work?
The wrapper acts as a pass-through to the SOAP API, so all the data is coming from the same place. The only difference is that the data is returned in JSON format and the endpoints are more RESTful.
Here's a summary of changes
- Endpoint names are more predictable and consistent
- All property names are changed to snake_case
- All date and time properties are converted to ISO 8601 format
- All enum values are converted to strings
