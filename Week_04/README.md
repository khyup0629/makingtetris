# Week 4.

- 템플릿 사용하여 API구현하기
- API 명세서 작성

## 환경 구축

AWS에서 `Ubuntu 18.04`로 인스턴스를 하나 생성해줍니다.   
WinSCP의 PuTTy를 통해 서버에 접속해 아래의 명령어를 입력해 환경을 구축합니다.

```
// 관리자 루트로 접속
sudo su
apt update
apt upgrade
apt install nginx -y
// nginx가 잘 구동되는지 체크
systemctl status nginx
```

이제 사전에 준비된 `api-server-node` 압축파일의 파일을 풀고 WinSCP를 통해 `/home/ubuntu` 경로에 드래그 앤 드롭으로 넣어줍니다.   
그리고 터미널을 다시 띄우고 `api-server-node` 폴더를 `/var/www` 경로로 옮겨줍니다.

```
sudo mv api-server-node /var/www
```

```
cd /var/www/api-server-node
vi package.json
```

`package.json` 파일을 수정해줍시다.   

![image](https://user-images.githubusercontent.com/43658658/134478339-9411cee6-5d29-4ab1-8e9b-84680932b262.png)

repository와 관련된 내용을 삭제해주고 저장합니다.   
문법에 맞게 지우지 않으면, 후에 있을 `npm install`에서 파싱 오류가 발생합니다.   
(모듈을 다운 받을 때 패키지 파일을 파싱하여 그 정보를 토대로 다운로드 받기 때문입니다)

> <h3>npm 설치</h3>

- [npm](https://ko.wikipedia.org/wiki/Npm_(%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4))   
npm (노드 패키지 매니저/Node Package Manager)은 `자바스크립트` 프로그래밍 언어를 위한 `패키지 관리자`이다. 자바스크립트 런타임 환경 Node.js의 기본 패키지 관리자이다. 
명령 줄 클라이언트(`npm`), 그리고 공개 패키지와 지불 방식의 개인 패키지의 온라인 데이터베이스(`npm 레지스트리`)로 이루어져 있다. 
이 레지스트리는 클라이언트를 통해 접근되며 사용 가능한 패키지들은 npm 웹사이트를 통해 찾아보고 검색할 수 있다. 패키지 관리자와 레지스트리는 npm사에 의해 관리된다.

```
// npm 설치 전 한 번 더 업데이트
apt update
apt install npm
```

`package.json`이 있는 폴더 안에서 아래의 명령어를 입력하면 `package.json`에 적혀있는 정보들을 토대로 필요한 모듈들을 다운로드 해줍니다.

```
npm install
```

Node.js를 이용해 원격에서 파일을 추가, 수정, 삭제할 때 js파일이 들어있는 폴더에 권한을 설정해주어야 합니다.   

```
sudo chmod -R 777 api-server-node
```

chmod 777 : 모든 사용자가 읽고 쓰고 실행할 수 있는 권한 지정   
-R : 지정한 디렉토리의 하위 디렉토리를 포함하여 모든 권한 지정

```
node index.js
```



