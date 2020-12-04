# TT 2019-B052
[![Netlify Status](https://api.netlify.com/api/v1/badges/ee76620c-2359-49f2-bcdf-ef7697dfefe0/deploy-status)](https://app.netlify.com/sites/serene-haibt-2239b4/deploys)
![Last Commit](https://img.shields.io/github/last-commit/martinez-acosta/TT-2019-B052)
> TT 2019-B052 project

## Project Goals


Develop a web app that allows the edition of a database diagram under the entity-relationship model and performs its validation, later the diagram can be transformed into the relational model with the possibility of obtaining the database schema in SQL statements or get the document oriented database schema and have the possibility to implement the non-relational model in a NoSQL database as MongoDB.

## Included

- Nuxt
- Vue 2
- Vue Router 3
- Vuex 3
- Nuxtjs/Axios
- Authentication with JWT Token
- Vuetify

## Project Status

- You can test the application at https://serene-haibt-2239b4.netlify.app/
- Backend project in https://api-tt-2019-b052.herokuapp.com/ and the code in https://github.com/omaraparicio07/TT2019-B052
- User management with JWT Token
- Entity-Relationship diagrams can be made with GoJS libray.

## TODO
- ~~ ER diagram's validations ~~
- ~~ Mapping from ER Diagram to Relational Model ~~
- ~~ SQL script generation ~~
- Mapping from ER Diagram to NoSQL Conceptual Model
- Generate data schema for MongoDB with MongoDB’s query language

## Build Setup

```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).
