import typing
import os
import argparse
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def process_videos(video_folder: str, overlay_image_path: str):
    """
    指定されたフォルダ内のすべての動画を処理し、指定された画像でオーバーレイします。
    """
    all_video_paths: typing.List[str] = os.listdir(video_folder)
    already_processed_videos: typing.List[str] = []

    for filename in all_video_paths:

        remove_prefix_flag = False
        # すでに処理されたファイルはスキップ
        if filename.startswith("プロセス済み"):
            remove_prefix_flag = True

        if filename.endswith(".mp4"):
            video_path = os.path.join(video_folder, filename)
            
            # 動画とオーバーレイ画像を読み込む
            video = VideoFileClip(video_path)
            overlay = ImageClip(overlay_image_path).set_duration(video.duration).resize(video.size)

            # 動画に画像をオーバーレイする
            final_video = CompositeVideoClip([video, overlay], size=video.size)

            # 出力フォルダが存在しない場合は作成
            output_folder = os.path.join(video_folder, 'processed')
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # 出力ファイルパスを定義
            output_filename = "k_" + filename
            output_path = os.path.join(output_folder, output_filename)

            if remove_prefix_flag:
                output_path = output_path.replace("プロセス済み", "")
            
            # 結果をファイルに書き込む
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

            print(f"{filename} を処理しました。")
            already_processed_videos.append(filename)

def main():
    parser = argparse.ArgumentParser(description="MP4動画に画像をオーバーレイします。")
    parser.add_argument("video_folder", help="MP4動画が含まれるディレクトリへのパス。")
    parser.add_argument("overlay_image", help="オーバーレイ画像へのパス。")
    
    args = parser.parse_args()
    process_videos(args.video_folder, args.overlay_image)

if __name__ == "__main__":
    main()
