const express = require('express');
const app = express();
const port = 3000;

// Define routes
app.use(express.static('public'));

// Start server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
