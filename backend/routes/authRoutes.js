const express = require('express');
const AuthController = require('../controllers/authController');

const router = express.Router();
const authController = new AuthController();

// Authentication routes
router.post('/login', authController.login.bind(authController));
router.post('/register-family', authController.registerFamily.bind(authController));
router.post('/register-member', authController.registerMember.bind(authController));

// Food entry routes
router.post('/food-entry', authController.addFoodEntry.bind(authController));

module.exports = router;