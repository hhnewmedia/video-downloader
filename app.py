import streamlit as st
import subprocess
import os

st.title("跨平台影音下載與壓縮小工具")

url = st.text_input("請貼上影片網址：")
compress_level = st.selectbox("請選擇壓縮級別：", ["不壓縮", "中度壓縮 (720p)", "高度壓縮 (480p)"])

if st.button("開始處理"):
    if url:
        st.info("影片下載中，這可能需要幾十秒鐘，請稍候...")
        
        # 步驟 0: 清理前次運作遺留的暫存檔案，避免干擾
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")
        if os.path.exists("final_video.mp4"):
            os.remove("final_video.mp4")
        
        # 步驟 1: 使用 yt-dlp 下載影片，強制要求最終輸出為 mp4 格式
        download_cmd = [
            "yt-dlp", 
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
            "--merge-output-format", "mp4",
            "-o", "temp_video.mp4", 
            url
        ]
        
        # 執行指令並捕捉可能發生的錯誤訊息
        result = subprocess.run(download_cmd, capture_output=True, text=True)
        
        # 檢查檔案是否真的有產生出來
        if not os.path.exists("temp_video.mp4"):
            st.error("❌ 下載失敗！可能是該平台阻擋了伺服器，或網址不支援。")
            with st.expander("點此查看詳細系統錯誤訊息"):
                st.code(result.stderr)
        else:
            st.info("影片處理中...")
            output_file = "final_video.mp4"
            
            # 步驟 2: 進行壓縮或重新命名
            try:
                if compress_level == "中度壓縮 (720p)":
                    ffmpeg_cmd = ["ffmpeg", "-i", "temp_video.mp4", "-vf", "scale=-2:720", "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-y", output_file]
                    subprocess.run(ffmpeg_cmd)
                elif compress_level == "高度壓縮 (480p)":
                    ffmpeg_cmd = ["ffmpeg", "-i", "temp_video.mp4", "-vf", "scale=-2:480", "-c:v", "libx264", "-crf", "28", "-preset", "fast", "-y", output_file]
                    subprocess.run(ffmpeg_cmd)
                else:
                    os.rename("temp_video.mp4", output_file)
                    
                # 步驟 3: 產生下載按鈕
                if os.path.exists(output_file):
                    with open(output_file, "rb") as file:
                        st.download_button(
                            label="⬇️ 點擊下載影片",
                            data=file,
                            file_name="downloaded_video.mp4",
                            mime="video/mp4"
                        )
                    st.success("✅ 處理完成！")
                else:
                    st.error("❌ 壓縮或處理過程中發生錯誤。")
                    
            except Exception as e:
                st.error(f"發生未預期的程式錯誤：{e}")
                
    else:
        st.warning("請先輸入網址！")
