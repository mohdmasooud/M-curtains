# M Curtains - Haute Couture & Bespoke Luxury Drapery Atelier

A full-stack luxury **Curtain E-Commerce & Atelier Management Platform** built with **Python, Django, SQL (SQLite ORM), Bootstrap 5.3, Vanilla CSS, and Hardware-Accelerated 3D JavaScript**.

The project is architected strictly into **Two Applications**:
1. **User Application (`apps.user_app`)**: Storefront, 3D Canvas Stardust & Parallax Hero, 3D Interactive Drapery Studio, Product Discovery & Filtering, 3D Room Visualizer, Custom Measurement & Pricing Calculator (in ₹ INR), Shopping Bag, Discount Coupons, Multi-step Checkout, Order Tracking, Printable Invoices, Customer Auth, Profiles & Saved Addresses.
2. **Admin Application (`apps.admin_app`)**: Staff-only Custom Admin Portal, Dashboard KPI Metrics, Chart.js Visualizations, Curtain Products CRUD, Categories & Fabrics CRUD, Order Fulfillment & Status Stepper, Customer Account Controls, Coupon Engine, and Direct Interactive SQL Console.

---

## 🌟 Key Features & Highlights

### 1. User Application (`apps.user_app`)
- **Modern 3D Home-Page Experience**:
  - Hardware-accelerated 3D Gold Stardust particle canvas with automatic offscreen pause (`IntersectionObserver`) for 60fps performance.
  - 3D Interactive Drapery Studio with real-time fabric switching (Velvet, Linen, Blackout), Day/Sunset/Night ambient lighting simulation, and interactive draw slider.
  - Parallax 3D tilt cards with dynamic light glare effects.
- **Product Discovery & Dynamic Filtering**:
  - Filter by Category (*Royal Velvet, French Linen, 100% Thermal Blackout, Sheer & Voile, Jacquard, Motorized*).
  - Filter by Room (*Living Room, Master Suite, Dining Salon, Home Theater*).
  - Filter by Light Control (Sheer, Room Darkening, Total Blackout).
  - Dynamic price range filter, multi-criteria sorting, and live instant search API.
- **Dynamic Sizing & Price Calculator (₹ INR)**:
  - Custom width (cm) × drop length (cm) dynamic pricing with pleat style and lining selection.
  - Real-time price updates via asynchronous calculation API.
- **Room Drapery Visualizer & Yardage Guide**:
  - Interactive room visualizer with fabric swatches and day/night lighting modes.
  - Step-by-step sizing guide and fabric meter recommendation calculator.
- **Shopping Bag, Coupons & Checkout**:
  - Session-backed cart preserving exact custom panel dimensions and tailoring specifications.
  - Active promotional codes (`LUXE20`, `LUXEVIP15`).
  - Secure checkout with instant order generation, status stepper, and printable PDF invoices.
- **User Authentication & Management**:
  - Modern, responsive Login and Registration (with password confirmation and error highlights).
  - Client Dashboard, Profile updates, and multi-address book.

### 2. Admin Application (`apps.admin_app`)
- **Custom Branded Admin Dashboard**:
  - Real-time KPIs: Total Revenue, Total Orders, Active Customers, Low Stock Alerts.
  - Chart.js Graphical Analytics: Order status distribution doughnut chart and category share bar chart.
- **Catalog Management**:
  - Full CRUD operations for Curtain Products, Categories, and Fabrics.
- **Order Fulfillment & Logistics**:
  - Order status pipeline (*Pending, Confirmed, Tailoring, Shipped, Delivered, Cancelled*).
  - Courier tracking assignment (e.g., `FEDEX-ATELIER-892`) and tailoring notes.
- **Customer & Coupon Management**:
  - Toggle customer account status (activate/deactivate).
  - Create and manage promo coupons with percentage discounts and minimum spend thresholds.
- **Direct Interactive SQL Database Console**:
  - Execute direct SQL queries with real-time tabular output and execution time metrics.

---

## 🔐 Default Credentials for Testing

| Role | Username | Password | Portals |
| :--- | :--- | :--- | :--- |
| **Store Administrator** | `admin` | `admin123` | Custom Admin: `/store-admin/` |
| **Demo Customer** | `customer` | `customer123` | Storefront: `/accounts/dashboard/` |

---

## 🛠️ Technology Stack
- **Backend:** Python 3, Django (Full ORM, Context Processors, Automated Unit Test Suites)
- **Database:** SQL (SQLite default, PostgreSQL/MySQL compatible)
- **Frontend:** HTML5, CSS3 (Modern Glassmorphism & GPU transforms), Vanilla JavaScript (ES6+), Bootstrap 5.3
- **Data Visualization:** Chart.js
- **Typography & Icons:** Cormorant Garamond, Plus Jakarta Sans, Outfit, FontAwesome 6

---

## 🚀 Getting Started & Setup Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations user_app admin_app
python manage.py migrate
```

### 3. Run Automated Test Suite (19 Tests)
```bash
python manage.py test
```

### 4. Launch the Development Server
```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/` to explore the storefront and `http://127.0.0.1:8000/store-admin/` for the Admin Portal.

---

## 📁 Project Architecture

```
d:/curtain/
├── manage.py
├── requirements.txt
├── README.md
├── curtain_shop/             # Django root configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/
│   ├── user_app/             # 1. User Application (Storefront, Auth, Catalog, Cart, Orders)
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── cart.py
│   │   ├── urls.py
│   │   └── tests.py
│   └── admin_app/            # 2. Admin Application (Dashboard, CRUD, Operations, SQL Console)
│       ├── views.py
│       ├── forms.py
│       ├── decorators.py
│       ├── urls.py
│       └── tests.py
├── static/
│   ├── css/                  # main.css, admin.css, home_3d.css
│   ├── js/                   # home_3d.js, main.js, calculator.js, visualizer.js, admin_charts.js
│   └── images/               # High-res local curtain fabric assets
└── templates/                # Bootstrap 5 responsive templates
    ├── base.html
    ├── admin_base.html
    ├── core/
    ├── accounts/
    ├── products/
    ├── cart/
    ├── orders/
    └── store_admin/
```
