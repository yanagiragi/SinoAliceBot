$script_path = $MyInvocation.MyCommand.Path

cd "$script_path/../../"
$scrcpy = "../scrcpy-win64-v2.0/scrcpy.exe"

Start-Process "$scrcpy" -NoNewWindow -ArgumentList "--stay-awake --turn-screen-off --show-touches --power-off-on-close --window-x=960 --window-y=50 --window-width=461 --window-height=976"

Start-Sleep -Seconds 10

python main.py --debug true --routine "ProjectSekaiDaily"
python main.py --debug true --routine "HeavenBurnsRedDaily"
python main.py --debug true --routine "Deemo2Daily"
python main.py --debug true --routine "SinoaliceDaily"

$proc = Get-Process -Name "scrcpy"
Stop-Process -InputObject $proc