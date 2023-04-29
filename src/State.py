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
    COOP_SELECT_STAGE = '共鬪 (選ぶ)', 
    OS_ABOUT_TO_CLOSE_ALL_TASKS = 'OS-已開啟程式 (主畫面過渡)'
    OS_CLOSE_ALL_TASKS = 'OS-已開啟程式'
    OS_HOME = 'OS-主畫面'
    
    HEAVEN_BURNS_RED_APP_HOME = 'HBD-開始畫面'
    HEAVEN_BURNS_RED_HOME = 'HBD-主畫面',
    HEAVEN_BURNS_RED_LOGIN_BONUS = 'HBD-登入獎勵',
    HEAVEN_BURNS_RED_COMFIRM = 'HBD-待確認項目',
    HEAVEN_BURNS_RED_SKIP = 'HBD-待跳過項目',
    HEAVEN_BURNS_RED_DOWNLOAD = 'HBD-下載資源',
    HEAVEN_BURNS_RED_INHERIT = 'HBD-繼承帳號',
    
    PROJECT_SEKAI_APP_HOME = 'PS-開始畫面'
    PROJECT_SEKAI_HOME = 'PS-主畫面',
    PROJECT_SEKAI_LOGIN_BONUS = 'PS-登入獎勵',
    PROJECT_SEKAI_COMFIRM = 'PS-待確認項目',
    PROJECT_SEKAI_DOWNLOAD = 'PS-下載資源',
    PROJECT_SEKAI_PLAY_LOGIN = 'PS-Play登入',
    
    DEEMO2_CONFRIM = 'D2-待確認項目',
    DEEMO2_CLOSE = 'D2-待關閉項目',
    DEEMO2_LOGO = 'D2-Logo',
    DEEMO2_LOGIN_BONUS = 'D2-登入獎勵',
    DEEMO2_HOME = 'D2-主畫面',
    
    SINOALICE_LOGO = 'SA-Logo'
    SINOALICE_CLOSE = 'SA-待關閉項目',
    SINOALICE_CANCEL = 'SA-待取消項目'
    SINOALICE_OK = 'SA-待確認項目'
    SINOALICE_MISSION_MAIN = 'SA-主要任務'
    SINOALICE_MISSION_DAILY = 'SA-每日任務'
    SINOALICE_MISSION_DAILY_NO_REWARD = 'SA-每日任務 (已領取)'
    SINOALICE_HOME = 'SA-主畫面'
    SINOALICE_RECEIVE_REWARD = 'SA-領取獎勵'