const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
    user: process.env.POSTGRES_USER,
    password: process.env.POSTGRES_PASSWORD,
    host: process.env.POSTGRES_HOST,
    port: process.env.POSTGRES_PORT,
    database: process.env.POSTGRES_DATABASE
});

const executeQuery = async (query, params = []) => {
    const client = await pool.connect();
    try {
        const result = await client.query(query, params);
        return result.rows;
    } catch (error) {
        console.error('Database query error:', error);
        throw error;
    } finally {
        client.release();
    }
};

// 1. Login Dashboard - Authentication
async function loginUser(familyName, memberName, password) {
    try {
        // First, get the family_id
        const familyQuery = `
            SELECT family_id 
            FROM family 
            WHERE family_username = $1
        `;
        const familyResult = await executeQuery(familyQuery, [familyName]);

        if (familyResult.length === 0) {
            return { success: false, message: "Family not found!" };
        }

        const familyId = familyResult[0].family_id;

        // Then, check member credentials
        const memberQuery = `
            SELECT member_id, member_username 
            FROM member 
            WHERE family_id = $1 
            AND member_username = $2 
            AND member_password = $3
        `;
        const memberResult = await executeQuery(memberQuery, [familyId, memberName, password]);

        if (memberResult.length === 0) {
            return { success: false, message: "Invalid member credentials!" };
        }

        // Return success with user data
        return {
            success: true,
            data: {
                familyId: familyId,
                familyName: familyName,
                memberId: memberResult[0].member_id,
                memberName: memberResult[0].member_username
            }
        };
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, message: "An error occurred during login." };
    }
}

// 2. Register Family
async function registerFamily(familyName) {
    try {
        // Check if family already exists
        const checkQuery = `
            SELECT family_id 
            FROM family 
            WHERE family_username = $1
        `;
        const existingFamily = await executeQuery(checkQuery, [familyName]);

        if (existingFamily.length > 0) {
            return { success: false, message: "Family name already exists!" };
        }

        // Insert new family
        const insertQuery = `
            INSERT INTO family (family_username)
            VALUES ($1)
            RETURNING family_id
        `;
        await executeQuery(insertQuery, [familyName]);

        return { success: true, message: "Family registered successfully!" };
    } catch (error) {
        console.error('Family registration error:', error);
        return { success: false, message: "An error occurred during registration." };
    }
}

// 3. Register Member
async function registerMember(familyName, memberName, password) {
    try {
        // First, get the family_id
        const familyQuery = `
            SELECT family_id 
            FROM family 
            WHERE family_username = $1
        `;
        const familyResult = await executeQuery(familyQuery, [familyName]);

        if (familyResult.length === 0) {
            return { success: false, message: "Family not found!" };
        }

        const familyId = familyResult[0].family_id;

        // Check if member already exists in this family
        const checkQuery = `
            SELECT member_id 
            FROM member 
            WHERE family_id = $1 
            AND member_username = $2
        `;
        const existingMember = await executeQuery(checkQuery, [familyId, memberName]);

        if (existingMember.length > 0) {
            return { success: false, message: "Member already exists in this family!" };
        }

        // Insert new member
        const insertQuery = `
            INSERT INTO member (family_id, member_username, member_password)
            VALUES ($1, $2, $3)
            RETURNING member_id
        `;
        await executeQuery(insertQuery, [familyId, memberName, password]);

        return { success: true, message: "Member registered successfully!" };
    } catch (error) {
        console.error('Member registration error:', error);
        return { success: false, message: "An error occurred during member registration." };
    }
}

// 4. Dashboard - Add Food Entry
async function addFoodEntry(memberId, foodName, isLiked, isHealthy, timestamp) {
    try {
        // If no timestamp is provided, use current timestamp
        const foodTimestamp = timestamp || new Date().toISOString().split('T')[0];
        
        const query = `
            INSERT INTO food (timestamp, member_id, food, is_liked, is_healthy)
            VALUES (TO_TIMESTAMP($1, 'YYYY-MM-DD'), $2, $3, $4, $5)
            RETURNING food_id
        `;
        await executeQuery(query, [foodTimestamp, memberId, foodName, isLiked, isHealthy]);

        return { success: true, message: "Food entry added successfully!" };
    } catch (error) {
        console.error('Food entry error:', error);
        return { success: false, message: "An error occurred while adding food entry." };
    }
}

// Export all functions
module.exports = {
    loginUser,
    registerFamily,
    registerMember,
    addFoodEntry,
    executeQuery
};