Save-My-Save
===

부제: **내 세이브 파일을 저장해줘**

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/game.png?raw=true" title="game.png" alt="game.png"></img><br/> 
(게임 화면)

> *세이브 슬롯이 꽉찼다!*

    RPG류의 게임을 진행하다 보면 세이브 파일의 [슬롯]이 부족할 때가 있습니다.

    그럴 때 어쩔수 없이 마지막 세이브파일 위에 덮어씌워 저장하셨나요?

### 이젠 모든 세이브 파일을 백업하세요!

+ 세이브 파일의 폴더를 **버전별로 백업**합니다!
+ 원할 때마다 이전 세이브 백업 버전을 언제든지 불러올 수 있습니다.
+ 편리한 **GUI**
+ 확장자 지정 가능!

빌드 하기전에!
---
* **Windows**에서 `build.bat`로 빌드 가능합니다.
* **Python**이 깔려있어야 하며, python venv가 정상 작동해야 합니다.

빌드하는 방법
---
<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/1.png?raw=true" title="1.png" alt="1.png"></img><br/>
 
 1. `build.bat`을 실행한다.

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/2.png?raw=true" title="2.png" alt="2.png"></img><br/>

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/3.png?raw=true" title="3.png" alt="3.png"></img><br/>

 2. 빌드를 성공하면 `save_my_save.exe`가 생성된다. 


# 사용법

## 백업
<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/main.PNG?raw=true" title="main.PNG" alt="main.PNG"></img><br/>

1. 세이브 파일이 존재하는 **타겟 폴더**를 선택해야 한다. `찾아보기...`를 누른다.

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/select_target.PNG?raw=true" title="select_target.PNG" alt="select_target.PNG"></img><br/>

2. 폴더를 선택한다.

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/lets_backup.PNG?raw=true" title="lets_backup.PNG" alt="lets_backup.PNG"></img><br/>

3. 백업 대상 파일을 드랍다운 메뉴에서 선택한다.

    여기서는 sav 문자열 포함을 선택했다.

    또한 백업 폴더를 다른 경로로 지정할 수 있다. 따로 설정하지 않으면 타겟 폴더 내에 backup 폴더가 생기고 그 폴더에 파일을 백업한다.
    
    완료했다면 `백업`을 누른다. 

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/dwbackup.PNG?raw=true" title="dwbackup.PNG" alt="dwbackup.PNG"></img><br/>

4. 백업 대상 파일 목록이 표시된다.

    백업 폴더 이름을 설정한 뒤 `백업 진행` 버튼을 누른다.

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/complete_backup.PNG?raw=true" title="complete_backup.PNG" alt="complete_backup.PNG"></img><br/>

5. 백업이 완료되었다. `백업 버전 목록`에 해당 폴더가 나타난다.


## 롤백

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/rollback.PNG?raw=true" title="rollback.PNG" alt="rollback.PNG"></img><br/>

1. 백업할 버전을 선택한다.

    그리고 `롤백` 버튼을 누른다.

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/dwrollback.PNG?raw=true" title="dwrollback.PNG" alt="dwrollback.PNG"></img><br/>

2. `롤백하기` 버튼을 누르면 버전 폴더에 있는 해당 파일들이 타겟 폴더에 덮어써진다. 

    체크박스를 활성화하면 현재 타겟 폴더의 내용을 백업할 수 있다.

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/complete_rollback.PNG?raw=true" title="complete_rollback.PNG" alt="complete_rollback.PNG"></img><br/>


3. 롤백에 성공했다.

롤백은 백업 버전 폴더에 있는 대상 파일을 타겟 폴더에 복사-붙여넣기하는 방식으로 이루어진다.

## 그 외 기능

### 파일 확인

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/home.png?raw=true" title="home.png" alt="home.png"></img><br/>

금색 `파일 확인` 버튼을 누르면 백업할 파일 목록을 확인할수 있다.

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/files.png?raw=true" title="files.png" alt="files.png"></img><br/>

백업될 파일을 미리 확인할 수 있다.

### 폴더 열기

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/openfolder.png?raw=true" title="openfolder.png" alt="openfolder.png"></img><br/>

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/backups.png?raw=true" title="backups.png" alt="backups.png"></img><br/>

`폴더 열기`를 누르면 Windows 탐색기가 열린다.

백업 폴더 내 버전 폴더들을 볼 수 있다.

### 폴더 삭제

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/del.png?raw=true" title="del.png" alt="del.png"></img><br/>

버전을 선택하여 **오른쪽 마우스**를 누르면 제거 버튼이 나타난다.

### 타겟 파일 변경

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/targetfiles.png?raw=true" title="targetfiles.png" alt="targetfiles.png"></img><br/>

타겟 파일을 변경할 수 있다. 기본적인 리스트는 위와 같다.

<img src="https://github.com/simjeehoon/src_repository/blob/master/Save-My-Save/master/extension.png?raw=true" title="extension.png" alt="extension.png"></img><br/>

`확장자 직접 입력...` 을 누르면 위와 같이 확장자를 직접 지정할 수 있다.

#### gui.py의 12번째 라인 target_options의 리스트를 수정하면 타겟 파일 리스트를 변경할 수 있다.
```py
target_options = {
            "sav 문자열 포함": ".*sav.*",
            "*.rpgsave": ".*[.]rpgsave$",
            "*.rvdata": ".*[.]rvdata$",
            "*.rvdata2": ".*[.]rvdata2$",
            "모든 파일": ".*",
            "확장자 직접 입력...": None
        }
```

key는 드랍다운 메뉴에 표시되는 이름이며, value는 정규표현식이다.