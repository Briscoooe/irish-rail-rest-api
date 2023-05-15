An unofficial REST API replacement for the [Irish Rail Realtime API](http://api.irishrail.ie/realtime/). The current API returns XML across a series of inconsistently named SOAP endpoints and hasn't been updated since 2012. I used Flask to make a self-documenting OpenAPI REST API around it, making it easier to interact with and get a view of how the different endpoints relate to each other

Made using [APIFlask](https://apiflask.com/), deployed on [Fly.io](https://fly.io/).

# How does it work?
The wrapper acts as a pass-through to the SOAP API, so all the data is coming from the same place. The only difference is that the data is returned in JSON format and the endpoints are more RESTful.
Here's a summary of changes
- Endpoint names are more predictable and consistent
- All property names are changed to snake_case
- All date and time properties are converted to ISO 8601 format
- All enum values are converted to strings

# Breaking changes
Some query parameters and property names have been changed or removed completely
- Station `description` has been changed to `name`
- Search result `description_sp` has been removed
- Station type values are as follows: 
  - M has been changed to `mainline`
  - S has been changed to `stops`
  - D has been changed to `dart`
  - A was removed completely and is the default value