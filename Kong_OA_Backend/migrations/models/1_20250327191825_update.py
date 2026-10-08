from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `oa_users` ALTER COLUMN `is_active` DROP DEFAULT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `oa_users` ALTER COLUMN `is_active` SET DEFAULT 1;"""
