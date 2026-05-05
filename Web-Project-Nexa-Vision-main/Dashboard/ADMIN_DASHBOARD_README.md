# Admin Dashboard - User Management System

## Overview
The Admin Dashboard is a secure, admin-only interface for managing all users in the MEGASYST application. Only administrators can access this page to view, control, and manage user accounts.

## Features

### 1. Authentication System
- **Login**: Admin users can login with username and password
- **Registration**: First user registered automatically becomes admin, subsequent users are regular users
- **Session Management**: JWT tokens stored in browser localStorage
- **Admin-Only Access**: Non-admin users are denied access even if they have valid credentials

### 2. User Management
- **View All Users**: Display complete list of all system users
- **Change User Roles**: Promote regular users to admin or demote admins to regular users
- **Deactivate Users**: Temporarily disable user accounts without deleting them
- **Activate Users**: Re-enable deactivated user accounts
- **Delete Users**: Permanently remove user accounts from the system

### 3. Statistics Dashboard
- **Total Users**: Count of all registered users
- **Total Admins**: Number of admin accounts
- **Active Users**: Count of currently active users

### 4. User Information Displayed
- Username
- Email
- Role (Admin/User)
- Account Status (Active/Inactive)
- Join Date

## Backend Implementation

### Database Collections

#### Users Collection
```json
{
  "username": "string (unique)",
  "email": "string (unique)",
  "password_hash": "string (bcrypt hashed)",
  "role": "string (admin or user)",
  "is_active": "boolean",
  "created_at": "datetime"
}
```

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
  - Body: `{ username, email, password }`
  - Returns: JWT token and user info
  
- `POST /api/auth/login` - Login user
  - Body: `{ username, password }`
  - Returns: JWT token and user info
  
- `GET /api/auth/me` - Get current user info
  - Headers: `Authorization: Bearer {token}`
  - Returns: Current user details

#### User Management (Admin Only)
- `GET /api/users` - Get all users
  - Headers: `Authorization: Bearer {token}` (Admin required)
  - Returns: List of all users
  
- `PUT /api/users/{username}/role` - Change user role
  - Headers: `Authorization: Bearer {token}` (Admin required)
  - Body: `{ new_role: "admin" or "user" }`
  - Returns: Updated user
  
- `PUT /api/users/{username}/deactivate` - Deactivate user
  - Headers: `Authorization: Bearer {token}` (Admin required)
  - Returns: Deactivation status
  
- `PUT /api/users/{username}/activate` - Activate user
  - Headers: `Authorization: Bearer {token}` (Admin required)
  - Returns: Activation status
  
- `DELETE /api/users/{username}` - Delete user
  - Headers: `Authorization: Bearer {token}` (Admin required)
  - Returns: Deletion status

## Security Features

1. **Password Hashing**: All passwords are hashed using bcrypt
2. **JWT Authentication**: Stateless token-based authentication
3. **Role-Based Access Control**: Only admins can access dashboard and manage users
4. **Self-Protection**: Users cannot delete or deactivate their own accounts
5. **Token Validation**: All API requests validate JWT tokens

## How to Use

### First-Time Setup

1. Start the backend server:
```bash
cd backend
python -m pip install -r requirements.txt
python main.py
```

2. Install new dependencies if needed:
```bash
pip install PyJWT bcrypt pydantic[email]
```

3. Access the Dashboard:
   - Navigate to `http://localhost:8000/Dashboard/Dashboard.html`
   - You'll be redirected to the login screen

### Admin Registration

1. On the login page, click "Create Account"
2. Fill in username, email, and password
3. Click "Register"
4. **Note**: The first user to register becomes an admin
5. You'll be logged in and can access the user management dashboard

### Managing Users

#### View Users
- All registered users appear in the main user table
- Includes username, email, role, status, and join date

#### Change User Role
- Click the role-change button (shield icon) next to the user
- Confirm the role change in the modal
- User role updates immediately

#### Deactivate User
- Click the deactivate button (ban icon) next to an active user
- Deactivated users cannot login but their data remains
- User status changes to "Inactive"

#### Activate User
- Click the activate button (check icon) next to an inactive user
- User can login again after activation
- User status changes to "Active"

#### Delete User
- Click the delete button (trash icon) next to the user
- Confirm deletion (this cannot be undone)
- User is permanently removed from the system

### Logout
- Click the "Logout" button in the top right
- You'll be returned to the login screen
- Session token is cleared from browser storage

## Browser Requirements

- Modern browser with localStorage support
- JavaScript enabled
- ES6 (ECMAScript 2015) or higher

## Local Storage

The dashboard stores the following in browser localStorage:
- `token`: JWT authentication token (for session persistence)

Token is automatically cleared on logout or when invalid.

## Error Handling

- Invalid credentials: "Invalid credentials" message
- Non-admin users: "Admin access required" message
- Network errors: Specific error message displayed
- Duplicate username/email: User receives error during registration
- Failed actions: Error message shown with retry option

## File Structure

```
Dashboard/
  ├── Dashboard.html          # Main dashboard UI
  ├── dashboard-admin.js      # JavaScript functionality
backend/
  ├── main.py                 # FastAPI backend with auth & user management
  ├── requirements.txt        # Python dependencies (updated)
  ├── seed.py                 # Database seeding utility
```

## Environment Variables

Create a `.env` file in the backend folder:
```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=dashboard_db
SECRET_KEY=your-secret-key-change-this-in-production
```

## Future Enhancements

- User profile editing
- Password change functionality
- Email verification
- Two-factor authentication (2FA)
- Advanced user search and filtering
- Bulk user operations
- User activity logs
- Email notifications for admin actions
- Role-based permissions beyond admin/user
- User ban/unban functionality

## Support

For issues or questions, contact the development team.
