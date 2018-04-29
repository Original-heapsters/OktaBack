# CACHAR Back End

## Technologies Used
  * Python
    * Flask
    * SQLAlchemy
  * Heroku

## Hurdles
  * Could not connect to an ec2 instance from UCLA network, had to transplant app to heroku
  * First time working with a vanilla SQLAlchemy, took a while to learn

## Basic Architecture
We wanted to use flask purely as an api server so we built out the following endpoints. Unfortunately we were not able to execute the /nearby endpoint how we wanted :(.
```
/user
  GET
    Retrieved user information from the database
  POST
    Stored user information fetched from okta into local db
```
```
/place
  POST
    Allowed user to place an asset, given any coordinates and any asset
```
```
/found
  GET
    Retrieved an asset by its ID for the front end to display
```
```
/nearby
  GET
    Based on current reported location, retrieve all assets nearby for the front end to display
```
```
/mark
  POST
    Allowed a user to leave their mark on a asset dropped in the world, similar to signing a guestbook
```

## Data Models

```json
// USER
{
"id":"UUID",
"firstName":"STRING",
"lastName":"STRING",
"radiusSettings":"STRING"
}
```

```json
// ASSET
{
"id":"UUID",
"owner":"User.id",
"link":"URL",
"type":"ENUM",
"latlon":"STRING,STRING",
"markedList":[MARK]
}
```

```json
// MARK
{
"id":"UUID",
"user":"User.id",
"asset":"Asset.id",
"note":"STRING"
}
```
