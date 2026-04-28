# Event Ticketing & Management System
A full-stack web app for event registration, ticket issuance, and QR-based check-in — built with Flask, MySQL, and vanilla JS.

## Features
- Student and admin interfaces
- QR code ticket generation on registration
- Live webcam QR scanner for check-in verification

## Tech Stack
Python · Flask · MySQL · HTML/CSS · JavaScript

## How to Run
1. Install dependencies
```bash
   pip install flask mysql-connector-python qrcode pillow
```
2. Set up the database
```bash
   mysql -u root -p < db/schema.sql
```
3. Run
```bash
   python main.py
```
4. Open `http://localhost:5000`

## Author
[Srishti Arora](https://github.com/srishtiiarora)
