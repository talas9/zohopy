"""Projects, Tasks, Time Entries. Ref: https://www.zoho.com/books/api/v3/projects/"""

from __future__ import annotations

from typing import Any

from zohopy.products._base import AsyncResource, SyncResource

_P = "/books/v3"


class Projects(SyncResource):
    _api_prefix, _resource = _P, "projects"

    def activate(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "active")

    def inactivate(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "inactive")

    def clone(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "clone")

    def list_users(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "users")

    def list_tasks(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "tasks")

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def list_invoices(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "invoices")

    def assign_users(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "users", data)

    def invite_user(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "users/invite", data)

    def get_user(self, id: str, user_id: str) -> dict[str, Any]:
        return self._client.get(self._path(id, "users", user_id))

    def update_user(self, id: str, user_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(id, "users", user_id), json=data)

    def delete_user(self, id: str, user_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "users", user_id))

    def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "comments", data)

    def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "comments", comment_id))

    def add_task(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "tasks", data)

    def get_task(self, id: str, task_id: str) -> dict[str, Any]:
        return self._client.get(self._path(id, "tasks", task_id))

    def update_task(self, id: str, task_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._client.put(self._path(id, "tasks", task_id), json=data)

    def delete_task(self, id: str, task_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "tasks", task_id))


class AsyncProjects(AsyncResource):
    _api_prefix, _resource = _P, "projects"

    async def activate(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "active")

    async def inactivate(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "inactive")

    async def clone(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "clone")

    async def list_users(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "users")

    async def list_tasks(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "tasks")

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def list_invoices(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "invoices")

    async def assign_users(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "users", data)

    async def invite_user(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "users/invite", data)

    async def get_user(self, id: str, user_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(id, "users", user_id))

    async def update_user(self, id: str, user_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(id, "users", user_id), json=data)

    async def delete_user(self, id: str, user_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "users", user_id))

    async def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "comments", data)

    async def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "comments", comment_id))

    async def add_task(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "tasks", data)

    async def get_task(self, id: str, task_id: str) -> dict[str, Any]:
        return await self._client.get(self._path(id, "tasks", task_id))

    async def update_task(self, id: str, task_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._client.put(self._path(id, "tasks", task_id), json=data)

    async def delete_task(self, id: str, task_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "tasks", task_id))


class Tasks(SyncResource):
    _api_prefix, _resource = _P, "tasks"

    def mark_open(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/open")

    def mark_ongoing(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/ongoing")

    def mark_completed(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "status/completed")

    def update_completed_percentage(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "completedpercentage", data)

    def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._action_post(id, "comments", data)

    def list_comments(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "comments")

    def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "comments", comment_id))

    def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return self._client.post(self._path(id, "attachment"), files=files)

    def get_attachment(self, id: str) -> dict[str, Any]:
        return self._action_get(id, "attachment")

    def delete_attachment(self, id: str) -> dict[str, Any]:
        return self._client.delete(self._path(id, "attachment"))


class AsyncTasks(AsyncResource):
    _api_prefix, _resource = _P, "tasks"

    async def mark_open(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/open")

    async def mark_ongoing(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/ongoing")

    async def mark_completed(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "status/completed")

    async def update_completed_percentage(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "completedpercentage", data)

    async def add_comment(self, id: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self._action_post(id, "comments", data)

    async def list_comments(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "comments")

    async def delete_comment(self, id: str, comment_id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "comments", comment_id))

    async def add_attachment(self, id: str, files: dict[str, Any]) -> dict[str, Any]:
        return await self._client.post(self._path(id, "attachment"), files=files)

    async def get_attachment(self, id: str) -> dict[str, Any]:
        return await self._action_get(id, "attachment")

    async def delete_attachment(self, id: str) -> dict[str, Any]:
        return await self._client.delete(self._path(id, "attachment"))


class TimeEntries(SyncResource):
    _api_prefix, _resource = _P, "timeentries"

    def start_timer(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "timer/start")

    def stop_timer(self, id: str) -> dict[str, Any]:
        return self._action_post(id, "timer/stop")

    def get_timer(self) -> dict[str, Any]:
        return self._client.get(self._path("runningtimer"))


class AsyncTimeEntries(AsyncResource):
    _api_prefix, _resource = _P, "timeentries"

    async def start_timer(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "timer/start")

    async def stop_timer(self, id: str) -> dict[str, Any]:
        return await self._action_post(id, "timer/stop")

    async def get_timer(self) -> dict[str, Any]:
        return await self._client.get(self._path("runningtimer"))
