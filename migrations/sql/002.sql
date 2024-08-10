ALTER TABLE expenses
    DROP COLUMN IF EXISTS expense_details;

ALTER TABLE expenses
    ADD COLUMN IF NOT EXISTS expense_details JSON[] DEFAULT '{}'::JSON[] NOT NULL;
