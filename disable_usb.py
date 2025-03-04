import subprocess
import ctypes
import sys
import time
import os

disable_usb_script = r"""Get-PnpDevice | Where-Object {$_.InstanceId -like "USB\ROOT_HUB*"} | Disable-PnpDevice -Confirm:$false -ErrorAction SilentlyContinue
"""

enable_usb_script = r"""$devices = Get-PnpDevice | Where-Object { 
    $_.InstanceId -like "USB\ROOT_HUB*" -and $_.Status -eq "Error" 
}
if ($devices) {
    $devices | Enable-PnpDevice -Confirm:$false
    Write-Host "Portas USB reativadas com sucesso!"
} else {
    Write-Host "Nenhum dispositivo USB desativado encontrado."
}
"""

def write_files(files, names = ['enable.ps1','disable.ps1']):
    for file, name in zip(files, names):
        with open(name, 'w') as f:
            for line in file.split('\n'):
                f.write(f'{line} \n')

def is_admin():
    """
    Verifica se o script está sendo executado com privilégios de administrador.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_powershell_script(script_path):
    try:
        command = [
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",  
            "-File", script_path
        ]
        
        if is_admin():
            subprocess.run(command, check=True, shell=True)
        else:
            # Re-executa o script com elevação
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(command), None, 1
            )
            
        print("Script executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the script: {e}")

def clear_cli():
    subprocess.run('cls', shell=True)

def show_proces():
    clear_cli()
    print('Processing...')

def main():
    while(True):
        print('USB Ports')
        print('1 - Disable')
        print('2 - Enable')
        print('3 - Disable and Enable')
        print('4 - Exit')
        try:
            op = int(input('Choose an option: '))
        except:
            print('Invalid value: must be an integer')
            continue
        
        if op == 3:
            time_wait = int(input('Waiting time (int):'))
            show_proces()
            run_powershell_script('disable.ps1')
            print("USB port disabled")
            time.sleep(time_wait)
            run_powershell_script('enable.ps1')
            print("USB port enabled")
            time.sleep(1)
        elif op == 2:
            show_proces()
            run_powershell_script('enable.ps1')
            print("USB port enabled")
            time.sleep(1)
        elif op == 1:
            show_proces()
            run_powershell_script('disable.ps1')
            print("USB port disabled")
            time.sleep(2)
        elif op == 4:
            break
        
        clear_cli()

if __name__ == "__main__":
    write_files([enable_usb_script, disable_usb_script])
    main()
    #with open('time.txt', 'r') as f:
    #    inter = int(f.read().strip())
    #print(inter)
    #show_proces()
    #run_powershell_script('disable.ps1')
    #print("Porta desativada")
    #time.sleep(inter)
    #run_powershell_script('enable.ps1')
    #print("Porta Ativada")
    #time.sleep(1)
    os.remove('enable.ps1')
    os.remove('disable.ps1')
