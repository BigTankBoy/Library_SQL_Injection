<h1 align="center">📚 전자도서관📚</h1>

<div align="center">

도서관 속에서 <strong>FLAG</strong>를 찾아보세요!<br/>
플레이어는 검색 창 하나만으로 DB 깊숙한 곳에 숨겨진 비밀을 캐내야 합니다.

![Made with Flask](https://img.shields.io/badge/Powered%20by-Flask-yellow?logo=flask&logoColor=black)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![CTF](https://img.shields.io/badge/Category-Web%20Exploitation-blueviolet)

</div>

---

## 🛠 구성

| 폴더 / 파일           | 설명                                  |
|------------------------|---------------------------------------|
| `app.py`              | Flask 진입점, **/search**에 취약점 포함 |
| `templates/`          | Jinja2 템플릿 (검색, 장르, 도서 페이지) |
| `static/`             | CSS & 이미지 리소스                   |
| `library.db`          | **SQLite** DB — 8개 장르, 240권, 사용자 테이블, 그리고 **FLAG** |

---
