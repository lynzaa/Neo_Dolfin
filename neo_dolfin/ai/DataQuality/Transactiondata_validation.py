# -*- coding: utf-8 -*-
"""

@author: Aishwarya and Liny

This script is designed for validating transactional datasets within the DolFin database.
It performs several types of data validations to ensure the integrity of the data:
Not-null constraints - Ensures that essential fields do not contain NULL values.
Unique constraints - Verifies that specific fields (like transaction IDs) contain only unique values.
Range validations - Checks that numerical fields fall within specified ranges.
Allowed values validation - Confirms that certain fields contain only predefined permissible values.
Regex pattern matching - Uses regular expressions to validate the formatting of fields such as institution codes and timestamps.

These validations are crucial for maintaining the quality and reliability of the transactional data, which is key for accurate processing and analysis in financial contexts.
"""

import sqlite3
from collections import defaultdict
import re

# Database connection path
db_path = 'dolfin_db.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

"""
Define validation rules for the transactions table
This dictionary contains sets of rules designed to ensure data integrity for transaction entries.
These rules verify that the data entries are complete, unique,
within acceptable ranges, conform to allowed values, and match specified formats, supporting the reliability and accuracy of transaction processing.
"""

validation_rules = {
    'not_null': ['id', 'type', 'status', 'amount', 'account', 'balance', 'direction', 'class', 'institution', 'postDate', 'trans_u_id'],
    'unique': ['id'],
    'ranges': {
        'amount': (0, float('inf')),
        'balance': (0, float('inf')),  # non-negative balances
    },
    'allowed_values': {
        'status': ['posted', 'pending', 'failed', 'reversed'],
        'direction': ['credit', 'debit'],
        'class': ['transfer', 'payment', 'income', 'investment'],
    },
    'regex': {
        'institution': r'^AU[0-9]{5}$',
        'postDate': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$',  # ISO 8601 date pattern
    }
}

"""
This section of the script compiles the validation results for the transaction data 
based on predefined rules. It checks for null values, duplicate entries, range anomalies, non-conforming values, and pattern mismatches. 
The results help identify data integrity issues, ensuring the transaction database maintains high standards of data quality.
Each validation check captures and records specific issues which can then be addressed to improve overall data accuracy and reliability.

"""
results = defaultdict(list)

# Validate not-null constraints
for col in validation_rules['not_null']:
    cursor.execute(f"SELECT COUNT(*) FROM transactions WHERE {col} IS NULL;")
    null_count = cursor.fetchone()[0]
    if null_count > 0:
        results['transactions'].append(f"Column '{col}' has {null_count} NULL values.")

# Validate unique constraints
for col in validation_rules['unique']:
    cursor.execute(f"SELECT {col}, COUNT(*) FROM transactions GROUP BY {col} HAVING COUNT(*) > 1;")
    duplicates = cursor.fetchall()
    if duplicates:
        results['transactions'].append(f"Column '{col}' has {len(duplicates)} duplicate values.")

# Validate ranges
for col, (min_val, max_val) in validation_rules['ranges'].items():
    cursor.execute(f"SELECT COUNT(*) FROM transactions WHERE {col} < ? OR {col} > ?;", (min_val, max_val))
    out_of_range_count = cursor.fetchone()[0]
    if out_of_range_count > 0:
        results['transactions'].append(f"Column '{col}' has {out_of_range_count} values out of range [{min_val}, {max_val}].")

# Validate allowed values
for col, allowed_vals in validation_rules['allowed_values'].items():
    cursor.execute(f"SELECT COUNT(*) FROM transactions WHERE {col} NOT IN ({','.join(['?'] * len(allowed_vals))});", allowed_vals)
    invalid_count = cursor.fetchone()[0]
    if invalid_count > 0:
        results['transactions'].append(f"Column '{col}' has {invalid_count} invalid values.")

# Validate regex patterns
for col, pattern in validation_rules['regex'].items():
    cursor.execute(f"SELECT {col} FROM transactions;")
    values = cursor.fetchall()
    invalid_values = [value[0] for value in values if not re.match(pattern, str(value[0]))]
    if invalid_values:
        results['transactions'].append(f"Column '{col}' has {len(invalid_values)} values that do not match the pattern '{pattern}'.")

# Close the connection
conn.close()

# Display the validation results
for issue in results['transactions']:
    print(f"  - {issue}")
