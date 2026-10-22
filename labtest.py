# uv add matplotlib
# uv add numpy

import numpy as np
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm
from datetime import datetime

# ==========================
# 댓글 수집
# ==========================
total_comments = []
num_posts = 100

for post_id in tqdm(range(1, num_posts + 1)):
    url = f"http://board.nyan101.com/comments/{post_id}"
    response = requests.get(url)
    comments = response.json()
    total_comments.extend(comments)

print(f"[+] get {len(total_comments)} comments")
print()

# ==========================
# 사용자별 댓글 정리
# ==========================
print("[+] processing...")

user_comments = {}

for comment in total_comments:
    author_id = comment["author_id"]

    if author_id not in user_comments:
        user_comments[author_id] = []

    user_comments[author_id].append(comment)

print(f"[+] get {len(user_comments)} users")
print(f"[+] users : {list(user_comments.keys())}")
print()

# ==========================
# 한글 폰트 (Windows)
# ==========================
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ==========================
# 사용자별 그래프 출력
# ==========================
for target_user_id in user_comments:

    target_user_name = user_comments[target_user_id][0]["author_name"]

    print(f"User #{target_user_id} : {target_user_name}")

    # 24시간 x 7일
    activity_matrix = np.zeros((24, 7), dtype=int)

    # 댓글 분석
    for comment in user_comments[target_user_id]:

        dt = datetime.strptime(
            comment["created_at"],
            "%Y-%m-%d %H:%M"
        )

        weekday = dt.weekday()      # 0~6
        hour = dt.hour              # 0~23

        activity_matrix[hour][weekday] += 1

    # ----------------------
    # 그래프
    # ----------------------
    plt.figure(figsize=(6, 8))

    plt.imshow(activity_matrix,
               cmap="YlOrRd",
               aspect="auto")

    plt.colorbar(label="활동 횟수")

    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    plt.xticks(range(7), weekdays)

    hours = [f"{i:02d}" for i in range(24)]
    plt.yticks(range(24), hours)

    plt.title(f"User #{target_user_id} ({target_user_name})의 활동 패턴")

    # 숫자 표시
    for hour in range(24):
        for weekday in range(7):
            if activity_matrix[hour][weekday] > 0:
                plt.text(
                    weekday,
                    hour,
                    activity_matrix[hour][weekday],
                    ha="center",
                    va="center",
                    fontsize=8
                )

    plt.tight_layout()
    plt.show()

    # 저장하려면 아래 사용
    # plt.savefig(
    #     f"{target_user_id}_{target_user_name}.png",
    #     dpi=300,
    #     bbox_inches="tight"
    # )
    # plt.close()
