# CollabStory - Collaborative Story Generator

A real-time collaborative storytelling platform where multiple users can contribute to stories simultaneously with AI-powered writing assistance.

## Pages & Features

### **Home Page** (`/`)
- Browse all public stories
- Filter by genre (Fantasy, Sci-Fi, Mystery, etc.)
- Search stories by title or content
- View story statistics (contributors, words, nodes)
- Quick access to create new stories

### **Create Story Page** (`/create/`)
- Story title and genre selection
- Initial prompt/premise input
- Cover image upload (optional)
- Maximum contributors setting
- Public/private visibility toggle

### **Story Detail Page** (`/<story_id>/`)
- **Story Content Display**
  - Real-time story content with author attribution
  - Word count and contribution tracking
  - AI-generated content indicators

- **Writing Interface**
  - Live text editor for adding content
  - Word count display
  - Submit new story nodes

- **AI Writing Assistant**
  - Plot twist suggestions
  - Character development ideas
  - Dialogue assistance
  - Setting descriptions
  - Conflict generation
  - Story continuation prompts

- **Real-time Collaboration**
  - Active writers list
  - Live typing indicators
  - Instant content updates
  - Real-time comments

### **User Authentication**
- **Login Page** (`/users/login/`)
- **Registration Page** (`/users/register/`)
- **User Profile** (`/users/profile/`)

### **Admin Panel** (`/admin/`)
- Story management
- User management
- AI prompt tracking
- Contribution analytics

## How It Works

### Real-time Collaboration
1. **Join a Story** - Click "Continue Writing" on any public story
2. **See Active Writers** - View who's currently writing
3. **Write Together** - Add your contribution in real-time
4. **Live Updates** - See others' content appear instantly
5. **AI Assistance** - Get writing suggestions powered by Google Gemini

### Story Creation Process
1. **Create** - Start with a title, genre, and initial prompt
2. **Invite** - Share the story link with collaborators
3. **Collaborate** - Multiple users add content simultaneously
4. **AI Help** - Use AI suggestions for plot twists, characters, etc.
5. **Discuss** - Comment and discuss story direction

### AI Writing Features
- **Context-Aware** - AI understands your story's current state
- **Multiple Types** - Different suggestion categories available
- **Fallback System** - Works even without API key
- **Real-time** - Suggestions appear instantly

## Technology Stack

- **Backend**: Django 4.2+ with Django Channels
- **Real-time**: WebSockets with Redis
- **AI**: Google Gemini API
- **Frontend**: Bootstrap 5, HTMX, JavaScript
- **Database**: SQLite

## Quick Start

1. **Install & Setup**
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

2. **Access the App**
   - Main app: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

3. **Start Writing**
   - Register/Login
   - Create your first story
   - Invite others to collaborate
   - Use AI suggestions for inspiration

## Demo Features

- **Multi-user Writing** - Open multiple browser tabs to see real-time collaboration
- **AI Suggestions** - Click any AI button to see intelligent writing prompts
- **Live Updates** - Watch content appear instantly as others write
- **Story Management** - Create, edit, and manage collaborative stories

---
