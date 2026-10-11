"""Notification Hub — multi-channel notification delivery with templates and digest.

Supports in-app, email-style, and webhook channels with priority routing,
template rendering, read/unread tracking, and digest aggregation.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from string import Template
from typing import Any


class NotificationChannel(str, enum.Enum):
    IN_APP = "IN_APP"
    EMAIL = "EMAIL"
    WEBHOOK = "WEBHOOK"
    SLACK = "SLACK"


class NotificationPriority(str, enum.Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class NotificationCategory(str, enum.Enum):
    SYSTEM = "SYSTEM"
    ALERT = "ALERT"
    COLLABORATION = "COLLABORATION"
    COMPLIANCE = "COMPLIANCE"
    INCIDENT = "INCIDENT"
    TASK = "TASK"
    REPORT = "REPORT"


@dataclass
class NotificationTemplate:
    template_id: str
    name: str
    subject_template: str
    body_template: str
    channel: NotificationChannel
    category: NotificationCategory = NotificationCategory.SYSTEM
    created_at: float = field(default_factory=time.time)

    def render(self, variables: dict[str, str]) -> tuple[str, str]:
        subject = Template(self.subject_template).safe_substitute(variables)
        body = Template(self.body_template).safe_substitute(variables)
        return subject, body

    def to_dict(self) -> dict[str, Any]:
        return {
            "template_id": self.template_id,
            "name": self.name,
            "subject_template": self.subject_template,
            "body_template": self.body_template,
            "channel": self.channel.value,
            "category": self.category.value,
        }


@dataclass
class Notification:
    notification_id: str
    recipient: str
    channel: NotificationChannel
    priority: NotificationPriority
    category: NotificationCategory
    subject: str
    body: str
    sender: str = "system"
    tenant_id: str | None = None
    workspace_id: str | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    is_read: bool = False
    read_at: float | None = None
    delivered: bool = False
    delivered_at: float | None = None
    created_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "notification_id": self.notification_id,
            "recipient": self.recipient,
            "channel": self.channel.value,
            "priority": self.priority.value,
            "category": self.category.value,
            "subject": self.subject,
            "body": self.body,
            "sender": self.sender,
            "tenant_id": self.tenant_id,
            "workspace_id": self.workspace_id,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "is_read": self.is_read,
            "read_at": self.read_at,
            "delivered": self.delivered,
            "delivered_at": self.delivered_at,
            "created_at": self.created_at,
        }


@dataclass
class UserPreferences:
    user_id: str
    enabled_channels: set[NotificationChannel] = field(
        default_factory=lambda: {NotificationChannel.IN_APP}
    )
    muted_categories: set[NotificationCategory] = field(default_factory=set)
    digest_enabled: bool = False
    digest_interval_seconds: int = 3600
    quiet_hours_start: int | None = None
    quiet_hours_end: int | None = None


class NotificationHub:
    """Multi-channel notification hub with template rendering and digest."""

    def __init__(self, max_per_user: int = 10000) -> None:
        self._notifications: dict[str, Notification] = {}
        self._by_recipient: dict[str, list[str]] = {}
        self._templates: dict[str, NotificationTemplate] = {}
        self._preferences: dict[str, UserPreferences] = {}
        self._digest_buffer: dict[str, list[str]] = {}
        self._max_per_user = max_per_user
        self._lock = threading.Lock()
        self._total_sent = 0
        self._total_delivered = 0

    def register_template(self, name: str, subject_template: str,
                          body_template: str,
                          channel: NotificationChannel = NotificationChannel.IN_APP,
                          category: NotificationCategory = NotificationCategory.SYSTEM) -> NotificationTemplate:
        tmpl = NotificationTemplate(
            template_id=uuid.uuid4().hex[:12],
            name=name,
            subject_template=subject_template,
            body_template=body_template,
            channel=channel,
            category=category,
        )
        with self._lock:
            self._templates[tmpl.template_id] = tmpl
        return tmpl

    def set_preferences(self, user_id: str,
                        enabled_channels: set[NotificationChannel] | None = None,
                        muted_categories: set[NotificationCategory] | None = None,
                        digest_enabled: bool | None = None) -> UserPreferences:
        with self._lock:
            prefs = self._preferences.get(user_id)
            if prefs is None:
                prefs = UserPreferences(user_id=user_id)
                self._preferences[user_id] = prefs
            if enabled_channels is not None:
                prefs.enabled_channels = enabled_channels
            if muted_categories is not None:
                prefs.muted_categories = muted_categories
            if digest_enabled is not None:
                prefs.digest_enabled = digest_enabled
            return prefs

    def get_preferences(self, user_id: str) -> UserPreferences:
        with self._lock:
            return self._preferences.get(user_id, UserPreferences(user_id=user_id))

    def send(self, recipient: str, subject: str, body: str,
             channel: NotificationChannel = NotificationChannel.IN_APP,
             priority: NotificationPriority = NotificationPriority.NORMAL,
             category: NotificationCategory = NotificationCategory.SYSTEM,
             sender: str = "system",
             tenant_id: str | None = None,
             workspace_id: str | None = None,
             resource_type: str | None = None,
             resource_id: str | None = None,
             metadata: dict[str, Any] | None = None) -> Notification | None:
        prefs = self.get_preferences(recipient)
        if channel not in prefs.enabled_channels and priority != NotificationPriority.URGENT:
            return None
        if category in prefs.muted_categories and priority != NotificationPriority.URGENT:
            return None

        notif = Notification(
            notification_id=uuid.uuid4().hex[:12],
            recipient=recipient,
            channel=channel,
            priority=priority,
            category=category,
            subject=subject,
            body=body,
            sender=sender,
            tenant_id=tenant_id,
            workspace_id=workspace_id,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata or {},
        )

        with self._lock:
            self._notifications[notif.notification_id] = notif
            user_list = self._by_recipient.setdefault(recipient, [])
            user_list.append(notif.notification_id)
            if len(user_list) > self._max_per_user:
                removed_id = user_list.pop(0)
                self._notifications.pop(removed_id, None)
            self._total_sent += 1

            if prefs.digest_enabled and priority != NotificationPriority.URGENT:
                self._digest_buffer.setdefault(recipient, []).append(notif.notification_id)
            else:
                notif.delivered = True
                notif.delivered_at = time.time()
                self._total_delivered += 1

        return notif

    def send_from_template(self, template_id: str, recipient: str,
                           variables: dict[str, str],
                           priority: NotificationPriority = NotificationPriority.NORMAL,
                           **kwargs: Any) -> Notification | None:
        with self._lock:
            tmpl = self._templates.get(template_id)
        if tmpl is None:
            return None
        subject, body = tmpl.render(variables)
        return self.send(
            recipient=recipient, subject=subject, body=body,
            channel=tmpl.channel, priority=priority,
            category=tmpl.category, **kwargs,
        )

    def broadcast(self, recipients: list[str], subject: str, body: str,
                  **kwargs: Any) -> list[Notification]:
        results = []
        for r in recipients:
            n = self.send(recipient=r, subject=subject, body=body, **kwargs)
            if n:
                results.append(n)
        return results

    def mark_read(self, notification_id: str) -> bool:
        with self._lock:
            notif = self._notifications.get(notification_id)
            if notif is None:
                return False
            if not notif.is_read:
                notif.is_read = True
                notif.read_at = time.time()
            return True

    def mark_all_read(self, recipient: str) -> int:
        count = 0
        with self._lock:
            ids = self._by_recipient.get(recipient, [])
            for nid in ids:
                notif = self._notifications.get(nid)
                if notif and not notif.is_read:
                    notif.is_read = True
                    notif.read_at = time.time()
                    count += 1
        return count

    def get_inbox(self, recipient: str, unread_only: bool = False,
                  category: NotificationCategory | None = None,
                  limit: int = 50) -> list[Notification]:
        with self._lock:
            ids = self._by_recipient.get(recipient, [])
            results = []
            for nid in reversed(ids):
                notif = self._notifications.get(nid)
                if notif is None:
                    continue
                if unread_only and notif.is_read:
                    continue
                if category and notif.category != category:
                    continue
                results.append(notif)
                if len(results) >= limit:
                    break
        return results

    def get_unread_count(self, recipient: str) -> int:
        with self._lock:
            ids = self._by_recipient.get(recipient, [])
            return sum(1 for nid in ids
                       if nid in self._notifications and not self._notifications[nid].is_read)

    def flush_digest(self, recipient: str) -> list[Notification]:
        with self._lock:
            ids = self._digest_buffer.pop(recipient, [])
            delivered = []
            for nid in ids:
                notif = self._notifications.get(nid)
                if notif and not notif.delivered:
                    notif.delivered = True
                    notif.delivered_at = time.time()
                    self._total_delivered += 1
                    delivered.append(notif)
        return delivered

    def delete(self, notification_id: str) -> bool:
        with self._lock:
            notif = self._notifications.pop(notification_id, None)
            if notif is None:
                return False
            if notif.recipient in self._by_recipient:
                self._by_recipient[notif.recipient] = [
                    n for n in self._by_recipient[notif.recipient] if n != notification_id
                ]
            return True

    def list_templates(self) -> list[dict[str, Any]]:
        with self._lock:
            return [t.to_dict() for t in self._templates.values()]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            by_channel: dict[str, int] = {}
            by_priority: dict[str, int] = {}
            unread = 0
            for n in self._notifications.values():
                by_channel[n.channel.value] = by_channel.get(n.channel.value, 0) + 1
                by_priority[n.priority.value] = by_priority.get(n.priority.value, 0) + 1
                if not n.is_read:
                    unread += 1
            return {
                "total_notifications": len(self._notifications),
                "total_sent": self._total_sent,
                "total_delivered": self._total_delivered,
                "total_unread": unread,
                "templates_registered": len(self._templates),
                "unique_recipients": len(self._by_recipient),
                "by_channel": by_channel,
                "by_priority": by_priority,
                "digest_buffers_active": len(self._digest_buffer),
            }


_INSTANCE: NotificationHub | None = None
_LOCK = threading.Lock()


def get_notification_hub() -> NotificationHub:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = NotificationHub()
    return _INSTANCE
