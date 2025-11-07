const db = require('../config/db');

class AuthController {
    async login(req, res) {
        try {
            const { familyName, memberName, password } = req.body;
            const result = await db.loginUser(familyName, memberName, password);
            
            if (result.success) {
                res.status(200).json(result);
            } else {
                res.status(401).json(result);
            }
        } catch (error) {
            console.error('Login error:', error);
            res.status(500).json({ 
                success: false, 
                message: 'Server error during login' 
            });
        }
    }

    async registerFamily(req, res) {
        try {
            const { familyName } = req.body;
            const result = await db.registerFamily(familyName);
            
            if (result.success) {
                res.status(201).json(result);
            } else {
                res.status(400).json(result);
            }
        } catch (error) {
            console.error('Family registration error:', error);
            res.status(500).json({ 
                success: false, 
                message: 'Server error during family registration' 
            });
        }
    }

    async registerMember(req, res) {
        try {
            const { familyName, memberName, password } = req.body;
            const result = await db.registerMember(familyName, memberName, password);
            
            if (result.success) {
                res.status(201).json(result);
            } else {
                res.status(400).json(result);
            }
        } catch (error) {
            console.error('Member registration error:', error);
            res.status(500).json({ 
                success: false, 
                message: 'Server error during member registration' 
            });
        }
    }

    async addFoodEntry(req, res) {
        try {
            const { memberId, foodName, isLiked, isHealthy } = req.body;
            const result = await db.addFoodEntry(memberId, foodName, isLiked, isHealthy);
            
            if (result.success) {
                res.status(201).json(result);
            } else {
                res.status(400).json(result);
            }
        } catch (error) {
            console.error('Food entry error:', error);
            res.status(500).json({ 
                success: false, 
                message: 'Server error while adding food entry' 
            });
        }
    }
}

module.exports = AuthController;