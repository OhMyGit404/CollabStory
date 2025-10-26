# CollabStory - End of Semester Project

## Project Overview
CollabStory is a real-time collaborative storytelling platform that allows multiple users to contribute to stories simultaneously with AI-powered writing assistance.

## Key Features Implemented

### 🚀 Core Functionality
- **Real-time Collaborative Writing** - Multiple users can write simultaneously
- **AI Writing Assistant** - Powered by Google Gemini API
- **Story Management** - Create, edit, and manage collaborative stories
- **User Authentication** - Secure user registration and login
- **WebSocket Integration** - Live updates and typing indicators

### 🤖 AI Integration
- Plot twist suggestions
- Character development ideas
- Dialogue assistance
- Setting descriptions
- Conflict generation
- Writing style analysis

### 🔄 Real-time Features
- Live typing indicators
- Instant content updates
- Active writer tracking
- Real-time comments

## Technology Stack

- **Backend**: Django 4.2+ with Django Channels
- **Real-time**: WebSockets with Redis
- **AI**: Google Gemini API
- **Frontend**: Bootstrap 5, HTMX, JavaScript
- **Database**: SQLite (development)
- **Task Queue**: Celery with Redis

## Project Structure

```
CollabStory/
├── CollabStory/          # Main Django project
│   ├── settings.py       # Configuration
│   ├── urls.py          # URL routing
│   └── asgi.py          # ASGI configuration
├── stories/              # Core stories app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── consumers.py     # WebSocket consumers
│   ├── forms.py         # Django forms
│   └── templates/       # HTML templates
├── users/               # User management
├── community/           # Community features
├── ai_assistant/        # AI integration
├── collaboration/       # Collaboration tools
├── static/              # CSS, JS, images
└── requirements.txt     # Dependencies
```

## Database Models

- **Story** - Main story entity with metadata
- **StoryNode** - Individual story contributions
- **WritingSession** - Active writing sessions
- **Contribution** - User contribution tracking
- **AIWritingPrompt** - AI-generated suggestions
- **StoryComment** - Story discussions

## API Endpoints

- `GET /` - Story list
- `POST /create/` - Create new story
- `GET /<id>/` - Story detail
- `POST /<id>/add_node/` - Add story node
- `GET /<id>/ai_suggestion/` - Get AI suggestion
- `POST /<id>/comment/` - Add comment

## WebSocket Routes

- `ws://localhost:8000/ws/story/<story_id>/` - Real-time collaboration

## Security Features

- Environment variable configuration
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure session handling

## Installation & Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables in `.env` file
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`

## Demo Instructions

1. Access the application at http://127.0.0.1:8000
2. Register a new account or login
3. Create a new story with initial prompt
4. Open the story in multiple browser tabs/windows
5. Add content and see real-time updates
6. Test AI suggestions for different writing prompts
7. Invite others to collaborate on the story

## Technical Achievements

- Implemented real-time collaboration using Django Channels
- Integrated Google Gemini API for AI writing assistance
- Created responsive UI with Bootstrap 5
- Implemented WebSocket communication for live updates
- Built comprehensive user authentication system
- Designed scalable database schema for collaborative features

## Future Enhancements

- Mobile app support
- Advanced story analytics
- Export to various formats
- Social features and user profiles
- Advanced AI models integration
- Story templates and challenges

---

**Project Status**: Complete and functional
**Demo Ready**: Yes
**Production Ready**: Yes (with proper configuration)
