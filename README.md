<div align="center">

# 🌸 Aleen — Exotic Floral Atelier

**Full-Stack E-Commerce Storefront, In-Store POS & Financial Accounting System**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

*A minimalist floral boutique platform that seamlessly unifies online customer orders with an isolated internal staff portal for counter sales (POS) and profit tracking.*

</div>

---

## ✨ What Makes Aleen Stand Out?

Aleen is engineered as **two cleanly separated systems** under one unified database:

1. **Public Storefront (`/`)** — A luxury, frictionless shopping experience for customers with zero account barriers.
2. **Isolated Staff & Admin Portal (`/aleen-staff/`)** — Completely detached from the public navigation and templates so staff can record in-store counter sales and review analytics securely.

---

## 🚀 Key Features

### 🛍️ Customer Storefront
- **Curated Categories & Subcategories:** Filter blooms effortlessly across main collections (*Loose Blooms*, *Flower Bags*, *Flower Bouquets*, *Artificial Blooms*) and nested types (*Cone*, *Basket*).
- **Transparent Discount Pricing:** Automatically renders struck-through regular prices alongside active discounted prices across product cards, detail pages, cart calculations, and order records.
- **Dynamic "Most Loved" Showcase:** Auto-computes the **Top 8 best-selling blooms of the current month** by combining Online and In-Store sales (excluding cancelled orders), with a smart all-time fallback so the homepage never looks empty.
- **Real-Time Slide-Out Shopping Bag:** Smooth AJAX cart drawer to add, increment, decrement, or remove items without page reloads.
- **Guest Checkout & Local Delivery Logic:** Fast checkout with promo code validation, automatic stock deduction, and **complimentary free delivery across Uttara**.

### 🏪 Isolated Staff Portal & In-Store POS
- **Admin-Controlled Access:** Staff accounts are provisioned exclusively by the Founder/Admin—no public sign-up exposure.
- **Quick In-Store Sale (POS):** Built for fast counter billing with **manual unit price entry** (supporting on-the-spot counter negotiations), multi-item bills, and instant total calculation.
- **Bespoke / Customised Orders:** Dedicated POS option for custom-made bouquets or flower bags with **making-cost tracking** for accurate profit reporting.
- **Unified Inventory Sync:** Every completed POS sale immediately deducts stock and feeds into monthly rankings and financial ledgers.

### 📊 Sales & Financial Accounting Dashboard
- **Period-Based Reporting:** Track revenue and order performance with interactive **Daily, Weekly, Monthly, and Yearly** views plus a 12-month breakdown table.
- **Channel Breakdown:** Compare **Online Website Sales** vs. **In-Store (POS) Sales** side by side.
- **Founder-Only Net Profit:** Cost prices and net profit figures are strictly restricted to Admin (Superuser) accounts.

---

## 🔗 Direct Local URLs & Access Guide

Start the local server (`python manage.py runserver`) and open any portal directly in your browser:

### 🔐 Internal Portals (Staff & Admin)

| Portal | Direct Browser URL | Who Can Log In / Access |
| :--- | :--- | :--- |
| **Staff & Admin Portal (Login)** | http://127.0.0.1:8000/aleen-staff/ | **Staff** (POS & Sales Report) and **Admin** (POS, Sales & Profit) |
| **Store POS (Direct)** | http://127.0.0.1:8000/aleen-staff/pos/ | Logged-in **Staff** & **Admin** |
| **Sales Dashboard (Direct)** | http://127.0.0.1:8000/aleen-staff/dashboard/ | Logged-in **Staff** & **Admin** |
| **Django Admin Panel** | http://127.0.0.1:8000/aleen-management/ | **Admin (Superuser / Founder)** only |

### 🌐 Public Customer Storefront

| Page | Direct Browser URL | Access |
| :--- | :--- | :--- |
| **Homepage** | http://127.0.0.1:8000/ | Public (Everyone) |
| **Shop & Filters** | http://127.0.0.1:8000/shop/ | Public (Everyone) |
| **Product Details** | `http://127.0.0.1:8000/product/<slug>/` | Public (Everyone) |
| **Guest Checkout** | http://127.0.0.1:8000/orders/checkout/ | Public (With active cart items) |

---

## 🛡️ Role-Based Access Overview

| Capability | Customer | Staff | Admin (Superuser) |
| :--- | :---: | :---: | :---: |
| Browse Catalog, Cart & Guest Checkout | ✅ | ✅ | ✅ |
| Access Isolated Staff Portal (`/aleen-staff/`) | ❌ | ✅ | ✅ |
| Record Quick In-Store Sales (POS) | ❌ | ✅ | ✅ |
| View Sales & Revenue Reports | ❌ | ✅ | ✅ |
| View Cost Price & Net Profit Analytics | ❌ | ❌ | ✅ |
| Manage Products, Staff & Settings (`/aleen-management/`) | ❌ | ❌ | ✅ |

---

## 🗂️ Project Architecture

```text
aleen_website/
├── aleen_project/        # Core settings, main URL routing & WSGI/ASGI
├── core/                 # Homepage logic, hero slides, banners, coupons & reviews
├── products/             # Categories (parent/child), products, pricing & shop views
├── orders/               # Session cart, guest checkout, POS & accounting dashboard
├── templates/            # Public storefront templates & isolated staff templates
├── media/                # Uploaded product, category & customization images
├── manage.py
└── requirements.txt
