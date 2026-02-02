## Project Overview

JWT 기반 인증, Redis 캐시 및 Rate Limit, Webhook 보안 검증(HMAC), OAuth 소셜 로그인을 포함하여 실서비스 구조를 고려한 FastAPI 백엔드 서버입니다.

## Architecture

![architecture](./docs/architecture.svg)

- Ngrok: 외부 공개를 위한 엔드 포인트 제공
- Nginx: Reverse Proxy 및 HTTPS 처리
- FastAPI: API 서버
- PostgreSQL: 사용자 및 도메인 데이터 저장
- Redis: 캐시, Rate Limit, JWT 블랙리스트


## Stack

| Category | Tech |
|---------|------|
| Backend | FastAPI, Python |
| DB | PostgreSQL |
| Cache | Redis |
| Auth | JWT, OAuth |
| Infra | Docker, Docker Compose, Nginx |

## Features

### Authentication
- JWT Access Token 발급
- Redis 기반 로그아웃 by set 블랙리스트

### Rate Limiting
- 사용자별 요청 제한 by Redis INCR + TTL  

### Webhook Security
- HMAC-SHA256 기반 서명 검증
- Timestamp 기반 Replay Attack 방지

### Caching
- DB 데이터 캐싱 by Redis

## Focused On

- 단순 CRUD가 아닌 실서비스 구조를 목표로 설계
- JWT 강제 만료를 위해 Redis 블랙리스트 도입
- API 남용 방지를 위한 Rate Limit 구현
- Webhook 위변조 방지를 위한 HMAC 검증 로직 구현
- Docker Compose를 활용한 인프라 구성 
