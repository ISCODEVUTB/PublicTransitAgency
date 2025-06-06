const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 8080;

app.use(express.static(path.join(__dirname, 'build/web')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build/web', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});