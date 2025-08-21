echo 
PATH = $(dirname ${BASH_SOURCE[0]})

git pull || { echo "[오류] git pull 실패"; exit 1; }
python3 $(PATH) || { echo "[오류] DatasetUpdater.py 실행 실패"; exit 1; }

git add . || { echo "[오류] git add 실패"; exit 1; }

COMMIT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo "===== git commit ====="
git commit -m "[$COMMIT_TIME] update status using AutoCommit"
commitResult=$?

if [[ $commitResult -eq 1 ]]; then
    echo "[정보] 커밋할 변경 사항이 없습니다."
elif [[ $commitResult -ne 0 ]]; then
    echo "[오류] git commit 실패"
    exit 1
fi

read -p "변경 사항을 원격 저장소에 push 하시겠습니까? (y/n): " doPush
if [[ "$doPush" =~ ^[Yy]$ ]]; then
    echo "===== git push 실행 ====="
    git push || { echo "[오류] git push 실패"; exit 1; }
    echo "[완료] 변경 사항이 $COMMIT_TIME 시각으로 원격 저장소에 푸시되었습니다."
else
    echo "[중단] push 명령이 취소되었습니다."
fi

