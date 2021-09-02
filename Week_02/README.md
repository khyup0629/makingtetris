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
MySQL의 `보안 설정`을 해주어야 합니다. 역시 가이드 메뉴얼에 나와있으니 따라해보시기 바랍니다.

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

- [외부에서 MySQL에 접속하기 가이드 메뉴얼](https://luminitworld.tistory.com/82)

`Datagrip`을 통해 MySQL을 외부에서 접속할 수 있습니다.

```
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
```

위의 에러코드는 패스워드 규칙에 어긋나는 패스워드를 사용했을 때 나타납니다.   
- [패스워드 정책 변경](https://kamang-it.tistory.com/entry/MySQL%ED%8C%A8%EC%8A%A4%EC%9B%8C%EB%93%9C-%EC%A0%95%EC%B1%85-%ED%99%95%EC%9D%B8-%EB%B3%80%EA%B2%BD%ED%95%98%EA%B8%B0)

```
mysql > SHOW VARIABLES LIKE 'validate_password%'
```

위의 명령문을 통해 보여지는 패스워드 정책(password policy)은 아래와 같습니다.

![image](https://user-images.githubusercontent.com/43658658/131485489-6fc9d5f9-97b2-4613-abfb-f07fd40af6cd.png)

- validate_password_check_user_name   : 패스워드에 `user id`가 들어갔는지를 묻습니다. 만약 아이디와 패스워드가 모두 root인데 만약 on이 켜져있다면 이는 불가능합니다.
- validate_password_length            : 패스워드의 `길이`를 의미합니다. 8자 이상이어야 한다는 이야기이다.
- validate_password_mixed_case_count  : `대소문자`를 적어도 1회 이상 써야합니다.
- validate_password_number_count      : `숫자`를 적어도 1회 이상 써야합니다.
- validate_password_special_char_count: `특수문자`를 적어도 1회 이상 써야합니다.

- [MySQL 사용자 생성 및 권한 부여](https://idmango.com/108)

어떤 사용자에 대한 데이터베이스 권한을 삭제하고 싶으면 아래의 명령어를 입력합니다.

```
mysql> revoke all privileges on 데이터베이스이름.* from '사용자이름'@'%';
```

외부에서 MySQL에 접속하기 위한 절차는 아래와 같습니다.

1. `Datagrip` 설치하기
2. MySQL `사용자` 생성하기
3. `데이터베이스` 생성하기
4. 생성한 사용자가 데이터베이스에 접근하도록 `권한 허용`하기
5. `mysqld.cnf` 파일 내용 편집 및 EC2 인스턴스 `인바운딩 규칙` `3306번 포트` 설정하기
6. `Datagrip`을 통해 인스턴스의 퍼블릭 IP로 접속하기

아래와 같이 `Test Connection`을 클릭하고 `Succeeded`가 뜨면 MySQL로 접속이 가능하다는 것을 의미합니다.

![image](https://user-images.githubusercontent.com/43658658/131488844-13dc5641-6d64-49a0-9e33-518c8e268cfa.png)

> <h3>phpMyAdmin 설치하기</h3>

phpMyAdmin : 웹 기반 인터페이스를 통해 MySQL 및 MariaDB 서버를 관리하기 위한 오픈소스 php 기반 도구입니다. MySQL와 상호 작용하면서 사용자 계정 및 권한을 관리하고, SQL문을 실행하고, 다양한 데이터 형식으로 데이터를 가져오고 내보낼 수 있습니다.

- [Ubuntu 18.04 phpMyAdmin 설치 가이드 메뉴얼](https://ko.linux-console.net/?p=277)

phpMyAdmin를 설치하기 전에 시스템에 Nginx 및 php-fpm이 설치되어 있어야합니다.   

```
$ sudo ln -s  /usr/share/phpmyadmin /var/www/html/phpmyadmin
```

위의 명령어를 통해 `심볼릭 링크`를 생성한 이후에는 `/etc/nginx/sites-available/default` 경로로 들어갑니다.

```
$ sudo vi /etc/nginx/sites-available/default
```

vi 편집기의 내용 중 아래의 내용이 적힌 곳을 찾아서 `index.php`를 추가해서 적어줍니다.

![image](https://user-images.githubusercontent.com/43658658/131524215-a5e02039-0c87-4ad8-8b19-4b6e05565ec1.png)

모든 설정이 끝났으면 `Nginx를 재시작`한 후, 웹 브라우저에서 인스턴스의 `퍼블릭IP/phpmyadmin`의 URL로 접속합니다.

이전에 생성한 `MySQL의 외부 접속 허용 사용자 ID와 비밀번호`를 입력해 phpMyAdmin에 접속할 수 있습니다.

![image](https://user-images.githubusercontent.com/43658658/131524798-c90ece23-394e-4624-8339-f57c8a93522d.png)

> <h3>AWS EC2에 Domain 적용</h3>

- [Gabia(가비아)](https://domain.gabia.com/?gclid=Cj0KCQjwpreJBhDvARIsAF1_BU0zc8GdGcPBFSMdsJJmTp_xVkg8lsDgIRhyoEEKa94nroz5NHYpAuQaAhKWEALw_wcB)에서 원하는 이름으로 도메인을 구매합니다.

가비아에서 `도메인을 구입`하여 ip주소 대신에 `도메인을 이용`하여 AWS EC2 퍼블릭 IPv4 주소에 보다 `쉽게 접근`할 수 있도록 할 수 있습니다.

- [EC2에 Domain 적용하기 가이드 메뉴얼](https://yusang.tistory.com/32)

도메인은 꼭 `.com`이 아니더라도 가격이 저렴한 `.site`나 `.xyz`를 이용할 수 있습니다.   
AWS EC2 인스턴스에 올바르게 도메인이 적용되면 `도메인 주소/index.php`로 접속했을 때 아래와 같은 페이지가 띄워집니다.

![image](https://user-images.githubusercontent.com/43658658/131627805-38bf3c25-7ea6-405f-8a0f-b367f0144f60.png)

> <h3>HTTPS 적용하기</h3>

- [Let's Encrypt, certbot에 관한 개념](https://jootc.com/p/201901062488)
- [Let's Encrypt를 이용해 인스턴스에 HTTPS 적용하기 가이드 메뉴얼](https://yusang.tistory.com/33?category=835611)
- [ln 명령어와 하드/소프트(심볼릭) 링크](https://jhnyang.tistory.com/269)

![image](https://user-images.githubusercontent.com/43658658/131777923-b1265275-b51d-48a8-85ce-cfcc9cf49edc.png)

위와 같은 에러가 발생한다면, 인스턴스의 인바운드 규칙에서 `80번 포트`의 허용 IP주소를 `0.0.0.0/0`으로 설정해서 모든 IP가 접속가능하도록 하면 해결할 수 있습니다.

반드시 `HTTPS`로 접근하기 위한 `443번 포트`를 인바운딩 규칙을 통해 열어주어야 합니다.

`SSL 인증서`를 발급 받는 과정까지 마무리했으면 [테스트 사이트](https://www.ssllabs.com/ssltest/)에서 SSL 서버에 대한 테스트를 해볼 수 있습니다.   
(SSL 인증서를 발급 받기까지 `시간이 소요`될 수 있습니다)   
아래와 같은 화면이 뜬다면 성공적으로 인증이 완료된 것입니다.

![image](https://user-images.githubusercontent.com/43658658/131798478-20ba7684-6eca-4357-a179-6d147c06be09.png)

모든 과정이 끝나면, 웹 브라우저에 `도메인 이름`을 입력하면 `자동으로 HTTPS로 연결`되며 php와 연동된 화면이 띄워집니다.   
(HTTPS로 연결되면 URL 옆에 `자물쇠 모양`이 나타납니다)

![image](https://user-images.githubusercontent.com/43658658/131826677-fa46abe6-5194-44b7-b9b1-1fb36beb619e.png)

서버 블럭(example.com) 생성해서 HTTPS 적용하기 참고 사이트들

- [Let's Encrypt를 이용해 인스턴스에 HTTPS 적용하기 가이드 메뉴얼](https://velog.io/@pinot/Ubuntu-18.04%EC%97%90%EC%84%9C-Lets-Encrypt%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-Nginx%EC%97%90-SSL%EC%9D%84-%EC%A0%81%EC%9A%A9%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95)
- [서버 블럭(example.com) 설정하기](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-18-04#step-5-setting-up-server-blocks-(recommended)) : HTTPS를 적용하기 위해선 거쳐야하는 과정입니다. `도메인을 만들 때마다` 반드시 진행되어야 하는 과정입니다.사이트의 5번 섹션을 참고하시면 됩니다. `example.com=도메인이름`을 의미합니다!

서버 블럭을 생성할 때, `index.html` 파일을 만드는 작업을 꼭 수행하지 않아도 됩니다.   

> <h3>서브 도메인 생성 및 적용</h3>

- [서브 도메인 생성 및 적용 가이드 메뉴얼](https://mr-shopper.tistory.com/entry/%EC%84%9C%EB%B8%8C%ED%95%98%EC%9C%84-%EB%8F%84%EB%A9%94%EC%9D%B8-%EB%A7%8C%EB%93%9C%EB%8A%94-%EB%B0%A9%EB%B2%95-%EA%B0%80%EB%B9%84%EC%95%84-CNAME-%EB%A0%88%EC%BD%94%EB%93%9C-%EC%B6%94%EA%B0%80-%EC%84%A4%EC%A0%95)
 
홈페이지가 바껴서 서브 도메인 생성과 관련된 앞부분이 메뉴얼과 좀 다릅니다.   
`[My 가비아]->[DNS 관리툴]`로 접속해서 도메인 리스트 중 서브 도메인을 만들고자 하는 도메인의 `설정`을 누르시고 `레코드 설정`을 통해 CNAME을 입력하시면 됩니다.   
CNAME을 입력할 때는 `값/위치`의 마지막에 .(점)을 붙여주지만, 실제로 Nginx를 통해 서브 도메인을 적용한 실제 서브 도메인에는 .(점)이 빠진 형태의 URL이 됩니다.

저는 `test`와 `product` 서브 도메인을 생성했습니다.   
이에 맞는 디렉토리들을 `/var/www/html`의 하위 디렉토리로 생성하고, 각 디렉토리 속에 `phpinfo` 파일을 만들었습니다.   
그리고, `/etc/nginx/sites-available` 경로의 `default`에 각 서브 도메인과 관련된 `server`내용을 추가합니다.   
(기존 도메인과 관련된 내용 밑에 추가로 작성해 주시면 됩니다)

![image](https://user-images.githubusercontent.com/43658658/131842081-1ac4f8e7-32d7-4303-9c05-7c72cdc41c83.png)

마지막으로 Nginx를 다시 시작하고, 각 서브 도메인으로 접속하면 `phpinfo` 파일이 나타납니다.

![image](https://user-images.githubusercontent.com/43658658/131841815-e2e83e7f-cda9-43a8-9a9e-8c9e6c84f4ab.png)

![image](https://user-images.githubusercontent.com/43658658/131841738-601bd09f-bc67-4a18-b04d-120a7516d308.png)
