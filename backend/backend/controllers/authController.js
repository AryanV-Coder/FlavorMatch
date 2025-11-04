const { createClient } = require('@supabase/supabase-js');

// Initialize Supabase client
const supabaseUrl = 'YOUR_SUPABASE_URL';
const supabaseKey = 'YOUR_SUPABASE_KEY';
const supabase = createClient(supabaseUrl, supabaseKey);

class AuthController {
    async login(req, res) {
        try {
            const { family_name, member_name, password } = req.body;

            // Query the database for the user
            const { data, error } = await supabase
                .from('family_members')
                .select('*')
                .eq('family_name', family_name)
                .eq('member_name', member_name)
                .single();

            if (error || !data) {
                return res.status(401).json({
                    message: 'Invalid credentials'
                });
            }

            // In production, use proper password hashing
            if (data.password !== password) {
                return res.status(401).json({
                    message: 'Invalid credentials'
                });
            }

            return res.status(200).json({
                message: 'Login successful',
                user: {
                    family_name: data.family_name,
                    member_name: data.member_name
                }
            });
        } catch (error) {
            console.error('Login error:', error);
            return res.status(500).json({
                message: 'Internal server error'
            });
        }
    }
}

module.exports = AuthController;