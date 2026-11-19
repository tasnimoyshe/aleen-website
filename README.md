<div align="center">

# ALEEN — Exotic Floral Atelier

**Full-Stack E-Commerce Platform, Bespoke Order Workflow & Role-Based In-Store POS System**

<p>
  <img src="https://img.shields.io/badge/Python-Backend-2D2427?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-Framework-933B5B?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-Design-9F9679?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/JavaScript-AJAX_Cart-2D2427?style=for-the-badge&logo=javascript&logoColor=F7DF1E" alt="JavaScript" />
</p>

[Overview](#overview) • [Key Features](#key-features) • [Access Control](#role-based-access-control) • [Backend Highlights](#backend-engineering-highlights) • [Setup Guide](#local-setup)

</div>

---

## Overview

**Aleen** is an end-to-end digital storefront and operations platform engineered for a boutique floral atelier. Beyond standard online shopping, it bridges physical store operations and digital commerce inside a single Django & PostgreSQL codebase—supporting walk-in POS billing, Pinterest-inspired bespoke photo orders, real-time stock synchronization, and executive profit analytics with strict role separation.

---

## Key Features

### Customer Storefront
- **Editorial Floral Catalog:** Structured browsing across *Flower Bouquets*, *Flower Bags*, *Loose Blooms*, and *Artificial Blooms* with real-time stock availability checks.
- **AJAX Slide-Out Shopping Bag:** Instant cart updates (`add`, `increment`, `decrement`, `remove`) and live subtotal calculations without page reloads.
- **Smart Guest Checkout:** Streamlined order flow featuring promo/coupon code validation and automatic complimentary delivery detection for Uttara addresses.
- **Bespoke Customization Workflow (`/orders/customize/`):** Dedicated custom order portal where customers upload Pinterest or inspiration photos with client-side live preview, add budget/occasion notes, and receive an immediate **20-minute confirmation call modal**.

### Operations, POS & Analytics (`/aleen-staff/`)
- **In-Store Point of Sale (POS):** Enables staff to record walk-in sales for both catalog products and one-off custom arrangements, automatically deducting inventory and updating sales counters.
- **Multi-Range Sales Dashboard:** Interactive filtering across **Today**, **This Week**, **Current Month**, **Full Year**, and **Custom Month/Year**, complete with a 12-month revenue matrix and top-selling product leaderboard (covering both standard and custom items).
- **Custom Request Management:** Visual thumbnail previews of customer-uploaded reference images and one-click `is_contacted` call tracking inside the management console.

---

## Role-Based Access Control

A unified private portal (`/aleen-staff/`) dynamically adapts its UI and data visibility based on authenticated user privileges:

| Capability | Customer | Staff (`is_staff`) | Admin (`is_superuser`) |
| :--- | :---: | :---: | :---: |
| Browse Catalog, Cart & Guest Checkout | Yes | Yes | Yes |
| Submit Bespoke Photo Requests | Yes | Yes | Yes |
| In-Store POS Billing & Walk-In Sales | No | Yes | Yes |
| Sales Volume & Top-Selling Reports | No | Yes | Yes |
| Unit Cost & Net Profit Margin Visibility | No | **Restricted** | Yes |
| Django Management Console (`/aleen-management/`) | No | **Restricted** | Yes |

---

## Backend Engineering Highlights

- **Transactional Integrity:** Both online checkouts and in-store POS submissions execute inside `django.db.transaction.atomic()` blocks to prevent partial order creation or stock desynchronization.
- **Database-Level Aggregations:** Revenue, cost of goods sold (COGS), net profit, and 12-month financial breakdowns are computed directly via PostgreSQL queries using Django ORM `ExpressionWrapper`, `Coalesce`, `ExtractMonth`, and conditional `Case/When` annotations.
- **Security & Configuration Hygiene:** Sensitive credentials (`SECRET_KEY`, database configuration) are isolated via `.env`, admin access is served under a non-default route (`/aleen-management/`), and all state-mutating endpoints enforce CSRF protection and `POST`-only decorators.

---

## Project Architecture

```text
aleen_website/
├── aleen_project/        # Core project settings, root URL routing, WSGI/ASGI
├── core/                 # Homepage, hero showcase, site settings & coupons
├── products/             # Floral catalog models, categories, shop & detail views
├── orders/               # Session cart, guest checkout, POS, analytics & custom requests
├── accounts/             # User & authentication extensions
├── templates/            # Modular Tailwind CSS templates (storefront & staff portal)
├── static/               # Brand assets and custom stylesheets
└── requirements.txt      # Pinned Python dependencies
