CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_filename TEXT NOT NULL,
    mmh3_hash TEXT NOT NULL UNIQUE,
    date DATE NOT NULL,
    invoice_number INTEGER NOT NULL,
    amount REAL NOT NULL,
    paid TEXT CHECK(paid IN ('no', 'prepaid', 'paid')) NOT NULL,
    comment TEXT
);
