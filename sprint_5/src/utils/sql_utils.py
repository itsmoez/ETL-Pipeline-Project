import uuid
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def create_db_tables(connection, cursor):
    LOGGER.info('create_db_tables: started')
    try:

        LOGGER.info('create_db_tables: creating mystery_shop_visit table')
        cursor.execute(
            '''
            -- Create branch table
        CREATE TABLE IF NOT EXISTS branches (
            branch_id UUID PRIMARY KEY,
            branch_name VARCHAR(255) NOT NULL
        );
        
        -- Create transactions table
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id UUID PRIMARY KEY,
            branch_id UUID NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            total NUMERIC(10, 2),
            trans_type VARCHAR(50),
            CONSTRAINT fk_branch
                FOREIGN KEY (branch_id)
                REFERENCES branches(branch_id)
                ON DELETE CASCADE
        );
        
        
        -- Create products table
        CREATE TABLE IF NOT EXISTS products (
            product_id UUID PRIMARY KEY,
            product_name VARCHAR(50),
            price NUMERIC(10, 2) NOT NULL
        );
        
        
        -- Create transaction_items table
        CREATE TABLE IF NOT EXISTS transaction_items (
            items_id UUID PRIMARY KEY,
            transaction_id UUID NOT NULL,
            product_id UUID NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            CONSTRAINT fk_transactions
                FOREIGN KEY (transaction_id)
                REFERENCES transactions(transaction_id)
                ON DELETE CASCADE,
            CONSTRAINT fk_products
                FOREIGN KEY (product_id)
                REFERENCES products(product_id)
                ON DELETE CASCADE
        );
                    '''
        )

        LOGGER.info('create_db_tables: committing')
        connection.commit()

        LOGGER.info('create_db_tables: done')
    except Exception as ex:
        LOGGER.info(f'create_db_tables: failed to run sql: {ex}')
        raise ex

