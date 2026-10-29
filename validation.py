from datetime import date


def task_body(title=None, notes=None, due_date=None, status=None):
    body = {}
    if title is not None:
        if not title.strip() or len(title) > 1024:
            raise ValueError('Title must contain 1–1024 characters, including non-whitespace text.')
        body['title'] = title
    if notes is not None:
        if len(notes) > 8192:
            raise ValueError('Notes must be at most 8192 characters.')
        body['notes'] = notes
    if due_date is not None:
        # Empty string explicitly clears the date. None leaves it unchanged.
        if due_date == '':
            body['due'] = None
        else:
            parsed = date.fromisoformat(due_date)
            if parsed.isoformat() != due_date:
                raise ValueError('Use YYYY-MM-DD for due_date.')
            body['due'] = due_date + 'T00:00:00.000Z'
    if status is not None:
        if status not in ('needsAction', 'completed'):
            raise ValueError('Status must be needsAction or completed.')
        body['status'] = status
        if status == 'needsAction':
            body['completed'] = None
    return body
