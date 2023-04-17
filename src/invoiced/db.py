import sqlite3

DBNAME = "invoices.db"

def is_hash_present(mmh3_hash):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM invoices
        WHERE mmh3_hash = ?;
    """

    cursor.execute(query, (mmh3_hash,))
    count = cursor.fetchone()[0]

    connection.close()
    return count > 0

def insert_invoice(original_filename, mmh3_hash, date, invoice_number, amount, paid='no', comment=None):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()

    query = """
        INSERT INTO invoices
        (original_filename, mmh3_hash, date, invoice_number, amount, paid, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """

    try:
        cursor.execute(query,
            (original_filename, mmh3_hash, date, invoice_number, amount, paid, comment))
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: invoices.mmh3_hash" in str(e):
            print(f"The file {original_filename} (hash {mmh3_hash}) already exists.")
        else:
            raise
    finally:
        connection.commit()
        connection.close()
