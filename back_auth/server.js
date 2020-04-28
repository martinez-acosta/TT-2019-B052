const fs = require('fs')
const express = require('express')
const jwt = require('jsonwebtoken')
const cors = require('cors')
const bodyParser = require('body-parser')
const events = require('./db/events.json')

const app = express()

app.use(cors())
app.use(bodyParser.json())

// Con Vuex vamos a enviar las credenciales de cada usuario a los endpoints register, dashboard, etc..

// En respuesta el servidor enviara el jwt que incluye la información del usuario

// En llamadas subsecuentes usaremos axios para agregar ese jwt en el header de la llamada para pedir datos protegidos, como los eventos o datos que necesitemos

app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to the API.'
  })
})

app.get('/dashboard', verifyToken, (req, res) => {
  // Verificamos que el jwt sea el mismo:
  // Más info en: https://www.youtube.com/watch?v=7Q17ubqLfaM
  jwt.verify(req.token, 'the_secret_key', (err) => {
    if (err) {
      // Si el token ha sido manipulado o está expirado, manda eror 401
      res.sendStatus(401)
    } else {
      // Mandamos el objeto eventos:
      // Ojo, la app cliente debe saber cómo manejar el objeto, debe saber cómo está estructurado
      res.json({
        events
      })
    }
  })
})

app.post('/register', (req, res) => {
  if (req.body) {
    const user = {
      name: req.body.name,
      email: req.body.email,
      password: req.body.password
    }
    const data = JSON.stringify(user, null, 2)
    console.log('req recibido: ' + data)
    const dbUserEmail = require('./db/user.json').email
    const errorsToSend = []

    if (dbUserEmail === user.email) {
      errorsToSend.push('An account with this email already exists.')
    }
    if (user.password.length < 5) {
      errorsToSend.push('Password too short.')
    }
    if (errorsToSend.length > 0) {
      res.status(400).json({ errors: errorsToSend })
    } else {
      fs.writeFile('./db/user.json', data, (err) => {
        if (err) {
          console.log(err + data)
        } else {
          const token = jwt.sign({ user }, 'the_secret_key')
          // In a production app, you'll want the secret key to be an environment variable
          res.json({
            token,
            email: user.email,
            name: user.name
          })
        }
      })
    }
  } else {
    res.sendStatus(400)
  }
})

app.post('/login', (req, res) => {
  const userDB = fs.readFileSync('./db/user.json')
  const userInfo = JSON.parse(userDB)
  if (
    req.body &&
    req.body.email === userInfo.email &&
    req.body.password === userInfo.password
  ) {
    const token = jwt.sign({ userInfo }, 'the_secret_key')
    // In a production app, you'll want the secret key to be an environment variable
    res.json({
      token,
      email: userInfo.email,
      username: userInfo.username
    })
  } else {
    res.status(401).json({ error: 'Invalid login. Please try again.' })
  }
})

// MIDDLEWARE
function verifyToken(req, res, next) {
  const bearerHeader = req.headers.authorization

  if (typeof bearerHeader !== 'undefined') {
    const bearer = bearerHeader.split(' ')
    const bearerToken = bearer[1]
    req.token = bearerToken
    next()
  } else {
    res.sendStatus(401)
  }
}

app.listen(3000, () => {
  console.log('Server started on port 3000')
})
