# AGENTS.md — Time&You

## Proje

Time&You, kullanıcıların odaklanma/çalışma sürelerini takip ettiği sade ve kullanışlı bir productivity web uygulamasıdır.

Temel MVP akışı:

- Kullanıcı giriş yapar.
- Focus session başlatır.
- Çalışmasını tamamlar.
- Session kaydedilir.
- Dashboard üzerinden geçmişini ve temel istatistiklerini görür.

Uzun vadede goals, streak, gamification, AI Coach, haftalık AI raporları ve notification gibi özelliklerle büyütülecektir.

Proje aynı zamanda AWS, Terraform, Docker, Kubernetes ve GitOps öğrenmek için kullanılan gerçek bir portföy projesidir.

---

## Temel Teknoloji Yönü

- Frontend: Next.js + TypeScript
- UI: Tailwind CSS + shadcn/ui
- Backend: Python + FastAPI
- Database: PostgreSQL
- Container: Docker
- Cloud: AWS
- IaC: Terraform
- Kubernetes: EKS
- Kubernetes package management: Helm
- CI: GitHub Actions
- GitOps: Argo CD
- Progressive delivery: Argo Rollouts
- Monitoring: Prometheus + Grafana + CloudWatch

Authentication için AWS Cognito kullanılacaktır.

İlk backend yapısı iki microservice'ten oluşur:

- `focus-service`
- `analytics-service`

Gereksiz yere yeni servisler eklenmemelidir.

---

## Genel Mimari

### İlk MVP'nin mantıksal yapısı:

    ```text
    Frontend
    |
    +-- Cognito
    |
    +-- Focus Service
    |
    +-- Analytics Service
                |
            PostgreSQL


---


## Repository Yapısı

### Ana repository:


time&you/
├── frontend/
├── services/   
│   ├── focus-service/
│   └── analytics-service/
├── infrastructure/
│   └── terraform/
├── deployment/
│   └── helm/
├── docker-compose.yml
├── README.md
└── AGENTS.md


İlerleyen aşamada ayrı bir GitOps repository oluşturulacaktır:

time&you-gitops/

Application repository source code'u, GitOps repository ise Kubernetes'in desired state'ini içerir.

---

## Geliştirme Yaklaşımı

Proje aşama aşama geliştirilecektir.

### Temel sıra:

Domain Design
    ↓
Local MVP
    ↓
Docker
    ↓
AWS + Terraform
    ↓
EKS + Kubernetes
    ↓
Helm
    ↓
GitHub Actions
    ↓
Argo CD / GitOps
    ↓
Dev / Staging / Prod
    ↓
Canary / Rollback
    ↓
Monitoring
    ↓
Yeni ürün özellikleri


Henüz gelinmemiş aşamaların karmaşıklığı mevcut geliştirmeye taşınmamalıdır.

AI, DynamoDB, EventBridge, notification, gamification ve ileri seviye microservice mimarisi sonraki aşamalardır.

---

## Kodlama Kuralları:

- Basit çözüm yeterliyse karmaşık çözüm kullanma.
- Gereksiz abstraction veya dependency ekleme.
- Clean, okunabilir ve test edilebilir kod yaz.
- Anlamlı ve tutarlı isimlendirme kullan.
- Secret veya credential'ları source code'a koyma.
- Mevcut mimari kararları kullanıcı onayı olmadan değiştirme.
- Yeni teknoloji, dependency veya AWS servisi eklemeden önce gerekçesini açıkla.
- Büyük mimari değişikliklerden önce kısa bir plan sun ve onay bekle.
- Küçük ve açıkça istenmiş değişiklikleri doğrudan uygulayabilirsin.

---

## Mevcut Durum

Proje sıfırdan başlamaktadır.

Henüz uygulama kodu oluşturulmamıştır.

### İlk görevler:

Domain Design

- User
- FocusSession
- Topic
- Analytics
- İki microservice'in sorumlulukları

Önce tasarımı açıkla; kodlamaya başlamadan önce onay bekle.

Local MVP

- Next.js
- FastAPI
- PostgreSQL
- AWS Cognito authentication
- Focus session
- Session history
- Basic dashboard/analytics

Docker

- Servisleri containerize et.
- Docker Compose ile tüm sistemi lokal olarak çalıştır.

### İlk hedef:

Önce küçük, temiz ve gerçekten çalışan bir Time&You MVP oluştur. Sonra bunu adım adım AWS, Kubernetes ve GitOps altyapısına taşı.