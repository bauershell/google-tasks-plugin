import unittest
from unittest.mock import patch
from fastmcp import Client
import server


class MCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_discovery_pagination_and_patch(self):
        async with Client(server.mcp) as client:
            tools = {tool.name: tool for tool in await client.list_tools()}
            self.assertEqual(len(tools), 5)
            self.assertTrue(tools['list_tasks'].annotations.readOnlyHint)
            self.assertFalse(tools['create_task'].annotations.readOnlyHint)
            with patch('server.call', return_value={'items': [], 'nextPageToken': 'next'}) as api:
                result = await client.call_tool('list_tasks', {
                    'list_id': 'my-list', 'include_completed': True, 'page_token': 'page-2'})
                self.assertFalse(result.is_error)
                api.assert_called_once_with('tasks', 'list', tasklist='my-list',
                    maxResults=100, showCompleted=True, showHidden=True,
                    showDeleted=False, pageToken='page-2')
            with patch('server.call', return_value={'id': 'task-1', 'status': 'completed'}) as api:
                result = await client.call_tool('update_task', {'task_id': 'task-1', 'status': 'completed'})
                self.assertFalse(result.is_error)
                api.assert_called_once_with('tasks', 'patch', tasklist='@default',
                    task='task-1', body={'status': 'completed'})

    async def test_invalid_date_does_not_write(self):
        async with Client(server.mcp) as client:
            with patch('server.call') as api:
                result = await client.call_tool('create_task',
                    {'title': 'Example', 'due_date': '2026-02-30'}, raise_on_error=False)
                self.assertTrue(result.is_error)
                api.assert_not_called()
