import httpx
from tqdm import tqdm
from rich.console import Console
console = Console()
# def downloadFile(url: str, save_path: str, params=None):
#     try:
#         if params:
#             console.log(params)
#             response = requests.get(url, params=params, stream=True)
#         else:
#             response = requests.get(url, stream=True)
#         if response.status_code == 200:
#             total_size = int(response.headers.get('content-length', 0))
#             block_size = 1024
#             progressBar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f"Downloading {save_path}")
            
#             # 打开文件并开始下载
#             with open(save_path, 'wb') as file:
#                 for data in response.iter_content(block_size):
#                     progressBar.update(len(data))
#                     file.write(data)
            
#             progressBar.close()
#             if total_size != 0 and progressBar.n != total_size:
#                 print("\n下载不完整 请检查网络（重新下载请删除服务器后重新安装）")
#                 return False
#             else:
#                 print("\n下载完成!")
#             return True
#         else:
#             print(f"无法下载 HTTP 状态码: {response.status_code} （重新下载请删除服务器后重新安装）")
#             return False
#     except Exception as e:
#         print(f"出现错误: {e}")
#         return False
async def downloadfile(url: str, path: str, params=None, timeout: int = 60, threads: int = 1) -> bool:
    try:
        async with httpx.AsyncClient(timeout=timeout,params=params, limits=httpx.Limits(max_connections=threads)) as Client:
            response = await Client.get(url=url,)
            if response.status_code == 200:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                progressBar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f"Downloading {path}")
                with open(path, 'wb') as file:
                    async for data in response.aiter_bytes(block_size):
                        progressBar.update(len(data))
                        file.write(data)
                progressBar.close()
                if total_size != 0 and progressBar.n != total_size:
                    console.log(f"下载不完整 请检查网络（重新下载请删除服务器后重新安装）")
                    return False
                else:
                    console.log(f"下载完成!")
                return True
            else:
                console.log(f"无法下载 HTTP 状态码: {response.status_code} （重新下载请删除服务器后重新安装）")
                return False
    except Exception as e:
        console.log(f"出现错误: {e}")
        return False