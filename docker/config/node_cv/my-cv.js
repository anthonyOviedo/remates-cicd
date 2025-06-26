const express = require('express')
const path = require('path')
const app = express()
const port = 8801

app.use(express.static('public'))


app.use(express.static(path.join(__dirname, 'public')))


app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/home', 'index.html'))
})

app.get('/main', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/pages', 'main.html'))
})

app.get('/about', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/pages', 'about.html'));
});

app.get('/contact', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/pages', 'contact.html'));
});

app.get('/portafolio', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/pages', 'portafolio.html'));
});

app.get('/services', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/pages', 'services.html'));
});






app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})