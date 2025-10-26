import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Story, WritingSession

class StoryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.story_id = self.scope['url_route']['kwargs']['story_id']
        self.room_group_name = f'story_{self.story_id}'
        
        # Check if story exists
        story = await self.get_story()
        if not story:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Notify others that user joined
        if not isinstance(self.scope['user'], AnonymousUser):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_activity',
                    'message': f'{self.scope["user"].username} joined the writing session',
                    'user': self.scope['user'].username,
                    'activity_type': 'joined'
                }
            )
            
            # Update writing session
            await self.update_writing_session(True)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Notify others that user left
        if not isinstance(self.scope['user'], AnonymousUser):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_activity',
                    'message': f'{self.scope["user"].username} left the writing session',
                    'user': self.scope['user'].username,
                    'activity_type': 'left'
                }
            )
            
            # Update writing session
            await self.update_writing_session(False)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data['type']
            
            if message_type == 'new_node':
                # Broadcast new story node to all users
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'story_update',
                        'node_content': data['content'],
                        'author': data['author'],
                        'node_id': data['node_id'],
                        'created_at': data.get('created_at'),
                        'word_count': data.get('word_count', 0)
                    }
                )
            
            elif message_type == 'user_typing':
                # Broadcast typing indicator
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_indicator',
                        'user': data['user'],
                        'is_typing': data['is_typing']
                    }
                )
            
            elif message_type == 'cursor_position':
                # Broadcast cursor position for collaborative editing
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'cursor_update',
                        'user': data['user'],
                        'position': data['position'],
                        'selection': data.get('selection')
                    }
                )
            
            elif message_type == 'ai_suggestion':
                # Broadcast AI suggestion
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'ai_suggestion_update',
                        'suggestion': data['suggestion'],
                        'prompt_type': data['prompt_type'],
                        'author': data.get('author', 'AI Assistant')
                    }
                )
            
            elif message_type == 'comment':
                # Broadcast new comment
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'comment_update',
                        'comment': data['comment'],
                        'author': data['author'],
                        'comment_id': data['comment_id']
                    }
                )
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON data'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))

    async def story_update(self, event):
        # Send new story node to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_node',
            'node_content': event['node_content'],
            'author': event['author'],
            'node_id': event['node_id'],
            'created_at': event.get('created_at'),
            'word_count': event.get('word_count', 0)
        }))

    async def user_activity(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_activity',
            'message': event['message'],
            'user': event['user'],
            'activity_type': event['activity_type']
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['user'],
            'is_typing': event['is_typing']
        }))

    async def cursor_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'cursor_position',
            'user': event['user'],
            'position': event['position'],
            'selection': event.get('selection')
        }))

    async def ai_suggestion_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'ai_suggestion',
            'suggestion': event['suggestion'],
            'prompt_type': event['prompt_type'],
            'author': event['author']
        }))

    async def comment_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'comment',
            'comment': event['comment'],
            'author': event['author'],
            'comment_id': event['comment_id']
        }))

    @database_sync_to_async
    def get_story(self):
        try:
            return Story.objects.get(id=self.story_id)
        except Story.DoesNotExist:
            return None

    @database_sync_to_async
    def update_writing_session(self, is_active):
        if isinstance(self.scope['user'], AnonymousUser):
            return
        
        try:
            story = Story.objects.get(id=self.story_id)
            writing_session, created = WritingSession.objects.get_or_create(
                story=story,
                user=self.scope['user'],
                defaults={'is_active': is_active}
            )
            if not created:
                writing_session.is_active = is_active
                writing_session.save()
        except Story.DoesNotExist:
            pass
