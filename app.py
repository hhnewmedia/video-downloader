import streamlit as st
import subprocess
import os

st.title("跨平台影音下載與壓縮小工具")

url = st.text_input("請貼上影片網址：")
compress_level = st.selectbox("請選擇壓縮級別：", ["不壓縮", "中度壓縮 (720p)", "高度壓縮 (480p)"])

if st.button("開始處理"):
    if url:
        st.info("影片下載中，請稍候...")
        
        # 1. 使用 yt-dlp 下載影片 (示意指令)
        download_cmd = ["yt-dlp", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]", "-o", "temp_video.%(ext)s", url]
        subprocess.run(download_cmd)
        
        st.info("影片壓縮中...")
        
        # 2. 使用 FFmpeg 進行壓縮 (示意指令)
        output_file = "final_video.mp4"
        if compress_level == "中度壓縮 (720p)":
            ffmpeg_cmd = ["ffmpeg", "-i", "temp_video.mp4", "-vf", "scale=-2:720", "-c:v", "libx264", "-crf", "23", "-preset", "fast", output_file]
            subprocess.run(ffmpeg_cmd)
        elif compress_level == "高度壓縮 (480p)":
            ffmpeg_cmd = ["ffmpeg", "-i", "temp_video.mp4", "-vf", "scale=-2:480", "-c:v", "libx264", "-crf", "28", "-preset", "fast", output_file]
            subprocess.run(ffmpeg_cmd)
        else:
            os.rename("temp_video.mp4", output_file)

        # 3. 提供下載按鈕
        with open(output_file, "rb") as file:
            btn = st.download_button(
                label="點擊下載影片",
                data=file,
                file_name="downloaded_video.mp4",
                mime="video/mp4"
            )
            
        st.success("處理完成！")
    else:
        st.warning("請先輸入網址！")
