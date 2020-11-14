from enum import Enum

class State(Enum):
    IDLE = 'IDLE'    
    BATTLE = '周回する'
    REMATCH = '再戦'
    NEXT = '次へ'
    NO_AP = 'AP 回復 確認'
    OSOUJI = 'お掃除中'
    OSOUJI_COMFIRM = 'お掃除 確認'
    OSOUJI_RESULT_COMFIRM = 'お掃除 結果確認'
    HOME = 'ホームページ'
    SELECT_EVENT = '物語 選択'
    SELECT_STAGE = 'イベント 選択'
    SELECT_LEVEL = '章節 選択'
    SELECT_LEVEL_CONFIRM = '章節 確認'
    OSOUJI_LEVEL_COMFIRM = 'お掃除 確認 (体力不足)'
    STORY_SKIP = 'SKIP'
    STAGE_NORMAL_IDLE = '章節 選択頁面 (Normal)'
    STAGE_HARD_IDLE = '章節 選択頁面 (HARD)'
    STAGE_LOOP_END = '章節ループ 任務完了'
    CLEANUP_BEFORE_DONE = '任務完了 直前'
    DONE = '任務完了'
    TARGET_LEVEL_NOT_FOUND = 'ターゲット章節 検索中'
    TARGET_STAGE_NOT_FOUND = 'ターゲットイベント 検索中',
    BATTLE_RESULT_COMFIRM = '周回 完了'
    DOWNLOADING = 'ダウンロード 中'
    DOWNLOADPOPOUT = 'ダウンロード 提示'
    ONSTART = '起動 中'
    APPSTART = '開始'
    INFO = 'お知らせ'
    COOP_NOT_PICK_GUILD_MEMBER_PANEL = '共鬪 (ランダム)'
    COOP_PICK_GUILD_MEMBER_PANEL = '共鬪 (ギルドメンバー)'