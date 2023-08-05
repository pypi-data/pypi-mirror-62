# Unleashed [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Canadian Mental Health Association](https://i.imgur.com/GvXBeY4.png)](https://cmha.ca/donate)
A Python library to interact with the Unleashed API. This is based off of Jonathan Sokolowski's original module but intended to be maintained and updated for future versions of Python.

# Documentation
As it stands, the module is currently quite basic. It currently only allows you to pull data from an endpoint (but allows for specifications.)

**Install the module**

`pip install Unleashed`

**Import the module**

`from Unleashed import Unleashed`

**Set up a client**

`Client = Unleashed.Client(api_key, api_id)`

**Request an endpoint**

This will return JSON data from a specified endpoint. It can be iterated through like a Python dictionary.

`data = Client.request_endpoint("SalesOrders")`

**Request an endpoint with specifications**

`data = Client.request_endpoint("SalesOrders", "pageSize=50&startDate=2019-11-20")`

**Request only the items from an endpoint**

`data = Client.return_items("SalesOrders", "pageSize=50&startDate=2019-11-20")`

**Request only the pagination from an endpoint**

`data = Client.return_pagination("SalesOrders", "pageSize=50&startDate=2019-11-20")`

**Request data and specify a page**

`data = Client.request_endpoint("SalesOrders", "pageSize=50&startDate=2019-11-20", 2)`

# Acknowledgements
[Jonathan Sokolowski](https://github.com/jsok/) for the original Unleashed module. You can view it [here.](https://github.com/jsok/unleashed)
