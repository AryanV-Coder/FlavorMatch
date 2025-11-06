const express = require('express');
const cors = require('cors');
const db = require('./config/db');
const authRoutes = require('./routes/authRoutes');
require('dotenv').config();

const app = express();

// Enable CORS for specific origin
app.use(cors({
    origin: ['http://127.0.0.1:5500', 'http://localhost:5500'],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Accept']
}));

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Test route
app.get('/test', (req, res) => {
    res.json({ message: 'Server is running!' });
});

// Login route
app.post('/api/login', async (req, res) => {
    try {
        const { familyName, memberName, password } = req.body;
        const result = await db.loginUser(familyName, memberName, password);
        res.json(result);
    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ success: false, message: 'Server error during login' });
    }
});

// Register family route
app.post('/api/register-family', async (req, res) => {
    try {
        const { familyName } = req.body;
        const result = await db.registerFamily(familyName);
        res.json(result);
    } catch (error) {
        console.error('Family registration error:', error);
        res.status(500).json({ success: false, message: 'Server error during family registration' });
    }
});

// Register member route
app.post('/api/register-member', async (req, res) => {
    try {
        const { familyName, memberName, password } = req.body;
        const result = await db.registerMember(familyName, memberName, password);
        res.json(result);
    } catch (error) {
        console.error('Member registration error:', error);
        res.status(500).json({ success: false, message: 'Server error during member registration' });
    }
});

// Add food entry route
app.post('/api/food-entry', async (req, res) => {
    try {
        const { memberId, foodName, isLiked, isHealthy } = req.body;
        const result = await db.addFoodEntry(memberId, foodName, isLiked, isHealthy);
        res.json(result);
    } catch (error) {
        console.error('Food entry error:', error);
        res.status(500).json({ success: false, message: 'Server error while adding food entry' });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ success: false, message: 'Something broke!' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Test the server: http://localhost:${PORT}/test`);
});