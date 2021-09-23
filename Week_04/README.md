# Week 4.

- Node.js 환경 구축(nginx 설치, npm 설치, 리버스 프록시 설정, pm2 설치)
- 템플릿 사용하여 API구현하기
- API 명세서 작성

## 환경 구축

AWS에서 `Ubuntu 18.04`로 인스턴스를 하나 생성해줍니다.   
(이때 인바운드 규칙에서 3000번 포트를 개방합니다)
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

![image](https://user-images.githubusercontent.com/43658658/134497244-92f9229a-7826-45d6-8d30-589e207cd858.png)

`node`를 정상적으로 실행하면 위와 같은 화면이 됩니다.   
`[Ctrl] + [C]`를 눌러 `node를 종료`합니다.

> <h3>리버스 프록시 서버 설정</h3>

node를 실행하게 되면 80번 포트를 통해 통신을 할 수 없게 됩니다. 계속해서 3000번 포트를 사용해야합니다.   
또한 SSL인증을 하게 되어도 의미가 없어집니다.   
원래 Client에서 Server로 요청을 보내게 되면 Web Server가 먼저 해당 내용을 받아서 Backend Language와 DB에 보내주게 됩니다.   
하지만 3000번 포트로 연결되면 Web Server를 거치지 않고 바로 Backend Language로 넘어가기 때문에   
Web Server에 SSL 보안 인증을 받아도 이용할 수가 없는 것입니다.   
따라서 보안에도 문제가 발생합니다.   

이를 해결하기 위해 `리버스 프록시(Reverse Proxy) 서버`를 이용하게 됩니다.
3000번 포트로의 요청을 리버스 프록시 서버로 가게 하고 nginx(Web Server)로 오는 요청을 3000번 포트로 돌리게 합니다.   
따라서 모든 요청이 3000번 포트를 통해 리버스 프록시 서버로 갑니다.

`리버스 프록시 서버`를 이용하면 보안에 대한 문제가 해결됩니다.   
웹서버 앞쪽에 리버스 프록시 서버를 두면 리버스 프록시 서버가 마치 웹 서버와 같은 역할을 하는 것처럼 보입니다.   
실제로 중요한 내용들은 뒤쪽에 내부 망에 두게 되면 리버스 프록시 서버가 해킹되더라도 피해를 줄일 수 있습니다.

=> [리버스 프록시 개념](https://ohhhmycode.tistory.com/2)   
=> [리버스 프록시(reverse proxy) 가이드 메뉴얼](https://sanghaklee.tistory.com/11)

```
sudo vi /etc/nginx/sites-available/default
```

![image](https://user-images.githubusercontent.com/43658658/134500339-90a0054c-52ac-4189-a041-fd6cde75e966.png)

`default`에 들어가서 먼저 root의 내용을 api-server-node로 바꿔줍니다.   
index 파일에 `index.js` 파일을 추가해줍니다.   
그리고 `location`의 위치에 위의 내용까지 추가해줍니다.

> <h3>pm2 설치</h3>

`pm2`는 웹 서버를 서비스할 때 서비스가 중단이 되지 않도록 하기 위한 프로그램입니다.
Node는 싱글 쓰레드를 사용하므로 개발자가 서버를 관리할 때 클라이언트에게 서비스가 중단될 수 있습니다.   
pm2는 멀티 쓰레드를 지원하므로 클라이언트에게 중단 없이 서비스를 할 수 있게 됩니다.

=> [pm2 패키지 설치 및 사용법](https://dydals5678.tistory.com/100)

```
// pm2 설치
npm install pm2 -g
```

```
// pm2 시작
pm2 start index.js
// 실행할 js파일을 --watch 옵션으로 실행하면 소스 수정 후 저장하면 자동으로 node를 재시작해줘서 소스적용이 됩니다. 
pm2 start app.js --watch 
//백그라운드로 실행되는 프로그램을 데몬이라고 부릅니다. 
//nodaemon을 치면 백그라운드 실행이아니라서 실행후 바로 log를 볼 수 있게 됩니다. 
pm2 start app.js --watch --no-daemon 
//--ignore-watch="(파일경로)" 옵션으로 실행하면 해당 파일경로에 파일들이 수정될때는 서버가 재시작 하지 않습니다.
pm2 start app.js --watch --ignore-watch="(파일경로)" --no-daemon 
```

```
// pm2 로그 확인
pm2 log
// pm2의 상태 체크
pm2 status
```






