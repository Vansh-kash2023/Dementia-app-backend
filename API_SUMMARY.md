# Dementia App Backend API Summary

Base URL (local): `http://127.0.0.1:10000`

Auth:
- JWT is returned from `POST /login` as `access_token`.
- For protected routes, send header: `Authorization: Bearer <access_token>`.

## Health and Utility

### GET /
- Description: Health check endpoint.
- Auth: No
- Response: `{ "message": "Server up and running" }`

### GET /static/uploads/<filename>
- Description: Serves local uploaded files from `UPLOAD_FOLDER`.
- Auth: No
- Notes: Legacy endpoint; image uploads are now stored in Cloudinary.

## Authentication

### POST /signup
- Description: Register a new user.
- Auth: No
- Request JSON:
  - `email` (string)
  - `password` (string)
  - `name` (string)
  - `emergency_contact` (string, optional)
- Request Body Example:
```json
{
  "email": "test.user@example.com",
  "password": "Test@1234",
  "name": "Test User",
  "emergency_contact": "+91-9999999999"
}
```
- Success: `201` with `{ "message": "User registered successfully" }`

### POST /login
- Description: Login with email and password.
- Auth: No
- Request JSON:
  - `email` (string)
  - `password` (string)
- Request Body Example:
```json
{
  "email": "test.user@example.com",
  "password": "Test@1234"
}
```
- Success: `200` with `{ "access_token": "..." }`

### GET /profile
- Description: Get current user's profile.
- Auth: Yes (JWT required)
- Response fields: `name`, `email`, `emergency_contact`

### GET /protected
- Description: Example protected endpoint.
- Auth: Yes (`@jwt_required`)
- Notes: Current implementation expects `current_user["username"]`, but login stores identity as user id string.

## Memories

### POST /memories
- Description: Create a memory with image upload to Cloudinary.
- Auth: Yes (JWT required)
- Request JSON:
  - `image` (base64 string, supports JPEG/PNG; can be data URL format)
  - `title` (string, optional)
  - `description` (string, optional)
  - `date` (string, optional)
- Request Body Example:
```json
{
  "title": "Birthday Memory",
  "description": "This was my 25th birthday celebration.",
  "date": "2026-03-22",
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
}
```
- Success: `201` with created memory data including `image_url`

### GET /memories
- Description: List current user's memories.
- Auth: Yes (JWT required)

### GET /memories/<id>
- Description: Get memory by id.
- Auth: No explicit auth check in route.

### PUT /memories/<id>
- Description: Update memory fields.
- Auth: No explicit auth check in route.
- Request JSON (any): `title`, `description`, `image_url`, `date`
- Request Body Example:
```json
{
  "title": "Updated Memory Title",
  "description": "Updated memory description",
  "date": "2026-03-23",
  "image_url": "https://res.cloudinary.com/your-cloud/image/upload/v123/sample.jpg"
}
```

### DELETE /memories/<id>
- Description: Delete memory.
- Auth: No explicit auth check in route.

## Familiar Faces

### POST /faces
- Description: Create familiar face with image upload to Cloudinary.
- Auth: Yes (JWT required)
- Request JSON:
  - `image` (base64 string, supports JPEG/PNG)
  - `name` (string)
  - `relationship` (string)
- Request Body Example:
```json
{
  "name": "Rahul",
  "relationship": "Son",
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
}
```
- Success: `201` with created face object

### GET /faces
- Description: List current user's familiar faces.
- Auth: Yes (JWT required)

### GET /faces/<id>
- Description: Get familiar face by id.
- Auth: No explicit auth check in route.

### PUT /faces/<id>
- Description: Update familiar face fields.
- Auth: No explicit auth check in route.
- Notes: Route currently references `photo_url` and `voice_note_url`, which are not present in the model.
- Request Body Example:
```json
{
  "name": "Rahul Sharma",
  "relationship": "Son"
}
```

### DELETE /faces/<id>
- Description: Delete familiar face.
- Auth: No explicit auth check in route.

## Reminders

### POST /reminders
- Description: Create reminder.
- Auth: Yes (JWT required)
- Request JSON:
  - `title` (string)
  - `description` (string, optional)
  - `time` (string)
  - `date` (string, optional)
  - `repeat` (string, optional)
  - `status` (boolean, optional)
- Request Body Example:
```json
{
  "title": "Take medicine",
  "description": "After breakfast",
  "time": "09:00",
  "date": "2026-03-23",
  "repeat": "daily",
  "status": false
}
```

### GET /reminders
- Description: List current user's reminders.
- Auth: Yes (JWT required)

### GET /reminders/<id>
- Description: Get reminder by id.
- Auth: No explicit auth check in route.

### PUT /reminders/<id>
- Description: Update reminder fields.
- Auth: No explicit auth check in route.
- Request Body Example:
```json
{
  "title": "Take medicine (updated)",
  "description": "After breakfast and water",
  "time": "09:30",
  "date": "2026-03-24",
  "repeat": "daily",
  "status": true
}
```

### DELETE /reminders/<id>
- Description: Delete reminder.
- Auth: No explicit auth check in route.

## Answers and Assessment

### POST /answers
- Description: Save answer records in bulk.
- Auth: Yes (JWT required)
- Request JSON: array of objects:
  - `answer_text` (string)
  - `question` (string)
  - `scored` (int, optional)
- Request Body Example:
```json
[
  {
    "question": "What is your name?",
    "answer_text": "My name is John.",
    "scored": 1
  },
  {
    "question": "Where do you live?",
    "answer_text": "I live in Mumbai.",
    "scored": 0
  }
]
```
- Success: `201` with created answer list

### GET /answers
- Description: Get all answers.
- Auth: No

### POST /gen_ai
- Description: Generate contextual AI response using user data.
- Auth: Yes (JWT required)
- Request JSON:
  - `message` (string)
- Request Body Example:
```json
{
  "message": "What should I do today?"
}
```
- Response: `{ "message": "...model output..." }`

### GET /generate_report
- Description: Generate user performance report from answers.
- Auth: Yes (JWT required)
- Response includes counts, answer list, and summary statistics.
