-- Invoice table with unconfirmed or missing data.
-- Records are moved from this table to the invoices table
-- upon manual confirmation.
CREATE TABLE IF NOT EXISTS invoices_unconfirmed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mmh3_hash TEXT NOT NULL UNIQUE,
    original_filename TEXT NOT NULL,
    filename TEXT,
    issuer TEXT,
    date DATE,
    invoice_number TEXT,
    amount REAL,
    iban TEXT,
    bic TEXT,
    reference TEXT,
    text TEXT,
    paid_initial TEXT CHECK(paid_initial IN ('automatic', 'no', 'prepaid')) NOT NULL,
    paid TEXT CHECK(paid IN ('yes', 'no')) NOT NULL,
    comment TEXT
);

-- Proper invoice table.
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mmh3_hash TEXT NOT NULL UNIQUE,
    original_filename TEXT NOT NULL,
    -- Generated name, based on slug and date.
    filename TEXT NOT NULL UNIQUE,
    -- Issuer slug.
    issuer TEXT NOT NULL,
    date DATE NOT NULL,
    invoice_number TEXT NOT NULL,
    amount REAL NOT NULL,
    iban TEXT NOT NULL,
    bic TEXT,
    reference TEXT,
    text TEXT,
    -- Initial status, as derived by the extracted data.
    paid_initial TEXT CHECK(paid_initial IN ('automatic', 'no', 'prepaid')) NOT NULL,
    -- Dynamic status, as set by a human, initialized to yes if
    -- paid_initial is automatic or prepaid.
    paid TEXT CHECK(paid IN ('yes', 'no')) NOT NULL,
    comment TEXT,
    CHECK ((reference IS NOT NULL AND text IS NULL) OR (reference IS NULL AND text IS NOT NULL))
);


-- Create a combined_invoices view with records from both invoices and invoices_unconfirmed tables
CREATE VIEW IF NOT EXISTS invoices_combined AS
SELECT id, mmh3_hash, original_filename, filename, issuer, date, invoice_number, amount, iban, bic, reference, text, paid_initial, paid, comment, 'confirmed' AS status
FROM invoices
UNION ALL
SELECT id, mmh3_hash, original_filename, filename, issuer, date, invoice_number, amount, iban, bic, reference, text, paid_initial, paid, comment, 'unconfirmed' AS status
FROM invoices_unconfirmed;
