# Admin Dashboard - Quick Start Guide

## What's New?

Your project now has a complete **Admin-Only User Management Dashboard** with authentication, role-based access control, and comprehensive user management features.

## Quick Setup (5 minutes)

### Step 1: Install New Dependencies
```bash
cd backend
pip install -r requirements.txt
```

This installs:
- `PyJWT` - For JWT token authentication
- `bcrypt` - For secure password hashing

### Step 2: Update Environment
Create/update `.env` file in the `backend` folder:
```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=dashboard_db
SECRET_KEY=super-secret-key-change-this
```

### Step 3: Start Backend
```bash
cd backend
python -m uvicorn main:app --reload
```

### Step 4: Access Dashboard
Open your browser: `http://localhost:8000/Dashboard/Dashboard.html`

## First Use

1. **Create Admin Account**:
   - Click "Create Account" 
   - Enter username, email, password
   - First user automatically becomes admin

2. **Login & Access Dashboard**:
   - Use your credentials to login
   - You'll see the User Management Dashboard

3. **Manage Users**:
   - View all users in the table
   - Click action buttons to manage users:
     - 🛡️ Shield icon: Change role (Admin ↔ User)
     - 🚫 Ban icon: Deactivate/Activate user
     - 🗑️ Trash icon: Delete user

## Key Features

✅ **Authentication**
- Secure login/registration
- JWT token-based sessions
- Auto-logout on token expiry

✅ **Admin-Only Access**
- Non-admins cannot access dashboard
- Role-based access control at backend

✅ **User Management**
- View all users with details
- Change user roles
- Deactivate/Activate accounts
- Delete user accounts
- Real-time statistics

✅ **Security**
- Passwords are bcrypt hashed
- JWT token validation
- Self-protection (can't delete own account)

## API Endpoints

### Public
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login

### Admin Only
- `GET /api/users` - View all users
- `PUT /api/users/{username}/role` - Change role
- `PUT /api/users/{username}/deactivate` - Deactivate user
- `PUT /api/users/{username}/activate` - Activate user
- `DELETE /api/users/{username}` - Delete user

## Files Changed/Added

### New Files
- `Dashboard/dashboard-admin.js` - Dashboard functionality
- `Dashboard/ADMIN_DASHBOARD_README.md` - Full documentation

### Modified Files
- `Dashboard/Dashboard.html` - Complete redesign for admin dashboard
- `backend/main.py` - Added auth & user management
- `backend/requirements.txt` - Added new dependencies

## Common Tasks

### Create Another Admin
1. Login as admin
2. In user table, find user
3. Click shield icon → select "admin"
4. Confirm

### Disable User Login
1. Find user in table
2. Click ban icon
3. Confirm deactivation
4. User shows as "Inactive"

### Re-enable User
1. Find inactive user
2. Click check icon
3. Confirm activation
4. User shows as "Active"

### Delete User Permanently
1. Find user
2. Click trash icon
3. Confirm deletion
4. User removed from system

## Troubleshooting

### "Admin access required"
- You're not logged in as admin
- Only the first registered user is admin by default

### "Invalid credentials"
- Wrong username or password
- Username is case-sensitive

### Cannot access dashboard
- Make sure backend is running: `python -m uvicorn main:app --reload`
- Check API URL: `http://localhost:8000`
- Clear browser cache and cookies

### Users not loading
- Check MongoDB connection
- Verify `MONGODB_URI` in `.env`
- Check browser console for errors (F12)

## default Ports

- Frontend: `http://localhost:3000` or `http://localhost:8000`
- Backend API: `http://localhost:8000`
- MongoDB: `localhost:27017`

## Next Steps

After initial setup, you can:
1. Create more admin accounts
2. Invite users to register
3. Manage user roles and permissions
4. Monitor user activity
5. Deactivate inactive accounts

## Need Help?

Refer to `ADMIN_DASHBOARD_README.md` for:
- Detailed API documentation
- Security features explanation
- Database schema
- Advanced features
- Future enhancements

---

**Enjoy your new Admin Dashboard!** 🚀
