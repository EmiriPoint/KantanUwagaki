import typing
import os
import argparse
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def process_videos(video_folder, overlay_image_path):
    # フォルダ内のすべてのファイルを反復処理します

    all_video_paths:typing.List[str] = os.listdir(video_folder)
    already_processed_videos:typing.List[str] = []

    for filename in all_video_paths:
        
        if filename.startswith("プロセス済み"):
            filename = filename[6:]

        if filename.endswith(".mp4"):

            # ファイル名を取得する
            video_name = filename[:-4]

            # すでに処理済みのファイルであればスキップする
            if video_name in already_processed_videos:
                continue

            video_path = os.path.join(video_folder, filename)
            
            # 動画とオーバーレイ画像を読み込む
            video = VideoFileClip(video_path)
            overlay = ImageClip(overlay_image_path).set_duration(video.duration).resize(video.size)

            # 動画の上に画像をオーバーレイする
            final_video = CompositeVideoClip([video, overlay], size=video.size)

            ## 出力フォルダを作成する
            output_folder = os.path.join(video_folder, 'プロセス済み')
            
            # 出力ファイルパスを定義する
            output_path = os.path.join(output_folder + filename)
            
            # ファイルに結果を書き込む
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

            print(f"Processed {filename}")

            already_processed_videos.append(video_name)

def main():
    parser = argparse.ArgumentParser(description="MP4動画の一連に画像をオーバーレイします。")
    parser.add_argument("video_folder",
                        help="MP4動画が含まれているディレクトリへのパス。")
    parser.add_argument("overlay_image",
                        help="オーバーレイ画像へのパス。")
    
    args = parser.parse_args()

    process_videos(args.video_folder, args.overlay_image)

if __name__ == "__main__":
    main()
