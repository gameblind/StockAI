
# 示例调用
if __name__ == "__main__":
    response = create_video_task(
        prompt="A futuristic city with flying cars under a sunset sky",
        negative_prompt="low quality, blurry",
        cfg_scale=0.8,
        mode="pro",
        aspect_ratio="16:9",
        duration="5",
        callback_url=None,
        external_task_id="custom_task_001"
    )

    if response:
        logging.info("Task Created:")
        logging.info(json.dumps(response, indent=4))

    task_id = response.get("task_id") if response else None
    if task_id:
        while True:
            task_status = get_task_status(task_id=task_id)
            if task_status:
                logging.info("Task Status:")
                logging.info(json.dumps(task_status, indent=4))

                if task_status.get("task_status") == "succeed":
                    videos = task_status.get("task_result", {}).get("videos", [])
                    for video in videos:
                        video_url = video.get("url")
                        if video_url:
                            save_video(video_url)
                    break
                elif task_status.get("task_status") == "failed":
                    logging.error(f"Task failed: {task_status.get('task_status_msg')}")
                    break