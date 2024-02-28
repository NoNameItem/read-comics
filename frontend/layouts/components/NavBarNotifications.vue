<script lang="ts" setup>
import avatar3 from "@images/avatars/avatar-3.png"
import avatar4 from "@images/avatars/avatar-4.png"
import avatar5 from "@images/avatars/avatar-5.png"
import paypal from "@images/svg/paypal.svg"
import type { Notification } from "@layouts/types"

const notifications = ref<Notification[]>([
  {
    id:       1,
    img:      avatar4,
    isSeen:   true,
    subtitle: "Won the monthly best seller badge",
    time:     "Today",
    title:    "Congratulation Flora! 🎉",
  },
  {
    id:       2,
    isSeen:   false,
    subtitle: "5 hours ago",
    text:     "Tom Holland",
    time:     "Yesterday",
    title:    "New user registered.",
  },
  {
    id:       3,
    img:      avatar5,
    isSeen:   true,
    subtitle: "You have 10 unread messages",
    time:     "11 Aug",
    title:    "New message received 👋🏻",
  },
  {
    color:    "error",
    id:       4,
    img:      paypal,
    isSeen:   false,
    subtitle: "Received Payment",
    time:     "25 May",
    title:    "PayPal",
  },
  {
    id:       5,
    img:      avatar3,
    isSeen:   true,
    subtitle: "New order received from john",
    time:     "19 Mar",
    title:    "Received Order 📦",
  },
])

const removeNotification = (notificationId: number) => {
  notifications.value.forEach((item, index) => {
    if (notificationId === item.id) { notifications.value.splice(index, 1) }
  })
}

const markRead = (notificationId: number[]) => {
  notifications.value.forEach((item) => {
    notificationId.forEach((id) => {
      if (id === item.id) { item.isSeen = true }
    })
  })
}

const markUnRead = (notificationId: number[]) => {
  notifications.value.forEach((item) => {
    notificationId.forEach((id) => {
      if (id === item.id) { item.isSeen = false }
    })
  })
}

const handleNotificationClick = (notification: Notification) => {
  if (!notification.isSeen) { markRead([notification.id]) }
}
</script>

<template>
  <Notifications
    :notifications="notifications"
    @click:notification="handleNotificationClick"
    @read="markRead"
    @remove="removeNotification"
    @unread="markUnRead"
  />
</template>
