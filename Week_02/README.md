# Week 2.

1. Local 서버 구축 : Window/MacOS + Apache, Php, MySQL (Bitnami)
- 외부에서 접속하기 : phpinfo 띄우기 - Apache와 잘 연동되는지 체크 (by 포트포워딩)

2. AWS 서버 구축 : Linux + Nginx, Php, MySQL
- 외부에서 접속하기 : phpinfo 띄우기 - Apache와 잘 연동되는지 체크
- MySQL 외부에서 접속하기 (DataGrip or Workbench)
- phpMyAdmin 설치
- Domain 적용 (가비아, 후이즈 ... 구입)
- HTTPS 적용 (let's encrypt)

3. 챌린지
- Sub Domain 적용 (Dev, Prod)
- Redirection 적용 (IP to Domain) - 네이버 예시

## Local 서버 구축

> <h3>Bitnami 설치</h3>

구글에 `Bitnami wamp`를 검색하고 자신의 컴퓨터에 맞는 운영체제로 설치합니다.

- [Bitnami WAMP 다운로드 사이트](https://bitnami.com/stack/wamp)

Bitnami WAMP에는 Apache, Php, MySQL이 모두 포함되어 있습니다.   
설치 완료 후 크롬 브라우저를 띄운 후 localhost로 들어가면 bitnami 공식 홈페이지가 뜨는 것을 확인할 수 있습니다.

![image](https://user-images.githubusercontent.com/43658658/131337445-2d542560-e643-416d-ad0a-c2452ee710fb.png)

> <h3>포트포워딩 설정</h3>

포트포워딩 : 공유기에 외부 접근이 일어날 경우 설정한 포트로 접근이 가능하도록 해주는 것입니다.

cmd 창을 열고(단축키 [Win]+[R]) `ipconfig`를 입력해 현재 자신의 인터넷 공유기의 게이트웨이 주소를 파악합니다.

![image](https://user-images.githubusercontent.com/43658658/131337995-4b5dfb1a-2a27-4926-8b6a-b4e21d9b7393.png)

인터넷 브라우저에 해당 주소를 입력해 접속합니다.   
iptime의 경우 아이디와 비밀번호에 별다른 설정을 하지 않았다면, 아이디, 비밀번호 모두 `admin`입니다.   
(다른 브랜드의 공유기일 경우 검색하면 나옵니다)

[NAT 설정] - [포트 포워딩]으로 들어가서 `새로 추가` 버튼을 눌러줍니다.

![image](https://user-images.githubusercontent.com/43658658/131340047-842c6ef8-3af6-4c46-8a1b-da1c13158eb4.png)

서비스 포트는 `외부 포트`와 같습니다.   
내부 포트는 HTTP의 연결 포트인 `80`을 적어줍니다.   
IP 주소는 `ipconfig`에서 `IPv4의 주소`를 입력하시면 됩니다.

