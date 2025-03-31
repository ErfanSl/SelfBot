from telethon import TelegramClient, events
import asyncio

# اطلاعات API
api_id = 26769044  
api_hash = "e24a76ce4cf9f8e24dd701a611a3b3ed"
client = TelegramClient("selfbot", api_id, api_hash)

# یوزرنیم ربات شما
bot_username = "@ErfanSl_Bot"  # تغییر به یوزرنیم ربات شما

# دیکشنری برای ذخیره پیام‌ها
message_cache = {}

# ذخیره پیام‌های دریافتی و عکس‌های تایمی
@client.on(events.NewMessage(incoming=True))
async def store_message(event):
    if event.is_private:  # فقط در چت‌های خصوصی
        sender = await event.get_sender()
        sender_name = sender.first_name if sender else "نامشخص"
        sender_id = sender.id if sender else "نامشخص"
        sender_username = f"@{sender.username}" if sender.username else "ندارد"

        # ذخیره پیام در حافظه
        message_cache[event.message.id] = {
            "message": event.message,
            "sender_name": sender_name,
            "sender_id": sender_id,
            "sender_username": sender_username
        }

        # ذخیره عکس‌های تایمی بلافاصله بعد از دریافت
        if event.message.media and event.message.photo:
            try:
                file_path = await client.download_media(event.message.media)
                if file_path:
                    caption = f"📸 *عکس تایمی ذخیره شد!*\n👤 *فرستنده:* {sender_name}\n🆔 *ID:* {sender_id}\n🔗 *یوزرنیم:* {sender_username}"
                    await client.send_file(bot_username, file_path, caption=caption)
            except Exception as e:
                print(f"❌ خطا در ذخیره عکس تایمی: {e}")

# بررسی حذف پیام‌ها
@client.on(events.MessageDeleted)
async def deleted_message(event):
    for msg_id in event.deleted_ids:
        if msg_id in message_cache:
            deleted_data = message_cache[msg_id]
            deleted_msg = deleted_data["message"]
            sender_name = deleted_data["sender_name"]
            sender_id = deleted_data["sender_id"]
            sender_username = deleted_data["sender_username"]
            
            message_content = f"🚨 *پیام حذف شد!*\n\n👤 *فرستنده:* {sender_name}\n🆔 *ID:* {sender_id}\n🔗 *یوزرنیم:* {sender_username}\n\n"
            if deleted_msg.text:
                message_content += f"📝 *متن:* {deleted_msg.text}\n"

            # ارسال پیام حذف‌شده به ربات
            try:
                await client.send_message(bot_username, message_content)
            except Exception as e:
                print(f"❌ خطا هنگام ارسال پیام به ربات: {e}")

            # ارسال فایل‌های حذف‌شده
            if deleted_msg.media:
                try:
                    file_path = await client.download_media(deleted_msg.media)
                    if file_path:
                        await client.send_file(bot_username, file_path, caption="🖼 *رسانه حذف‌شده!*")
                except Exception as e:
                    print(f"❌ خطا در ذخیره و ارسال رسانه: {e}")

            # حذف پیام از حافظه
            del message_cache[msg_id]

client.start()
print("✅ سلف‌بات فعال شد! لطفاً پیام ارسال و حذف کنید تا تست شود.")
client.run_until_disconnected()

