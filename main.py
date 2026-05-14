import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

# التوكن
TOKEN = "8314642811:AAFrNDND_jZNLfU1HRbZHaskkaDoSz73X0s"

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if not url.startswith("http"):
        return 

    msg = await update.message.reply_text(
        "🚀 جاري تحضير الفيديو بأعلى جودة للصوت والصورة..."
    )
 
    # إنشاء مجلد التحميل
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        # أفضل جودة فيديو + صوت
        "format": "bestvideo+bestaudio/best",

        # اسم الملف
        "outtmpl": "downloads/%(title)s.%(ext)s",

        # تحويل نهائي MP4
        "merge_output_format": "mp4",

        "quiet": True,

        # بوست بروسس لتحويل الفيديو
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # الاسم النهائي بعد الدمج
            filename = ydl.prepare_filename(info)

            # تحويل الامتداد إلى mp4 إذا تغير
            filename = os.path.splitext(filename)[0] + ".mp4"

        # إرسال الفيديو
        with open(filename, "rb") as video_file:
            await update.message.reply_video(
                video=video_file,
                caption="✅ تم التحميل بجودة صافية\nجاهز للنشر في السناب والستوري",
                supports_streaming=True
            )

        # حذف الملف بعد الإرسال
        os.remove(filename)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ:\n{str(e)}")


# تشغيل البوت
if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & (~filters.COMMAND),
            download_video
        )
    )

    print("✅ البوت شغال الآن...")

    app.run_polling()