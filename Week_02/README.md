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

## AWS 서버 구축

> <h3>인스턴스(서버) 생성</h3>

- [AWS 홈페이지](https://ap-northeast-2.console.aws.amazon.com/console/home?region=ap-northeast-2)에 접속해서 일반 계정으로 회원가입을 진행합니다.

![image](https://user-images.githubusercontent.com/43658658/131344551-8ddf98f4-dbb9-4335-a1c7-ea8e761dd13f.png)

회원가입 완료 후 우측 상단에 보면 지역을 설정할 수가 있습니다. 기본값은 미국으로 되어있을 것입니다.   
지역을 `서울`로 설정해줍니다.

이제 AWS 홈페이지 검색창에 `EC2`를 입력하고 검색합니다.

그리고 좌측 탭에 `인스턴스`를 클릭합니다.

우측 상단에 `인스턴스 시작`을 누릅니다.

단계1 : 우분투 서버 18.04 버전을 선택합니다.   
단계2 : 프리 티어 버전을 사용합니다.   
단계3 : VPC, Subnet을 생성했다면 해당되는 ID를 선택합니다. `퍼블릭 IP 자동 할당`은 활성화로 선택합니다.   
단계4 : 스토리지는 SSD(gp3)을 선택하고 크기는 30GB까지 무료이므로 최대로 설정합니다.   
단계5 : 넘어갑니다.   
단계6 : `보안 그룹`에서 인바운딩 규칙을 설정했다면 해당 보안 그룹을 설정해주시고, 설정하지 않았다면 이곳에서 `규칙 추가`를 통해 직접 작성할 수 있습니다.   
단계7 : 설정 사항을 다시 한 번 체크하고 인스턴스를 생성합니다. 키파일을 [C드라이브]-[AWS] 폴더를 생성하고 그 안에 저장합니다.   

> <h3>우분투의 폴더 구조를 GUI환경으로 보기</h3>

- [WinSCP 다운로드 사이트](https://winscp.net/eng/download.php)에 접속해 `WinSCP`를 다운 받습니다.   

WinSCP를 실행합니다.

![image](https://user-images.githubusercontent.com/43658658/131346880-b6ac609a-6a4d-4639-9417-fa6d96ea6803.png)

호스트 이름은 인스턴스의 퍼블릭 IP 주소입니다.   
(탄력적 IP를 할당 받으면 탄력적 IP 주소를 입력하면 됩니다)

![image](https://user-images.githubusercontent.com/43658658/131346981-a4166544-e9bd-440e-a8a8-04aefb5bb34c.png)

비밀번호 입력란 밑에 고급을 클릭합니다.   
[SSH]-[인증]으로 들어가 인스턴스 생성 후에 받은 키파일을 선택합니다.   
(윈도우는 .pem 확장자를 인식할 수 없습니다. WinSCP를 이용해 .ppk 확장자로 바꿔주는 작업입니다)

현재 설정에 대해 `저장`을 해준 뒤에 `로그인`을 클릭합니다.

WinSCP를 이용해 우분투의 폴더 구조를 GUI 환경으로 볼 수 있게 됩니다.

> <h3>인스턴스에 접속하기</h3>

![image](https://user-images.githubusercontent.com/43658658/131347943-1b099dba-798e-4744-88de-f05279c3baad.png)

WinSCP 창에서 `PuTTy`를 킵니다.

> <h3>Nginx, Php, MySQL을 우분투에 설치하기</h3>

구글에 `ubuntu 18.04 nginx php mysql`이라는 키워드로 검색합니다.

- [ubuntu 18.04 nginx php mysql 설치 가이드 메뉴얼](https://www.digitalocean.com/community/tutorials/how-to-install-linux-nginx-mysql-php-lemp-stack-ubuntu-18-04)

가이드 메뉴얼을 따라서 Nginx, Php, MySQL을 다운 받습니다.

Nginx는 Apache와 같은 역할의 웹 서버 프로그램입니다.   
터미널을 통해 Nginx를 설치하고 인스턴스의 할당받은 퍼블릭 IP 주소로 웹 브라우저를 이용해 접속하면 아래와 같은 화면이 나타납니다.   
(이때, 반드시 인스턴스의 인바운드 규칙에 HTTP 포트(80번)로의 접근을 허용해 주어야 합니다.

![image](https://user-images.githubusercontent.com/43658658/131358279-4820eb69-44b6-4494-b7b6-fe713eaa9372.png)

MySQL을 설치한 뒤에 `sudo mysql`을 통해 MySQL로 접속이 되는지 확인할 수 있습니다.   
(`exit`를 통해 다시 MySQL 밖으로 나올 수 있습니다)
MySQL의 보안 설정을 해주어야 합니다. 역시 가이드 메뉴얼에 나와있으니 따라해보시기 바랍니다.

Nginx에서는 반드시 `php-fpm`을 설치해주어야합니다.   
Apache에는 php와 자동으로 연동되도록 해주는 프로그램이 같이 설치되지만,   
Nginx에는 그런 것이 없으므로, Nginx와 php를 연동시켜주는 `php-fpm`을 반드시 설치해주어야 합니다.

> <h3>nginx와 php 연동하기</h3>

php가 제대로 설치되었는지 확인하기 위해서 아래와 같은 절차를 진행합니다.   
먼저 nginx의 root로 들어가줍니다. root의 주소는 `/var/www/html`입니다.

```
  $ cd /var/www/html
```

vi 편집기를 이용해 `index.php`라는 파일을 만들어주고, 아래와 같이 내용을 입력합니다.

```
  $ sudo vi index.php
```

```
<?php
phpinfo();
?>
```

(입력창에선 `i`키를 누르고 편집상태로 들어가고 `ESC`키를 통해서 명령 상태로 돌아올 수 있습니다)   
(`:wq+[enter]`를 통해서 작성한 글자를 저장할 수 있습니다)

이제 nginx와 php를 연동시켜야합니다.   
vi 편집기를 이용해 기본 nginx 설정 파일로 들어갑니다. `/etc/nginx/sites-available/default`의 위치에 있습니다.   
(`h, j, k, l`키를 이용해 커서를 상하좌우로 이동할 수 있습니다)

![image](https://user-images.githubusercontent.com/43658658/131363121-96654242-2e76-4fd7-b57a-9280085225e1.png)

위의 상태에서 주석을 해제하여 아래처럼 만듭니다. 그리고 유의할 점은 php7.0을 php7.2로 고쳐야 한다는 것입니다.   
우분투 18.04에서 php-fpm을 설치할 경우 php7.2-fpm 버전이 자동으로 설치되기 때문입니다.

![image](https://user-images.githubusercontent.com/43658658/131363539-a4eb1a12-5d98-4153-8979-f81e32219771.png)

`:wq`로 저장하고 나온 뒤에 nginx를 재시작 해줍니다.

```
  $ sudo service nginx restart
```

이제 마지막으로 웹 브라우저에서 인스턴스의 `퍼블릭 IP 주소/index.php`로 접속해서 아래와 같이 php와 연동이 되는 것을 확인합니다.

![image](https://user-images.githubusercontent.com/43658658/131363925-8a35fbf2-64cf-49d3-8fa2-1a61c0a1a1fa.png)

> <h3>MySQL 외부에서 접속하기</h3>

- [Datagrip 다운로드 사이트](https://www.jetbrains.com/datagrip/)

