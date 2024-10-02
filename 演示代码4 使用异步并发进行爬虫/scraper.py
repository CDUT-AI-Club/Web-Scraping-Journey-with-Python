import aiohttp
import asyncio
import os
import time
from hashlib import md5


class AsyncImageDownloader:
    def __init__(
        self,
        url,
        output_folder,
        num_images,
        response_time_limit=10,
        max_workers=5,
        max_retries=3,
    ):
        self.url = url
        self.output_folder = output_folder
        self.num_images = num_images
        self.response_time_limit = response_time_limit
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.image_hashes = set()
        self.task_queue = asyncio.Queue()

        os.makedirs(output_folder, exist_ok=True)

    async def save_image(self, session, i):
        start_time = time.perf_counter()
        retries = 0
        while retries < self.max_retries:
            try:
                async with session.get(
                    self.url, timeout=self.response_time_limit
                ) as response:
                    if response.status == 200:
                        content = await response.read()
                        image_hash = md5(content).hexdigest()

                        # 检查是否是重复图片
                        if image_hash in self.image_hashes:
                            print(f"第{i}次尝试获取到重复图片，重新下载。")
                            return False  # 返回 False 表示下载失败

                        # 保存图片
                        self.image_hashes.add(image_hash)
                        image_path = os.path.join(
                            self.output_folder, f"person_{i + 1}.jpg"
                        )
                        with open(image_path, "wb") as file:
                            file.write(content)
                        elapsed_time = time.perf_counter() - start_time
                        print(f"图片保存成功: {image_path}，耗时: {elapsed_time:.2f}秒")
                        return True

                    else:
                        print(f"图片获取失败, 状态码: {response.status}")
                        retries += 1

            except asyncio.TimeoutError:
                print(f"第{i}次尝试请求时间超时，重试中...")
                retries += 1
            except Exception as e:
                print(f"第{i}次尝试出现错误: {e}")
                retries += 1

        return False  # 返回 False 表示下载失败

    async def worker(self, session):
        while True:
            i = await self.task_queue.get()
            if i is None:
                break
            success = await self.save_image(session, i)
            if not success:
                await self.task_queue.put(i)  # 失败时重新放回队列
            self.task_queue.task_done()

    async def download_images(self):
        start_total_time = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            # 将所有图片索引放入队列
            for i in range(self.num_images):
                await self.task_queue.put(i)

            # 启动工作线程
            tasks = [
                asyncio.create_task(self.worker(session))
                for _ in range(self.max_workers)
            ]

            await self.task_queue.join()  # 等待队列处理完成

            # 停止工作线程
            for _ in range(self.max_workers):
                await self.task_queue.put(None)

            await asyncio.gather(*tasks)  # 等待所有工作线程完成

        total_time_elapsed = time.perf_counter() - start_total_time
        print(
            f"数据集创建完毕，共保存图片 {self.num_images} 张，总耗时: {total_time_elapsed:.2f}秒。"
        )


def main():
    url = "https://thispersondoesnotexist.com/"
    output_folder = "ai_generated_faces"
    num_images = 100

    downloader = AsyncImageDownloader(url, output_folder, num_images)

    # 使用当前事件循环
    loop = asyncio.get_event_loop()
    loop.run_until_complete(downloader.download_images())


if __name__ == "__main__":
    main()
